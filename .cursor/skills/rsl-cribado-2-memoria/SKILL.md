---
name: rsl-cribado-2-memoria
description: PRISMA screening 2 step 2 — index full texts. PDFs in RSL/picoc/<fecha>-cribado-2-<MARCO>/docs/pdf/ → docs/md/ with page locators, Graphify graph at graphify-out/graph.json, memoria-traza.json. Same prepare/stamp/build/verify as graphify-theme corpus mode. Use when the user says rsl-cribado-2-memoria or after PDFs are in docs/pdf/.
---

# rsl-cribado-2-memoria

Memory of screening-2 corpus so agents query papers without reopening PDFs. Separate graph from the theme; never touches `RSL/PDF/` or theme `graphify-out/`.

```text
docs/[titulo-breve]/RSL/picoc/<fecha-base>-cribado-2-<MARCO>/
  docs/pdf/<Id>-<titulo-slug>.pdf
  docs/md/<stem>.md
  docs/md/_raw/<stem>.txt
  index-manifest.json
  memoria-traza.json
  graphify-out/graph.json
```

Invoke: `Usa rsl-cribado-2-memoria sobre docs/<slug>/`.

## Procedure

1. `pnpm -s cribado2:prepare docs/<slug>`. ERROR «no tiene PDF» → run `rsl-cribado-2` and/or alineamiento first.
2. Exit 2 (`needs_agent`): read only that PDF; write `docs/md/<stem>.md` (≥ 8 headings, `[PDF p.N]`). Then `pnpm -s cribado2:stamp docs/<slug> <archivo.pdf>` and repeat prepare until OK.
3. `pnpm -s cribado2:build docs/<slug>` until OK (updates `memoria-traza.json`; falla si `integridad` PDF/MD ↔ `documentos.json` no pasa).
4. `pnpm -s cribado2:status docs/<slug>` debe dar **integridad OK** antes de `rsl-cribado-2-polish`. Diagnóstico: `pnpm -s cribado2:integrity docs/<slug>`.
5. Si integridad falla (PDF duplicado, DOI/título cruzados): sustituir el PDF correcto, borrar `docs/md/<stem>.md` y `_raw`, `prepare` → `build` de nuevo.
6. Chat: converted/skipped, agent MDs, nodes/edges, graph path, example `pnpm -s cribado2:query docs/<slug> "…"`. Then Cierre.

## Cierre

- Failure: `ERROR: <mensaje>. <arreglo>`.
- Success: `OK: memoria de <n> PDF en RSL/picoc/<carpeta-cribado-2>/graphify-out/graph.json (<nodos> nodos). Próximo paso: Usa rsl-cribado-2-polish sobre docs/<slug>/`.

## Forbidden

- Refreshing root/theme graph or writing theme `RSL/MD/`.
- Skipping verify or indexing with failed verify or failed integridad.
- Declarar memoria lista si el MD no corresponde al `id`/DOI de `documentos.json`.
- Downloading PDFs or full-text inclusion decisions (other skills).
