<!-- paper:section id=encabezado -->
# Inteligencia artificial para la detección de accesos anómalos y amenazas en servicios de almacenamiento en la nube: revisión sistemática de técnicas, modelos y evidencia de evaluación

**Problemática (pregunta de investigación):** ¿Qué técnicas y modelos de inteligencia artificial se han evaluado para detectar accesos anómalos y amenazas de seguridad en servicios de almacenamiento en la nube basados en *object storage*, en escenarios de alto volumen de telemetría del plano de datos, comportamiento legítimo variable y abuso con credenciales válidas, y qué evidencia existe sobre efectividad, precisión, recall, tasa de falsos positivos, latencia de detección y tiempo hasta detección en comparación con métodos convencionales (reglas, firmas, umbrales estáticos) en condiciones de evaluación comparables?
<!-- /paper:section -->

## I. Introducción

<!-- paper:section id=contexto -->
### Contexto

#### 1.1 Definiciones generales

Los servicios de almacenamiento en la nube basados en *object storage* permiten guardar y recuperar objetos (archivos, blobs) mediante interfaces de programación de aplicaciones (API), con escalado elástico y facturación por uso. En proveedores como Amazon Web Services (S3), Microsoft Azure (Blob) o Google Cloud Storage, la telemetría del plano de datos —p. ej. *data events* y registros de auditoría de buckets— registra quién accede a qué objeto, desde dónde y con qué operación. Ese volumen de registros supera con frecuencia la capacidad de análisis manual y alimenta tanto operaciones de seguridad como cumplimiento.

Por *inteligencia artificial* (IA) se entiende aquí el uso de aprendizaje automático, aprendizaje profundo, minería de datos y técnicas de detección de anomalías para modelar comportamiento legítimo y señalar accesos atípicos o amenazas. Los métodos *convencionales* incluyen reglas estáticas, firmas, umbrales y sistemas de detección de intrusiones (IDPS) diseñados para redes o hosts, que a menudo se adaptan de forma incompleta al plano de objetos.

La *detección de accesos anómalos* busca identificar patrones de acceso que se desvían de una línea base; la *amenaza de seguridad* abarca, en este trabajo, abuso con credenciales válidas, exfiltración, escalada de privilegios sobre buckets y otras acciones maliciosas visibles en logs de almacenamiento. Desde la *ingeniería de software*, el interés no es solo el algoritmo aislado, sino el artefacto evaluado: servicio, pipeline de ingestión, integración con monitoreo y requisitos no funcionales (latencia, tasa de falsos positivos, coste de telemetría).

#### 1.2 Lo que se sabe del tema hasta la fecha

La evidencia secundaria reciente se organiza en revisiones de distinta amplitud y tipología, que esta revisión sistemática de la literatura (RSL) toma como frontera.

Hagemann y Katsarou (2020), en actas de congreso, sintetizan un corpus amplio sobre detección de anomalías en computación en la nube. Abordan aprendizaje automático, aprendizaje profundo y métodos estadísticos. **Qué no cubre:** no acota la población a servicios de *object storage*, ni el abuso con credenciales válidas, ni comparaciones homogéneas frente a baselines sobre la misma telemetría de objetos.

Omogbehin et al. (2026) revisan el aprendizaje automático para la seguridad y el control de acceso a datos en la nube, con énfasis en detección de anomalías y amenaza interna. Reportan métricas, datasets como Amazon Access y el conjunto CERT (*Computer Emergency Response Team*), y vacíos de diversidad de datos y ataques adversariales. **Qué no cubre:** no delimita primarios evaluados solo en interfaces de programación de aplicaciones de *object storage* ni comparaciones empíricas de IA frente a reglas en un mismo escenario de logs de objetos.

Nasim et al. (2025) realizan una revisión sistemática de la literatura con 115 estudios (2017–2024) sobre técnicas de IDPS en computación en la nube. Documentan enfoques basados en aprendizaje automático y la dificultad de adaptar IDPS clásicos a arquitecturas elásticas. La población mezcla red y almacenamiento y recurre con frecuencia a benchmarks de tráfico de red. **Qué no cubre:** la síntesis no está centrada en telemetría del plano de datos de *object storage* ni en métricas operativas comparables entre IA y métodos convencionales en ese dominio.

