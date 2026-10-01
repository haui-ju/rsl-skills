<!-- paper:section id=encabezado -->
# Inteligencia artificial para la detección de accesos anómalos y amenazas en servicios de almacenamiento en la nube

**Tema.** Revisión sistemática de estudios primarios que evalúan técnicas y modelos de inteligencia artificial para detectar accesos anómalos y amenazas en servicios de almacenamiento basados en *object storage*, con énfasis en telemetría del plano de datos, comparación frente a métodos convencionales y métricas de despliegue. · **Problemática.** ¿Qué técnicas y modelos de inteligencia artificial se han evaluado para detectar accesos anómalos y amenazas de seguridad en servicios de almacenamiento en la nube basados en *object storage*, en escenarios de alto volumen de telemetría del plano de datos, comportamiento legítimo variable y abuso con credenciales válidas, y qué evidencia existe sobre efectividad, precisión, recall, tasa de falsos positivos, latencia de detección y tiempo hasta detección en comparación con métodos convencionales (reglas, firmas, umbrales estáticos) en condiciones de evaluación comparables? · **Objetivo.** Sintetizar esa evidencia primaria, clasificar técnicas y modelos, registrar baselines y métricas reportadas, y describir el contexto de ingeniería de software de las evaluaciones, de forma repetible y alineada con un protocolo de población, intervención, comparación y resultado (PICO).
<!-- /paper:section -->

## I. Introducción

<!-- paper:section id=contexto -->
### Contexto

Los marcos europeos de ciberseguridad exigen monitorización y registro sobre sistemas que procesan y almacenan datos. El Reglamento de aplicación (UE) 2024/2690 (European Union, 2024), en el marco de la directiva NIS2 (*Network and Information Security Directive 2*), refuerza esa exigencia. No sustituye, sin embargo, la necesidad de evidencia sobre qué controles detectan a tiempo abusos con credenciales legítimas en almacenamiento externalizado.

Sobre ese almacenamiento externalizado operan con frecuencia servicios de *object storage*, que exponen objetos mediante interfaces de programación de aplicaciones, con telemetría del plano de datos —*data events* y registros de auditoría de buckets— que supera con frecuencia el análisis manual. Aquí la inteligencia artificial (IA) designa aprendizaje automático, aprendizaje profundo y detección de anomalías frente a reglas, firmas y sistemas de detección de intrusiones orientados a red o hosts. Desde ingeniería de software interesa el artefacto evaluado: pipeline de ingestión, integración con monitoreo y requisitos no funcionales como latencia y tasa de falsos positivos.

Las revisiones recientes se acercan al objeto sin cerrar el mapa pedido. Hagemann y Katsarou (2020) sintetizan detección de anomalías en computación en la nube con aprendizaje automático y métodos estadísticos, pero sin acotar la población a *object storage* ni comparaciones homogéneas sobre la misma telemetría de objetos. Nasim et al. (2025) abarcan 115 estudios (2017–2024) sobre intrusiones en la nube, con red y almacenamiento mezclados y apoyo frecuente en benchmarks de tráfico; Omogbehin et al. (2026) se centran en datos y control de acceso con aprendizaje automático y advierten vacíos en diversidad de datos y ataques adversariales, aunque no restringen primarios a registros de acceso vía interfaces de programación de aplicaciones ni contrastan de forma sistemática IA y reglas en un mismo escenario. Alzoubi y Aljaafreh (2020) y Moudni y Ziyati (2025) revisan algoritmos o controles en almacenamiento en la nube sin sintetizar evaluaciones conductuales con IA sobre esos registros ni métricas operativas comparables frente a baselines convencionales.

Entre esas fronteras persisten tensiones operativas. Compiten la evidencia de nube genérica y la telemetría de buckets; los estudios de control de acceso con aprendizaje automático y lo que un centro de operaciones de seguridad necesita sobre almacenamiento gestionado; y las métricas de laboratorio frente a falsos positivos, latencia y tiempo hasta detección cuando el atacante usa credenciales válidas. Esas tensiones motivan el problema y la pregunta de investigación que orienta esta revisión sistemática de la literatura (RSL).
<!-- /paper:section -->

<!-- paper:section id=problema -->
### El problema

Los proveedores incorporan analítica sobre telemetría de almacenamiento y el volumen de registros del plano de datos supera el mantenimiento manual de reglas estáticas. De ahí que la pregunta deje de ser si existe IA en seguridad cloud y pase a ser qué técnicas se evaluaron en *object storage*, con qué métricas y frente a qué baselines en condiciones declaradas por los autores.

