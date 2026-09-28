#!/usr/bin/env python3
"""Verifica docs/<slug>/picoc/<fecha>-<MARCO>/picoc.md contra playbooks/vocabulario-controlado.md.

Reglas:
  MARCO  **Marco:** == sufijo de la carpeta == formato.marco de paper/paper.yml (por defecto PICOCT)
  PG     pregunta general == § 1.2 Problemática de la ficha (informe-polish.md | informe.md)
  R1     cada fila de la tabla de componentes justifica su origen citando el tema (“…”)
  R2     una fila por componente del marco; keywords de cada fila (salvo T) == su bloque en Scopus, WoS e IEEE Xplore;
         T == filtro de año en las 3 bases; sin filtros de tipo de documento; IEEE Xplore ≤ 10 comodines
  R3     exactamente 1 RQ (¿…?) por componente del marco, enlazada desde la tabla
  KW     palabras clave ES/EN: primero descriptores IEEE preferidos (con pág.), libres solo al final y justificados
  IEEE   cada descriptor declarado es preferido en ieee-thesaurus.json y está en su bloque

Uso:
  python3 scripts/picoc-lint.py docs/<slug>                              # valida el último picoc
  python3 scripts/picoc-lint.py docs/<slug>/picoc/<fecha>-<MARCO>/picoc.md
  python3 scripts/picoc-lint.py --latest docs/<slug>                     # marco configurado + último picoc (OK | DESFASADO | FALTA)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import picoc_versions as pv  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
THES_JSON = ROOT / "global" / "thesaurus" / "ieee-thesaurus.json"
DATABASES = ("Scopus", "Web of Science", "IEEE Xplore")
IEEE_MAX_WILDCARDS = 10
FORBIDDEN = ("Cribado", "T — Filtros", "T - Filtros", "Filtros", "Términos libres")
FILTER_PREFIX = re.compile(r"(DT|PY|PUBYEAR|LIMIT-TO)\s*=?\s*$", re.I)
QUESTION = re.compile(r"¿[^?]+\?", re.S)


def rel(p: Path) -> Path:
    p = p.resolve()
    return p.relative_to(ROOT) if ROOT in p.parents else p


def sections(text: str, level: str = "##") -> dict[str, str]:
    parts = re.split(rf"^{level}\s+(.+)$", text, flags=re.M)
    return {parts[i].strip(): parts[i + 1] for i in range(1, len(parts), 2)}


def find(secs: dict[str, str], prefix: str) -> str | None:
    p = prefix.casefold()
    return next((v for k, v in secs.items() if k.casefold().startswith(p)), None)


def table(body: str) -> list[dict[str, str]]:
    rows = [l.strip() for l in body.splitlines() if l.strip().startswith("|")]
    if len(rows) < 2:
        return []

    def cells(line: str) -> list[str]:
        return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]

    head = cells(rows[0])
    return [dict(zip(head, cells(r))) for r in rows[2:]]


def col(row: dict[str, str], prefix: str) -> str:
    p = prefix.casefold()
    return next((v for k, v in row.items() if k.casefold().startswith(p)), "")


def norm_term(t: str) -> str:
    t = re.sub(r'^"IEEE Terms"\s*:\s*', "", t.strip(), flags=re.I)
    t = t.replace('"', "").replace("“", "").replace("”", "")
    return re.sub(r"\s+", " ", t).strip().casefold()


def norm_text(s: str) -> str:
    s = re.sub(r"[*_`]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def question(body: str | None) -> str | None:
    m = QUESTION.search(body or "")
    return norm_text(m.group(0)) if m else None


def code_block(body: str | None) -> str | None:
    if body is None:
        return None
    m = re.search(r"```[a-z]*\n(.*?)```", body, flags=re.S)
    return m.group(1) if m else None


def query_blocks(q: str) -> list[list[str]]:
    blocks = []
    for m in re.finditer(r"\(([^()]*)\)", q):
        if FILTER_PREFIX.search(q[: m.start()].rstrip()):
            continue
        inner = re.sub(r"^\s*ALL\s*=\s*", "", m.group(1))
        blocks.append([norm_term(t) for t in re.split(r"\s+OR\s+", inner.strip()) if t.strip()])
    return blocks


def ficha_question(theme: Path) -> tuple[str | None, Path | None]:
    for name in ("informe-polish.md", "informe.md"):
        f = theme / name
        if f.is_file():
            body = find(sections(f.read_text(encoding="utf-8"), "###"), "1.2")
            return question(body), f
    return None, None


def paper_question(theme: Path) -> tuple[str | None, Path | None]:
    paper = theme / "paper"
    vs = sorted(p for p in paper.iterdir() if p.is_dir() and re.match(r"\d{4}-\d{2}-\d{2}", p.name)) if paper.is_dir() else []
    for v in reversed(vs):
        for name in ("paper-polish.md", "paper-borrador.md"):
            f = v / name
            if not f.is_file():
                continue
            m = re.search(r"<!-- paper:section id=encabezado -->(.*?)<!-- /paper:section -->", f.read_text(encoding="utf-8"), re.S)
            if m:
                pm = re.search(r"Problemática[^\n]*\n?(.*?)(?:\n\s*\n|\Z)", m.group(1), re.S)
                return question(pm.group(0) if pm else None), f
    return None, None


def main(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    secs = sections(text)
    theme = pv.theme_of(path.resolve())
    errs: list[str] = []
    warns: list[str] = []

    m = re.search(r"\*\*Marco:\*\*\s*(PICOCT|PICOC|PICO)\b", text)
    if not m:
        print("FAIL: falta '**Marco:** PICO|PICOC|PICOCT'")
        return 1
    marco = m.group(1)
    comps = pv.COMPONENTS[marco]
    folder = pv.dir_marco(path)
    if folder is None:
        errs.append("MARCO: el archivo debe estar en picoc/<AAAA-MM-DD>[-n]-<MARCO>/picoc.md")
    elif folder != marco:
        errs.append(f"MARCO: **Marco:** {marco} pero la carpeta es {folder}")
    configured = pv.configured_marco(theme)
    if configured != marco:
        errs.append(f"MARCO: paper.yml pide {configured} y este picoc es {marco} (correr rsl-picoc)")

    for k in secs:
        if any(k.casefold().startswith(f.casefold()) for f in FORBIDDEN):
            errs.append(f"sección prohibida: '## {k}' (el cribado, los filtros y los términos libres no van como sección)")

    general = question(find(secs, "Pregunta general"))
    if not general:
        errs.append("PG: falta la pregunta general (¿…?)")
    else:
        fq, ff = ficha_question(theme)
        if fq is None:
            warns.append("PG: no hay ficha (informe-polish.md / informe.md § 1.2) para comparar la pregunta general")
        elif fq != general:
            errs.append(f"PG: la pregunta general difiere de la § 1.2 de {rel(ff)} (debe copiarse literal)")
        pq, pf = paper_question(theme)
        if pq is not None and pq != general:
            warns.append(f"PG: la Problemática del encabezado de {rel(pf)} difiere de la pregunta general")

    rq_rows = table(find(secs, "Preguntas por componente") or "")
    rq_by: dict[str, list[str]] = {}
    for r in rq_rows:
        c = col(r, "Comp")
        rq_by.setdefault(c, []).append(col(r, "RQ"))
        q = col(r, "Pregunta")
        if not (q.startswith("¿") and q.endswith("?")):
            errs.append(f"R3: la pregunta de {c} no es interrogativa (¿…?)")
        if not col(r, "Dato"):
            errs.append(f"R3: {c} sin 'Dato a extraer'")
    for c in comps:
        if len(rq_by.get(c, [])) != 1:
            errs.append(f"R3: {c} tiene {len(rq_by.get(c, []))} preguntas (debe ser 1)")
    for c in rq_by:
        if c not in comps:
            errs.append(f"R3: componente '{c}' no pertenece a {marco}")
    rq_ids = {c: ids[0] for c, ids in rq_by.items() if ids and ids[0]}

    comp_rows = table(find(secs, "Tabla de componentes") or "")
    if not comp_rows:
        errs.append("R2: falta la 'Tabla de componentes (1:1 con las queries)'")
    by_comp = {col(r, "Comp"): r for r in comp_rows}
    if [col(r, "Comp") for r in comp_rows] != comps:
        errs.append(f"R2: la tabla debe tener exactamente las filas {', '.join(comps)} en ese orden (tiene {', '.join(col(r, 'Comp') for r in comp_rows) or '—'})")
    rows_terms: list[tuple[str, list[str]]] = []
    years: tuple[int, int] | None = None
    for c in comps:
        r = by_comp.get(c)
        if r is None:
            continue
        if not col(r, "Concepto").strip("*_ —-"):
            errs.append(f"R2: {c} sin concepto")
        if rq_ids.get(c) and rq_ids[c] not in col(r, "RQ"):
            errs.append(f"R3: {c} debe enlazar {rq_ids[c]} (tiene {col(r, 'RQ') or '—'})")
        if not re.search(r"[“\"][^”\"]{3,}[”\"]", col(r, "Justific")):
            errs.append(f"R1: la justificación de {c} no cita el tema (“…”)")
        kw = col(r, "Keywords")
        if c == "T":
            ym = re.search(r"(\d{4})\s*[–-]\s*(\d{4})", kw)
            if not ym:
                errs.append("R2: T debe indicar el rango de años (p. ej. `2020–2026`)")
            else:
                years = (int(ym.group(1)), int(ym.group(2)))
            continue
        terms = [norm_term(t) for t in re.findall(r"`([^`]+)`", kw)]
        if not terms:
            errs.append(f"R2: {c} sin keywords")
        if len(set(terms)) != len(terms):
            errs.append(f"R2: {c} tiene keywords repetidas")
        rows_terms.append((c, terms))

    for db in DATABASES:
        body = find(secs, f"Query {db}")
        q = code_block(body)
        if q is None:
            errs.append(f"R2: falta 'Query {db}' con bloque de código")
            continue
        if db == "IEEE Xplore" and q.count("*") > IEEE_MAX_WILDCARDS:
            errs.append(f"R2 [{db}]: {q.count('*')} comodines; IEEE Xplore admite {IEEE_MAX_WILDCARDS} (usar frases sin * fuera de P)")
        if re.search(r"DOCTYPE|\bDT\s*=", q):
            errs.append(f"R2 [{db}]: quitar el filtro de tipo de documento (lo decide el usuario en el cribado)")
        blocks = query_blocks(q)
        if len(blocks) != len(rows_terms):
            errs.append(f"R2 [{db}]: {len(blocks)} bloques en la query vs {len(rows_terms)} componentes con keywords")
        for (c, terms), blk in zip(rows_terms, blocks):
            extra, missing = sorted(set(blk) - set(terms)), sorted(set(terms) - set(blk))
            if extra or missing or len(blk) != len(terms):
                errs.append(
                    f"R2 [{db}] {c}: tabla {len(terms)} vs query {len(blk)}"
                    + (f" · solo en query: {extra}" if extra else "")
                    + (f" · solo en tabla: {missing}" if missing else "")
                )
        if years:
            a, b = years
            ok = {
                "Scopus": re.search(rf"PUBYEAR\s*>\s*{a - 1}\b", q) and re.search(rf"PUBYEAR\s*<\s*{b + 1}\b", q),
                "Web of Science": re.search(rf"PY\s*=\s*\(\s*{a}\s*-\s*{b}\s*\)", q),
                "IEEE Xplore": re.search(rf"{a}\s*[–-]\s*{b}", body or ""),
            }[db]
            if not ok:
                errs.append(f"R2 [{db}]: falta el filtro de año {a}–{b} de T")
        elif re.search(r"PUBYEAR|\bPY\s*=", q):
            errs.append(f"R2 [{db}]: filtro de año sin componente T en {marco}")

    kw_rows = table(find(secs, "Palabras clave") or "")
    if not kw_rows:
        errs.append("KW: falta la tabla 'Palabras clave'")
    kw_ieee: set[str] = set()
    seen_free = False
    thes = json.loads(THES_JSON.read_text(encoding="utf-8"))["terms"] if THES_JSON.exists() else None
    if thes is None:
        errs.append("IEEE: falta global/thesaurus/ieee-thesaurus.json (pnpm run bootstrap)")
    for r in kw_rows:
        es, en, tipo = col(r, "Español"), col(r, "Inglés"), col(r, "Tipo").casefold()
        if not es or not en:
            errs.append(f"KW: fila sin español o inglés ({es or en})")
        if tipo.startswith("ieee"):
            if seen_free:
                errs.append(f"KW: '{en}' es IEEE pero aparece después de un término libre (los libres van al final)")
            if not re.search(r"p\.\s*\d+", col(r, "Pág")):
                errs.append(f"KW: '{en}' sin página IEEE (p.N)")
            if thes is not None:
                e = thes.get(norm_text(en).casefold())
                if not e:
                    errs.append(f"KW: '{en}' no existe en el IEEE Thesaurus (márcalo Libre)")
                elif not e["preferred"]:
                    errs.append(f"KW: '{en}' no es preferido (USE {e['USE']})")
            kw_ieee.add(norm_text(en).casefold())
        elif tipo.startswith("libre"):
            seen_free = True
            if not col(r, "Justific").strip("*_ —-"):
                errs.append(f"KW: el término libre '{en}' necesita una justificación breve")
        else:
            errs.append(f"KW: '{en}' con Tipo '{col(r, 'Tipo')}' (usa IEEE | Libre)")

    if thes is not None:
        for c, terms in rows_terms:
            for d in re.findall(r"([^·(]+?)\s*\(p\.\s*\d+\)", col(by_comp[c], "Descriptor")):
                name = d.strip()
                e = thes.get(re.sub(r"\s+", " ", name).casefold())
                if not e:
                    errs.append(f"IEEE: {c} '{name}' no existe en el IEEE Thesaurus")
                elif not e["preferred"]:
                    errs.append(f"IEEE: {c} '{name}' no es preferido (USE {e['USE']})")
                k = name.casefold()
                if not any(t == k or (t.endswith("*") and k.startswith(t[:-1])) for t in terms):
                    errs.append(f"IEEE: {c} descriptor '{name}' no aparece en su bloque de la query")
                if k not in kw_ieee:
                    errs.append(f"KW: el descriptor '{name}' ({c}) falta en Palabras clave")

    for w in warns:
        print(f"WARN {w}")
    if errs:
        print(f"FAIL {rel(path)} ({marco})")
        for e in errs:
            print(f"  - {e}")
        return 1
    total = sum(len(t) for _, t in rows_terms)
    print(f"PASS {rel(path)} ({marco}) · {len(rows_terms)} bloques · {total} términos · {len(rq_rows)} RQ · T {years[0]}–{years[1]} · 3 bases" if years
          else f"PASS {rel(path)} ({marco}) · {len(rows_terms)} bloques · {total} términos · {len(rq_rows)} RQ · 3 bases")
    return 0


def resolve(arg: str) -> Path:
    p = Path(arg)
    p = p if p.is_absolute() else Path.cwd() / p
    if not p.is_dir():
        return p
    if pv.PICOC_DIR_RE.match(p.name):
        return p / pv.PICOC_FILE
    f = pv.latest_file(p)
    if f is None:
        sys.exit(f"FAIL: {arg} no tiene picoc/<fecha>-<MARCO>/picoc.md (correr rsl-picoc)")
    return f


def latest(arg: str) -> int:
    theme = Path(arg)
    theme = theme if theme.is_absolute() else Path.cwd() / theme
    marco, f, state = pv.status(theme)
    src = "paper.yml" if (theme / "paper" / "paper.yml").exists() else "por defecto, sin paper.yml"
    print(f"marco: {marco} ({src})")
    print(f"último: {rel(f) if f else '—'}")
    print(f"estado: {state}" + ("" if state == "OK" else " → correr rsl-picoc"))
    return 0 if state == "OK" else 1


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == "--latest":
        sys.exit(latest(args[1]))
    if len(args) != 1 or args[0].startswith("-"):
        print(__doc__)
        sys.exit(2)
    target = resolve(args[0])
    if not target.is_file():
        sys.exit(f"FAIL: no existe {args[0]}")
    sys.exit(main(target))