Alzoubi y Aljaafreh (2020) ofrecen, como frontera adicional, una revisión narrativa de algoritmos de aprendizaje automático para seguridad en la nube, incluidos ataques orientados a almacenamiento. Una revisión de controles en almacenamiento en la nube (2020–2024) en *International Journal of Systems Security and Engineering* trata el aprendizaje automático como una técnica entre otras, sin foco en detección conductual con IA sobre registros de acceso a objetos.

#### 1.3 Situación actual y disputas

La literatura disputa al menos tres tensiones. Primera: **nube genérica versus plano de almacenamiento**. Las revisiones amplias (Hagemann & Katsarou, 2020; Nasim et al., 2025) mezclan capas de red, hosts y servicios; los equipos que operan buckets necesitan evidencia sobre *data events* y audit logs, no solo sobre tráfico. Segunda: **control de acceso con aprendizaje automático (ML) frente a detección en un centro de operaciones de seguridad (SOC) sobre objetos**. Omogbehin et al. (2026) priorizan seguridad de datos y acceso; ello no equivale a evaluar modelos sobre la misma telemetría que usaría un SOC para almacenamiento S3 o Blob. Tercera: **métricas de laboratorio versus despliegue**. Muchos primarios reportan precisión o exactitud en datasets sintéticos o de red; la discusión operativa exige falsos positivos, latencia y tiempo hasta detección cuando el atacante usa credenciales legítimas.

En la práctica, incidentes con robo de credenciales y exfiltración masiva desde entornos de almacenamiento gestionado muestran que la detección tardía tiene costo para organizaciones y titulares de datos. El Reglamento de aplicación (UE) 2024/2690 (European Union, 2024), en el marco de la directiva europea de ciberseguridad NIS2 (*Network and Information Security Directive 2*), refuerza monitorización y registro sobre sistemas que procesan y almacenan datos. Esa presión **motiva** criterios operativos; **no** sustituye la necesidad de sintetizar evidencia primaria sobre qué modelos de IA aportan detección oportuna en *object storage* frente a reglas y controles nativos.
<!-- /paper:section -->

<!-- paper:section id=problema -->
### El problema

**Problemática (pregunta de investigación):** ¿Qué técnicas y modelos de inteligencia artificial se han evaluado para detectar accesos anómalos y amenazas de seguridad en servicios de almacenamiento en la nube basados en *object storage*, en escenarios de alto volumen de telemetría del plano de datos, comportamiento legítimo variable y abuso con credenciales válidas, y qué evidencia existe sobre efectividad, precisión, recall, tasa de falsos positivos, latencia de detección y tiempo hasta detección en comparación con métodos convencionales (reglas, firmas, umbrales estáticos) en condiciones de evaluación comparables?

#### 2.1 Tendencias o nuevas perspectivas

Dos tendencias reconfiguran el problema. Por un lado, los proveedores de nube integran detección basada en modelos estadísticos o de aprendizaje automático sobre telemetría de almacenamiento, lo que obliga a contrastar esos controles con pipelines propios. Por otro, el volumen de registros del plano de datos crece más rápido que la capacidad de reglas estáticas mantenidas a mano, lo que impulsa aprendizaje no supervisado y analítica conductual. Surge la necesidad de preguntar no solo si existe IA en seguridad cloud, sino **qué técnicas se evaluaron en object storage**, **con qué métricas** y **frente a qué baselines** en condiciones comparables.

#### 2.2 Discrepancias existentes

Existe discrepancia entre tres frentes. Primero, revisiones que cartografían anomalías o IDPS en toda la nube (Hagemann & Katsarou, 2020; Nasim et al., 2025). Segundo, revisiones centradas en datos y acceso en la nube (Omogbehin et al., 2026; Alzoubi & Aljaafreh, 2020). Tercero, la escasez relativa de síntesis que crucen telemetría de *object storage*, modelos de IA, comparación con métodos convencionales y métricas operativas en un mismo mapa. La discrepancia no es la ausencia total de papers adyacentes, sino la falta de mapa reproducible para ingeniería de software y operaciones.

#### 2.3 Vacíos de conocimiento