Las síntesis existentes cartografían anomalías o intrusiones en toda la nube o la seguridad de datos con aprendizaje automático, pero rara vez cruzan telemetría de objetos, modelos de IA, comparación con métodos convencionales y métricas operativas en un solo mapa reproducible. Cuando los primarios no reportan baseline comparable, la revisión documentará esa ausencia como hallazgo y no como fallo del cribado.

Si el conjunto incluido resulta escaso, el informe explicitará el vacío en lugar de forzar un metaanálisis cuantitativo.

> ¿Qué técnicas y modelos de inteligencia artificial se han evaluado para detectar accesos anómalos y amenazas de seguridad en servicios de almacenamiento en la nube basados en *object storage*, en escenarios de alto volumen de telemetría del plano de datos, comportamiento legítimo variable y abuso con credenciales válidas, y qué evidencia existe sobre efectividad, precisión, recall, tasa de falsos positivos, latencia de detección y tiempo hasta detección en comparación con métodos convencionales (reglas, firmas, umbrales estáticos) en condiciones de evaluación comparables?
<!-- /paper:section -->

<!-- paper:section id=justificacion -->
### Justificación

El tema articula seguridad en la nube, detección de anomalías con IA y artefactos evaluables de ingeniería de software. Se descartó un planteamiento genérico de «inteligencia artificial y ciberseguridad en la nube» que duplicaría mapas ya publicados (Nasim et al., 2025; Hagemann & Katsarou, 2020). El recorte a *object storage* y credenciales válidas responde a un problema operativo documentado en la literatura secundaria y a marcos que exigen monitorización sobre datos almacenados (European Union, 2024). Las obras citadas en el contexto orientan la delimitación; no forman por sí solas la población incluida según los criterios de inclusión del protocolo (2021–2026).

La síntesis interesa a responsables de arquitectura y cumplimiento —incluidas micro y pequeñas empresas sin un centro de operaciones de seguridad pleno— que deben elegir telemetría, familia de modelos y umbrales antes de desplegar un pipeline. En el Perú, quien define finalidades sigue siendo responsable del tratamiento aunque el almacenamiento sea del proveedor; la revisión de alertas sobre metadatos de acceso debe ser proporcionada (Ley N° 29733; Congreso de la República del Perú, 2011). Los resultados no sustituyen identidad y acceso ni controles nativos; ofrecen un mapa de evidencia para decisiones de ingeniería y para exigir, cuando proceda, tasas de falsos positivos acordes a equipos reducidos.

Una RSL es necesaria porque el campo cuenta con revisiones parciales y el riesgo de repetir cartografías genéricas es alto. Kitchenham y Charters (2007) recomiendan protocolo predefinido para reducir sesgo y documentar búsqueda y selección; el reporte sigue las directrices *Preferred Reporting Items for Systematic Reviews and Meta-Analyses* (PRISMA) 2020 (Page et al., 2021) en la selección y su diagrama de flujo.
<!-- /paper:section -->

<!-- paper:section id=objetivo-rsl -->
### Objetivo de la RSL

El objetivo general es sintetizar estudios primarios que evalúen técnicas y modelos de inteligencia artificial para detectar accesos anómalos y amenazas en servicios de almacenamiento en la nube basados en *object storage*. El análisis abarcará métricas de desempeño, validez de los escenarios de evaluación y requisitos de despliegue desde la ingeniería de software.

Objetivos específicos, alineados con el protocolo de población, intervención, comparación y resultado (PICO):

1. **RQ1 (P):** Identificar qué servicios o artefactos de almacenamiento y qué fuentes de telemetría abordan los estudios, y si consideran escenarios con credencial válida o amenaza interna.
2. **RQ2 (I):** Catalogar técnicas y modelos de IA evaluados (familia, herramienta o framework).
3. **RQ3 (C):** Registrar con qué métodos convencionales se comparan o contrastan los enfoques de IA y el tipo de comparación.
4. **RQ4 (O):** Extraer métricas reportadas y requisitos de despliegue desde ingeniería de software (precisión, recall, F1, área bajo la curva [AUC], falsos positivos, latencia, tiempo hasta detección, artefacto, escala, integración con monitoreo o gestión de información y eventos de seguridad [SIEM]).

