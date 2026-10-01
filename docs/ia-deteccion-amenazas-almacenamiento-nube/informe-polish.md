# Informe RSL — IA y detección de amenazas en almacenamiento en la nube

## 1. Tema de la investigación elegido para la RSL

### 1.1 Tema

Inteligencia artificial (IA) para la detección de accesos anómalos y amenazas de seguridad en servicios de almacenamiento en la nube (*object storage*): revisión sistemática de la literatura (RSL) de técnicas, modelos y evidencia de evaluación.

### 1.2 Problemática

¿Qué técnicas y modelos de inteligencia artificial se han evaluado para detectar accesos anómalos y amenazas de seguridad en servicios de almacenamiento en la nube basados en *object storage*, en escenarios de alto volumen de telemetría del plano de datos, comportamiento legítimo variable y abuso con credenciales válidas, y qué evidencia existe sobre efectividad, precisión, recall, tasa de falsos positivos, latencia de detección y tiempo hasta detección en comparación con métodos convencionales (reglas, firmas, umbrales estáticos) en condiciones de evaluación comparables?

### 1.3 Objeto de estudio

Identificar y sintetizar estudios primarios que evalúen técnicas y modelos de IA —aprendizaje automático, aprendizaje profundo, detección de anomalías y analítica conductual sobre registros de acceso a objetos (p. ej. *audit logs* y *data events*)— para detectar accesos anómalos y amenazas en almacenamiento en la nube. El análisis abarcará métricas de desempeño, validez de los escenarios de evaluación y requisitos de despliegue de artefactos software (servicios, pipelines de observabilidad, integración con monitoreo) desde la ingeniería de software.

## 2. Palabras clave

Las palabras clave, el marco PICOCT (población, intervención, comparación, resultado, contexto y tiempo), las queries y los criterios de inclusión y exclusión se encuentran en [picoc/2026-09-30-2-PICOCT/picoc.md](picoc/2026-09-30-2-PICOCT/picoc.md).

## 3. Artículos de revisión de literatura relacionados con el tema de investigación

*(Mínimo dos revisiones; meta: tres estudios secundarios ancla. Tipología distinta en cada fila.)*