Persiste un vacío metodológico: no se dispone de una síntesis que clasifique primarios por proximidad a telemetría real de objetos (frente a benchmarks de red), que registre escenarios con credenciales válidas y que agregue evidencia sobre falsos positivos, latencia y tiempo hasta detección. Si el cribado confirma pocos estudios, el hallazgo de vacío debe reportarse explícitamente en lugar de forzar un metaanálisis cuantitativo.

#### 2.4 Contraste: situación actual vs situación deseada

**Situación actual:** evidencia fragmentada entre nube genérica, seguridad de datos con ML y IDPS elásticos; riesgo de desplegar modelos entrenados en datasets ajenos al plano de objetos.  
**Situación deseada:** un mapa de primarios evaluados en *object storage*, con síntesis de técnicas, baselines y validez externa de los escenarios.  
**Pregunta de investigación** (protocolo de población, intervención, comparación, resultado, contexto y tiempo [PICOCT], formulación literal):

> ¿Qué técnicas y modelos de inteligencia artificial se han evaluado para detectar accesos anómalos y amenazas de seguridad en servicios de almacenamiento en la nube basados en *object storage*, en escenarios de alto volumen de telemetría del plano de datos, comportamiento legítimo variable y abuso con credenciales válidas, y qué evidencia existe sobre efectividad, precisión, recall, tasa de falsos positivos, latencia de detección y tiempo hasta detección en comparación con métodos convencionales (reglas, firmas, umbrales estáticos) en condiciones de evaluación comparables?
<!-- /paper:section -->

<!-- paper:section id=justificacion -->
### Justificación

#### 3.1 Justificación de la elección del tema

El tema articula seguridad en la nube, detección de anomalías con IA y artefactos de ingeniería de software evaluables (pipelines, integración con monitoreo). Se descartó un planteamiento genérico de «IA y ciberseguridad cloud» que colisionaría con Nasim et al. (2025) y Hagemann y Katsarou (2020). El recorte a *object storage* y credenciales válidas responde a un problema operativo documentado en la literatura secundaria y en marcos de gestión de riesgo que exigen monitorización sobre datos almacenados.

La síntesis interesa a titulares de datos y a organizaciones —incluidas micro y pequeñas empresas sin un SOC pleno— que externalizan almacenamiento. La revisión contrastará evidencia sobre falsos positivos y supervisión humana con el marco de protección de datos personales en el Perú (Ley N° 29733; Congreso de la República del Perú, 2011) y con principios de uso responsable de la inteligencia artificial.

#### 3.2 Utilidad de los resultados de la revisión

Los resultados orientarán a responsables de arquitectura y cumplimiento que deben justificar controles sobre almacenamiento gestionado: qué telemetría activar, qué familia de modelos evaluar y qué métricas exigir antes de desplegar un pipeline en producción. No sustituyen la configuración de identidad y acceso ni los controles nativos del proveedor; ofrecen un mapa de evidencia primaria para decisiones de ingeniería.

#### 3.3 Necesidad de una RSL

Una revisión sistemática de la literatura es necesaria porque el campo cuenta con revisiones parciales en frentes adyacentes y el riesgo de duplicar mapas genéricos es alto. Kitchenham y Charters (2007) recomiendan un protocolo predefinido para reducir el sesgo del investigador y documentar búsqueda y selección de forma repetible. El reporte seguirá la guía de *Preferred Reporting Items for Systematic Reviews and Meta-Analyses* (PRISMA) 2020 (Page et al., 2021) para hacer auditable el proceso de identificación y cribado cuando las secciones metodológicas del trabajo se activen en el documento final.
<!-- /paper:section -->

<!-- paper:section id=objetivo-rsl -->
### Objetivo de la RSL

El objetivo general es sintetizar estudios primarios que evalúen técnicas y modelos de inteligencia artificial para detectar accesos anómalos y amenazas en servicios de almacenamiento en la nube basados en *object storage*, analizando métricas de desempeño, validez de los escenarios de evaluación y requisitos de despliegue desde la ingeniería de software.

Objetivos específicos, alineados con las preguntas del protocolo de población, intervención, comparación, resultado, contexto y tiempo (PICOCT):