La contribución prevista es un mapa reproducible de técnicas y modelos evaluados sobre telemetría de *object storage*, con síntesis de validez externa frente a baselines convencionales cuando la evidencia lo permita.
<!-- /paper:section -->

<!-- paper:section id=organizacion -->
### Organización del contenido de la revisión

Este manuscrito desarrolla la Introducción y la Metodología hasta el cribado de título y resumen (marco PICO, palabras clave, ecuación de búsqueda, criterios y proceso PRISMA). Resultados, Discusión, Conclusión y Declaraciones se incorporarán tras la extracción y síntesis de los estudios que pasen el cribado a texto completo. El protocolo PICO del tema, registrado el 1 de octubre de 2026, fija la pregunta general, las preguntas por componente y los criterios aplicados.
<!-- /paper:section -->

## II. Metodología

La revisión sigue el protocolo de revisiones sistemáticas en ingeniería de software de Kitchenham y Charters (2007), fijado antes de la búsqueda para reducir sesgo y hacer repetible la trazabilidad entre pregunta, ecuación y criterios. A continuación se presentan el marco PICO, las palabras clave, las ecuaciones en Scopus y Web of Science, los criterios de inclusión y exclusión y el proceso de selección según PRISMA 2020.

<!-- paper:section id=marco-pico -->
### A. Pregunta PICO y sus componentes

Se adoptó el marco PICO (población, intervención, comparación y resultado) para acotar la población a servicios de almacenamiento en la nube y su telemetría, la intervención a técnicas de inteligencia artificial, la comparación a métodos convencionales y el resultado a métricas de detección y despliegue. Kitchenham y Charters (2007, p. 11) recomiendan el marco PICOC (población, intervención, comparación, resultado y contexto) en ingeniería de software.
Aquí se adopta PICO: el despliegue se extrae en RQ4 junto con las métricas y el periodo 2021–2026 queda en el criterio de inclusión CI1.

**Tabla 1 — Marco PICO**

| P | I | C | O |
|---|---|---|---|
| Servicios de almacenamiento en la nube, telemetría de acceso a objetos y escenarios con credencial válida | Técnicas y modelos de IA para detección de anomalías y amenazas | Métodos convencionales frente a IA | Métricas de desempeño y detección oportuna |

> ¿Qué técnicas y modelos de inteligencia artificial se han evaluado para detectar accesos anómalos y amenazas de seguridad en servicios de almacenamiento en la nube basados en *object storage*, en escenarios de alto volumen de telemetría del plano de datos, comportamiento legítimo variable y abuso con credenciales válidas, y qué evidencia existe sobre efectividad, precisión, recall, tasa de falsos positivos, latencia de detección y tiempo hasta detección en comparación con métodos convencionales (reglas, firmas, umbrales estáticos) en condiciones de evaluación comparables?

**Tabla 2 — Preguntas por componente**

| Componente | Código | Pregunta |
|---|---|---|
| P | RQ1 | ¿Qué servicios o artefactos de almacenamiento en la nube (*object storage*, buckets, logs del plano de datos) y qué fuentes de telemetría (*data events*, *audit logs*) abordan los estudios, y si consideran abuso con credencial válida o amenaza interna? |
| I | RQ2 | ¿Qué técnicas y modelos de inteligencia artificial se evalúan para detectar accesos anómalos o amenazas? |
| C | RQ3 | ¿Con qué métodos convencionales se comparan o contrastan los enfoques de IA (reglas, firmas, umbrales estáticos, IDPS clásico)? |
| O | RQ4 | ¿Qué métricas de efectividad, precisión y detección oportuna se reportan y qué requisitos de despliegue desde ingeniería de software (artefacto, escala, integración con monitoreo o SOC/SIEM) se describen? |
<!-- /paper:section -->

<!-- paper:section id=palabras-clave -->
### B. Palabras clave pertinentes

Los términos combinan descriptores del IEEE Thesaurus (Institute of Electrical and Electronics Engineers [IEEE], 2019) y términos libres, siguiendo la recomendación de usar palabras clave de las bases indexadas (Kitchenham y Charters, 2007, p. 14).

**Tabla 3 — Palabras clave por componente**