| Referencia bibliográfica (APA) | DOI / URL | Razón | PDF |
|--------------------------------|-----------|-------|-----|
| Hagemann, M., & Katsarou, D. (2020). A systematic review on anomaly detection for cloud computing environments. In *Proceedings of the 3rd Artificial Intelligence and Cloud Computing Conference (AICCC '20)* (pp. 144–149). ACM. | https://doi.org/10.1145/3442536.3442550 | Revisión sistemática en actas de congreso; según los autores, abarca un corpus amplio sobre anomalías en nube (aprendizaje automático, aprendizaje profundo y métodos estadísticos). Delimita el universo que esta RSL debe recortar hacia telemetría de almacenamiento y credenciales válidas. | Pendiente |
| Omogbehin, B. I., Sigwele, T., Semong, T., Maenge, A., Nedev, Z., & Hlomani, H. (2026). Securing cloud data with machine learning: Trends, gaps, and performance metrics. *IAES International Journal of Artificial Intelligence, 15*(1), 44–55. | https://doi.org/10.11591/ijai.v15.i1.pp44-55 | Revisión narrativa de ML para control de acceso y seguridad de datos en la nube, con énfasis en detección de anomalías y amenaza interna (*insider threat*). Reporta métricas y datasets Amazon Access y CERT, pero no acota primarios evaluados solo en APIs de *object storage* ni comparaciones homogéneas frente a reglas sobre la misma telemetría. | `RSL/PDF/omogbehin-2026-securing-cloud-data-ml.pdf` |
| Nasim, S. S., Pranav, P., & Dutta, S. (2025). A systematic literature review on intrusion detection techniques in cloud computing. *Discover Computing, 28*, 107. | https://doi.org/10.1007/s10791-025-09641-y | Revisión sistemática de la literatura (115 estudios, 2017–2024) sobre sistemas de detección y prevención de intrusiones (IDPS) en nube. Población amplia, con benchmarks de red frecuentes (p. ej. NSL-KDD, CICIDS2017); frontera a acotar hacia *object storage* y registros del plano de datos. | `RSL/PDF/nasim-2025-idps-cloud-slr.pdf` |

**Fronteras de solapamiento (no sustituyen a las tres revisiones ancla):**

| Frontera | DOI | Uso en el protocolo |
|----------|-----|---------------------|
| Alzoubi, H. B., & Aljaafreh, A. (2020). A review of machine learning algorithms for cloud computing security. *Electronics, 9*(9), 1379. | https://doi.org/10.3390/electronics9091379 | Revisión narrativa (no SLR) sobre algoritmos de ML en seguridad cloud, incluidos ataques orientados a almacenamiento; contrasta saturación del corredor ML–cloud frente al recorte PICOC. |
| Revisión de seguridad en almacenamiento en la nube (2020–2024), *International Journal of Systems Security and Engineering* (IIETA). | https://doi.org/10.18280/ijsse.150403 | Revisión de controles en almacenamiento cloud (ML como una técnica entre otras); delimita qué ya se sintetizó sobre *storage* sin foco en detección conductual con IA sobre logs de objetos. |

**Queries Scopus auxiliares** (localizar revisiones faltantes; el marco formal está en el PICOCT, sección 2):

```
TITLE-ABS-KEY ( "systematic review" OR "systematic literature review" OR "scoping review" )
AND TITLE-ABS-KEY ( "anomaly detection" AND "cloud computing" )
AND PUBYEAR > 2018

TITLE-ABS-KEY ( ( "cloud storage" OR "object storage" OR "data storage" ) AND ( "machine learning" OR "deep learning" OR "artificial intelligence" ) AND ( "systematic review" OR "literature review" ) )
AND PUBYEAR > 2019

TITLE-ABS-KEY ( "cloud data security" AND "machine learning" AND ( "systematic review" OR "literature review" ) )
AND PUBYEAR > 2020
```

## 4. Estado del conocimiento y necesidad de una nueva RSL

La evidencia secundaria ya cartografía frentes amplios que no deben confundirse con el aporte propuesto. Según Hagemann y Katsarou (2020), la revisión en actas abarca detección de anomalías en computación en la nube con técnicas heterogéneas, sin focalizar el abuso con credenciales válidas sobre *object storage*. Omogbehin et al. (2026) sintetizan aprendizaje automático para seguridad de datos y acceso en la nube y priorizan detección de anomalías. Señalan vacíos de diversidad de datos y ataques adversariales, pero no delimitan primarios evaluados solo en servicios de *object storage* ni baselines convencionales en el mismo escenario de telemetría. Nasim et al. (2025) documentan 115 estudios sobre sistemas de detección y prevención de intrusiones (IDPS) en nube y el desajuste con arquitecturas elásticas; la población mezcla red y almacenamiento. Alzoubi y Aljaafreh (2020) revisan algoritmos de aprendizaje automático para amenazas en la nube, incluidos escenarios de almacenamiento, sin el recorte de población del marco PICOCT de esta RSL.

En consecuencia, persiste la necesidad de una RSL en Ingeniería de Software que sintetice primarios cuya evaluación ocurra en telemetría de *object storage* y contraste modelos de IA con métodos convencionales en condiciones comparables. La contribución prevista es un mapa reproducible de técnicas y modelos evaluados, con síntesis de validez externa (telemetría real frente a benchmarks de red) y de métricas operativas (falsos positivos, latencia, tiempo hasta detección). Si el cribado confirma escasez de primarios, el hallazgo de vacío metodológico será resultado explícito, no un metaanálisis cuantitativo forzado. Además del hueco bibliográfico, organizaciones que almacenan datos en la nube deben priorizar detección sobre acceso a objetos con criterios operativos alineados a monitorización y registro en gestión de riesgo cibernético (Reglamento de aplicación [UE] 2024/2690).

## 5. Línea(s) de investigación de la UTP

La investigación responde, en primer lugar, a la línea de **aplicaciones de tecnologías de la información y la comunicación (TIC)**, electrónicas, robóticas y de telecomunicaciones para competitividad, salud, educación y seguridad ciudadana. Esa línea promueve aplicaciones informáticas con impacto en protección de datos e infraestructura digital, en coherencia con los objetivos de desarrollo sostenible (ODS) 9 y 16. La síntesis aporta criterios de arquitectura y operación segura para titulares de datos y para organizaciones, incluidas micro y pequeñas empresas sin un centro de operaciones de seguridad pleno, que dependen de almacenamiento en la nube. La revisión contrastará evidencia sobre falsos positivos y supervisión humana con el marco de protección de datos personales (Ley N° 29733) y con principios de uso responsable de la inteligencia artificial.

De forma complementaria, se vincula con la línea **«Computación Científica»** de la Universidad Tecnológica del Perú (UTP), en la medida en que examina modelos de aprendizaje automático y métricas de evaluación como objetos de análisis computacional en procesos de ingeniería.

## 6. Competencias de la carrera

El tema se relaciona con **tecnologías de vanguardia** y **ciberseguridad**, al examinar detección de amenazas en infraestructura en la nube y criterios de evaluación de controles basados en IA. Conecta con **desarrollo de software** y **análisis de sistemas complejos**, porque el objeto incluye artefactos evaluables: servicios, pipelines de observabilidad e integración con monitoreo. También exige requisitos no funcionales de latencia, falsos positivos y escalabilidad de ingestión de registros; los falsos positivos afectan la continuidad del servicio y la confianza del usuario. Dialoga con **desarrollo con IA** y **inteligencia de negocios** al sintetizar métricas para decidir el despliegue de modelos en producción. La síntesis orienta a responsables de arquitectura y cumplimiento que deben justificar controles sobre almacenamiento gestionado en la nube.

## 7. Título tentativo de la RSL

Inteligencia artificial para la detección de accesos anómalos y amenazas en servicios de almacenamiento en la nube: revisión sistemática de técnicas, modelos y evidencia de evaluación
