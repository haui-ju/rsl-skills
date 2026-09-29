#!/usr/bin/env python3
"""Verifica docs/<slug>/picoc/<fecha>-<MARCO>/picoc.md contra playbooks/vocabulario-controlado.md.

Reglas:
  MARCO  **Marco:** == sufijo de la carpeta == formato.marco de config.yml (por defecto PICOCT)
  PG     pregunta general == § 1.2 Problemática de la ficha (informe-polish.md | informe.md)
  R1     cada fila de la tabla de componentes justifica su origen citando el tema (“…”)
  R2     una fila por componente del marco; keywords de cada fila (salvo T) == su bloque en Scopus, WoS e IEEE Xplore;
         filtros de CR en las queries: periodo (== T si lo hay) en las 3 bases; tipo de documento e idioma en Scopus y WoS;
         acceso abierto en Scopus (OA) y anotado bajo WoS e IEEE Xplore; IEEE Xplore ≤ 10 comodines; ≤ 100 keywords en total
  R3     exactamente 1 RQ (¿…?) por componente del marco, enlazada desde la tabla
  KY     '## Keywords' tras 'Palabras clave': 5 o 6 filas (EN · ES · Comp.) que van al paper; cada término sale de
         Palabras clave con su mismo componente y cada componente del marco (salvo T) aporta al menos una
  CR     última sección '## Criterios de inclusión y exclusión' con '### Inclusión' y '### Exclusión': listas de viñetas
         breves (≤ 25 palabras, ≥ 2 por lista); la inclusión fija periodo (== T), idioma, tipo de documento y acceso abierto
  KW     palabras clave ES/EN: primero descriptores IEEE preferidos (con pág.), libres solo al final y justificados
  IEEE   cada descriptor declarado es preferido en ieee-thesaurus.json y está en su bloque
  VOC    **Vocabulario:** cita (IEEE, 2019) siempre, (ACM, 2012) si se usa «ACM CCS» y (NLM, 2026) si se usa «MeSH»; solo los usados

Uso:
  python3 scripts/picoc-lint.py docs/<slug>                              # valida el último picoc
  python3 scripts/picoc-lint.py docs/<slug>/picoc/<fecha>-<MARCO>/picoc.md
  python3 scripts/picoc-lint.py --latest docs/<slug>                     # marco configurado + último picoc (OK | DESFASADO | FALTA) + carpeta de la siguiente versión
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import picoc_versions as pv  # noqa: E402
from rsl_out import Fail, error, ok, run  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
THES_JSON = ROOT / "global" / "thesaurus" / "ieee-thesaurus.json"
DATABASES = ("Scopus", "Web of Science", "IEEE Xplore")
IEEE_MAX_WILDCARDS = 10
MAX_QUERY_TERMS = 100
SUGERENCIA = "cribado-1-sugerencia.md"
FORBIDDEN = ("Cribado", "T — Filtros", "T - Filtros", "Filtros", "Términos libres")
FILTER_PREFIX = re.compile(r"(DT|PY|LA|PUBYEAR|LIMIT-TO|DOCTYPE|LANGUAGE)\s*=?\s*$", re.I)
QUESTION = re.compile(r"¿[^?]+\?", re.S)
CRITERIA = "Criterios de inclusión y exclusión"
KEYWORDS_MIN, KEYWORDS_MAX = 5, 6
CRITERION_MAX_WORDS = 25
LANGUAGE_RE = re.compile(r"idioma|inglés|español|portugués|francés|alemán|english|spanish", re.I)
DOCTYPE_RE = re.compile(r"revista|congreso|conferencia|actas|arbitra|revisi[oó]n por pares|journal|proceedings", re.I)
OA_RE = re.compile(r"acceso abierto|open access", re.I)
PERIOD_RE = re.compile(r"(\d{4})\s*(?:[–-]|y|a|al|hasta)\s*(\d{4})")
LANGS = {"English": r"ingl[eé]s|english", "Spanish": r"español|spanish", "Portuguese": r"portugu[eé]s|portuguese",
         "French": r"franc[eé]s|french", "German": r"alem[aá]n|german"}
DOCTYPES = {"ar": (r"revista|journal", "Article"), "cp": (r"congreso|conferencia|actas|proceedings", "Proceedings Paper")}


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


VOCABS = {  # vocabulario -> (cita en la cabecera, uso en el cuerpo, nombre)
    "IEEE": (r"\(IEEE,\s*\d{4}\)", None, "IEEE Thesaurus (IEEE, 2019)"),
    "ACM": (r"\(ACM,\s*\d{4}\)", r"\bACM CCS\b", "ACM Computing Classification System (ACM, 2012)"),
    "MeSH": (r"\(NLM,\s*\d{4}\)", r"\bMeSH\b", "Medical Subject Headings (NLM, 2026)"),
}


def vocab_header(text: str) -> str:
    m = re.search(r"\*\*Vocabulario:\*\*(.*?)(?:·\s*\*\*Tema:\*\*|$)", text, flags=re.M)
    return m.group(1) if m else ""


def vocab_used(text: str) -> list[str]:
    """Vocabularios que el picoc usa: IEEE siempre; ACM CCS y MeSH si alguna justificación los cita."""
    body = "\n".join(l for l in text.splitlines() if "**Vocabulario:**" not in l)
    return [k for k, (_, use, _) in VOCABS.items() if use is None or re.search(use, body)]


def ficha_questions(theme: Path) -> tuple[list[str], Path | None]:
    for name in ("informe-polish.md", "informe.md"):
        f = theme / name
        if f.is_file():
            body = find(sections(f.read_text(encoding="utf-8-sig"), "###"), "1.2") or ""
            return [norm_text(q) for q in QUESTION.findall(body)], f
    return [], None


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
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        raise Fail(f"{rel(path)} no está en UTF-8", "guárdalo como UTF-8")
    if not text.strip():
        raise Fail(f"{rel(path)} está vacío", "regenera el marco con rsl-picoc")
    secs = sections(text)
    theme = pv.theme_of(path.resolve())
    errs: list[str] = []
    warns: list[str] = []

    m = re.search(r"\*\*Marco:\*\*\s*([A-Za-z]+)\b", text)
    if not m:
        raise Fail(f"{rel(path)} no declara '**Marco:** <letras>' (p. ej. PICOCT, PIO)", "regenera el marco con rsl-picoc")
    try:
        marco = pv.marco_label(m.group(1))
        comps = pv.parse_marco(marco)
    except pv.MarcoError as e:
        raise Fail(f"**Marco:** de {rel(path)}: {e}", "regenera el marco con rsl-picoc")
    configured = pv.configured_marco(theme)
    folder = pv.dir_marco(path)
    if folder is None:
        errs.append("MARCO: el archivo debe estar en picoc/<AAAA-MM-DD>[-n]-<MARCO>/picoc.md")
    elif folder != marco:
        errs.append(f"MARCO: **Marco:** {marco} pero la carpeta es {folder}")
    if configured != marco:
        errs.append(f"MARCO: config.yml pide {configured} y este picoc es {marco} (correr rsl-picoc)")

    for k in secs:
        if any(k.casefold().startswith(f.casefold()) for f in FORBIDDEN):
            errs.append(f"sección prohibida: '## {k}' (el cribado, los filtros y los términos libres no van como sección)")

    general = question(find(secs, "Pregunta general"))
    if not general:
        errs.append("PG: falta la pregunta general (¿…?)")
    else:
        fqs, ff = ficha_questions(theme)
        if ff is None:
            warns.append("PG: no hay ficha (informe-polish.md / informe.md § 1.2) para comparar la pregunta general")
        elif not fqs:
            errs.append(f"PG: la § 1.2 de {rel(ff)} no tiene una pregunta ¿…?")
        elif len(fqs) > 1:
            errs.append(f"PG: la § 1.2 de {rel(ff)} tiene {len(fqs)} preguntas; debe haber una sola pregunta general")
        elif fqs[0] != general:
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
                if years[0] > years[1]:
                    errs.append(f"R2: T tiene los años invertidos ({years[0]}–{years[1]}); va del más antiguo al más reciente")
            continue
        terms = [norm_term(t) for t in re.findall(r"`([^`]+)`", kw)]
        if not terms:
            errs.append(f"R2: {c} sin keywords")
        if len(set(terms)) != len(terms):
            errs.append(f"R2: {c} tiene keywords repetidas")
        rows_terms.append((c, terms))

    n_terms = sum(len(t) for _, t in rows_terms)
    if n_terms > MAX_QUERY_TERMS:
        errs.append(f"R2: la query tiene {n_terms} keywords; el máximo es {MAX_QUERY_TERMS} (quitar las redundantes o las de menor evidencia)")

    crit_inc = " ".join(
        norm_text(re.sub(r"^\s*[-*]\s+", "", l))
        for l in (find(sections(find(secs, CRITERIA) or "", "###"), "Inclusión") or "").splitlines()
        if re.match(r"^\s*[-*]\s+\S", l)
    )
    cr_years = PERIOD_RE.search(crit_inc)
    period = years or ((int(cr_years.group(1)), int(cr_years.group(2))) if cr_years else None)
    cr_langs = {l for l, rx in LANGS.items() if re.search(rx, crit_inc, re.I)}
    cr_types = {c for c, (rx, _) in DOCTYPES.items() if re.search(rx, crit_inc, re.I)}
    cr_oa = bool(OA_RE.search(crit_inc))
    for db in DATABASES:
        body = find(secs, f"Query {db}")
        q = code_block(body)
        if q is None:
            errs.append(f"R2: falta 'Query {db}' con bloque de código")
            continue
        if db == "IEEE Xplore" and q.count("*") > IEEE_MAX_WILDCARDS:
            errs.append(f"R2 [{db}]: {q.count('*')} comodines; IEEE Xplore admite {IEEE_MAX_WILDCARDS} (usar frases sin * fuera de P)")
        if db == "Scopus":
            q_types = {c.lower() for c in re.findall(r"DOCTYPE\s*(?:,\s*\"|\()\s*(\w+)", q, re.I)}
            q_langs = {l.capitalize() for l in re.findall(r"LANGUAGE\s*,\s*\"(\w+)\"", q, re.I)}
        elif db == "Web of Science":
            dt = re.search(r"\bDT\s*=\s*\(([^)]*)\)", q)
            la = re.search(r"\bLA\s*=\s*\(([^)]*)\)", q)
            names = {v.casefold(): c for c, (_, v) in DOCTYPES.items()}
            q_types = {names.get(x.strip().strip('"').casefold(), x.strip()) for x in re.split(r"\s+OR\s+", dt.group(1))} if dt else set()
            q_langs = {x.strip().strip('"').capitalize() for x in re.split(r"\s+OR\s+", la.group(1))} if la else set()
        if db != "IEEE Xplore":
            if not q_types:
                errs.append(f"R2 [{db}]: falta el filtro de tipo de documento de los criterios de inclusión")
            elif (q_types & set(DOCTYPES)) != cr_types:
                errs.append(f"R2 [{db}]: el tipo de documento de la query ({', '.join(sorted(q_types))}) no coincide con los criterios de inclusión ({', '.join(sorted(cr_types)) or '—'})")
            if not q_langs:
                errs.append(f"R2 [{db}]: falta el filtro de idioma de los criterios de inclusión")
            elif q_langs != cr_langs:
                errs.append(f"R2 [{db}]: los idiomas de la query ({', '.join(sorted(q_langs))}) no coinciden con los criterios de inclusión ({', '.join(sorted(cr_langs)) or '—'})")
        if cr_oa:
            has_oa = re.search(r"\bOA\s*,\s*\"", q, re.I) if db == "Scopus" else OA_RE.search(body or "")
            if not has_oa:
                errs.append(f"R2 [{db}]: falta el filtro de acceso abierto de los criterios de inclusión" + ("" if db == "Scopus" else " (anotado bajo la query)"))
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
        if period:
            a, b = period
            has_year = {
                "Scopus": re.search(rf"PUBYEAR\s*>\s*{a - 1}\b", q) and re.search(rf"PUBYEAR\s*<\s*{b + 1}\b", q),
                "Web of Science": re.search(rf"PY\s*=\s*\(\s*{a}\s*-\s*{b}\s*\)", q),
                "IEEE Xplore": re.search(rf"{a}\s*[–-]\s*{b}", body or ""),
            }[db]
            if not has_year:
                errs.append(f"R2 [{db}]: falta el filtro de año {a}–{b} de " + ("T" if years else "los criterios de inclusión"))
        elif re.search(r"PUBYEAR|\bPY\s*=", q):
            errs.append(f"R2 [{db}]: filtro de año sin periodo en los criterios de inclusión")

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

    heads = re.findall(r"^##\s+(.+)$", text, flags=re.M)
    kw_en = {}
    for r in kw_rows:
        for term in col(r, "Inglés").split("/"):
            kw_en.setdefault(norm_text(term).casefold(), col(r, "Comp"))
    ky_body = secs.get("Keywords")
    ky_rows = table(ky_body or "")
    if ky_body is None:
        errs.append(f"KY: falta '## Keywords' ({KEYWORDS_MIN} o {KEYWORDS_MAX} palabras clave, las más relevantes, que van al paper)")
    else:
        pos = [h.strip() for h in heads]
        if "Palabras clave" in pos and pos.index("Keywords") != pos.index("Palabras clave") + 1:
            errs.append("KY: '## Keywords' va justo después de '## Palabras clave'")
        if not KEYWORDS_MIN <= len(ky_rows) <= KEYWORDS_MAX:
            errs.append(f"KY: '## Keywords' tiene {len(ky_rows)} filas; deben ser {KEYWORDS_MIN} o {KEYWORDS_MAX}, solo las más relevantes")
        seen = set()
        for r in ky_rows:
            en, es, c = norm_text(col(r, "Keyword")), norm_text(col(r, "Palabra")), col(r, "Comp")
            if not en or not es:
                errs.append(f"KY: fila sin inglés o español ({en or es or '—'})")
                continue
            if en.casefold() in seen:
                errs.append(f"KY: '{en}' repetida")
            seen.add(en.casefold())
            if en.casefold() not in kw_en:
                errs.append(f"KY: '{en}' no está en la tabla 'Palabras clave' (las keywords salen de ahí)")
            elif kw_en[en.casefold()] != c:
                errs.append(f"KY: '{en}' es del componente {kw_en[en.casefold()]} en Palabras clave, no de {c or '—'}")
        missing = [c for c in comps if c != "T" and c not in {col(r, "Comp") for r in ky_rows}]
        if ky_rows and missing:
            errs.append(f"KY: falta al menos una keyword de {', '.join(missing)} (deben estar todos los componentes del marco salvo T)")

    n_inc = n_exc = 0
    crit = find(secs, CRITERIA)
    if crit is None:
        errs.append(f"CR: falta la sección final '## {CRITERIA}' (qué se acepta y qué no para revisar un artículo)")
    else:
        if not heads[-1].strip().casefold().startswith(CRITERIA.casefold()):
            errs.append(f"CR: '## {CRITERIA}' debe ser la última sección (después va '{heads[-1].strip()}')")
        subs = sections(crit, "###")
        lists = {}
        for name in ("Inclusión", "Exclusión"):
            body = find(subs, name)
            items = [norm_text(re.sub(r"^\s*[-*]\s+", "", l)) for l in (body or "").splitlines() if re.match(r"^\s*[-*]\s+\S", l)]
            lists[name] = items
            if body is None:
                errs.append(f"CR: falta '### {name}' dentro de '## {CRITERIA}'")
                continue
            if len(items) < 2:
                errs.append(f"CR: '### {name}' necesita al menos 2 criterios en viñetas (tiene {len(items)})")
            for it in items:
                if len(it.split()) > CRITERION_MAX_WORDS:
                    errs.append(f"CR: criterio de {name.lower()} demasiado largo ({len(it.split())} palabras; máximo {CRITERION_MAX_WORDS}): «{it[:60]}…»")
        inc = " ".join(lists.get("Inclusión", []))
        n_inc, n_exc = len(lists.get("Inclusión", [])), len(lists.get("Exclusión", []))
        if lists.get("Inclusión"):
            if not LANGUAGE_RE.search(inc):
                errs.append("CR: la inclusión debe fijar el idioma (p. ej. «artículos en inglés o español»)")
            if not DOCTYPE_RE.search(inc):
                errs.append("CR: la inclusión debe fijar el tipo de documento (p. ej. «artículos de revista revisados por pares»)")
            if not cr_years:
                errs.append("CR: la inclusión debe fijar el periodo (p. ej. «artículos publicados entre 2021 y 2026»)")
            if not cr_oa:
                errs.append("CR: la inclusión debe fijar el acceso abierto (criterio por defecto; «artículos de acceso abierto»)")
            if years and not re.search(rf"{years[0]}\s*(?:[–-]|y|a|al|hasta)\s*{years[1]}", inc):
                errs.append(f"CR: la inclusión debe usar el mismo periodo que T ({years[0]}–{years[1]})")

    head = vocab_header(text)
    used = vocab_used(text)
    for k, (cite, _, name) in VOCABS.items():
        cited = bool(re.search(cite, head))
        if k in used and not cited:
            errs.append(f"VOC: la cabecera (**Vocabulario:**) debe citar {name}" + ("" if k == "IEEE" else f", porque las justificaciones usan {k if k == 'MeSH' else 'ACM CCS'}"))
        elif cited and k not in used:
            errs.append(f"VOC: la cabecera cita {name}, pero ninguna justificación lo usa (cita solo los vocabularios usados)")

    for w in warns:
        print(f"WARN {w}")
    if errs:
        for e in errs:
            print(f"  - {e}")
        return error(f"el picoc {rel(path)} ({marco}) tiene {len(errs)} error(es) (ver detalle arriba)", "corrígelo regenerando una versión con rsl-picoc")
    total = sum(len(t) for _, t in rows_terms)
    return ok(f"picoc {rel(path)} ({marco}) válido: {len(rows_terms)} bloques, {total} términos, {len(rq_rows)} RQ" + (f", T {years[0]}–{years[1]}" if years else "") + f", 3 bases, {len(ky_rows)} keywords, {n_inc} criterios de inclusión y {n_exc} de exclusión")


def resolve(arg: str) -> Path:
    p = Path(arg)
    p = p if p.is_absolute() else Path.cwd() / p
    if not p.is_dir():
        return p
    if pv.PICOC_DIR_RE.match(p.name):
        return p / pv.PICOC_FILE
    f = pv.latest_file(p)
    if f is None:
        raise Fail(f"{arg} no tiene picoc/<fecha>-<MARCO>/picoc.md", f"créalo con: Usa rsl-picoc sobre {arg.rstrip('/')}/")
    return f


def latest(arg: str) -> int:
    theme = Path(arg)
    theme = theme if theme.is_absolute() else Path.cwd() / theme
    if not theme.is_dir():
        raise Fail(f"{arg} no es la carpeta de un tema", "usa docs/<slug>")
    marco, f, state = pv.status(theme)
    src = pv.CONFIG if (theme / pv.CONFIG).exists() else f"por defecto, sin {pv.CONFIG}"
    nxt = f"{rel(pv.next_dir(theme, marco))}/"
    print(f"marco: {marco} ({src})")
    print(f"último: {rel(f) if f else '—'}")
    print(f"estado: {state}")
    print(f"siguiente versión: {nxt}")
    sug = f.parent / SUGERENCIA if f else None
    if sug and sug.exists():
        print(f"sugerencia: {rel(sug)} (pendiente: rsl-picoc modo sugerencia)")
    if state != "OK":
        what = "no hay picoc" if state == "FALTA" else f"el último picoc no es {marco} (cambió formato.marco)"
        return error(f"picoc {state}: {what}", f"corre rsl-picoc; la versión nueva va en {nxt}")
    if sug and sug.exists():
        return ok(f"marco {marco} al día ({rel(f)}), con sugerencia del cribado 1 pendiente", f"Usa rsl-picoc sobre {rel(theme)}/ (modo sugerencia; va en {nxt})")
    return ok(f"marco {marco} al día ({rel(f)})")


def cli(args: list[str]) -> int:
    try:
        return dispatch(args)
    except pv.MarcoError as e:
        raise Fail(str(e), e.fix)


def dispatch(args: list[str]) -> int:
    if len(args) == 2 and args[0] == "--latest":
        return latest(args[1])
    if len(args) != 1 or args[0].startswith("-"):
        print(__doc__)
        return error("uso: picoc:lint <docs/slug | picoc.md> · picoc:latest <docs/slug>", code=2)
    target = resolve(args[0])
    if not target.is_file():
        raise Fail(f"no existe {args[0]}", "indica docs/<slug> o un picoc.md")
    return main(target)


if __name__ == "__main__":
    run(cli)
