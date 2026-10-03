---
name: rsl-cribado-2-polish
description: PRISMA screening 2 full-text evaluation. CI/CE from picoc.md, graph queries per record, decisions SI|PODRIA|NO then cribado2:cuota for min_rsl (RELLENO-LEVE/ALTO). Writes cribado-2-evaluacion.md and .cribado-2/decisiones.jsonl. Use after rsl-cribado-2-memoria when cribado2:status is OK.
---

# rsl-cribado-2-polish

Full-text screening against `CI*` / `CE*` in the linked `picoc.md`. **`config.yml` → `cribado_2.min_rsl`** (default 40) is the target count of **accepted** studies in the trace (SI + PODRIA + rellenos), not “40 pure SI”.

**Output:** `cribado-2-evaluacion.md` — `# | id | titulo | decision | motivo` (same order as `documentos.md`).

**Decisions (trace):**

| decision | Meaning |
|----------|---------|
| `SI` | Meets CI/CE; contributes to the RSL |
| `PODRIA` | Useful but weak on some criterion — explain in `motivo` |
| `RELLENO-LEVE` | Merit `NO`, promoted by `cuota` to reach `min_rsl` (mild fit) |
| `RELLENO-ALTO` | Merit `NO`, promoted after leve pool exhausted |
| `NO` | Does not serve |

CSV `¿Se acepta?` (in `rsl-cribado-2-aplicar`) = `SI` for SI, PODRIA, both rellenos; `NO` otherwise. Justificación = plain `motivo` only.

Invoke: `Usa rsl-cribado-2-polish sobre docs/<slug>/`.

## Procedure

1. `pnpm -s cribado2:status docs/<slug>` OK (incluye **integridad**). Si falla → `rsl-cribado-2-memoria`, no polish.
2. `pnpm -s cribado2:polish-prepare docs/<slug>` → `.cribado-2/criterios.md`, `registros.jsonl`.
3. Batches of **10** solo de registros con `evaluable: true` e `indexado: true` (no lotes para `descargado: no` / `sin_acceso`). Per batch:
   - **defensor-rsl** (modo **cribado-2**): `pnpm -s cribado2:query docs/<slug> "<Id> …"` per record; write table under `.cribado-2/propuestas/lote-NN.md` → `## Defensor`.
   - **critico-rsl** (modo **cribado-2**): same evidence; append `## Crítico` (disagreements only).
   - Resolve disagreements in `.cribado-2/resoluciones.md` if needed.
   - Append **merit** lines to `.cribado-2/evaluaciones/lote-NN.jsonl` (one JSON per id):

```json
{"orden":1,"id":"R001","decision":"SI","criterios":["CI3","CI4"],"motivo":"…","fuente":"grafo","relleno":{"elegible":false}}
```

For merit `NO` that could still help the project if quota needs filling: `"relleno":{"elegible":true,"nivel":"leve"|"alto","orden":1}` (lower `orden` = preferred).

4. `pnpm -s cribado2:polish-merge docs/<slug>` → `.cribado-2/decisiones.jsonl` (merit = SI|PODRIA|NO).
5. `pnpm -s cribado2:cuota docs/<slug>` — applies `min_rsl` on **indexed** PDFs only; promotes `NO` with `relleno.elegible`; **WARN** (not ERROR) if corpus cannot reach `min_rsl`.
6. `pnpm -s cribado2:polish-report docs/<slug>` → `cribado-2-evaluacion.md` + hash; en `picoc/<fecha>-<MARCO>/` escribe `cribado-2.shadow.jsonl` (una línea `_meta` + una por id del corpus: `id`, `decision`, `acepta`, `motivo`, `criterios`) para `cribado2:apply` sin parsear el MD.
7. Chat: counts by decision, cuota summary, path to evaluacion. Cierre.

## Cierre

- Failure: `ERROR: <qué falta>. <arreglo>`.
- Success: `OK: cribado-2-evaluacion.md con <n> registros (SI <a>, PODRIA <b>, relleno <c>, NO <d>). Próximo paso: Usa rsl-cribado-2-aplicar sobre docs/<slug>/ tras tu revisión.`

## Forbidden

- Reading whole PDFs when the cribado-2 graph covers the record.
- Decisions without CI/CE from picoc.
- Download, align, or editing `documentos.json` retrieval fields here.
