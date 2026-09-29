"""Metodología del paper como espejo del último picoc/<fecha>-<MARCO>/picoc.md.

Bloques espejo (se copian del picoc aunque la sección esté frozen; la prosa alrededor no se toca):
  marco-pico           Tabla del marco (concepto por componente), pregunta general (> ¿…?) y tabla de RQ
  palabras-clave       Tabla III: Keywords (EN) == términos de cada bloque de la query, mismo orden, ni uno más
                       ni uno menos (el * cuenta); Palabras clave (ES): una traducción por término (mismo número);
                       nota (_Nota._) que cita los mismos vocabularios que la cabecera del picoc (regla VOC)
  ecuacion-busqueda    bloques de Scopus y Web of Science idénticos a los del picoc (espacios aparte)
  criterios-seleccion  viñetas **CIn:** / **CEn:** con el mismo texto y orden que las listas del picoc
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

_spec = importlib.util.spec_from_file_location("picoc_lint", Path(__file__).with_name("picoc-lint.py"))
pl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pl)

MIRRORED = ("marco-pico", "palabras-clave", "ecuacion-busqueda", "criterios-seleccion")
DATABASES = ("Scopus", "Web of Science")
FENCE_RE = re.compile(r"```[^\n]*\n.*?```", re.S)
CRIT_RE = re.compile(r"^\s*[-*]\s+\*\*(C[IE])\d+:?\*\*:?\s*(.+)$", re.M)
NOTE_RE = re.compile(r"^\s*[_*]Nota\.[_*].*$", re.M)
PAPER_VOCAB = {  # cómo se nombra cada vocabulario en la nota del paper
    "IEEE": (r"IEEE Thesaurus", r"\((?:Institute of Electrical and Electronics Engineers \[IEEE\]|IEEE),\s*\d{4}\)"),
    "ACM": (r"ACM Computing Classification System", r"\((?:Association for Computing Machinery \[ACM\]|ACM),\s*\d{4}\)"),
    "MeSH": (r"Medical Subject Headings", r"\((?:National Library of Medicine \[NLM\]|NLM),\s*\d{4}\)"),
}
TERM_SPLIT = re.compile(r',\s*(?=(?:[^"]*"[^"]*")*[^"]*$)')


def _bullets(body: str | None) -> list[str]:
    return [pl.norm_text(re.sub(r"^\s*[-*]\s+", "", l)) for l in (body or "").splitlines() if re.match(r"^\s*[-*]\s+\S", l)]


def mirror(picoc: Path) -> dict:
    """Lo que el paper debe copiar del picoc."""
    text = picoc.read_text(encoding="utf-8-sig")
    secs = pl.sections(text)
    comp_rows = pl.table(pl.find(secs, "Tabla de componentes") or "")
    crit = pl.sections(pl.find(secs, pl.CRITERIA) or "", "###")
    return {
        "comps": [pl.col(r, "Comp") for r in comp_rows if pl.col(r, "Comp") != "T"],
        "keywords": {pl.col(r, "Comp"): re.findall(r"`([^`]+)`", pl.col(r, "Keywords")) for r in comp_rows if pl.col(r, "Comp") != "T"},
        "concepts": {pl.col(r, "Comp"): pl.norm_text(pl.col(r, "Concepto")) for r in comp_rows},
        "question": pl.question(pl.find(secs, "Pregunta general")),
        "rqs": {pl.col(r, "Comp"): pl.norm_text(pl.col(r, "Pregunta")) for r in pl.table(pl.find(secs, "Preguntas por componente") or "")},
        "queries": {db: pl.code_block(pl.find(secs, f"Query {db}")) for db in DATABASES},
        "CI": _bullets(pl.find(crit, "Inclusión")),
        "CE": _bullets(pl.find(crit, "Exclusión")),
        "vocabs": pl.vocab_used(text),
    }


def tables(body: str) -> list[list[dict[str, str]]]:
    """Cada grupo de líneas | … | consecutivas, como filas dict."""
    out, cur = [], []
    for line in body.splitlines() + [""]:
        if line.strip().startswith("|"):
            cur.append(line)
        elif cur:
            out.append(pl.table("\n".join(cur)))
            cur = []
    return [t for t in out if t]


def split_terms(cell: str) -> list[str]:
    return [t.strip() for t in TERM_SPLIT.split(cell.strip()) if t.strip()]


def en_term(t: str) -> str:
    t = t.strip().strip("`").replace("\\*", "*")
    if len(t) > 2 and t.startswith("_") and t.endswith("_"):
        t = t[1:-1]
    return pl.norm_term(t)


def ws(s: str | None) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def _diff(want: list[str], got: list[str]) -> str:
    missing = [t for t in want if t not in got]
    extra = [t for t in got if t not in want]
    parts = [f"-{t}" for t in missing] + [f"+{t}" for t in extra]
    if not parts and want != got:
        parts.append("mismo conjunto, distinto orden")
    return " ".join(parts)


def check_keywords(body: str, m: dict) -> list[str]:
    issues = []
    table = next((t for t in tables(body) if any(k.casefold().startswith("keywords") or "(en)" in k.casefold() for k in t[0])), None)
    if table is None:
        return ["palabras-clave: falta la tabla Componente | Palabras clave (ES) | Keywords (EN)"]
    rows = {pl.col(r, "Comp"): r for r in table}
    if list(rows) != m["comps"]:
        issues.append(f"palabras-clave: filas {', '.join(rows) or '—'}; deben ser {', '.join(m['comps'])} en ese orden")
    for c in m["comps"]:
        r = rows.get(c)
        if r is None:
            continue
        en_cell = next((v for k, v in r.items() if k.casefold().startswith("keywords") or "(en)" in k.casefold()), "")
        es_cell = next((v for k, v in r.items() if k.casefold().startswith("palabras") or "(es)" in k.casefold()), "")
        en = split_terms(en_cell)
        if any(t.startswith("*") and t.endswith("*") and len(t) > 2 and not t.endswith("\\*") for t in en):
            issues.append(f"palabras-clave [{c}]: cursiva con *…*; usa _…_ (el * es comodín)")
        want = [pl.norm_term(t) for t in m["keywords"].get(c, [])]
        got = [en_term(t) for t in en]
        if want != got:
            issues.append(f"palabras-clave [{c}] Keywords (EN) ≠ bloque {c} de la query: {_diff(want, got)}")
        es = split_terms(es_cell)
        if len(es) != len(en):
            issues.append(f"palabras-clave [{c}]: {len(es)} términos en ES y {len(en)} en EN (una traducción por término)")
    note = "\n".join(NOTE_RE.findall(body))
    if not note:
        issues.append("palabras-clave: falta la nota bajo la tabla (_Nota._ …) que cita los vocabularios del picoc")
    else:
        for k in PAPER_VOCAB:
            name, cite = PAPER_VOCAB[k]
            has = bool(re.search(name, note) and re.search(cite, note))
            if k in m["vocabs"] and not has:
                issues.append(f"palabras-clave: la nota no cita {pl.VOCABS[k][2]}, que el picoc usa")
            elif k not in m["vocabs"] and re.search(name, note):
                issues.append(f"palabras-clave: la nota cita {pl.VOCABS[k][2]}, que el picoc no usa")
    return issues


def check_queries(body: str, m: dict) -> list[str]:
    issues, found = [], {}
    for b in re.findall(r"```[^\n]*\n(.*?)```", body, flags=re.S):
        db = "Scopus" if "TITLE-ABS-KEY" in b else "Web of Science" if re.search(r"\b(ALL|TS)\s*=", b) else None
        if db is None:
            issues.append("ecuacion-busqueda: bloque de código que no es Scopus ni Web of Science (solo esas dos bases van al paper)")
        elif db in found:
            issues.append(f"ecuacion-busqueda: {db} aparece dos veces")
        else:
            found[db] = b
    for db in DATABASES:
        want = m["queries"].get(db)
        if want is None:
            continue
        got = found.get(db)
        if got is None:
            issues.append(f"ecuacion-busqueda: falta el bloque de {db}")
            continue
        if ws(want) == ws(got):
            continue
        wb, gb = pl.query_blocks(want), pl.query_blocks(got)
        detail = [f"bloque {i + 1}: {_diff(w, g)}" for i, (w, g) in enumerate(zip(wb, gb)) if w != g]
        if len(wb) != len(gb):
            detail.append(f"{len(gb)} bloques y el picoc tiene {len(wb)}")
        issues.append(f"ecuacion-busqueda [{db}] ≠ query del picoc: " + ("; ".join(detail) or "cambian los filtros o la sintaxis"))
    return issues


def check_criteria(body: str, m: dict) -> list[str]:
    got = {"CI": [], "CE": []}
    for kind, txt in CRIT_RE.findall(body):
        got[kind].append(pl.norm_text(txt))
    issues = []
    for kind, name in (("CI", "inclusión"), ("CE", "exclusión")):
        want = m[kind]
        if want != got[kind]:
            missing = [t for t in want if t not in got[kind]]
            extra = [t for t in got[kind] if t not in want]
            what = [f"falta «{t}»" for t in missing] + [f"sobra «{t}»" for t in extra] or ["mismo texto, distinto orden"]
            issues.append(f"criterios-seleccion [{kind}] ≠ criterios de {name} del picoc: " + "; ".join(what))
    return issues


def check_marco(body: str, m: dict) -> list[str]:
    issues = []
    quote = "\n".join(re.findall(r"^>\s?(.*)$", body, flags=re.M))
    q = pl.question(quote) or pl.question(body)
    if m["question"] and q != m["question"]:
        issues.append("marco-pico: la pregunta general no es la del picoc (cópiala literal, como cita > ¿…?)")
    ts = tables(body)
    rq_t = next((t for t in ts if any(k.casefold().startswith("pregunta") for k in t[0])), None)
    if rq_t is None:
        issues.append("marco-pico: falta la tabla de preguntas por componente")
    else:
        got = {pl.col(r, "Comp"): pl.norm_text(pl.col(r, "Pregunta")) for r in rq_t}
        for c, want in m["rqs"].items():
            if got.get(c) != want:
                issues.append(f"marco-pico: la RQ de {c} no es la del picoc")
    comps = list(m["concepts"])
    fw_t = next((t for t in ts if set(comps) <= set(t[0])), None)
    if fw_t is None:
        issues.append(f"marco-pico: falta la tabla del marco (una columna por componente: {', '.join(comps)})")
    else:
        for c in comps:
            if pl.norm_text(fw_t[0].get(c, "")) != m["concepts"][c]:
                issues.append(f"marco-pico: el concepto de {c} en la tabla del marco no es el del picoc")
    return issues


CHECKS = {"marco-pico": check_marco, "palabras-clave": check_keywords, "ecuacion-busqueda": check_queries, "criterios-seleccion": check_criteria}


def check(sections: dict[str, str], picoc: Path) -> tuple[list[str], list[str]]:
    """(problemas, secciones revisadas) de las secciones espejo presentes."""
    m = mirror(picoc)
    present = [s for s in MIRRORED if s in sections]
    issues = [i for s in present for i in CHECKS[s](sections[s], m)]
    return issues, present


def prose_only(sid: str, content: str) -> str:
    """Texto de la sección sin sus bloques espejo (para el hash de frozen)."""
    if sid not in MIRRORED:
        return content
    text = FENCE_RE.sub("", content)
    keep = [l for l in text.splitlines()
            if not l.strip().startswith("|") and not l.lstrip().startswith(">") and not CRIT_RE.match(l) and not NOTE_RE.match(l)]
    return "\n".join(keep)