1. **RQ1 (P):** Identificar qué servicios o artefactos de almacenamiento y qué fuentes de telemetría abordan los estudios, y si consideran escenarios con credencial válida o amenaza interna.
2. **RQ2 (I):** Catalogar técnicas y modelos de IA evaluados (familia, herramienta o framework).
3. **RQ3 (C):** Registrar con qué métodos convencionales se comparan o contrastan los enfoques de IA y el tipo de comparación.
4. **RQ4 (O):** Extraer métricas reportadas (precisión, recall, F1, área bajo la curva [AUC], falsos positivos, latencia, tiempo hasta detección).
5. **RQ5 (Co):** Describir el contexto de ingeniería de software (artefacto, escala, despliegue en tiempo real, integración con SOC o con gestión de información y eventos de seguridad [SIEM]).
6. **RQ6 (T):** Caracterizar la distribución temporal de las publicaciones incluidas (2021–2026).

La contribución prevista es un mapa reproducible de técnicas y modelos evaluados sobre telemetría de *object storage*, con síntesis de validez externa frente a baselines convencionales cuando la evidencia lo permita.
<!-- /paper:section -->

<!-- paper:section id=organizacion -->
### Organización del contenido de la revisión

El presente borrador desarrolla la **Introducción** (contexto, problema, justificación, objetivos y organización). Las secciones de **Metodología** (marco PICOCT, palabras clave, ecuación de búsqueda, criterios de inclusión y exclusión, selección PRISMA, extracción y síntesis), **Resultados**, **Discusión**, **Conclusión** y **Declaraciones** se incorporarán en versiones posteriores del manuscrito, una vez completado el cribado y la extracción de datos de los estudios primarios. El protocolo de búsqueda PICOCT del tema fija la pregunta general, las preguntas por componente y los criterios de inclusión y exclusión que alimentarán la Metodología.
<!-- /paper:section -->

<!-- paper:section id=referencias -->
## Referencias

Alzoubi, H. B., & Aljaafreh, A. (2020). A review of machine learning algorithms for cloud computing security. *Electronics, 9*(9), Article 1379. https://doi.org/10.3390/electronics9091379

Congreso de la República del Perú. (2011). Ley N° 29733, Ley de protección de datos personales. *El Peruano*. https://www.leyes.congreso.gob.pe/Documentos/Leyes/29733.pdf

European Union. (2024). Commission Implementing Regulation (EU) 2024/2690 of 17 October 2024 laying down rules for the application of Directive (EU) 2022/2555 as regards technical and methodological requirements of cybersecurity risk-management measures and specifying criteria for the categorisation of incidents and cyber threats. *Official Journal of the European Union*. https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ%3AL_202402690

Hagemann, M., & Katsarou, D. (2020). A systematic review on anomaly detection for cloud computing environments. In *Proceedings of the 3rd Artificial Intelligence and Cloud Computing Conference (AICCC '20)* (pp. 144–149). Association for Computing Machinery. https://doi.org/10.1145/3442536.3442550

Kitchenham, B., & Charters, S. (2007). *Guidelines for performing systematic literature reviews in software engineering* (EBSE Technical Report EBSE-2007-01, Version 2.3). Keele University; University of Durham. https://www.elsevier.com/__data/promis_misc/525444systematicreviewsguide.pdf

Nasim, S. S., Pranav, P., & Dutta, S. (2025). A systematic literature review on intrusion detection techniques in cloud computing. *Discover Computing, 28*, Article 107. https://doi.org/10.1007/s10791-025-09641-y

Omogbehin, B. I., Sigwele, T., Semong, T., Maenge, A., Nedev, Z., & Hlomani, H. (2026). Securing cloud data with machine learning: Trends, gaps, and performance metrics. *IAES International Journal of Artificial Intelligence, 15*(1), 44–55. https://doi.org/10.11591/ijai.v15.i1.pp44-55

Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., Shamseer, L., Tetzlaff, J. M., Akl, E. A., Brennan, S. E., Chou, R., Glanville, J., Grimshaw, J. M., Hróbjartsson, A., Lalu, M. M., Li, T., Loder, E. W., Mayo-Wilson, E., McDonald, S., … Moher, D. (2021). The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. *BMJ, 372*, Article n71. https://doi.org/10.1136/bmj.n71
<!-- /paper:section -->
