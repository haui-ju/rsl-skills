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
  picoc.md              (input, from rsl-make-report)
  informe-polish.md     (output, this skill)
  picoc-polish.md       (output, this skill)
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

Spanish académico-profesional following `playbooks/redaccion-academica.md`: final text without work notes, acronyms defined on first use and dosified, one idea per sentence, no ×/+/-duro notation in prose, citations coherent with the section 3 table, short tentative title (section 7) that will anchor the paper title.

## Procedure (required)

1. Read `informe.md` (+ `topic.md`). Prefer theme Graphify lookup if `graphify-out/graph.json` exists (`graphify query ... --graph docs/[tema]/graphify-out/graph.json`). Do **not** refresh Graphify here. Avoid loading full PDFs; they live under `RSL/PDF/`.
2. **Auditoría del marco** (`playbooks/vocabulario-controlado.md`): leer `picoc.md` (si no existe, o si el informe aún trae tablas/queries en la sección 2, construirlo desde ahí). Correr `pnpm -s picoc:lint docs/[titulo-breve]/picoc.md` y **una** vez `pnpm -s thesaurus:check "…" "…"` con todos los términos EN de la tabla de búsqueda.
3. Launch in parallel: `critico-rsl`, `defensor-rsl`, `impacto-social-rsl`, `viabilidad-negocio-rsl`.
   Shared prompt: informe + `picoc.md` + salida del lint + tabla de `thesaurus:check` + “Evalúa/mejora este INFORME y su marco de búsqueda. Responde en español con el formato de tu rol.”
4. Brief debate synthesis in chat.
5. Write **`informe-polish.md`** (do not overwrite `informe.md` unless the user explicitly asks). Keep the same 7-point headings. Sección 2 = solo el enlace: `Las palabras clave, el marco PICOCT y las queries se encuentran en [picoc-polish.md](picoc-polish.md).` (ajustar el nombre del marco).
6. Write **`picoc-polish.md`** con la plantilla del playbook: reglas R1 (origen en el tema), R2 (tabla 1:1 con Scopus, Web of Science e IEEE Xplore) y R3 (1 RQ por componente); no preferidos sustituidos por su USE; ningún término nuevo sin `thesaurus:check`. `pnpm -s picoc:lint docs/[titulo-breve]/picoc-polish.md` → **PASS**.
7. **Forma y citas del informe:** `pnpm -s redaccion:lint docs/[titulo-breve]/informe-polish.md` + `pnpm -s paper:status docs/[titulo-breve] --cites docs/[titulo-breve]/informe-polish.md`. Launch **`redaccion-rsl`** with the lint output; apply its fixes (form only) until lint has 0 FAIL and every WARN is fixed or justified, and `--cites` is PASS.
8. List main changes (informe y marco) and still-missing PDFs under `RSL/PDF/`.
9. Chat — siguiente paso (no ejecutar aquí):

```text
Usa rsl-make-paper sobre docs/[titulo-breve]/
```

## Forbidden

- Creating informe from scratch (`rsl-make-report`).
- Topic-only panel without informe (`rsl-topic-panel`).
- Dropping UTP section structure (incl. 1.1 / 1.2 / 1.3).
- Moving or dumping PDFs into the theme root.
- Saving outside `docs/[titulo-breve]/`.
- Dejar descriptores inventados o no validados contra el thesaurus IEEE.
- Tablas o queries en la sección 2 del informe (solo el enlace a `picoc-polish.md`).
- Dejar en `informe-polish.md` notas de trabajo o trazabilidad interna ("Tema final consensuado en topic.md tras panel…", "Nota de artefacto", "exigidas por el panel", `[citar]`) o siglas sin definir.
- Entregar `picoc-polish.md` sin `picoc:lint` PASS (tabla ≠ query, términos sin origen en el tema, RQ faltantes).
