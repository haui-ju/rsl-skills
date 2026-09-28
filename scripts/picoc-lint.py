#!/usr/bin/env python3
"""Verifica un picoc.md / picoc-polish.md contra playbooks/vocabulario-controlado.md.

Reglas:
  R1  cada fila de búsqueda tiene `Origen en el tema`
  R2  términos de la tabla == términos de cada bloque en Scopus, Web of Science e IEEE Xplore; N correcto
  R3  exactamente 1 pregunta (¿…?) por componente del marco + pregunta general
  IEEE  cada descriptor declarado es término preferido en ieee-thesaurus.json y está en su bloque

Uso: python3 scripts/picoc-lint.py docs/<slug>/picoc.md
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THES_JSON = ROOT / "global" / "thesaurus" / "ieee-thesaurus.json"
DATABASES = ("Scopus", "Web of Science", "IEEE Xplore")
MARCOS = {
    "PICO": ["P", "I", "C", "O"],
    "PICOC": ["P", "I", "C", "O", "Co"],
    "PICOCT": ["P", "I", "C", "O", "Co", "T"],
}
FILTER_PREFIX = re.compile(r"(DT|PY|PUBYEAR|LIMIT-TO)\s*=?\s*$", re.I)


def sections(text: str) -> dict[str, str]:
    parts = re.split(r"^##\s+(.+)$", text, flags=re.M)
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


def code_block(body: str | None) -> str | None:
    if body is None:
        return None
    m = re.search(r"```[a-z]*\n(.*?)```", body, flags=re.S)
    return m.group(1) if m else None


def query_blocks(q: str) -> list[list[str]]:
    blocks = []
    for m in re.finditer(r"\(([^()]*)\)", q):
        if FILTER_PREFIX.search(q[: m.start()].rstrip()) or "DOCTYPE" in m.group(1):
            continue
        inner = re.sub(r"^\s*ALL\s*=\s*", "", m.group(1))
        blocks.append([norm_term(t) for t in re.split(r"\s+OR\s+", inner.strip()) if t.strip()])
    return blocks


def main(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    secs = sections(text)
    errs: list[str] = []

    m = re.search(r"\*\*Marco:\*\*\s*(PICOCT|PICOC|PICO)\b", text)
    if not m:
        print("FAIL: falta '**Marco:** PICO|PICOC|PICOCT'")
        return 1
    marco = m.group(1)
    comps = MARCOS[marco]

    general = find(secs, "Pregunta general")
    if not general or not re.search(r"¿[^?]+\?", general):
        errs.append("R3: falta la pregunta general (¿…?)")

    rq_rows = table(find(secs, "Preguntas por componente") or "")
    rq_by: dict[str, int] = {}
    for r in rq_rows:
        c = col(r, "Comp")
        rq_by[c] = rq_by.get(c, 0) + 1
        q = col(r, "Pregunta")
        if not (q.startswith("¿") and q.endswith("?")):
            errs.append(f"R3: la pregunta de {c} no es interrogativa (¿…?)")
        if not col(r, "Dato"):
            errs.append(f"R3: {c} sin 'Dato a extraer'")
    for c in comps:
        if rq_by.get(c, 0) != 1:
            errs.append(f"R3: {c} tiene {rq_by.get(c, 0)} preguntas (debe ser 1)")
    for c in rq_by:
        if c not in comps:
            errs.append(f"R3: componente '{c}' no pertenece a {marco}")

    search = table(find(secs, "Tabla de búsqueda") or "")
    if not search:
        errs.append("R2: falta la 'Tabla de búsqueda'")
    rows_terms: list[tuple[str, list[str]]] = []
    for r in search:
        c = col(r, "Comp")
        terms = [norm_term(t) for t in re.findall(r"`([^`]+)`", col(r, "Términos"))]
        rows_terms.append((c, terms))
        if not col(r, "Origen").strip("*_ —-"):
            errs.append(f"R1: {c} sin 'Origen en el tema'")
        n = col(r, "N")
        if not n.isdigit() or int(n) != len(terms):
            errs.append(f"R2: {c} N={n!r} pero hay {len(terms)} términos")
        if len(set(terms)) != len(terms):
            errs.append(f"R2: {c} tiene términos repetidos")

    for db in DATABASES:
        q = code_block(find(secs, f"Query {db}"))
        if q is None:
            errs.append(f"R2: falta 'Query {db}' con bloque de código")
            continue
        blocks = query_blocks(q)
        if len(blocks) != len(rows_terms):
            errs.append(f"R2 [{db}]: {len(blocks)} bloques en la query vs {len(rows_terms)} filas en la tabla")
        for (c, terms), blk in zip(rows_terms, blocks):
            extra, missing = sorted(set(blk) - set(terms)), sorted(set(terms) - set(blk))
            if extra or missing or len(blk) != len(terms):
                errs.append(
                    f"R2 [{db}] {c}: tabla {len(terms)} vs query {len(blk)}"
                    + (f" · solo en query: {extra}" if extra else "")
                    + (f" · solo en tabla: {missing}" if missing else "")
                )

    if THES_JSON.exists():
        thes = json.loads(THES_JSON.read_text(encoding="utf-8"))["terms"]
        for r, (c, terms) in zip(search, rows_terms):
            for d in re.findall(r"([^·(]+?)\s*\(p\.\s*\d+\)", col(r, "Descriptor")):
                name = d.strip()
                e = thes.get(re.sub(r"\s+", " ", name).casefold())
                if not e:
                    errs.append(f"IEEE: {c} '{name}' no existe en el IEEE Thesaurus")
                elif not e["preferred"]:
                    errs.append(f"IEEE: {c} '{name}' no es preferido (USE {e['USE']})")
                k = name.casefold()
                if not any(t == k or (t.endswith("*") and k.startswith(t[:-1])) for t in terms):
                    errs.append(f"IEEE: {c} descriptor '{name}' no aparece en su bloque de la query")
    else:
        errs.append("IEEE: falta global/thesaurus/ieee-thesaurus.json (pnpm run bootstrap)")

    if errs:
        print(f"FAIL {path} ({marco})")
        for e in errs:
            print(f"  - {e}")
        return 1
    total = sum(len(t) for _, t in rows_terms)
    print(f"PASS {path} ({marco}) · {len(rows_terms)} bloques · {total} términos · {len(rq_rows)} RQ · 3 bases")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(Path(sys.argv[1])))
