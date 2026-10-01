# Marco de búsqueda — IA y detección de amenazas en almacenamiento en la nube

**Marco:** PICO · **Vocabulario:** IEEE Thesaurus (IEEE, 2019) y términos libres · **Tema:** Inteligencia artificial para la detección de accesos anómalos y amenazas de seguridad en servicios de almacenamiento en la nube (*object storage*): revisión sistemática de técnicas, modelos y evidencia de evaluación

Protocolo: [`playbooks/vocabulario-controlado.md`](../../../../playbooks/vocabulario-controlado.md) · Debate: [picoc-debate.md](picoc-debate.md) · Verificación: `pnpm -s picoc:lint docs/ia-deteccion-amenazas-almacenamiento-nube`

## Pregunta general (problemática)

¿Qué técnicas y modelos de inteligencia artificial se han evaluado para detectar accesos anómalos y amenazas de seguridad en servicios de almacenamiento en la nube basados en *object storage*, en escenarios de alto volumen de telemetría del plano de datos, comportamiento legítimo variable y abuso con credenciales válidas, y qué evidencia existe sobre efectividad, precisión, recall, tasa de falsos positivos, latencia de detección y tiempo hasta detección en comparación con métodos convencionales (reglas, firmas, umbrales estáticos) en condiciones de evaluación comparables?

## Preguntas por componente

| RQ | Comp. | Pregunta (RQ) | Dato a extraer |
|----|-------|---------------|----------------|
| RQ1 | P | ¿Qué servicios o artefactos de almacenamiento en la nube (*object storage*, buckets, logs del plano de datos) y qué fuentes de telemetría (*data events*, *audit logs*) abordan los estudios, y si consideran abuso con credencial válida o amenaza interna? | Proveedor o API (S3, Blob, GCS, etc.) · tipo de log · escenario de credencial válida o *insider* (sí o no) |
| RQ2 | I | ¿Qué técnicas y modelos de inteligencia artificial se evalúan para detectar accesos anómalos o amenazas? | Familia (supervisado, no supervisado, aprendizaje profundo, grafos, secuencias) · herramienta o *framework* |
| RQ3 | C | ¿Con qué métodos convencionales se comparan o contrastan los enfoques de IA (reglas, firmas, umbrales estáticos, IDPS clásico)? | *Baseline* declarado · tipo de comparación (empírica o solo narrativa) |
| RQ4 | O | ¿Qué métricas de efectividad, precisión y detección oportuna se reportan y qué requisitos de despliegue desde ingeniería de software (artefacto, escala, integración con monitoreo o SOC/SIEM) se describen? | Precisión, recall, F1, AUC, falsos positivos, latencia, tiempo hasta detección · artefacto software · despliegue en tiempo real (sí o no) |

## Tabla de componentes (1:1 con las queries)

| Comp. | Concepto | RQ | Keywords | Descriptor IEEE (pág.) | Justificación |
|-------|----------|----|----------|------------------------|---------------|
| P | Servicios de almacenamiento en la nube, telemetría de acceso a objetos y escenarios con credencial válida | RQ1 | `"cloud storage"` · `cloud storag*` · `"object storage"` · `"data storage"` · `S3` · `"Amazon S3"` · `"blob storage"` · `"data event*"` · `"access log*"` · `"audit log"` · `"storage bucket"` · `"cloud computing security"` · `"insider threat"` · `credential` · `telemetry` | Cloud computing security (p.82) · Telemetry (p.536) | Nace de “servicios de almacenamiento en la nube basados en *object storage*”, “telemetría del plano de datos” y “abuso con credenciales válidas”; *insider threat* y *credential* son términos libres |
| I | Técnicas y modelos de IA para detección de anomalías y amenazas | RQ2 | `"artificial intelligence"` · `"machine learning"` · `"machine-learning"` · `"deep learning"` · `"anomaly detection"` · `"supervised learning"` · `"unsupervised learning"` · `"data mining"` | Artificial intelligence (p.30) · Machine learning (p.294) · Deep learning (p.126) · Anomaly detection (p.24) · Supervised learning (p.521) · Unsupervised learning (p.564) · Data mining (p.122) | Nace de “técnicas y modelos de inteligencia artificial” para detectar accesos anómalos y amenazas |
| C | Métodos convencionales frente a IA | RQ3 | `"rule-based"` · `signature` · `threshold` · `"static rule"` · `"statistical method"` · `"intrusion detection"` · `"access control"` | Intrusion detection (p.266) · Access control (p.6) | Nace de “métodos convencionales (reglas, firmas, umbrales estáticos)” en la problemática |
| O | Métricas de desempeño y detección oportuna | RQ4 | `measurement` · `metric` · `metrics` · `precision` · `recall` · `"classification accuracy"` · `"false alarm"` · `"detection rate"` · `latency` · `"detection time"` | Measurement (p.313) | Nace de “efectividad, precisión, recall, tasa de falsos positivos, latencia de detección y tiempo hasta detección”; el despliegue y la ingeniería de software se extraen en RQ4 sin filtrar la query |

