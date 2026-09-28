<!-- paper:section id=encabezado -->
# Introducción — Inteligencia artificial en el ciclo de vida del software para accesibilidad cognitiva y neurodivergencia: técnicas, fases de ingeniería y métricas de evaluación — una revisión sistemática de la literatura
<!-- /paper:section -->

## I. Introducción


<!-- paper:section id=contexto -->
### Contexto

#### 1.1 Definiciones generales

La accesibilidad digital designa el conjunto de propiedades que permiten a las personas —incluidas aquellas con discapacidad— percibir, operar y comprender productos y servicios digitales. En el ámbito web, las *Web Content Accessibility Guidelines* (WCAG) 2.2 constituyen el marco de referencia dominante para requisitos verificables de conformidad (World Wide Web Consortium [W3C], 2023). Chemnad y Othman (2024) recuerdan que la accesibilidad digital abarca, entre otras, discapacidades visuales, auditivas, motoras o cognitivas, y que la inteligencia artificial (IA) se ha explorado como medio para ampliar el acceso y la calidad de vida de las personas con discapacidad.

En paralelo, el trabajo del W3C *Cognitive and Learning Disabilities Accessibility* (COGA), en particular *Making Content Usable for People with Cognitive and Learning Disabilities*, articula orientaciones orientadas a barreras de comprensión, memoria, atención y carga cognitiva. Dichas orientaciones son, en gran medida, suplementarias respecto del núcleo normativo de conformidad WCAG y, con frecuencia, menos automatizables que los criterios centrados en percepción y operación. Aljedaani y Mollik (2026) subrayan que, en la literatura GenAI+web, WCAG domina como marco de referencia mientras COGA recibe consideración limitada.

Por *accesibilidad cognitiva* se entiende aquí la capacidad del software de reducir barreras cognitivas (p. ej. lenguaje sencillo, consistencia, control del ritmo, minimización de sobrecarga, pasos claros y posibilidad de deshacer acciones). *Neurodivergencia* se usa como categoría amplia que agrupa perfiles como trastorno del espectro autista (TEA), TDAH, dislexia o discapacidad intelectual, sin tratarla como caja negra ni como déficit clínico a “corregir”: el protocolo de la revisión estratificará poblaciones cuando la evidencia lo permita y privilegiará un enfoque de derechos y usabilidad.

La *inteligencia artificial*, incluidos el aprendizaje automático y los modelos de lenguaje grandes (LLM / GenAI), interviene cada vez más en la generación de contenido, la detección de problemas de accesibilidad y la remediación asistida. El *ciclo de vida del software* (requisitos, diseño, implementación, verificación y validación, operación) es el eje de la Ingeniería de Software: el interés de esta revisión no es la tecnología asistiva clínica en sí, sino cómo la IA se inserta en artefactos y procesos de ingeniería —con énfasis en testing, V&V y auditoría, y de forma subordinada en diseño y personalización en runtime— y qué métricas se emplean para evaluar calidad y accesibilidad cognitiva.

#### 1.2 Lo que se sabe del tema hasta la fecha

La evidencia reciente se organiza en frentes ya sintetizados por revisiones sistemáticas o de alcance, que esta RSL toma como frontera y no pretende repetir.

