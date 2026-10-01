---
name: rsl-cribado-2-polish
description: PRISMA screening 2 full-text evaluation. Reads CI/CE from picoc.md via documentos.json, queries only the cribado-2 Graphify graph in batches of 10 (defensor-rsl) plus critico-rsl per batch, writes cribado-2-evaluacion.md and .cribado-2/evaluaciones/lote-NN.jsonl. Decisions SI|NO|PODRIA. Use when the user says rsl-cribado-2-polish and memoria-traza shows indexed PDFs.
---

# rsl-cribado-2-polish

Full-text screening against the picoc inclusion/exclusion criteria (`CI*` / `CE*`). No new downloads or graph build.

**Input:** `picoc/<fecha-base>-cribado-2-<MARCO>/documentos.json` → `picoc` path → criteria (same rules as cribado 1: explicit CI/CE in picoc).

**Output:** `cribado-2-evaluacion.md` — columns `# | id | titulo | decision | motivo` in the same `#` order as `documentos.md`. `decision` ∈ `SI` | `NO` | `PODRIA`.

Invoke: `Usa rsl-cribado-2-polish sobre docs/<slug>/`.

## Procedure

1. Confirm `memoria-traza.json` and `graphify-out/graph.json` exist (`pnpm -s cribado2:status` OK). Only evaluate registros with PDF indexed (`graphify_indexed` or equivalent in traza).
2. Load criteria from the linked `picoc.md` (do not invent CE).
3. Split registros into batches of **10**. Per batch:
   - Subagent **defensor-rsl** (or dedicated cribado-2 prompt): for each id, `pnpm -s cribado2:query docs/<slug> "…"` scoped to that paper (title/id in the question).
   - Subagent **critico-rsl** reviews the batch with the same graph-only rule.
4. Append trace to `.cribado-2/evaluaciones/lote-NN.jsonl` (one JSON object per id: decision, criterios, motivo, fuente grafo).
5. Regenerate `cribado-2-evaluacion.md`. `NO` must cite at least one `CE` or unmet `CI`; `PODRIA` for relevant but uncertain full text.
6. Chat: counts SI/NO/PODRIA, path to evaluacion, open doubts. Then Cierre.

## Cierre

- Failure: `ERROR: <qué falta> (grafo, criterios, lote sin revisar). <arreglo>`.
- Success: `OK: cribado-2-evaluacion.md con <n> registros (SI <a>, NO <b>, PODRIA <c>). Próximo paso: revisión humana y, si aplica, aplicar decisiones finales al CSV en una skill futura.`

## Forbidden

- Reading whole PDFs when the cribado-2 graph already covers the record.
- Decisions without CI/CE from picoc.
- Editing `documentos.json` retrieval fields or re-running download inside this skill.
