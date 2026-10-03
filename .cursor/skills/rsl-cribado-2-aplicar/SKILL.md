---
name: rsl-cribado-2-aplicar
description: After the user approves cribado-2-evaluacion.md, writes resultados-<MARCO>-cribado-2.csv for the cribado-2 corpus only (documentos.json rows; e.g. 52 SI retrieval). Binary ¿Se acepta? + Justificación cribado 2. Updates prisma.json eligibility/included. Use when the user says rsl-cribado-2-aplicar.
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

- **Solo filas del corpus cribado-2** (`documentos.json`, mismo orden que `documentos.md`), no el CSV unificado completo de cribado 1.
- Columnas bibliográficas = fila del `resultados-<MARCO>-cribado-1.csv` con el mismo `id` (sin columnas de cribado 1 al final).
- Append **`¿Se acepta?`** y **`Justificación cribado 2`**.
- `¿Se acepta?` = **`SI`** o **`NO`** únicamente (`SI` si decisión ∈ {SI, PODRIA, RELLENO-LEVE, RELLENO-ALTO}).
- Justificación = **motivo completo** del shadow/decisiones (por qué SI o NO según CI/CE o retrieval); **sin** prefijos PODRIA/relleno ni recorte con «…»; breve pero con la razón decisiva explícita.
- No recuperado (`descargado≠si` / `sin_acceso`): **`NO`** y motivo breve en prosa académica (p. ej. acceso abierto declarado pero sin PDF disponible, o de pago / sin acceso). **Prohibido** HTTP, bots, scripts o «descarga automática» en CSV e informes.

## Procedure

1. `pnpm -s cribado2:apply docs/<slug>`. ERROR if hash mismatch → `pnpm -s cribado2:polish-report docs/<slug>`.
2. Chat: SI/NO counts, path to `-cribado-2.csv`, PRISMA eligibility line, `min_rsl` / cuota warning if any. Cierre.

## Cierre

- Failure: `ERROR: <mensaje>. <arreglo>`.
- Success: `OK: picoc/<carpeta>/resultados-<MARCO>-cribado-2.csv con <n> registros (SI <a>, NO <b>). Próximo paso: síntesis / paper (sección resultados).`

## Forbidden

- Applying without user approval of the current evaluation report.
- Changing decisions by hand in the CSV (use polish + cuota + report).