| Componente | Palabras clave (ES) | Keywords (EN) |
|---|---|---|
| P | almacenamiento en la nube, almacenamiento en la nube, almacenamiento de objetos, almacenamiento de datos, Amazon S3, Amazon S3, almacenamiento blob, eventos del plano de datos, registros de acceso, registro de auditoría, bucket de almacenamiento, seguridad en computación en la nube, amenaza interna, credencial, telemetría | "cloud storage", cloud storag\*, "object storage", "data storage", S3, "Amazon S3", "blob storage", "data event\*", "access log\*", "audit log", "storage bucket", _Cloud computing security_, "insider threat", credential, _Telemetry_ |
| I | inteligencia artificial, aprendizaje automático, aprendizaje automático, aprendizaje profundo, detección de anomalías, aprendizaje supervisado, aprendizaje no supervisado, minería de datos | _"Artificial intelligence"_, _"Machine learning"_, "machine-learning", _"Deep learning"_, _"Anomaly detection"_, _"Supervised learning"_, _"Unsupervised learning"_, _"Data mining"_ |
| C | reglas basadas en firmas, firma, umbral estático, regla estática, método estadístico, detección de intrusiones, control de acceso | "rule-based", signature, threshold, "static rule", "statistical method", _"Intrusion detection"_, _"Access control"_ |
| O | medición, métrica, métricas, precisión, exhaustividad, exactitud de clasificación, falsas alarmas, tasa de detección, latencia, tiempo de detección | _measurement_, metric, metrics, precision, recall, "classification accuracy", "false alarm", "detection rate", latency, "detection time" |

_Nota._ En cursiva, descriptores del IEEE Thesaurus (IEEE, 2019); el resto son términos libres.
<!-- /paper:section -->

<!-- paper:section id=ecuacion-busqueda -->
### C. Ecuación de búsqueda

Cada bloque del marco se traduce en un conjunto de términos unidos por OR; los bloques se combinan con AND. Scopus busca en título, resumen y palabras clave; Web of Science en todos los campos indexados, coherente con las exportaciones del cribado. Las ecuaciones incorporan periodo, tipo de documento, idioma y acceso abierto para documentar la búsqueda (Kitchenham y Charters, 2007, p. 16); en Web of Science el filtro de acceso abierto se aplicó en la interfaz de la base.

**Scopus**

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

**Web of Science**

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

**Tabla 4 — Búsqueda por base de datos**

| Base | Fecha de búsqueda | Años | Campos | Filtros | Registros |
|---|---|---|---|---|---|
| Scopus | [[ fecha de búsqueda ]] | 2021–2026 | TITLE-ABS-KEY | artículo; inglés o español; acceso abierto | n = 111 |
| Web of Science | [[ fecha de búsqueda ]] | 2021–2026 | ALL= | artículo; inglés o español; acceso abierto (interfaz) | n = 250 |
<!-- /paper:section -->

<!-- paper:section id=criterios-seleccion -->
### D. Criterios de inclusión y exclusión

Los criterios reproducen el protocolo. En CE4, KDD (Knowledge Discovery and Data Cup) y CICIDS (Canadian Institute for Cybersecurity Intrusion Detection System) aluden a suites de benchmarks de tráfico de red.

**Criterios de inclusión**

- **CI1:** CI1. Estudios publicados entre 2021 y 2026.
- **CI2:** CI2. Artículos de revista revisados por pares en inglés o español, con acceso abierto al texto completo.
- **CI3:** CI3. Estudios que evalúen detección de accesos anómalos o amenazas en *object storage* (incluidos logs de buckets).
- **CI4:** CI4. Estudios que empleen técnicas de inteligencia artificial (aprendizaje automático, aprendizaje profundo, detección de anomalías o analítica conductual sobre logs de acceso).
- **CI5:** CI5. Estudios que reporten al menos una métrica de desempeño o detección (precisión, recall, F1, AUC, falsos positivos, latencia o tiempo hasta detección).

**Criterios de exclusión**

- **CE1:** CE1. Estudios cuyo único foco sea detección en red o *endpoint* sin capa de almacenamiento identificable.
- **CE2:** CE2. Trabajos centrados solo en cifrado en reposo o prevención de pérdida de datos sin detección basada en IA.
- **CE3:** CE3. Literatura gris, documentación comercial de proveedores cloud o blogs como evidencia primaria.
- **CE4:** CE4. Evaluaciones limitadas a benchmarks de tráfico de red (p. ej. KDD, CICIDS) sin relación con almacenamiento en nube.
<!-- /paper:section -->

<!-- paper:section id=seleccion-prisma -->
### E. Proceso de selección — Diagrama PRISMA