Chemnad y Othman (2024) realizaron una revisión sistemática y análisis bibliométrico de aplicaciones de IA a la accesibilidad digital (artículos académicos 2018–2023; cribado inicial de 3 706 registros en ACM Digital Library, IEEE Xplore, ScienceDirect, Scopus y Springer; análisis final de **43** artículos). Proponen un marco de clasificación por aplicaciones, retos, metodologías de IA y estándares de accesibilidad. Sus hallazgos enfatizan el **predominio de la accesibilidad digital impulsada por IA para discapacidades visuales**, revelan un vacío crítico en habla/audición, TEA, trastornos neurológicos y condiciones motoras, y señalan falta de adhesión a estándares de accesibilidad en muchos sistemas revisados (DOI https://doi.org/10.3389/frai.2024.1349668). **Qué no cubre:** no desagrega la evidencia por fase del ciclo de vida del software ni inventaría métricas cognitivas/COGA orientadas a V&V, Definition of Done o gates de integración continua.

Perry et al. (2024) sintetizaron **15** estudios sobre tecnologías de IA orientadas al funcionamiento adaptativo en condiciones del neurodesarrollo (NDC) en entornos cotidianos (p. ej. robótica, dispositivos móviles, realidad virtual), con énfasis en outcomes clínicos y de apoyo, no en entregables del ciclo de vida del software (*npj Digital Medicine, 7*, Article 370; DOI https://doi.org/10.1038/s41746-024-01355-7). **Qué no cubre:** requisitos, testing, auditoría de accesibilidad ni métricas de calidad de software; delimita la frontera clínico-asistiva respecto de la lente de Ingeniería de Software.

Aljedaani y Mollik (2026) revisaron **38** estudios peer-reviewed sobre LLM en accesibilidad web (W4A ’26 / ACM). Muestran adopción creciente de LLM en flujos de desarrollo y creación de contenido web; tareas predominantes text-céntricas y estructuralmente explícitas; **WCAG como marco principal** y **limitada consideración de COGA**; prácticas de evaluación heterogéneas; escasa participación directa de usuarios con discapacidad; y sesgo hacia issues visuales/percebibles o machine-detectable frente a comprensión y carga cognitiva (DOI https://doi.org/10.1145/3800424.3800452; espejo OA https://arxiv.org/abs/2605.13873). **Qué no cubre:** aunque algunos estudios sitúan LLM en remediación o apoyo al desarrollo, la síntesis es frontera **web/task-level**, no una taxonomía condición × técnica × **fase SE** × métrica para perfiles cognitivos/neurodivergentes.

Como fronteras de solapamiento —no como anclas a remake— se reconocen, además, el *scoping review* de Xu et al. (2025) sobre diseño de interacción humano–IA inclusivo/adaptativo para usuarios neurodivergentes (**117** papers; orientación HCI/AT; DOI https://doi.org/10.1080/17483107.2025.2579822) y la RSL de Paiva et al. (2021) sobre accesibilidad en procesos de Ingeniería de Software (**94** estudios), sin eje IA+cognitivo/COGA (DOI https://doi.org/10.1016/j.jss.2020.110819). En la práctica profesional, Bi et al. (2022) reportan que solo alrededor del **7 %** de practicantes enfocan discapacidad cognitiva frente a un peso mayor de barreras sensoriales (~**37 %** visión), lo que refuerza —sin sustituir— el contraste documental desde una lente SE (DOI https://doi.org/10.1145/3503508).

#### 1.3 Situación actual y disputas

La literatura disputa al menos tres tensiones. Primera: **sesgo sensorial versus cognitivo**. Chemnad y Othman (2024) documentan concentración en discapacidad visual; Aljedaani y Mollik (2026) muestran WCAG dominante y COGA al margen en GenAI+web; Bi et al. (2022) confirman un sesgo análogo en prioridades de practicantes. Segunda: **lente clínica/HCI versus lente de proceso SE**. Perry et al. (2024) y Xu et al. (2025) consolidan apoyo cotidiano e interacción inclusiva sin taxonomía anclada en fases y métricas de ingeniería. Tercera: **automatización versus validez con usuarios**. El auge de LLM y scanners WCAG sugiere eficiencia en V&V, pero las orientaciones cognitivas suelen exigir juicio experto o prueba con personas neurodivergentes; equiparar “WCAG verde” con inclusión cognitiva es ableísmo metodológico y produce *accesibilidad de fachada*.

En el Perú, la Ley 29973 (Ley General de la Persona con Discapacidad) reconoce derechos de accesibilidad a la información y las TIC —incluidos portales y, en el art. 21, lenguaje sencillo— (arts. 15, 21 y 23). La Resolución N.º 001-2025-PCM/SGTD obliga a la Administración Pública a adoptar WCAG 2.2 (y posteriores) de forma progresiva. Esa presión regulatoria **motiva** cumplimiento WCAG; **no** equivale a un mandato COGA ni garantiza por sí sola inclusión cognitiva. En Europa, el European Accessibility Act (EAA) y EN 301 549 refuerzan el mismo patrón: conformidad anclada en WCAG AA, con lo cognitivo fuera del núcleo más automatizable.
<!-- /paper:section -->

<!-- paper:section id=problema -->
### El problema

**Problemática (pregunta de investigación):** ¿Cómo se han integrado técnicas de inteligencia artificial en las fases del ciclo de vida del software —con énfasis en diseño, personalización en runtime y, sobre todo, verificación, evaluación y auditoría— orientadas a usuarios con discapacidad cognitiva o neurodivergencia; qué métricas se reportan (incluidas orientaciones COGA frente al núcleo WCAG); y qué celdas de la matriz *condición × técnica × fase SE × métrica* permanecen vacías frente al sesgo documentado hacia la accesibilidad sensorial/visual y frente a revisiones HCI/AT o GenAI+web que no estructuran el proceso de Ingeniería de Software?

#### 2.1 Tendencias o nuevas perspectivas

Dos tendencias reconfiguran el problema. Por un lado, la adopción de GenAI/LLM en flujos de desarrollo y de remediación de accesibilidad web (Aljedaani & Mollik, 2026) desplaza parte del esfuerzo hacia detección y generación asistida, a menudo en tareas WCAG-duras (texto alternativo, estructura, issues machine-detectable). Por otro, la presión regulatoria (Resolución N.º 001-2025-PCM/SGTD; EAA/EN 301 549) eleva el costo de ignorar accesibilidad, pero incentiva sobre todo checklists automatizables. Surge así la necesidad de preguntar no solo *si* hay IA+a11y, sino *en qué fase SE*, *con qué métrica cognitiva* y *con qué grado de automatización válida*.

#### 2.2 Discrepancias existentes

Existe discrepancia entre (a) el volumen de síntesis sobre IA+accesibilidad digital con sesgo visual (Chemnad & Othman, 2024), (b) el volumen de síntesis clínico-asistiva o HCI para neurodesarrollo/neurodivergencia (Perry et al., 2024; Xu et al., 2025) y (c) la relativa escasez de síntesis que crucen **IA × cognitivo/COGA × fase SE × métrica de evaluación**, con énfasis en verificación. Paiva et al. (2021) ya mapearon accesibilidad en procesos SE, pero sin el eje IA+cognitivo que hoy introduce GenAI. La discrepancia no es la ausencia total de papers adyacentes, sino la **falta de organización SE-centrada** de lo existente, exportable a Definition of Done y gates de CI.

#### 2.3 Vacíos de conocimiento

Persiste un vacío operativo: no se dispone de una taxonomía **condición × técnica de IA × fase SE × métrica** que contraste explícitamente el sesgo visual/WCAG-duro, delimite HCI/AT clínico y señale, por celda, qué puede automatizarse en CI, qué exige juicio experto y qué requiere validación con usuarios COGA. La celda más aguda es **verificación/evaluación/auditoría × GenAI × COGA/cognitivo**; el inventario de métricas cognitivas usadas en V&V de software asistido por IA tampoco está estabilizado a escala de revisión. Diseño y personalización se cubren cuando la evidencia muestre componente de proceso o calidad de software, sin recentrar el objeto en HCI adaptativa ya cartografiada por Xu et al. (2025).

#### 2.4 Contraste: situación actual vs situación deseada

**Situación actual:** evidencia fragmentada entre accesibilidad digital+IA sesgada a lo visual, apoyo clínico/NDC y LLM+web con COGA débil; riesgo de cumplir checklists WCAG (y sellos de conformidad) sin abordar comprensión ni carga cognitiva.  
**Situación deseada:** un mapa de evidencia primaria anclado en Ingeniería de Software que diga, para cada celda de la taxonomía —empezando por V&V—, qué técnicas se han usado, en qué fase, con qué métricas y con qué límites éticos y de automatización.  
**Qué se propone estudiar:** sintetizar esa evidencia primaria (énfasis testing/V&V/auditoría; requisitos/diseño adaptativo y personalización cuando haya anclaje SE) para perfiles cognitivos o neurodivergentes, produciendo la taxonomía cuádruple con columna de transferibilidad a DoD/CI, con exclusión de intervenciones sin componente de proceso o calidad de software.

La pregunta de investigación (§2) formula, en forma interrogativa, precisamente ese contraste: no basta describir tendencias; hay que mapear *cómo*, *con qué métricas* y *qué celdas quedan vacías*.
<!-- /paper:section -->

<!-- paper:section id=justificacion -->
### Justificación

#### 3.1 Justificación de la elección del tema

El tema se eligió porque articula tres tópicos defendibles ante un revisor de Ingeniería de Software: accesibilidad cognitiva/neurodivergencia (con COGA), IA/GenAI aplicada a artefactos del ciclo de vida —en especial V&V—, y fases SE con métricas. Se descartó un título genérico de “software inclusivo” que colisionaba con síntesis HCI (Xu et al., 2025) y se exigió el recorte a ciclo de vida y métricas. Chemnad y Othman (2024), Aljedaani y Mollik (2026) y Bi et al. (2022) aportan evidencia de sesgo visual/WCAG o de prioridades de práctica que hace científicamente pertinente el contraste cognitivo, mientras Perry et al. (2024) evitan confundir el objeto con outcomes clínicos.

Más allá del público académico, los titulares de derecho son personas con discapacidad cognitiva e intelectual y perfiles neurodivergentes que, en el Perú, deben poder usar en igualdad de condiciones la información y las comunicaciones digitales (Ley 29973, arts. 15, 21 y 23). El valor público se sitúa en el horizonte de los Objetivos de Desarrollo Sostenible 10.2 y 4.5/4.a, sin atribuir a la revisión un impacto causal automático sobre la reducción de desigualdades.

#### 3.2 Utilidad de los resultados de la revisión

El artefacto aplicable mínimo no es un marco comercial de conformidad, sino una taxonomía con columna de transferibilidad que marque, por celda, qué evidencia puede alimentar un gate de CI, qué entra en Definition of Done como juicio experto y qué exige validación con personas neurodivergentes —en línea con la presión EAA/EN 301 549 y PCM/WCAG 2.2, que hoy anclan presumción de conformidad en WCAG y dejan lo cognitivo fuera del núcleo automatizable. Los resultados podrían, además, orientar protocolos de extracción en investigación SE y priorizar backlog de remediación cognitiva en productos educativos y de gobierno digital, **sin pretender certificar** cumplimiento legal ni sustituir auditoría/VPAT. Se escribe para investigadores y profesionales de calidad/accesibilidad —e indirectamente para equipos de govtech— que necesitan un mapa accionable, no un brochure de compliance.

#### 3.3 Necesidad de una RSL

Una revisión sistemática (frente a un ensayo o un mapeo informal) es necesaria porque el campo está saturado de revisiones parciales en fronteras adyacentes y el riesgo de remake es alto. Solo un protocolo reproducible (p. ej. PRISMA), con criterios de inclusión/exclusión SE explícitos y estratificación poblacional, permite demostrar el hueco —o documentar celdas vacías— de forma auditable. Si el pilot de la celda aguda V&V×GenAI×COGA resultara vacío o muy fino, el trabajo se reportará como mapeo de celdas vacías / SMS, no como una RSL “llena” inventada. El entregable mínimo no es la prosa sola, sino la taxonomía con columna de transferibilidad a DoD/CI.
<!-- /paper:section -->

<!-- paper:section id=objetivo-rsl -->
### Objetivo de la RSL

El objetivo primario —respuesta operativa a la pregunta de §2— es **sintetizar evidencia primaria** sobre técnicas de IA —con énfasis en GenAI/LLM como apoyo a testing, V&V y auditoría de criterios cognitivos/COGA— aplicadas a artefactos y procesos de Ingeniería de Software para perfiles cognitivos o neurodivergentes, produciendo una taxonomía **condición × técnica de IA × fase SE × métrica de evaluación** con columna de transferibilidad (**automatizable en CI / juicio experto / validación con usuarios COGA**).

Como objetivos subordinados: (a) contrastar esa evidencia frente al sesgo visual/WCAG-duro documentado por Chemnad y Othman (2024) y a la debilidad COGA en GenAI+web mostrada por Aljedaani y Mollik (2026); (b) delimitar el objeto frente al apoyo clínico/NDC de Perry et al. (2024) y frente a las fronteras HCI/AT (Xu et al., 2025) y SE-sin-IA-cognitiva (Paiva et al., 2021); (c) cubrir diseño adaptativo y personalización solo cuando exista anclaje a proceso o calidad de software.

Así se une el problema (fragmentación, sesgo y fachada WCAG en V&V) con lo ya hecho en fronteras adyacentes: no se rehace esos frentes; se organiza la intersección vacía en clave de ciclo de vida y métricas.

**Salvaguarda ética mínima:** no medicalizar la neurodivergencia; no sustituir evidencia clínica por métricas de ingeniería; no clasificar ni “remediar” perfiles cognitivos con GenAI sin criterios de consentimiento, sesgo y gobernanza; señalar cuando la evidencia omita participación de personas con discapacidad o contextos del Sur Global; situar ODS 10.2 y 4.5/4.a como horizonte de valor público, no como impacto causal automático del mapeo. Se rechaza el ableísmo metodológico de equiparar “escáner WCAG en verde” con accesibilidad cognitiva.
<!-- /paper:section -->

<!-- paper:section id=organizacion -->
### Organización del contenido de la revisión

El resto del trabajo se organiza, de forma prevista, así: (1) **Marco teórico y conceptual** (WCAG 2.2, COGA usable, neurodivergencia estratificada, IA/GenAI en SE, DoD/CI y límites de automatización); (2) **Metodología** (protocolo tipo PRISMA, bases IEEE/ACM/Scopus, cadenas de búsqueda, criterios de inclusión/exclusión SE vs HCI/AT/clínico, estratificación poblacional, extracción de la taxonomía cuádruple —incluida la columna de transferibilidad— y de métricas; tabla de solapamiento RQ-propia frente a Xu, Paiva, Chemnad, Perry y Aljedaani); (3) **Resultados** (mapas por condición, técnica, fase y métrica; contraste visual/WCAG vs cognitivo/COGA; celdas densas y vacías, con énfasis en V&V×GenAI×COGA); (4) **Discusión** (implicaciones para Ingeniería de Software, límites de GenAI en auditoría, ética, ableísmo/fachada y transferibilidad a DoD/CI bajo EAA/PCM); (5) **Conclusiones y trabajo futuro**. Un anexo metodológico recogerá la tabla de solapamiento y el registro del pilot de la celda aguda.
<!-- /paper:section -->

<!-- paper:section id=referencias -->
## Referencias

*(Borrador de trabajo — las tres RSL ancla; `rsl-polish-paper` publica la lista limpia.)*

Aljedaani, W., & Mollik, R. H. (2026). Large language models for web accessibility: A systematic literature review. In *Proceedings of the 23rd International Web for All Conference (W4A ’26)* (pp. 160–171). Association for Computing Machinery. https://doi.org/10.1145/3800424.3800452

Chemnad, K., & Othman, A. (2024). Digital accessibility in the era of artificial intelligence—Bibliometric analysis and systematic review. *Frontiers in Artificial Intelligence, 7*, Article 1349668. https://doi.org/10.3389/frai.2024.1349668

Perry, N., Sun, C., Munro, M., Boulton, K. A., & Guastella, A. J. (2024). AI technology to support adaptive functioning in neurodevelopmental conditions in everyday environments: A systematic review. *npj Digital Medicine, 7*, Article 370. https://doi.org/10.1038/s41746-024-01355-7
<!-- /paper:section -->
