---
name: rsl-polish-report
description: >-
  Polishes docs/[short-title]/informe.md with 4 agents and writes
  docs/[short-title]/informe-polish.md. Use when the user says
  rsl-polish-report. Does not create the report from scratch.
---

# rsl-polish-report

## Goal

Polish an existing `informe.md` via a 4-agent debate and save the result as **`informe-polish.md`** in the same theme folder. Do not create the informe from scratch.

## Paths (required)

```text
docs/[titulo-breve]/
  topic.md              (optional, from rsl-topic-panel)
  informe.md            (input, from rsl-make-report)
  informe-polish.md     (output, this skill)
  RSL/
    PDF/                (SLR PDFs — do not move; read if useful)
```

Preserve the UTP **7-point** structure from `rsl-make-report` (1.1–1.3 under point 1; points 2–7). Do not flatten or renumber.

## Invoke

```text
Usa rsl-polish-report sobre docs/ia-pipelines-amenazas/informe.md
```

Or the folder `docs/ia-pipelines-amenazas/`. If omitted → ask for path under `docs/`.

## Critic role

Real contribution, no false claims, no nonsense, correct citations, coherence. Does **not** mean discard the report.

## Writing style (required)

Spanish académico-profesional with connectors; cohesive paragraphs.

## Procedure (required)

1. Read `informe.md` (+ `topic.md`). Prefer theme Graphify lookup if `graphify-out/graph.json` exists (`graphify query ... --graph docs/[tema]/graphify-out/graph.json`). Do **not** refresh Graphify here. Avoid loading full PDFs; they live under `RSL/PDF/`.
2. **Auditoría de vocabulario** (`playbooks/vocabulario-controlado.md`): extraer todos los términos EN de la sección 2 (PICOC, tabla y query) y correr **una** vez `pnpm -s thesaurus:check "…" "…"`. Si el informe no trae marco PICOC, construirlo en el polish.
3. Launch in parallel: `critico-rsl`, `defensor-rsl`, `impacto-social-rsl`, `viabilidad-negocio-rsl`.
   Shared prompt: informe package + tabla de `thesaurus:check` + “Evalúa/mejora este INFORME. Responde en español con el formato de tu rol.”
4. Brief debate synthesis in chat.
5. Write **`informe-polish.md`** (do not overwrite `informe.md` unless the user explicitly asks). Keep the same 7-point headings. Sección 2 con el formato de `rsl-make-report` (PICOC + tabla con `Tipo`/`Pág. IEEE` + query por bloques + libres justificados): no preferidos sustituidos por su USE, UF incorporados, ningún término nuevo sin pasar por `thesaurus:check`.
6. List main changes and still-missing PDFs under `RSL/PDF/`.
7. Chat — siguiente paso (no ejecutar aquí):

```text
Usa rsl-make-paper sobre docs/[titulo-breve]/
```

## Forbidden

- Creating informe from scratch (`rsl-make-report`).
- Topic-only panel without informe (`rsl-topic-panel`).
- Dropping UTP section structure (incl. 1.1 / 1.2 / 1.3).
- Moving or dumping PDFs into the theme root.
- Saving outside `docs/[titulo-breve]/`.
- Dejar en sección 2 descriptores inventados o no validados contra el thesaurus IEEE.
