<!-- paper:section id=encabezado -->
# Inteligencia artificial para la detección de accesos anómalos y amenazas en servicios de almacenamiento en la nube

**Tema.** Revisión sistemática de estudios primarios que evalúan técnicas y modelos de inteligencia artificial para detectar accesos anómalos y amenazas en servicios de almacenamiento basados en *object storage*, con énfasis en telemetría del plano de datos, comparación frente a métodos convencionales y métricas de despliegue. · **Problemática.** ¿Qué técnicas y modelos de inteligencia artificial se han evaluado para detectar accesos anómalos y amenazas de seguridad en servicios de almacenamiento en la nube basados en *object storage*, en escenarios de alto volumen de telemetría del plano de datos, comportamiento legítimo variable y abuso con credenciales válidas, y qué evidencia existe sobre efectividad, precisión, recall, tasa de falsos positivos, latencia de detección y tiempo hasta detección en comparación con métodos convencionales (reglas, firmas, umbrales estáticos) en condiciones de evaluación comparables? · **Objetivo.** Sintetizar esa evidencia primaria, clasificar técnicas y modelos, registrar baselines y métricas reportadas, y describir el contexto de ingeniería de software de las evaluaciones, de forma repetible y alineada con un protocolo de población, intervención, comparación, resultado, contexto y tiempo.
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

Una RSL es necesaria porque el campo cuenta con revisiones parciales y el riesgo de repetir cartografías genéricas es alto. Kitchenham y Charters (2007) recomiendan protocolo predefinido para reducir sesgo y documentar búsqueda y selección; el reporte seguirá las directrices *Preferred Reporting Items for Systematic Reviews and Meta-Analyses* (PRISMA) 2020 (Page et al., 2021) cuando las secciones metodológicas del manuscrito estén activas.
<!-- /paper:section -->

<!-- paper:section id=objetivo-rsl -->
### Objetivo de la RSL

El objetivo general es sintetizar estudios primarios que evalúen técnicas y modelos de inteligencia artificial para detectar accesos anómalos y amenazas en servicios de almacenamiento en la nube basados en *object storage*. El análisis abarcará métricas de desempeño, validez de los escenarios de evaluación y requisitos de despliegue desde la ingeniería de software.

Objetivos específicos, alineados con el protocolo de población, intervención, comparación, resultado, contexto y tiempo (PICOCT):

1. **RQ1 (P):** Identificar qué servicios o artefactos de almacenamiento y qué fuentes de telemetría abordan los estudios, y si consideran escenarios con credencial válida o amenaza interna.
2. **RQ2 (I):** Catalogar técnicas y modelos de IA evaluados (familia, herramienta o framework).
3. **RQ3 (C):** Registrar con qué métodos convencionales se comparan o contrastan los enfoques de IA y el tipo de comparación.
4. **RQ4 (O):** Extraer métricas reportadas (precisión, recall, F1, área bajo la curva, falsos positivos, latencia, tiempo hasta detección), con atención a equipos sin centro de operaciones de seguridad pleno.
5. **RQ5 (Co):** Describir el contexto de ingeniería de software (artefacto, escala, despliegue en tiempo real, integración con monitoreo o gestión de información y eventos de seguridad).
6. **RQ6 (T):** Caracterizar la distribución temporal de las publicaciones incluidas (2021–2026).

La contribución prevista es un mapa reproducible de técnicas y modelos evaluados sobre telemetría de *object storage*, con síntesis de validez externa frente a baselines convencionales cuando la evidencia lo permita.
<!-- /paper:section -->

<!-- paper:section id=organizacion -->
### Organización del contenido de la revisión

Este manuscrito desarrolla la Introducción. Las secciones de Metodología —marco PICOCT, palabras clave, ecuación de búsqueda, criterios de inclusión y exclusión, selección según PRISMA, extracción y síntesis—, Resultados, Discusión, Conclusión y Declaraciones se incorporarán tras el cribado y la extracción de datos. El protocolo PICOCT del tema fija la pregunta general, las preguntas por componente y los criterios que alimentarán la Metodología.
<!-- /paper:section -->

<!-- paper:section id=referencias -->
## Referencias

Alzoubi, H. B., & Aljaafreh, A. (2020). A review of machine learning algorithms for cloud computing security. *Electronics, 9*(9), Article 1379. https://doi.org/10.3390/electronics9091379

Congreso de la República del Perú. (2011). Ley N° 29733, Ley de protección de datos personales. *El Peruano*. https://www.leyes.congreso.gob.pe/Documentos/Leyes/29733.pdf

European Union. (2024). Commission Implementing Regulation (EU) 2024/2690 of 17 October 2024 laying down rules for the application of Directive (EU) 2022/2555 as regards technical and methodological requirements of cybersecurity risk-management measures and specifying criteria for the categorisation of incidents and cyber threats. *Official Journal of the European Union*. https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ%3AL_202402690

Hagemann, M., & Katsarou, D. (2020). A systematic review on anomaly detection for cloud computing environments. In *Proceedings of the 3rd Artificial Intelligence and Cloud Computing Conference (AICCC '20)* (pp. 144–149). Association for Computing Machinery. https://doi.org/10.1145/3442536.3442550

Kitchenham, B., & Charters, S. (2007). *Guidelines for performing systematic literature reviews in software engineering* (EBSE Technical Report EBSE-2007-01, Version 2.3). Keele University; University of Durham. https://www.elsevier.com/__data/promis_misc/525444systematicreviewsguide.pdf

Moudni, M. E., & Ziyati, E. (2025). Advances and challenges in cloud data storage security: A systematic review. *International Journal of Systems Safety and Security Engineering, 15*(4), 675–688. https://doi.org/10.18280/ijsse.150403

Nasim, S. S., Pranav, P., & Dutta, S. (2025). A systematic literature review on intrusion detection techniques in cloud computing. *Discover Computing, 28*, Article 107. https://doi.org/10.1007/s10791-025-09641-y

Omogbehin, B. I., Sigwele, T., Semong, T., Maenge, A., Nedev, Z., & Hlomani, H. (2026). Securing cloud data with machine learning: Trends, gaps, and performance metrics. *IAES International Journal of Artificial Intelligence, 15*(1), 44–55. https://doi.org/10.11591/ijai.v15.i1.pp44-55

Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., Shamseer, L., Tetzlaff, J. M., Akl, E. A., Brennan, S. E., Chou, R., Glanville, J., Grimshaw, J. M., Hróbjartsson, A., Lalu, M. M., Li, T., Loder, E. W., Mayo-Wilson, E., McDonald, S., … Moher, D. (2021). The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. *BMJ, 372*, Article n71. https://doi.org/10.1136/bmj.n71
<!-- /paper:section -->
