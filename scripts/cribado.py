#!/usr/bin/env python3
"""Cribado 1 de PRISMA 2020 (título, resumen y palabras clave) conjunto de Scopus y Web of Science.

El usuario deja las exportaciones en la última versión del picoc (docs/<slug>/picoc/<fecha>-<MARCO>/):
Scopus en CSV y WoS en Excel (.xls) o texto tabulado (.txt). Cabeceras y mapeo: playbooks/columnas-scopus-wos.md.
Los agentes nunca leen las exportaciones: solo .cribado-1/registros.jsonl, por rangos de líneas.

Uso:
  cribado.py prepare  docs/<slug>     # WoS → CSV, resultados-<MARCO>.csv unificado, duplicados, registros.jsonl
  cribado.py merge    docs/<slug>     # propuestas/lote-NN.md + resoluciones.md → decisiones.jsonl y debate.md
  cribado.py report   docs/<slug>     # valida decisiones + síntesis → cribado-1.md y cribado-1.shadow.jsonl
  cribado.py keywords docs/<slug>     # rendimiento de los términos de la query → .cribado-1/keywords.md
  cribado.py set      docs/<slug> R012 SI|DUDA|NO "motivo" [CI3,CE5]   # corrección del usuario (DUDA = SI con duda)
  cribado.py apply    docs/<slug>     # resultados-<MARCO>-cribado-1.csv con «¿Se acepta?» y «Justificación cribado 1»

Trabajo interno (.cribado-1/): estado.json, registros.jsonl (registros únicos, uno por línea),
decisiones.jsonl y sintesis.json (los escribe rsl-cribado-1), propuestas/, keywords.md.
decisiones.jsonl: {"id": "R001", "decision": "SI|NO", "criterios": ["CE5"], "motivo": "…", "duda": false, "acuerdo": true}
sintesis.json:    {"aceptados": "…", "rechazados": "…", "dudas": "…"}  (por qué, en general, ≤ 120 palabras cada uno)
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_picoc_sync as sync  # noqa: E402
import picoc_versions as pv  # noqa: E402
from rsl_out import Fail, error, ok, run  # noqa: E402

STAGE = "cribado-1"
WORK = ".cribado-1"
COL_OK, COL_WHY = "¿Se acepta?", "Justificación cribado 1"
BATCH = 40
MOTIVO_MAX = 25
SINTESIS_MAX = 120
KW_MAX = 25
CRITERIA = "Criterios de inclusión y exclusión"
HASH_RE = re.compile(r"<!-- cribado:hash=([0-9a-f]+) -->")
COPYRIGHT_RE = re.compile(r"\s*(©|\(c\)|Copyright)\s.*$", re.I | re.S)
DOI_PREFIX = re.compile(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", re.I)
UNIFIED = ["Id", "Fuente", "Título", "Autores", "Año", "Revista", "DOI", "Id base", "Tipo de documento", "Idioma",
           "Acceso abierto", "Palabras clave autor", "Palabras clave índice", "Resumen", "Enlace", "Fila origen"]
MAP = {  # columna unificada -> (Scopus CSV, WoS Excel, WoS tabulado)
    "Título": ("Title", "Article Title", "TI"),
    "Autores": ("Authors", "Authors", "AU"),
    "Año": ("Year", "Publication Year", "PY"),
    "Revista": ("Source title", "Source Title", "SO"),
    "DOI": ("DOI", "DOI", "DI"),
    "Id base": ("EID", "UT (Unique WOS ID)", "UT"),
    "Tipo de documento": ("Document Type", "Document Type", "DT"),
    "Idioma": ("Language of Original Document", "Language", "LA"),
    "Acceso abierto": ("Open Access", "Open Access Designations", "OA"),
    "Palabras clave autor": ("Author Keywords", "Author Keywords", "DE"),
    "Palabras clave índice": ("Index Keywords", "Keywords Plus", "ID"),
    "Resumen": ("Abstract", "Abstract", "AB"),
    "Enlace": ("Link", "DOI Link", "DL"),
}
REQUIRED = ("Título", "Resumen")
USAGE = ("uso: cribado:prepare|merge|report|keywords|apply <docs/slug> · "
         "cribado:set <docs/slug> <id> SI|DUDA|NO \"motivo\" [criterios]")


def rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(p)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:12]


def fhash(p: Path) -> str:
    return sha(p.read_bytes())


def theme_dir(arg: str) -> Path:
    t = Path(arg)
    t = t if t.is_absolute() else Path.cwd() / t
    if not t.is_dir():
        raise Fail(f"{arg} no es la carpeta de un tema", "usa docs/<slug>")
    return t


def picoc_file(theme: Path) -> Path:
    f = pv.latest_file(theme)
    if f is None:
        raise Fail(f"{rel(theme)} no tiene picoc/<fecha>-<MARCO>/picoc.md", f"créalo con: Usa rsl-picoc sobre {rel(theme)}/")
    return f


def unified_name(picoc: Path) -> str:
    return f"resultados-{pv.dir_marco(picoc) or 'MARCO'}.csv"


# --- criterios ---------------------------------------------------------------

def criteria(picoc: Path) -> dict[str, str]:
    text = picoc.read_text(encoding="utf-8")
    m = re.search(rf"^## {re.escape(CRITERIA)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not m:
        raise Fail(f"{rel(picoc)} no tiene '## {CRITERIA}'", "regenera el picoc con rsl-picoc (modo parcial) para añadir los criterios")
    out: dict[str, str] = {}
    for head, code in (("Inclusión", "CI"), ("Exclusión", "CE")):
        sm = re.search(rf"^### {head}\s*$(.*?)(?=^### |\Z)", m.group(1), re.M | re.S)
        items = re.findall(r"^\s*[-*]\s+(.+)$", sm.group(1), re.M) if sm else []
        if not items:
            raise Fail(f"{rel(picoc)} no tiene viñetas en '### {head}'", "regenera el picoc con rsl-picoc (modo parcial)")
        explicit = [re.match(r"^\**\s*(" + code + r"\d+)\.?\s*\**\s*(.*)$", it.strip(), re.I) for it in items]
        if all(explicit):
            for match in explicit:
                out[match.group(1).upper()] = match.group(2).strip()
        else:
            # Legacy picoc: preserve historical numbering until rsl-picoc creates a new version.
            for i, it in enumerate(items, 1):
                out[f"{code}{i}"] = it.strip()
    return out


def dup_code(crit: dict[str, str]) -> str:
    return "DUPLICADO_TECNICO"


# --- lectura de exportaciones ---------------------------------------------------

def read_text_table(path: Path, delimiter: str) -> tuple[list[str], list[list[str]]]:
    raw = path.read_bytes()
    enc = "utf-16" if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else "utf-8-sig"
    try:
        text = raw.decode(enc)
    except UnicodeDecodeError:
        raise Fail(f"{rel(path)} no está en UTF-8", "expórtalo de nuevo desde la base (UTF-8)")
    try:
        rows = list(csv.reader(text.splitlines(), delimiter=delimiter))
    except csv.Error as e:
        raise Fail(f"{rel(path)} no es un archivo delimitado válido ({e})", "expórtalo de nuevo desde la base")
    if not rows or not any(rows[0]):
        raise Fail(f"{rel(path)} está vacío", "expórtalo de nuevo desde la base")
    return [h.strip() for h in rows[0]], [r for r in rows[1:] if any(c.strip() for c in r)]


def read_xls(path: Path) -> tuple[list[str], list[list[str]]]:
    try:
        import xlrd  # noqa: PLC0415
    except ImportError:
        raise Fail(f"para leer {path.name} hace falta xlrd", "instálalo con: pipx inject graphifyy xlrd (o exporta WoS como Tab delimited file .txt)")
    try:
        sh = xlrd.open_workbook(str(path)).sheet_by_index(0)
    except Exception as e:  # noqa: BLE001
        raise Fail(f"{rel(path)} no es un Excel válido ({type(e).__name__})", "expórtalo de nuevo desde Web of Science (Excel)")

    def val(v) -> str:
        if isinstance(v, float):
            if v == 0.0:
                return ""
            if v.is_integer():
                return str(int(v))
        s = str(v).strip()
        return "" if s in ("0", "0.0") else s

    rows = [[val(v) for v in sh.row_values(i)] for i in range(sh.nrows)]
    if not rows:
        raise Fail(f"{rel(path)} está vacío", "expórtalo de nuevo desde Web of Science")
    return rows[0], [r for r in rows[1:] if any(c for c in r)]


def kind_of(header: list[str]) -> int | None:
    """0 = Scopus CSV, 1 = WoS Excel (o su CSV convertido), 2 = WoS tabulado; None = desconocido."""
    h = set(header)
    if "Article Title" in h or "UT (Unique WOS ID)" in h:
        return 1
    if {"TI", "UT"} <= h or {"TI", "AB"} <= h:
        return 2
    if "Title" in h and ("EID" in h or "Source title" in h):
        return 0
    return None


def find_sources(folder: Path) -> tuple[Path | None, Path | None]:
    unified = unified_name(folder / "picoc.md")
    scopus, wos = [], []
    stems_native = {p.stem for p in folder.iterdir() if p.suffix.lower() in (".xls", ".txt")}
    for p in sorted(folder.iterdir()):
        if not p.is_file() or p.name.startswith(".") or "cribado" in p.name or p.name == unified:
            continue
        ext = p.suffix.lower()
        if ext == ".xls":
            wos.append(p)
        elif ext == ".txt":
            if kind_of(read_text_table(p, "\t")[0]) == 2:
                wos.append(p)
        elif ext == ".csv":
            k = kind_of(read_text_table(p, ",")[0])
            if k == 0:
                scopus.append(p)
            elif k == 1 and p.stem not in stems_native:
                wos.append(p)
    for name, found in (("Scopus", scopus), ("Web of Science", wos)):
        if len(found) > 1:
            raise Fail(f"hay {len(found)} exportaciones de {name} en {rel(folder)}/ ({', '.join(p.name for p in found)})", "deja solo una por base")
    if not scopus and not wos:
        raise Fail(f"no hay exportaciones de Scopus ni de Web of Science en {rel(folder)}/",
                   "exporta Scopus (CSV) y WoS (Excel o Tab delimited) con las queries del picoc y déjalos en esa carpeta (ver playbooks/columnas-scopus-wos.md)")
    return (scopus[0] if scopus else None), (wos[0] if wos else None)


def load_source(path: Path, base: str) -> tuple[list[dict], Path | None]:
    """Filas en columnas unificadas. Para WoS .xls/.txt escribe también <nombre>.csv con sus cabeceras originales."""
    converted = None
    if path.suffix.lower() == ".xls":
        header, rows = read_xls(path)
    elif path.suffix.lower() == ".txt":
        header, rows = read_text_table(path, "\t")
    else:
        header, rows = read_text_table(path, ",")
    k = kind_of(header)
    if k is None or (base == "Scopus") != (k == 0):
        raise Fail(f"{rel(path)} no tiene las cabeceras de {base}", "revisa la exportación (ver playbooks/columnas-scopus-wos.md)")
    if path.suffix.lower() in (".xls", ".txt"):
        converted = path.with_suffix(".csv")
        with converted.open("w", encoding="utf-8-sig", newline="") as fh:
            w = csv.writer(fh, quoting=csv.QUOTE_ALL)
            w.writerow(header)
            w.writerows(rows)
    idx = {h: i for i, h in enumerate(header)}
    for col in REQUIRED:
        if MAP[col][k] not in idx:
            raise Fail(f"{rel(path)} no tiene la columna {MAP[col][k]} ({col})", "exporta el registro completo, con resumen (ver playbooks/columnas-scopus-wos.md)")
    out = []
    for n, row in enumerate(rows, 2):
        rec = {"Fuente": base, "Fila origen": str(n)}
        for col, names in MAP.items():
            i = idx.get(names[k])
            rec[col] = row[i].strip() if i is not None and i < len(row) else ""
        fix_doi_enlace(rec)
        out.append(rec)
    return out, converted


def norm_title(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())


def norm_doi(s: str) -> str:
    return DOI_PREFIX.sub("", s.strip()).lower()


def strip_zero_field(s: str) -> str:
    s = (s or "").strip()
    return "" if s in ("0", "0.0") else s


def fix_doi_enlace(rec: dict) -> None:
    """WoS Excel suele dejar DOI Link en 0; unifica DOI y enlace doi.org cuando toca."""
    doi = strip_zero_field(rec.get("DOI", ""))
    link = strip_zero_field(rec.get("Enlace", ""))
    if not doi and link:
        doi = norm_doi(link)
    rec["DOI"] = norm_doi(doi) if doi else ""
    if not link and rec["DOI"]:
        rec["Enlace"] = f"https://doi.org/{rec['DOI']}"
    else:
        rec["Enlace"] = link


def keywords(rec: dict) -> str:
    terms, seen = [], set()
    for col in ("Palabras clave autor", "Palabras clave índice"):
        for t in rec.get(col, "").split(";"):
            t = t.strip()
            if t and t.lower() not in seen:
                seen.add(t.lower())
                terms.append(t)
    return "; ".join(terms[:KW_MAX]) + (" …" if len(terms) > KW_MAX else "")


# --- prepare -----------------------------------------------------------------

def cmd_prepare(theme: Path) -> int:
    picoc = picoc_file(theme)
    crit = criteria(picoc)
    folder = picoc.parent
    scopus, wos = find_sources(folder)
    recs, fuentes = [], []
    for path, base in ((scopus, "Scopus"), (wos, "WoS")):
        if path is None:
            continue
        rows, converted = load_source(path, base)
        if not rows:
            raise Fail(f"{rel(path)} no tiene registros", "revisa la exportación")
        fuentes.append({"base": base, "archivo": path.name, "hash": fhash(path), "n": len(rows),
                        "csv": converted.name if converted else path.name})
        recs += rows
    for n, r in enumerate(recs, 1):
        r["Id"] = f"R{n:03d}"

    seen: dict[tuple[str, str], dict] = {}
    dups, code = [], dup_code(crit)
    for r in recs:
        keys = [("DOI", norm_doi(r["DOI"])), ("Id base", r["Id base"]), ("título", norm_title(r["Título"]))]
        hit = next(((k, seen[(k, v)]) for k, v in keys if v and (k, v) in seen), None)
        if hit:
            keep = hit[1]
            dups.append({"id": r["Id"], "fuente": r["Fuente"], "de": keep["Id"], "fuente_de": keep["Fuente"].split(";")[0], "por": hit[0], "criterio": code})
            if r["Fuente"] not in keep["Fuente"]:
                keep["Fuente"] += f"; {r['Fuente']}"
            for col in MAP:
                if not keep[col] and r[col]:
                    keep[col] = r[col]
            continue
        for k, v in keys:
            if v:
                seen.setdefault((k, v), r)

    uni = folder / unified_name(picoc)
    with uni.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_ALL)
        w.writerow(UNIFIED)
        w.writerows([[r.get(c, "") for c in UNIFIED] for r in recs])

    work = folder / WORK
    (work / "propuestas").mkdir(parents=True, exist_ok=True)
    dup_ids = {d["id"] for d in dups}
    unique = [r for r in recs if r["Id"] not in dup_ids]
    with (work / "registros.jsonl").open("w", encoding="utf-8") as fh:
        for r in unique:
            fh.write(json.dumps({"id": r["Id"], "titulo": r["Título"] or "(sin título)",
                                 "resumen": COPYRIGHT_RE.sub("", r["Resumen"]) or "(sin resumen)",
                                 "palabras_clave": keywords(r) or "—",
                                 "doi": norm_doi(r["DOI"]) or None}, ensure_ascii=False) + "\n")
    lotes = [[i + 1, min(i + BATCH, len(unique)), unique[i]["Id"], unique[min(i + BATCH, len(unique)) - 1]["Id"]]
             for i in range(0, len(unique), BATCH)]
    (work / "criterios.md").write_text(
        "# Criterios del cribado 1\n\nCopiados de " + rel(picoc) + ".\n\n| Código | Criterio |\n|---|---|\n"
        + "".join(f"| {c} | {t} |\n" for c, t in crit.items()), encoding="utf-8")

    uhash = fhash(uni)
    dec = work / "decisiones.jsonl"
    try:
        old = json.loads((work / "estado.json").read_text(encoding="utf-8")).get("unificado_hash")
    except (FileNotFoundError, json.JSONDecodeError):
        old = None
    if dec.exists() and old != uhash:
        bak = work / f"decisiones-{old or 'sin-estado'}.jsonl.bak"
        dec.rename(bak)
        (work / "sintesis.json").unlink(missing_ok=True)
        print(f"WARN las exportaciones cambiaron: las decisiones anteriores pasan a {rel(bak)} (hay que volver a cribar)")
    elif dec.exists():
        print(f"WARN {rel(dec)} ya existe y las exportaciones son las mismas: se conserva")
    state = {"picoc": rel(picoc), "fecha": dt.date.today().isoformat(), "fuentes": fuentes, "unificado": uni.name,
             "unificado_hash": uhash, "criterios": crit, "duplicados": dups, "lotes": lotes,
             "registros": [{"id": r["Id"], "fuente": r["Fuente"], "titulo": r["Título"], "anio": r["Año"],
                            "doi": norm_doi(r["DOI"]), "id_base": r["Id base"]} for r in recs]}
    (work / "estado.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(" · ".join(f"{f['base']}: {f['n']} ({f['archivo']})" for f in fuentes)
          + f" · total: {len(recs)} · duplicados: {len(dups)} · únicos a cribar: {len(unique)}")
    if dups:
        por = {}
        for d in dups:
            por[d["por"]] = por.get(d["por"], 0) + 1
        print("duplicados (" + ", ".join(f"{n} por {k}" for k, n in por.items()) + "): "
              + ", ".join(f"{d['id']}→{d['de']}" for d in dups))
    for k, (a, b, ia, ib) in enumerate(lotes, 1):
        print(f"lote {k:02d}: líneas {a}–{b} de {rel(work / 'registros.jsonl')} ({ia}–{ib})")
    return ok(f"{rel(uni)} con {len(recs)} registros ({len(dups)} duplicado(s)); {len(unique)} únicos en {len(lotes)} lote(s)",
              "rsl-cribado-1: defensor-rsl propone y critico-rsl critica cada lote; luego decisiones.jsonl, sintesis.json y cribado:report")


# --- estado y decisiones -----------------------------------------------------

def load_state(theme: Path) -> tuple[Path, dict]:
    folder = picoc_file(theme).parent
    work = folder / WORK
    f = work / "estado.json"
    if not f.exists():
        raise Fail(f"no hay {rel(f)}", f"corre primero: pnpm -s cribado:prepare {rel(theme)}")
    try:
        state = json.loads(f.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        raise Fail(f"{rel(f)} está corrupto", f"vuelve a correr: pnpm -s cribado:prepare {rel(theme)}")
    for src in state["fuentes"]:
        p = folder / src["archivo"]
        if not p.exists() or fhash(p) != src["hash"]:
            raise Fail(f"la exportación {src['archivo']} cambió o ya no está desde cribado:prepare", f"vuelve a correr: pnpm -s cribado:prepare {rel(theme)} (y rsl-cribado-1)")
    uni = folder / state["unificado"]
    if not uni.exists() or fhash(uni) != state["unificado_hash"]:
        raise Fail(f"{state['unificado']} cambió o ya no está desde cribado:prepare", f"vuelve a correr: pnpm -s cribado:prepare {rel(theme)}")
    return folder, state


def load_decisions(work: Path) -> tuple[list[dict], list[str]]:
    f = work / "decisiones.jsonl"
    if not f.exists():
        raise Fail(f"no hay {rel(f)}", "escríbelo con rsl-cribado-1 (una línea JSON por registro único)")
    decs, errs = [], []
    for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            d = json.loads(line)
            if not isinstance(d, dict):
                raise ValueError
            decs.append(d)
        except ValueError:
            errs.append(f"línea {n}: no es un objeto JSON")
    return decs, errs


def load_sintesis(work: Path) -> tuple[dict, list[str]]:
    f = work / "sintesis.json"
    if not f.exists():
        return {}, [f"falta {f.name} (por qué se aceptaron, se rechazaron y quedaron en duda, en general)"]
    try:
        s = json.loads(f.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}, [f"{f.name} no es JSON válido"]
    errs = []
    for k in ("aceptados", "rechazados", "dudas"):
        txt = str(s.get(k) or "").strip()
        if not txt:
            errs.append(f"{f.name}: falta «{k}»")
        elif len(txt.split()) > SINTESIS_MAX:
            errs.append(f"{f.name}: «{k}» tiene {len(txt.split())} palabras (máx. {SINTESIS_MAX})")
    return s, errs


def validate(state: dict, decs: list[dict]) -> list[str]:
    crit = state["criterios"]
    dup_ids = {d["id"] for d in state["duplicados"]}
    need = [r["id"] for r in state["registros"] if r["id"] not in dup_ids]
    errs, seen = [], set()
    for d in decs:
        rid = d.get("id")
        if rid in seen:
            errs.append(f"{rid}: decisión repetida")
        seen.add(rid)
        if rid in dup_ids:
            errs.append(f"{rid}: es un duplicado (NO automático); no lleva decisión")
        elif rid not in need:
            errs.append(f"{rid}: no es un registro del unificado")
        if d.get("decision") not in ("SI", "NO"):
            errs.append(f"{rid}: decision «{d.get('decision')}» no es SI ni NO")
        cs = d.get("criterios") or []
        if not isinstance(cs, list) or any(c not in crit for c in cs):
            errs.append(f"{rid}: criterios {cs} con códigos que no están en el picoc ({', '.join(crit)})")
        if d.get("decision") == "NO" and not cs:
            errs.append(f"{rid}: un NO debe citar al menos un criterio (CE o el CI que no cumple)")
        motivo = str(d.get("motivo") or "").strip()
        if not motivo:
            errs.append(f"{rid}: falta el motivo")
        elif len(motivo.split()) > MOTIVO_MAX:
            errs.append(f"{rid}: motivo de {len(motivo.split())} palabras (máx. {MOTIVO_MAX})")
    missing = [r for r in need if r not in seen]
    if missing:
        errs.append(f"faltan {len(missing)} decisión(es): {', '.join(missing[:15])}{' …' if len(missing) > 15 else ''}")
    return errs


def decisions_hash(state: dict, decs: list[dict], sintesis: dict) -> str:
    return sha(json.dumps([state["unificado_hash"], sorted(decs, key=lambda d: d["id"]), sintesis], ensure_ascii=False, sort_keys=True).encode())


# --- report ------------------------------------------------------------------

def md_cell(s: str, n: int | None = None) -> str:
    s = " ".join(str(s).split()).replace("|", "\\|")
    return s if n is None or len(s) <= n else s[: n - 1].rstrip() + "…"


def pct(a: int, b: int) -> str:
    return f"{(100 * a / b):.1f} %".replace(".", ",") if b else "—"


def dashboard(state: dict, decs: list[dict], sint: dict, h: str) -> str:
    crit, recs = state["criterios"], {r["id"]: r for r in state["registros"]}
    dups = state["duplicados"]
    si = [d for d in decs if d["decision"] == "SI" and not d.get("duda")]
    dudas = [d for d in decs if d["decision"] == "SI" and d.get("duda")]
    no = [d for d in decs if d["decision"] == "NO"]
    total, screened = len(recs), len(decs)
    fuentes = " · ".join(f"{f['base']} (`{f['archivo']}`, n = {f['n']})" for f in state["fuentes"])
    L = ["# Cribado 1 — título, resumen y palabras clave", "", f"<!-- cribado:hash={h} -->", "",
         f"**Bases:** {fuentes} · **Unificado:** `{state['unificado']}` · **Picoc:** `{state['picoc']}` · **Fecha:** {state['fecha']}", "",
         "## Resumen", "", "| Indicador | n | % |", "|---|---|---|",
         f"| Registros identificados | {total} | |",
         f"| Duplicados eliminados | {len(dups)} | {pct(len(dups), total)} de los identificados |",
         f"| Registros cribados | {screened} | |",
         f"| **Pasan al cribado 2 (SI)** | **{len(si) + len(dudas)}** | **{pct(len(si) + len(dudas), screened)} de los cribados** |",
         f"| · aceptados sin duda | {len(si)} | {pct(len(si), screened)} |",
         f"| · con duda (se deciden a texto completo) | {len(dudas)} | {pct(len(dudas), screened)} |",
         f"| Se rechazan | {len(no)} | {pct(len(no), screened)} |",
         f"| Desacuerdos entre agentes | {sum(1 for d in decs if d.get('acuerdo') is False)} | |",
         f"| Corregidos por el usuario | {sum(1 for d in decs if d.get('usuario'))} | |", "",
         f"## Duplicados: {len(dups)}", ""]
    if dups:
        L += [f"Al inicio hubo {len(dups)} duplicados; se conservó la primera aparición (Scopus va primero).", "",
              "| Eliminado | Se conserva | Título | Motivo |", "|---|---|---|---|"]
        L += [f"| {d['id']} ({d['fuente']}) | {d['de']} ({d['fuente_de']}) | {md_cell(recs[d['id']]['titulo'], 110)} | mismo {d['por']} |" for d in dups]
    else:
        L.append(f"Sin duplicados en los {total} registros.")

    def listing(ds: list[dict], extra: str | None = None) -> list[str]:
        head = "| Id | Título | Fuente |" + (f" {extra} |" if extra else "")
        rows = []
        for d in ds:
            r = recs[d["id"]]
            tail = ""
            if extra == "Criterio":
                tail = f" {', '.join(d['criterios'])} |"
            elif extra:
                tail = f" {md_cell(d['motivo'])} |"
            rows.append(f"| {d['id']} | {md_cell(r['titulo'], 120)} | {r['fuente']} |{tail}")
        return [head, "|---|---|---|" + ("---|" if extra else "")] + rows

    L += ["", f"## Se aceptaron: {len(si)} ({pct(len(si), screened)})", "", f"**Por qué:** {sint['aceptados'].strip()}", ""]
    L += listing(si) if si else ["Ninguno."]
    L += ["", f"## Se rechazaron: {len(no)} ({pct(len(no), screened)})", "", f"**Por qué:** {sint['rechazados'].strip()}", "",
          "Cada rechazo cuenta en su criterio principal (el primero que cita).", ""]
    counts: dict[str, int] = {}
    for d in no:
        counts[d["criterios"][0]] = counts.get(d["criterios"][0], 0) + 1
    for pref, title in (("CI", "Por criterio de inclusión no cumplido"), ("CE", "Por criterio de exclusión")):
        cs = sorted((c for c in counts if c.startswith(pref)), key=lambda c: -counts[c])
        L += [f"### {title}", "", "| Criterio | Rechazos | % de los rechazados |", "|---|---|---|"]
        L += [f"| {c} — {md_cell(crit[c], 80)} | {counts[c]} | {pct(counts[c], len(no))} |" for c in cs] or ["| — | 0 | — |"]
        L.append("")
    L += ["### Lista", ""] + (listing(no, "Criterio") if no else ["Ninguno."])
    L += ["", f"## Dudas: {len(dudas)} ({pct(len(dudas), screened)}; van como SI y se deciden a texto completo)", "",
          f"**Por qué:** {sint['dudas'].strip()}", ""]
    L += listing(dudas, "Qué falta confirmar") if dudas else ["Ninguna."]
    ident = " y ".join(f"{'Web of Science' if f['base'] == 'WoS' else f['base']} (n = {f['n']})" for f in state["fuentes"])
    L += ["", "## PRISMA (para el paper)", "",
          f"Registros identificados en {ident}; duplicados eliminados (n = {len(dups)}); registros cribados (n = {screened}); "
          f"excluidos en el cribado de título y resumen (n = {len(no)}); pasan a texto completo (n = {len(si) + len(dudas)}).", "",
          "## Criterios", "", "| Código | Criterio |", "|---|---|"] + [f"| {c} | {md_cell(t)} |" for c, t in crit.items()]
    return "\n".join(L) + "\n"


def shadow(state: dict, decs: list[dict], h: str) -> str:
    by = {d["id"]: d for d in decs}
    dmap = {d["id"]: d for d in state["duplicados"]}
    lines = [json.dumps({"_meta": {"hash": h, "unificado": state["unificado"], "unificado_hash": state["unificado_hash"]}}, ensure_ascii=False)]
    for r in state["registros"]:
        base = {"id": r["id"], "fuente": r["fuente"], "uid": r["doi"] or r["id_base"], "titulo": r["titulo"][:80]}
        if r["id"] in dmap:
            d = dmap[r["id"]]
            base.update(decision="NO", criterios=[d["criterio"]], motivo=f"Duplicado de {d['de']} ({d['fuente_de']}; mismo {d['por']})", duda=False, duplicado_de=d["de"])
        else:
            d = by[r["id"]]
            base.update(decision=d["decision"], criterios=d.get("criterios") or [], motivo=d["motivo"].strip(), duda=bool(d.get("duda")))
        lines.append(json.dumps(base, ensure_ascii=False))
    return "\n".join(lines) + "\n"


def cmd_report(theme: Path) -> int:
    folder, state = load_state(theme)
    work = folder / WORK
    decs, errs = load_decisions(work)
    errs += validate(state, decs) if not errs else []
    sint, serrs = load_sintesis(work)
    errs += serrs
    if errs:
        for e in errs[:40]:
            print(f"  - {e}")
        return error(f"el cribado tiene {len(errs)} problema(s); no se escribió el reporte", "corrígelos en rsl-cribado-1 y vuelve a correr cribado:report")
    h = decisions_hash(state, decs, sint)
    (folder / f"{STAGE}.md").write_text(dashboard(state, decs, sint, h), encoding="utf-8")
    (folder / f"{STAGE}.shadow.jsonl").write_text(shadow(state, decs, h), encoding="utf-8")
    si = sum(1 for d in decs if d["decision"] == "SI")
    dudas = sum(1 for d in decs if d["decision"] == "SI" and d.get("duda"))
    return ok(f"cribado 1 de {len(state['registros'])} registros: {len(state['duplicados'])} duplicado(s), SI {si} (dudas {dudas}), NO {len(decs) - si} en {rel(folder / (STAGE + '.md'))} y {STAGE}.shadow.jsonl",
              f"revisa el reporte; si lo apruebas, Usa rsl-cribado-1-aplicar sobre {rel(theme)}/")


# --- keywords ----------------------------------------------------------------

def term_regex(term: str) -> re.Pattern:
    t = term.strip().strip('"').strip()
    parts = [re.escape(w).replace(r"\*", r"\w*") for w in re.split(r"[\s-]+", t) if w]
    return re.compile(r"(?<!\w)" + r"[\s-]+".join(parts) + r"(?!\w)", re.I)


def cmd_keywords(theme: Path) -> int:
    folder, state = load_state(theme)
    work = folder / WORK
    picoc = folder / "picoc.md"
    kw = sync.mirror(picoc)["keywords"]
    try:
        decs = {d["id"]: d["decision"] for d in load_decisions(work)[0]}
    except Fail:
        decs = {}
    regs = [json.loads(l) for l in (work / "registros.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    texts = {r["id"]: f"{r['titulo']} {r['resumen']} {r['palabras_clave']}" for r in regs}
    pats = {(c, t): term_regex(sync.en_term(t)) for c, ts in kw.items() for t in ts}
    L = ["# Rendimiento de los términos de la query (cribado 1)", "",
         f"Sobre {len(regs)} registros únicos (título, resumen y palabras clave). SI incluye las dudas. "
         "«Solo este término» = registros que ningún otro término de su componente recupera (se perderían si se quita).", "",
         "| Comp. | Término | Registros | SI | NO | Solo este término (SI / NO) |", "|---|---|---|---|---|---|"]
    hits_of = {k: {i for i, tx in texts.items() if p.search(tx)} for k, p in pats.items()}
    zero = []
    for (c, t), hits in hits_of.items():
        if not hits:
            zero.append(f"`{sync.en_term(t)}` ({c})")
            continue
        others = set().union(*(h for (c2, t2), h in hits_of.items() if c2 == c and t2 != t))
        only = hits - others
        s = sum(1 for i in hits if decs.get(i) == "SI")
        n = sum(1 for i in hits if decs.get(i) == "NO")
        os_ = sum(1 for i in only if decs.get(i) == "SI")
        L.append(f"| {c} | `{sync.en_term(t)}` | {len(hits)} | {s} | {n} | {os_} / {len(only) - os_} |")
    if zero:
        L += ["", "Sin registros: " + ", ".join(zero) + "."]
    cand: dict[str, list[int]] = {}
    for r in regs:
        d = decs.get(r["id"])
        for k in r["palabras_clave"].split(";"):
            k = k.strip().rstrip("…").strip()
            if not k or any(p.search(k) for p in pats.values()):
                continue
            c = cand.setdefault(k.lower(), [0, 0])
            c[0 if d == "SI" else 1] += 1
    top = sorted(((k, v) for k, v in cand.items() if v[0] >= 1 and v[0] >= v[1]), key=lambda x: (-x[1][0], x[1][1]))[:60]
    L += ["", "## Palabras clave de las fuentes que ninguna query cubre (≥ 1 registro aceptado y al menos tantos SI como NO)", "",
          "| Palabra clave | SI | NO |", "|---|---|---|"] + [f"| {k} | {a} | {b} |" for k, (a, b) in top] + (["| — | 0 | 0 |"] if not top else [])
    (work / "keywords.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return ok(f"{len(pats)} términos analizados ({len(zero)} sin registros), {len(top)} palabras clave candidatas en {rel(work / 'keywords.md')}",
              "rsl-cribado-1: debate de defensor-rsl y critico-rsl y cribado-1-sugerencia.md")


# --- merge -------------------------------------------------------------------

def md_rows(text: str, section: str) -> list[list[str]]:
    """Filas `| R001 | … |` bajo `## <section>` (hasta el siguiente `## `)."""
    m = re.search(rf"^## {re.escape(section)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    rows = []
    for line in (m.group(1) if m else "").splitlines():
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
        if cells and re.fullmatch(r"R\d{3,}", cells[0]):
            rows.append(cells)
    return rows


def codes(cell: str) -> list[str]:
    return [c.strip().upper() for c in re.split(r"[,;\s]+", cell) if re.fullmatch(r"C[IE]\d+", c.strip().upper())]


def cmd_merge(theme: Path) -> int:
    """Consolida propuestas/lote-NN.md (+ resoluciones.md) en decisiones.jsonl y debate.md."""
    folder, state = load_state(theme)
    work = folder / WORK
    regs = [json.loads(l)["id"] for l in (work / "registros.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    text_of = {json.loads(l)["id"]: json.loads(l) for l in (work / "registros.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
    res_file = work / "resoluciones.md"
    res = {r[0]: r for r in md_rows(res_file.read_text(encoding="utf-8"), "Resoluciones")} if res_file.exists() else {}
    decs, pending, probs, per_lote, lines = {}, [], [], [], []
    for k, (a, b, ia, ib) in enumerate(state["lotes"], 1):
        f = work / "propuestas" / f"lote-{k:02d}.md"
        if not f.exists():
            probs.append(f"falta {rel(f)} (defensor-rsl y critico-rsl del lote {k:02d})")
            continue
        txt = f.read_text(encoding="utf-8")
        dfn = {r[0]: r for r in md_rows(txt, "Defensor") if len(r) >= 5}
        if "## Crítico" not in txt:
            probs.append(f"{f.name}: falta la sección ## Crítico")
        ids = regs[a - 1:b]
        miss = [i for i in ids if i not in dfn]
        if miss:
            probs.append(f"{f.name}: el defensor no decidió {', '.join(miss)}")
        n_dis = 0
        for i in ids:
            if i not in dfn:
                continue
            _, dec, crit, duda, motivo = dfn[i][:5]
            decs[i] = {"id": i, "decision": dec.upper(), "criterios": codes(crit), "motivo": motivo,
                       "duda": dec.upper() == "SI" and duda.lower().startswith("s"), "acuerdo": True}
        for r in md_rows(txt, "Crítico"):
            if len(r) < 5 or r[0] not in decs or r[2].upper() == decs[r[0]]["decision"]:
                continue
            n_dis += 1
            i, d = r[0], decs[r[0]]
            if i in res:
                _, dec, crit, duda, motivo = (res[i] + [""] * 5)[:5]
                decs[i] = {"id": i, "decision": dec.upper(), "criterios": codes(crit), "motivo": motivo,
                           "duda": dec.upper() == "SI" and duda.lower().startswith("s"), "acuerdo": False}
                lines.append(f"- {i}: defensor {d['decision']}, crítico {r[2].upper()} → {dec.upper()}"
                             f"{' con duda' if decs[i]['duda'] else ''} ({', '.join(decs[i]['criterios']) or '—'}). {motivo}")
            else:
                t = text_of[i]
                pending.append(f"{i} · defensor {d['decision']} ({', '.join(d['criterios']) or '—'}) «{d['motivo']}» · "
                               f"crítico {r[2].upper()} ({r[3]}) «{r[4]}»\n    {t['titulo']} — {t['resumen'][:600]}")
        per_lote.append(f"| {k:02d} | {ia}–{ib} | {n_dis} |")
    if probs:
        for p in probs:
            print(f"  - {p}")
        return error(f"faltan propuestas en {len(probs)} punto(s)", "corre defensor-rsl y critico-rsl en esos lotes y vuelve a correr cribado:merge")
    if pending:
        for p in pending:
            print(f"  - {p}")
        return error(f"hay {len(pending)} desacuerdo(s) sin resolver",
                     f"escribe {rel(res_file)} con '## Resoluciones' y una fila | Id | Decisión | Criterios | Duda | Motivo | por desacuerdo; luego cribado:merge")
    old = {}
    dec_file = work / "decisiones.jsonl"
    if dec_file.exists():
        for l in dec_file.read_text(encoding="utf-8").splitlines():
            try:
                d = json.loads(l)
                if d.get("usuario"):
                    old[d["id"]] = d
            except (ValueError, KeyError):
                pass
    decs.update(old)
    dec_file.write_text("".join(json.dumps(decs[i], ensure_ascii=False) + "\n" for i in regs if i in decs), encoding="utf-8")
    (work / "debate.md").write_text(
        "# Debate del cribado 1\n\nDefensor-rsl propuso y critico-rsl criticó cada lote (`propuestas/`).\n\n"
        "| Lote | Registros | Desacuerdos |\n|---|---|---|\n" + "\n".join(per_lote) + "\n\n## Resolución\n\n"
        + ("\n".join(lines) if lines else "Sin desacuerdos.") + "\n", encoding="utf-8")
    si = sum(1 for d in decs.values() if d["decision"] == "SI")
    dudas = sum(1 for d in decs.values() if d["duda"])
    extra = f"; {len(old)} corrección(es) del usuario conservada(s)" if old else ""
    return ok(f"{len(decs)} decisiones en {rel(dec_file)}: SI {si} (dudas {dudas}), NO {len(decs) - si}, {len(lines)} desacuerdo(s) resuelto(s){extra}",
              "escribe .cribado-1/sintesis.json y corre cribado:report")


# --- set y apply -------------------------------------------------------------

def cmd_set(theme: Path, rid: str, decision: str, motivo: str, codes: str | None) -> int:
    folder, state = load_state(theme)
    work = folder / WORK
    decs, errs = load_decisions(work)
    if errs:
        raise Fail(f"decisiones.jsonl no se puede leer: {errs[0]}", "corrígelo o vuelve a correr rsl-cribado-1")
    rid = rid.upper()
    if any(d["id"] == rid for d in state["duplicados"]):
        raise Fail(f"{rid} es un duplicado (NO automático)", "no se corrige; si no lo es, revisa las exportaciones y vuelve a correr cribado:prepare")
    d = next((d for d in decs if d.get("id") == rid), None)
    if d is None:
        raise Fail(f"{rid} no tiene decisión en decisiones.jsonl", "usa un id del reporte (R001…)")
    duda = decision.upper() == "DUDA"
    new = {**d, "decision": "SI" if duda else decision.upper(), "motivo": motivo.strip(), "usuario": True, "duda": duda}
    if codes is not None:
        new["criterios"] = [c.strip().upper() for c in codes.split(",") if c.strip()]
    elif new["decision"] == "SI":
        new["criterios"] = [c for c in d.get("criterios", []) if c.startswith("CI")]
    probs = validate(state, [new if x is d else x for x in decs])
    if probs:
        for p in probs:
            print(f"  - {p}")
        return error(f"la corrección de {rid} no es válida; no se cambió nada", "revisa decisión (SI|DUDA|NO), motivo (≤ 25 palabras) y criterios del picoc")
    decs = [new if x is d else x for x in decs]
    (work / "decisiones.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in decs), encoding="utf-8")
    print(f"{rid}: {d.get('decision')} → {new['decision']} ({', '.join(new.get('criterios') or []) or 'sin criterios'})")
    return cmd_report(theme)


def cmd_apply(theme: Path) -> int:
    folder, state = load_state(theme)
    work = folder / WORK
    decs, errs = load_decisions(work)
    errs += validate(state, decs) if not errs else []
    sint, serrs = load_sintesis(work)
    if errs or serrs:
        return error(f"el cribado tiene {len(errs) + len(serrs)} problema(s)", f"corre pnpm -s cribado:report {rel(theme)} y corrígelos antes de aplicar")
    h = decisions_hash(state, decs, sint)
    sh = folder / f"{STAGE}.shadow.jsonl"
    dash = folder / f"{STAGE}.md"
    m = HASH_RE.search(dash.read_text(encoding="utf-8")) if dash.exists() else None
    try:
        lines = sh.read_text(encoding="utf-8").splitlines() if sh.exists() else []
        meta = json.loads(lines[0])["_meta"] if lines else {}
    except (json.JSONDecodeError, KeyError):
        meta = {}
    if not m or m.group(1) != h or meta.get("hash") != h:
        raise Fail(f"{dash.name} o {sh.name} no están al día con las decisiones", f"corre pnpm -s cribado:report {rel(theme)}, revísalo y vuelve a aplicar")
    rows = [json.loads(l) for l in lines[1:] if l.strip()]
    uni = folder / state["unificado"]
    with uni.open(encoding="utf-8-sig", newline="") as fh:
        table = list(csv.reader(fh))
    header, body = table[0], table[1:]
    if len(body) != len(rows) or any(b[0] != r["id"] for b, r in zip(body, rows)):
        raise Fail(f"{uni.name} y {sh.name} no tienen los mismos registros", f"vuelve a correr pnpm -s cribado:prepare {rel(theme)} y cribado:report")
    out = []
    for b, r in zip(body, rows):
        why = r["motivo"].rstrip(".")
        if not r.get("duplicado_de") and r["criterios"]:
            why += f" ({', '.join(r['criterios'])})"
        out.append(b + [r["decision"], why + "."])
    dest = uni.with_name(uni.stem + f"-{STAGE}.csv")
    with dest.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_ALL)
        w.writerow(header + [COL_OK, COL_WHY])
        w.writerows(out)
    si = sum(1 for o in out if o[-2] == "SI")
    return ok(f"{rel(dest)} con {len(out)} registros: SI {si}, NO {len(out) - si} (columnas «{COL_OK}» y «{COL_WHY}»)",
              "cribado a texto completo de los SI")


def main(args: list[str]) -> int:
    cmds = ("prepare", "merge", "report", "keywords", "set", "apply")
    if len(args) < 2 or args[0] not in cmds:
        print(__doc__)
        return error(USAGE, code=2)
    cmd, theme, rest = args[0], theme_dir(args[1]), args[2:]
    if cmd == "set" and len(rest) in (3, 4):
        return cmd_set(theme, rest[0], rest[1], rest[2], rest[3] if len(rest) == 4 else None)
    if cmd != "set" and not rest:
        return {"prepare": cmd_prepare, "merge": cmd_merge, "report": cmd_report, "keywords": cmd_keywords, "apply": cmd_apply}[cmd](theme)
    return error(USAGE, code=2)


if __name__ == "__main__":
    run(main)
