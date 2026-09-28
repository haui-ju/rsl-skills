---
name: rsl-polish-report
description: >-
  Polishes docs/[short-title]/informe.md with 4 agents and writes
  docs/[short-title]/informe-polish.md (same 7 UTP points). Refreshes the search
  framework through rsl-picoc only when needed. Use when the user says
  rsl-polish-report. Does not create the report from scratch.
---

# rsl-polish-report

Polish an existing `informe.md` into **`informe-polish.md`** (same folder, same UTP structure: 1.1–1.3 under point 1, points 2–7). Never overwrite `informe.md` unless asked.

Invoke: `Usa rsl-polish-report sobre docs/<slug>/informe.md` (or the folder). No path → ask.

The critic's job here: real contribution, no false claims, correct citations, coherence — not discarding the report.

## Procedure

1. Read `informe.md` (+ `topic.md` if present). Evidence via the theme graph (`graphify query "…" --graph docs/<slug>/graphify-out/graph.json`); no full PDFs, no Graphify refresh.
2. Parallel: `critico-rsl`, `defensor-rsl`, `impacto-social-rsl`, `viabilidad-negocio-rsl` (mode **informe**: local evidence first, web only to verify a claim or a missing review; at most 10 items each). Prompt = informe text + "Evalúa/mejora este INFORME. Responde en español con el formato de tu rol." The search framework is not debated here (that is `rsl-picoc`).
3. Brief synthesis in chat; write `informe-polish.md`. Section 2 = only the link to the latest `picoc/<carpeta>/picoc.md` (`pnpm -s picoc:latest docs/<slug>`), with this sentence: `Las palabras clave, el marco <MARCO> (<componentes en palabras>), las queries y los criterios de inclusión y exclusión se encuentran en [picoc/<carpeta>/picoc.md](picoc/<carpeta>/picoc.md).` This skill owns the link; `rsl-picoc` never edits the informe.
4. **Marco:** `pnpm -s picoc:latest docs/<slug>` and `pnpm -s picoc:lint docs/<slug>` (after writing `informe-polish.md`):
   - FALTA or DESFASADO → **`rsl-picoc`** full mode.
   - OK and the only lint FAIL is `PG` (the polished § 1.2 changed) → **`rsl-picoc`** light mode.
   - Any other lint FAIL → **`rsl-picoc`** full mode.
   - PASS → nothing.
5. Form and citations: `pnpm -s redaccion:lint docs/<slug>/informe-polish.md` and `pnpm -s paper:status docs/<slug> --cites docs/<slug>/informe-polish.md`. Give the lint output to **`redaccion-rsl`**; apply its fixes (form only) until 0 FAIL, every WARN fixed or justified, and `--cites` PASS.
6. Chat: main changes and missing PDFs under `RSL/PDF/`, then the Cierre line.

## Cierre

The last message of the skill is exactly one line:

- Stop at the first failure (any script returns `ERROR:`, `rsl-picoc` ends in ERROR, or `redaccion:lint` / `--cites` keep failing): `ERROR: <paso y script que falló, con su mensaje>. <cómo arreglarlo>`. Do not continue with later steps.
- Everything went well: `OK: informe pulido en docs/<slug>/informe-polish.md; marco <al día | regenerado en picoc/<carpeta>/>. Próximo paso: Usa rsl-make-paper sobre docs/<slug>/`.

## Forbidden

- Creating the informe from scratch (`rsl-make-report`) or running the topic panel.
- Changing the UTP structure; saving outside `docs/<slug>/`; moving PDFs.
- Tables or queries in section 2; editing `picoc/` by hand.
- Leaving work notes or internal traces (panel, `topic.md`, "Nota de artefacto", `[citar]`) or undefined acronyms.
- Ending with `redaccion:lint` FAIL, `--cites` FAIL or `picoc:latest` different from OK.
