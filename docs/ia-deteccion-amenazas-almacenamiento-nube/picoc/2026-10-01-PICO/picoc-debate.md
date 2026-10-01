# Debate — marco PICO (2026-10-01)

**Base:** `picoc/2026-09-30-2-PICOCT/picoc.md` · **Motivo:** el usuario fijó `formato.marco: PICO` en `config.yml` (cuatro componentes P, I, C, O).

## Posiciones (síntesis)

**Crítico:** el bloque C en AND puede excluir primarios sin comparador en resumen; `bucket` suelto y O con seguridad genérica inflan ruido; las keywords del paper deben priorizar *Anomaly detection* frente a *Intrusion detection*.

**Defensor:** quitar Co y T como bloques AND mejora recall sin relajar CI; telemetría, credencial e *insider* pertenecen a P; ingeniería de software y despliegue quedan en RQ4/CI, no como quinto AND.

## Decisiones

| Tema | Decisión |
|------|----------|
| Marco | PICO con 4 RQ (P, I, C, O); ventana 2021–2026 solo en CI1 y filtros de índice |
| Co → P/O | `insider threat`, `credential`, `telemetry` en bloque P; despliegue/SOC en RQ4, no en query O |
| Query O | Solo términos métricos (sin `software engineering` ni seguridad genérica en AND) |
| Query P | `bucket` sustituido por `"storage bucket"` |
| Query I | Se retira `AI` suelto |
| Keywords paper | 6 términos: *object storage*, *Cloud computing security*, *Anomaly detection*, *Machine learning*, *Intrusion detection*, *Measurement* |
| CI3 | Aclaración sobre logs de buckets con títulos genéricos de cloud security |
| Bloque C | Se mantiene en la ecuación (problemática comparativa); cribado 1 no rechazará solo por ausencia de `rule-based` en resumen si hay IA + almacenamiento |

## Pendiente para el usuario

- Tras cribado 1, si el cruce Scopus es muy escaso, valorar relajar el bloque C en la ecuación (comparación solo en RQ3 a texto completo).
- `rsl-polish-report` / `informe.md` §2: enlazar `picoc/2026-10-01-PICO/picoc.md`.
- Paper: Metodología y `--picoc-sync` quedarán desfasados hasta `rsl-make-paper` o nueva versión polish.