La selección se reporta según PRISMA 2020 (Page et al., 2021, p. 1), guía de presentación con lista de verificación de 27 ítems y diagrama de flujo; la ejecución del cribado sigue las etapas de Kitchenham y Charters (2007, pp. 19–20). El objetivo es hacer auditable el corpus buscado y las exclusiones por criterio, no demostrar por sí solo vacíos de literatura.

El cribado fue en dos etapas: título, resumen y palabras clave; a continuación recuperación y evaluación a texto completo de los registros aceptados en la primera etapa. [[ número de revisores y si trabajaron de forma independiente ]] [[ cómo se resolvieron los desacuerdos ]] [[ herramienta usada, p. ej. Rayyan o una hoja de cálculo ]]. Cada exclusión quedó asociada a un criterio de inclusión no cumplido o de exclusión aplicado.

1. Registros identificados en Scopus (n = 111) y en Web of Science (n = 250) con la ecuación (filtros de periodo, tipo, idioma y acceso abierto incluidos en la ecuación o en la interfaz).
2. Registros excluidos por filtros adicionales de la base de datos no contemplados en la ecuación (n = X).
3. Duplicados eliminados (n = 69).
4. Registros cribados por título y resumen (n = 292); excluidos (n = 70).
5. Informes buscados para recuperación (n = 222); no recuperados (n = X).
6. Informes evaluados a texto completo (n = X); excluidos por criterios (n = X).
7. Estudios incluidos en la revisión (n = X).

[[ AGREGAR DIAGRAMA ]]

*Fig. 1. Diagrama de flujo PRISMA 2020 del proceso de selección.*
<!-- /paper:section -->

<!-- paper:section id=referencias -->
## Referencias

Alzoubi, H. B., & Aljaafreh, A. (2020). A review of machine learning algorithms for cloud computing security. *Electronics, 9*(9), Article 1379. https://doi.org/10.3390/electronics9091379

Congreso de la República del Perú. (2011). Ley N° 29733, Ley de protección de datos personales. *El Peruano*. https://www.leyes.congreso.gob.pe/Documentos/Leyes/29733.pdf

European Union. (2024). Commission Implementing Regulation (EU) 2024/2690 of 17 October 2024 laying down rules for the application of Directive (EU) 2022/2555 as regards technical and methodological requirements of cybersecurity risk-management measures and specifying criteria for the categorisation of incidents and cyber threats. *Official Journal of the European Union*. https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ%3AL_202402690

Hagemann, M., & Katsarou, D. (2020). A systematic review on anomaly detection for cloud computing environments. In *Proceedings of the 3rd Artificial Intelligence and Cloud Computing Conference (AICCC '20)* (pp. 144–149). Association for Computing Machinery. https://doi.org/10.1145/3442536.3442550

Institute of Electrical and Electronics Engineers. (2019). *2019 IEEE thesaurus* (Version 1.0). https://www.ieee.org/publications/services/thesaurus-access-page.html

Kitchenham, B., & Charters, S. (2007). *Guidelines for performing systematic literature reviews in software engineering* (EBSE Technical Report EBSE-2007-01, Version 2.3). Keele University; University of Durham. https://www.elsevier.com/__data/promis_misc/525444systematicreviewsguide.pdf

Moudni, M. E., & Ziyati, E. (2025). Advances and challenges in cloud data storage security: A systematic review. *International Journal of Systems Safety and Security Engineering, 15*(4), 675–688. https://doi.org/10.18280/ijsse.150403

Nasim, S. S., Pranav, P., & Dutta, S. (2025). A systematic literature review on intrusion detection techniques in cloud computing. *Discover Computing, 28*, Article 107. https://doi.org/10.1007/s10791-025-09641-y

Omogbehin, B. I., Sigwele, T., Semong, T., Maenge, A., Nedev, Z., & Hlomani, H. (2026). Securing cloud data with machine learning: Trends, gaps, and performance metrics. *IAES International Journal of Artificial Intelligence, 15*(1), 44–55. https://doi.org/10.11591/ijai.v15.i1.pp44-55

Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., Shamseer, L., Tetzlaff, J. M., Akl, E. A., Brennan, S. E., Chou, R., Glanville, J., Grimshaw, J. M., Hróbjartsson, A., Lalu, M. M., Li, T., Loder, E. W., Mayo-Wilson, E., McDonald, S., … Moher, D. (2021). The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. *BMJ, 372*, Article n71. https://doi.org/10.1136/bmj.n71
<!-- /paper:section -->