## Palabras clave

| Español | Inglés | Comp. | Tipo | Pág. IEEE | Justificación |
|---------|--------|-------|------|-----------|---------------|
| seguridad en computación en la nube | Cloud computing security | P | IEEE | p.82 | — |
| telemetría | Telemetry | P | IEEE | p.536 | — |
| inteligencia artificial | Artificial intelligence | I | IEEE | p.30 | — |
| aprendizaje automático | Machine learning | I | IEEE | p.294 | — |
| aprendizaje profundo | Deep learning | I | IEEE | p.126 | — |
| detección de anomalías | Anomaly detection | I | IEEE | p.24 | — |
| aprendizaje supervisado | Supervised learning | I | IEEE | p.521 | — |
| aprendizaje no supervisado | Unsupervised learning | I | IEEE | p.564 | — |
| minería de datos | Data mining | I | IEEE | p.122 | — |
| detección de intrusiones | Intrusion detection | C | IEEE | p.266 | — |
| control de acceso | Access control | C | IEEE | p.6 | — |
| medición | Measurement | O | IEEE | p.313 | — |
| ingeniería de software | Software engineering | O | IEEE | p.497 | — |
| seguridad informática | Computer security | O | IEEE | p.100 | — |
| seguridad de la información | Information security | O | IEEE | p.254 | — |
| almacenamiento en la nube | cloud storage | P | Libre | — | Sin descriptor IEEE 2019 |
| almacenamiento de objetos | object storage | P | Libre | — | Sin descriptor IEEE 2019 |
| almacenamiento de datos | data storage | P | Libre | — | Sin descriptor IEEE 2019 |
| Amazon S3 | Amazon S3 / S3 | P | Libre | — | Servicio de referencia en telemetría de objetos |
| almacenamiento blob | blob storage | P | Libre | — | Equivalente Azure/GCP |
| eventos del plano de datos | data events | P | Libre | — | Telemetría de acceso a objetos |
| registros de acceso | access logs | P | Libre | — | Fuente habitual de evaluación |
| registro de auditoría | audit log | P | Libre | — | Sin descriptor IEEE |
| amenaza interna | insider threat | P | Libre | — | Relacionado con credenciales válidas |
| credencial | credential | P | Libre | — | Abuso con identidad auténtica |
| reglas basadas en firmas | rule-based / signature | C | Libre | — | Métodos convencionales del tema |
| umbral estático | threshold / static rule | C | Libre | — | *Baseline* no basado en aprendizaje |
| método estadístico | statistical method | C | Libre | — | Comparador frecuente en la literatura |
| precisión y exhaustividad | precision / recall | O | Libre | — | Métricas centrales del objeto de estudio |
| exactitud de clasificación | classification accuracy | O | Libre | — | Métrica reportada en primarios |
| falsas alarmas | false alarm | O | Libre | — | Operacional en SOC |
| tasa de detección | detection rate | O | Libre | — | Capacidad de detección |

## Keywords

| Keyword (EN) | Palabra clave (ES) | Comp. |
|--------------|--------------------|-------|
| object storage | almacenamiento de objetos | P |
| Cloud computing security | seguridad en computación en la nube | P |
| Anomaly detection | detección de anomalías | I |
| Machine learning | aprendizaje automático | I |
| Intrusion detection | detección de intrusiones | C |
| Measurement | medición | O |

## Query Scopus

```text
TITLE-ABS-KEY (
  ( "cloud storage" OR cloud storag* OR "object storage" OR "data storage" OR S3 OR "Amazon S3"
    OR "blob storage" OR "data event*" OR "access log*" OR "audit log" OR "storage bucket" OR "cloud computing security"
    OR "insider threat" OR credential OR telemetry )
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
ALL=("cloud storage" OR cloud storag* OR "object storage" OR "data storage" OR S3 OR "Amazon S3"
  OR "blob storage" OR "data event*" OR "access log*" OR "audit log" OR "storage bucket" OR "cloud computing security"
  OR "insider threat" OR credential OR telemetry)
AND ALL=("artificial intelligence" OR "machine learning" OR "machine-learning" OR "deep learning"
  OR "anomaly detection" OR "supervised learning" OR "unsupervised learning" OR "data mining")
AND ALL=("rule-based" OR signature OR threshold OR "static rule" OR "statistical method"
  OR "intrusion detection" OR "access control")
AND ALL=(measurement OR metric OR metrics OR precision OR recall OR "classification accuracy"
  OR "false alarm" OR "detection rate" OR latency OR "detection time")
AND PY=(2021-2026) AND DT=(Article) AND LA=(English OR Spanish)
```

