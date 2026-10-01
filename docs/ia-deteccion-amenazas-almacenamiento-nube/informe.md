# Informe RSL — IA y detección de amenazas en almacenamiento en la nube

## 1. Tema de la investigación elegido para la RSL

### 1.1 Tema

Inteligencia artificial (IA) para la detección de accesos anómalos y amenazas en servicios de almacenamiento en la nube (*object storage*): revisión sistemática de la literatura (RSL) de técnicas, modelos y evidencia de evaluación.

### 1.2 Problemática

¿Qué técnicas y modelos de inteligencia artificial se han evaluado para detectar accesos anómalos y amenazas de seguridad en servicios de almacenamiento en la nube basados en *object storage*, en escenarios de alto volumen de telemetría del plano de datos, comportamiento legítimo variable y abuso con credenciales válidas, y qué evidencia existe sobre su efectividad, precisión y capacidad de detección en comparación con métodos convencionales (reglas, firmas, umbrales estáticos) en condiciones de evaluación comparables?

### 1.3 Objeto de estudio

Identificar y sintetizar estudios primarios que evalúen técnicas y modelos de IA —aprendizaje automático, aprendizaje profundo, detección de anomalías y analítica conductual sobre registros de acceso a objetos (p. ej. *audit logs*, *data events*, operaciones de lectura y escritura)— para detectar accesos anómalos y amenazas en almacenamiento en la nube. El análisis abarcará métricas de desempeño, validez de los escenarios de evaluación y requisitos de despliegue desde la ingeniería de software.

## 2. Palabras clave

Las palabras clave, el marco PICOCT (población, intervención, comparación, resultado, contexto y tiempo), las queries y los criterios de inclusión y exclusión se encuentran en [picoc/2026-09-30-PICOCT/picoc.md](picoc/2026-09-30-PICOCT/picoc.md).

## 3. Artículos de revisión de literatura relacionados con el tema de investigación

| Referencia bibliográfica (APA) | DOI / URL | Razón | PDF |
|--------------------------------|-----------|-------|-----|
| Hagemann, M., & Katsarou, D. (2020). A systematic review on anomaly detection for cloud computing environments. In *Proceedings of the 3rd Artificial Intelligence and Cloud Computing Conference (AICCC '20)* (pp. 144–149). ACM. | https://doi.org/10.1145/3442536.3442550 | Según la revisión citada, sintetiza 215 estudios sobre detección de anomalías en nube (ML, DL y métodos estadísticos); delimita el corpus amplio que la propuesta debe **recortar** hacia telemetría de almacenamiento y credenciales válidas. | Pendiente |
| Omogbehin, B. I., Sigwele, T., Semong, T., Maenge, A., Nedev, Z., & Hlomani, H. (2026). Securing cloud data with machine learning: Trends, gaps, and performance metrics. *IAES International Journal of Artificial Intelligence, 15*(1), 44–55. | https://doi.org/10.11591/ijai.v15.i1.pp44-55 | Revisión de ML para **control de acceso y seguridad de datos en la nube**, con énfasis en detección de anomalías e *insider threat*; reporta métricas, datasets Amazon Access y CERT, y vacíos (diversidad de datos, ataques adversariales). | `RSL/PDF/omogbehin-2026-securing-cloud-data-ml.pdf` |
| Nasim, S. S., Pranav, P., & Dutta, S. (2025). A systematic literature review on intrusion detection techniques in cloud computing. *Discover Computing, 28*, 107. | https://doi.org/10.1007/s10791-025-09641-y | SLR (115 estudios, 2017–2024) sobre IDPS en nube; población amplia y benchmarks de red frecuentes (p. ej. NSL-KDD, CICIDS2017); frontera a acotar hacia *object storage* y registros del plano de datos. | `RSL/PDF/nasim-2025-idps-cloud-slr.pdf` |

**Queries Scopus auxiliares** (completar revisiones afines; el marco formal de búsqueda está en el PICOCT, sección 2):

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

El aporte propuesto es una RSL que mapee estudios primarios de IA evaluados sobre telemetría de *object storage*, incluido el abuso con credenciales válidas. Debe sintetizar evidencia comparativa frente a baselines convencionales con criterios explícitos de validez de la evaluación. La evidencia secundaria ya cartografía frentes amplios que no deben confundirse con ese recorte.

Según la revisión citada, Hagemann y Katsarou (2020) sintetizan 215 publicaciones sobre detección de anomalías en computación en la nube. Cubren aprendizaje automático, aprendizaje profundo y métodos estadísticos en escenarios heterogéneos, pero no focalizan el abuso con credenciales válidas sobre *object storage*. Omogbehin et al. (2026) revisan el aprendizaje automático para la seguridad de datos en la nube y priorizan la detección de anomalías e *insider threat*. Señalan vacíos de diversidad de datos y ataques adversariales, pero no acotan las interfaces de programación de aplicaciones (API) de *object storage* ni comparan de forma homogénea modelos de IA frente a reglas sobre la misma telemetría de objetos. Nasim et al. (2025) revisan técnicas de detección y prevención de intrusiones en la nube y documentan el desajuste con arquitecturas elásticas. La población mezcla red y almacenamiento y recurre con frecuencia a benchmarks de tráfico de red.

Persiste, por tanto, la necesidad de una RSL en Ingeniería de Software acotada a servicios de *object storage*. Debe sintetizar modelos de IA sobre registros de acceso a objetos y resultados de efectividad, precisión y detección oportuna frente a métodos convencionales. La síntesis debe contrastar telemetría de almacenamiento con benchmarks de red. Debe explicitar límites de validez externa cuando predominen conjuntos de datos sintéticos o ajenos al plano de datos. Así responde al volumen de registros, la variabilidad legítima y las credenciales auténticas de la problemática.

## 5. Línea(s) de investigación de la UTP

La investigación responde, en primer lugar, a la línea **«Computación Científica»**, transversal a los programas de Ingeniería de la Universidad Tecnológica del Perú (UTP), orientada a soluciones computacionales y modelos para analizar procesos de ingeniería. El estudio examina técnicas de inteligencia artificial como componentes evaluables (modelos, pipelines de telemetría, métricas de desempeño) en sistemas de almacenamiento en la nube, lo que encaja con el análisis riguroso de fenómenos técnicos mediante métodos computacionales.

De forma complementaria, se vincula con la línea de **aplicaciones de tecnologías de la información y la comunicación (TIC)**, electrónicas, robóticas y de telecomunicaciones para competitividad, salud, educación y seguridad ciudadana. Esa línea promueve aplicaciones informáticas con impacto en la protección de datos y servicios digitales. La síntesis aporta criterios de arquitectura y operación segura para organizaciones que dependen de almacenamiento en la nube.

## 6. Competencias de la carrera

El tema se relaciona con **tecnologías de vanguardia** y el área de **ciberseguridad**, al examinar detección de amenazas en infraestructura en la nube y criterios de evaluación de controles basados en IA. Conecta con **desarrollo de software** y **análisis de sistemas complejos**, porque el objeto incluye servicios de almacenamiento, pipelines de observabilidad e integración con monitoreo. También exige requisitos no funcionales: latencia, falsos positivos y escalabilidad de ingestión de registros. Dialoga con **desarrollo con IA** y **inteligencia de negocios** al sintetizar métricas para decidir el despliegue de modelos en producción.

## 7. Título tentativo de la RSL

Inteligencia artificial para la detección de accesos anómalos y amenazas en servicios de almacenamiento en la nube: revisión sistemática de técnicas, modelos y evidencia de evaluación
