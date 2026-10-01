---
name: rsl-cribado-2-aplicar
description: After the user approves cribado-2-evaluacion.md, writes resultados-<MARCO>-cribado-2.csv from the cribado-1 applied CSV (same rows; last two columns become ¿Se acepta? and Justificación cribado 2). Updates prisma.json eligibility/included. Use when the user says rsl-cribado-2-aplicar.
---

# rsl-cribado-2-aplicar

Closes full-text screening. Only after the user has read `cribado-2-evaluacion.md` (post `cribado2:cuota`); merit changes belong to `rsl-cribado-2-polish`, not here.

```text
docs/[titulo-breve]/picoc/<fecha>-<MARCO>/
  resultados-<MARCO>-cribado-1.csv   (read)
  cribado-2.shadow.jsonl             (read; generado por polish-report)
  prisma.json                        (eligibility + included, updated)
docs/[titulo-breve]/RSL/picoc/<fecha>-cribado-2-<MARCO>/
  cribado-2-evaluacion.md            (hash must match decisiones)
  .cribado-2/decisiones.jsonl        (fallback si falta shadow)
  → picoc/resultados-<MARCO>-cribado-2.csv
```

Invoke: `Usa rsl-cribado-2-aplicar sobre docs/<slug>/`.

## CSV rules

- Same rows and base columns as `resultados-<MARCO>-cribado-1.csv`.
- Remove the last two columns of cribado 1 (`¿Se acepta?`, `Justificación cribado 1`).
- Append **`¿Se acepta?`** and **`Justificación cribado 2`**.
- `¿Se acepta?` = `SI` if final decision ∈ {SI, PODRIA, RELLENO-LEVE, RELLENO-ALTO}; else `NO`.
- Justificación = plain `motivo` from `cribado-2.shadow.jsonl` (o `decisiones.jsonl` si no hay shadow); sin etiquetas PODRIA/relleno.
- Filas **sin** decisión de texto completo (no están en el corpus cribado-2): `¿Se acepta?` = `NO` y **Justificación cribado 2** = la misma **Justificación cribado 1** del CSV de entrada (no usar mensaje genérico).

## Procedure

1. `pnpm -s cribado2:apply docs/<slug>`. ERROR if hash mismatch → `pnpm -s cribado2:polish-report docs/<slug>`.
2. Chat: SI/NO counts, path to `-cribado-2.csv`, PRISMA eligibility line, `min_rsl` / cuota warning if any. Cierre.

## Cierre

- Failure: `ERROR: <mensaje>. <arreglo>`.
- Success: `OK: picoc/<carpeta>/resultados-<MARCO>-cribado-2.csv con <n> registros (SI <a>, NO <b>). Próximo paso: síntesis / paper (sección resultados).`

## Forbidden

- Applying without user approval of the current evaluation report.
- Changing decisions by hand in the CSV (use polish + cuota + report).