Filtro de interfaz: acceso abierto (Open Access).

## Query IEEE Xplore

```text
( "cloud storage" OR cloud storag* OR "object storage" OR "data storage" OR S3 OR "Amazon S3"
  OR "blob storage" OR "data event*" OR "access log*" OR "audit log" OR "storage bucket"
  OR "IEEE Terms":"Cloud computing security" OR "insider threat" OR credential
  OR "IEEE Terms":"Telemetry" )
AND
( "IEEE Terms":"Artificial intelligence" OR "IEEE Terms":"Machine learning" OR "machine-learning"
  OR "IEEE Terms":"Deep learning" OR "IEEE Terms":"Anomaly detection" OR "IEEE Terms":"Supervised learning"
  OR "IEEE Terms":"Unsupervised learning" OR "IEEE Terms":"Data mining" )
AND
( "rule-based" OR signature OR threshold OR "static rule" OR "statistical method"
  OR "IEEE Terms":"Intrusion detection" OR "IEEE Terms":"Access control" )
AND
( "IEEE Terms":"Measurement" OR metric OR metrics OR precision OR recall OR "classification accuracy"
  OR "false alarm" OR "detection rate" OR latency OR "detection time" )
```

Filtros de interfaz: año 2021–2026; artículos de revista; inglés o español; acceso abierto cuando esté disponible.

*Nota:* la query IEEE Xplore usa 6 comodines (`storag*`, `event*`, `log*`, `metric*`, etc.), por debajo del límite de 10.

## Validación de la búsqueda

| Estudio | DOI | ¿Debería recuperar Scopus? |
|---------|-----|----------------------------|
| Hagemann & Katsarou (2020), anomalías en nube | 10.1145/3442536.3442550 | Parcial: cubre `anomaly detection` y nube, pero es acta de congreso y anterior a 2021; calibra recall del bloque I |
| Omogbehin et al. (2026), ML y seguridad de datos en nube | 10.11591/ijai.v15.i1.pp44-55 | Sí: `machine learning`, seguridad de datos en nube, `anomaly detection` |
| Nasim et al. (2025), IDPS en nube | 10.1007/s10791-025-09641-y | Sí: `intrusion detection`, computación en nube, técnicas de ML |
| Alzoubi et al. (2020), ML en seguridad cloud | 10.3390/electronics9091379 | Parcial: `machine learning` y `cloud computing security`; población más amplia que *storage* |
| El Moudni & Ziyati (2025), almacenamiento en nube | 10.18280/ijsse.150403 | Parcial: `cloud storage` y ML entre otras técnicas; delimita vacío |

## Descriptores revisados y excluidos

- *Cloud computing* (p.82) aislado: demasiado amplio; el tema acota con almacenamiento y *Cloud computing security*.
- *Cryptography* (NT de *Data security*): el alcance excluye estudios centrados solo en cifrado en reposo sin detección conductual.
- *Phishing* y *Social engineering*: fuera del foco en telemetría de *object storage* salvo evaluación sobre logs de buckets.

## Criterios de inclusión y exclusión

### Inclusión

- CI1. Estudios publicados entre 2021 y 2026.
- CI2. Artículos de revista revisados por pares en inglés o español, con acceso abierto al texto completo.
- CI3. Estudios que evalúen detección de accesos anómalos o amenazas en *object storage* (incluidos logs de buckets).
- CI4. Estudios que empleen técnicas de inteligencia artificial (aprendizaje automático, aprendizaje profundo, detección de anomalías o analítica conductual sobre logs de acceso).
- CI5. Estudios que reporten al menos una métrica de desempeño o detección (precisión, recall, F1, AUC, falsos positivos, latencia o tiempo hasta detección).

### Exclusión

- CE1. Estudios cuyo único foco sea detección en red o *endpoint* sin capa de almacenamiento identificable.
- CE2. Trabajos centrados solo en cifrado en reposo o prevención de pérdida de datos sin detección basada en IA.
- CE3. Literatura gris, documentación comercial de proveedores cloud o blogs como evidencia primaria.
- CE4. Evaluaciones limitadas a benchmarks de tráfico de red (p. ej. KDD, CICIDS) sin relación con almacenamiento en nube.
