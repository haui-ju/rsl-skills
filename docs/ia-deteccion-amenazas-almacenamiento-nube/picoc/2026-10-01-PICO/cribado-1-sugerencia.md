# Sugerencia de búsqueda — cribado 1

<!-- cribado:sugerencia picoc=2026-10-01-PICO -->

Basada en 292 registros únicos de Scopus y Web of Science (SI 222, NO 70). No reemplaza la búsqueda: la amplía.

**Efecto esperado:** 3 términos agregados en P, 0 quitados; los términos nuevos apuntan a vacíos que las palabras clave de los aceptados ya muestran (`digital storage`, `cloud computing`) sin eliminar bloques que aportan SI (`telemetry`, `machine learning`).

## Keywords

| Comp. | Término | Estado | Evidencia | Vocabulario | Decisión |
|---|---|---|---|---|---|
| P | `cloud storage` | vale | 16 reg., 16 SI | libre | mantener |
| P | `object storage` | vale | 1 reg., 1 SI | libre | mantener |
| P | `data storage` | vale | 39 reg., 33 SI | libre | mantener |
| P | `s3` / `Amazon S3` | vale | 13+1 SI | libre | mantener |
| P | `access log*` / `audit log` | vale | 5+1 SI | libre | mantener |
| P | `insider threat` | vale | 6 SI | libre | mantener |
| P | `telemetry` | vale | 133 reg., 85 SI (ruido en NO) | IEEE p.536 | mantener |
| P | `storage bucket` | agregar | 0 en query; alinea CI3 | libre | agregar |
| P | `digital storage` | agregar | 35 SI en keywords de aceptados | libre | agregar |
| P | `cloud computing` | agregar | 33 SI en keywords de aceptados | libre | agregar (acotar con bloques I–O) |
| I | `machine learning` / `deep learning` / `anomaly detection` | vale | núcleo de SI | IEEE | mantener |
| C | `intrusion detection` | revisar | muchos NO de red; sigue aportando SI | IEEE | mantener (cribado 2 filtra) |
| O | `precision` / `recall` / `latency` | vale | métricas frecuentes en SI | libre / IEEE | mantener |

## Query Scopus

```text
TITLE-ABS-KEY (
  ( "cloud storage" OR cloud storag* OR "object storage" OR "data storage" OR "digital storage" OR "cloud computing"
    OR S3 OR "Amazon S3" OR "blob storage" OR "data event*" OR "access log*" OR "audit log" OR "storage bucket"
    OR "cloud computing security" OR "insider threat" OR credential OR telemetry )
  AND
  ( "artificial intelligence" OR "machine learning" OR "machine-learning" OR "deep learning"
    OR "anomaly detection" OR "supervised learning" OR "unsupervised learning" OR "data mining" )
  AND
  ( "rule-based" OR signature OR threshold OR "static rule" OR "statistical method"
    OR "intrusion detection" OR "access control" )
  AND
  ( measurement OR metric OR metrics OR precision OR recall OR "classification accuracy"
    OR "false alarm" OR "detection rate" OR latency OR "detection time" )
)
AND PUBYEAR > 2020 AND PUBYEAR < 2027
AND (LIMIT-TO(DOCTYPE,"ar")) AND (LIMIT-TO(LANGUAGE,"English") OR LIMIT-TO(LANGUAGE,"Spanish"))
AND (LIMIT-TO(OA,"all"))
```

## Query Web of Science

```text
ALL=("cloud storage" OR cloud storag* OR "object storage" OR "data storage" OR "digital storage" OR "cloud computing"
  OR S3 OR "Amazon S3" OR "blob storage" OR "data event*" OR "access log*" OR "audit log" OR "storage bucket"
  OR "cloud computing security" OR "insider threat" OR credential OR telemetry)
AND ALL=("artificial intelligence" OR "machine learning" OR "machine-learning" OR "deep learning"
  OR "anomaly detection" OR "supervised learning" OR "unsupervised learning" OR "data mining")
AND ALL=("rule-based" OR signature OR threshold OR "static rule" OR "statistical method"
  OR "intrusion detection" OR "access control")
AND ALL=(measurement OR metric OR metrics OR precision OR recall OR "classification accuracy"
  OR "false alarm" OR "detection rate" OR latency OR "detection time")
AND PY=(2021-2026) AND DT=(Article) AND LA=(English OR Spanish)
```

## Debate

- **Defensor:** agregar `digital storage`, `cloud computing` y `storage bucket` en P porque aparecen en aceptados y CI3; no quitar `telemetry` ni `intrusion detection` (≥3 SI y aportan recall).
- **Crítico:** `cloud computing` ensancha mucho; aceptado si permanece en AND con I–O.
- **Acuerdo:** agregar los tres términos en P; no eliminar términos de la query actual.
