---
name: rsl-cribado-2-alineamiento-pdfs
description: Moves user PDFs from docs/pdf-draft/ to docs/pdf/<Id>-<titulo-slug>.pdf by matching filename to pending registros in documentos.json; updates documentos.md and prisma retrieval. Idempotent after each batch of manual downloads. Use after dropping PDFs in pdf-draft or when the user says rsl-cribado-2-alineamiento-pdfs.
---

# rsl-cribado-2-alineamiento-pdfs

Aligns manual full texts with SI records from cribado 1. Does not download or build the graph.

Invoke: `Usa rsl-cribado-2-alineamiento-pdfs sobre docs/<slug>/`.

## Procedure

1. `pnpm -s cribado2:align docs/<slug>`. ERROR if `documentos.json` missing → run `rsl-cribado-2` first.
2. For each `docs/pdf-draft/*.pdf`: match a single pending row by **Id** (`R042.pdf` ↔ `R042`), normalized title (stem vs title slug), or DOI in the filename. On unique match, **move** to `docs/pdf/{Id}-{titulo-slug}.pdf`, set `descargado: si`, `fuente: alineamiento`. If the user declares no full-text access for a record, set `sin_acceso: true` and a short `porque` in `documentos.json` (leave `descargado: no`; still counts as not retrieved in PRISMA).
3. Chat: how many aligned, how many still without PDF, list WARN for ambiguous or unmatched drafts (user renames or fixes title). Then Cierre.

## Cierre

- Failure: `ERROR: <mensaje>. <arreglo>`.
- Success: `OK: <k> PDF alineados (<p> siguen sin PDF). Próximo paso: repite alineamiento si añadiste más borradores, o Usa rsl-cribado-2-memoria sobre docs/<slug>/`.

## Forbidden

- Copying instead of moving from `pdf-draft` (would leave duplicates).
- Guessing matches when two titles fit one file (leave WARN; user decides).
- Renaming by hand into `docs/pdf/` without updating the catalog (use `align`).
