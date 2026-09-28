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

En respuesta a la pregunta planteada, el objetivo general es sintetizar la evidencia primaria sobre técnicas de inteligencia artificial aplicadas a los procesos de Ingeniería de Software dirigidos a personas con discapacidad cognitiva o neurodivergentes. Esa evidencia se organizará en una taxonomía que cruza condición, técnica, fase del ciclo de vida y métrica, e indica para cada combinación si su resultado puede verificarse de forma automática en la integración continua, si requiere juicio experto o si exige pruebas con usuarios.

De él se derivan cinco objetivos específicos, uno por cada pregunta de investigación del protocolo:

1. Caracterizar los perfiles de discapacidad cognitiva o neurodivergencia que abordan los estudios, su grado de estratificación y la participación de personas con discapacidad.
2. Identificar las técnicas de inteligencia artificial aplicadas, incluidas la inteligencia artificial generativa y los modelos de lenguaje grandes, y el papel que cumplen en el proceso de software.
3. Contrastar la evidencia sobre accesibilidad cognitiva con la centrada en la accesibilidad sensorial o visual y en la conformidad con las pautas de accesibilidad para el contenido web.
4. Inventariar las métricas de evaluación reportadas y su grado de automatización.
5. Ubicar la inteligencia artificial en cada fase del ciclo de vida del software y medir el peso relativo de la verificación y la evaluación.

La revisión adopta, además, salvaguardas éticas explícitas. No medicaliza la neurodivergencia, no sustituye la evidencia clínica por métricas de ingeniería y señala cuándo los estudios omiten la participación de personas con discapacidad. Tampoco equipara un analizador de conformidad sin errores con la accesibilidad cognitiva.
<!-- /paper:section -->

<!-- paper:section id=organizacion -->
### Organización del contenido de la revisión

El resto del trabajo se organiza, de forma prevista, así: (1) **Marco teórico y conceptual** (WCAG 2.2, COGA usable, neurodivergencia estratificada, IA/GenAI en SE, DoD/CI y límites de automatización); (2) **Metodología** (protocolo tipo PRISMA, bases IEEE/ACM/Scopus, cadenas de búsqueda, criterios de inclusión/exclusión SE vs HCI/AT/clínico, estratificación poblacional, extracción de la taxonomía cuádruple —incluida la columna de transferibilidad— y de métricas; tabla de solapamiento RQ-propia frente a Xu, Paiva, Chemnad, Perry y Aljedaani); (3) **Resultados** (mapas por condición, técnica, fase y métrica; contraste visual/WCAG vs cognitivo/COGA; celdas densas y vacías, con énfasis en V&V×GenAI×COGA); (4) **Discusión** (implicaciones para Ingeniería de Software, límites de GenAI en auditoría, ética, ableísmo/fachada y transferibilidad a DoD/CI bajo EAA/PCM); (5) **Conclusiones y trabajo futuro**. Un anexo metodológico recogerá la tabla de solapamiento y el registro del pilot de la celda aguda.
<!-- /paper:section -->

## II. Metodología

La revisión siguió las directrices de Kitchenham y Charters (2007) para revisiones sistemáticas de la literatura en Ingeniería de Software. Un marco de búsqueda estructuró las preguntas y la estrategia de búsqueda, y la guía *Preferred Reporting Items for Systematic Reviews and Meta-Analyses* (PRISMA) 2020 organizó y documentó la selección de los estudios (Page et al., 2021).

<!-- paper:section id=marco-pico -->
### A. Pregunta PICOC y sus componentes

Se adoptó el marco de población, intervención, comparación, resultado y contexto (PICOC). Kitchenham y Charters (2007, p. 11) lo recomiendan para estructurar las preguntas de una revisión en Ingeniería de Software: amplía la pregunta clínica de población, intervención y resultado con la comparación, que fija frente a qué se contrasta la intervención, y con el contexto, que indica dónde se aplica. Ambos componentes son centrales en este tema. La comparación recoge el contraste entre la accesibilidad cognitiva y la accesibilidad sensorial o la conformidad normativa, y el contexto sitúa la inteligencia artificial en las fases del ciclo de vida del software.

Las mismas directrices advierten que en Ingeniería de Software hay menos estudios primarios que en medicina, por lo que conviene no restringir la población antes de tiempo (Kitchenham & Charters, 2007, p. 11). Por eso la población reúne varios perfiles cognitivos y neurodivergentes en lugar de uno solo. La ventana temporal no se trata como un componente del marco: se aplica como criterio de inclusión.

**Tabla I — Marco PICOC**

| P | I | C | O | C |
|---|---|---|---|---|
| Usuarios con discapacidad cognitiva o neurodivergencia: autismo, TDAH, discapacidad intelectual, dificultades de aprendizaje y dislexia | Técnicas de inteligencia artificial, incluidas la GenAI y los LLM | Accesibilidad sensorial o visual y conformidad normativa (WCAG), frente a las que se contrasta la accesibilidad cognitiva | Métricas de evaluación: usabilidad, experiencia de usuario, legibilidad, carga cognitiva y calidad de software | Ciclo de vida del software: requisitos, diseño, implementación, personalización en tiempo de ejecución, pruebas, verificación y validación, y auditoría |

**Pregunta general de investigación:**

> ¿Cómo se han integrado técnicas de inteligencia artificial en las fases del ciclo de vida del software —con énfasis en diseño, personalización en runtime y, sobre todo, verificación, evaluación y auditoría— orientadas a usuarios con discapacidad cognitiva o neurodivergencia; qué métricas se reportan (incluidas orientaciones COGA frente al núcleo WCAG); y qué celdas de la matriz *condición × técnica × fase SE × métrica* permanecen vacías frente al sesgo documentado hacia la accesibilidad sensorial/visual y frente a revisiones HCI/AT o GenAI+web que no estructuran el proceso de Ingeniería de Software?

**Tabla II — Preguntas de investigación por componente**

| Componente | Código | Pregunta |
|---|---|---|
| P | RQ1 | ¿Qué perfiles de discapacidad cognitiva o neurodivergencia (trastorno del espectro autista [TEA], trastorno por déficit de atención e hiperactividad [TDAH], discapacidad intelectual, dificultades de aprendizaje y dislexia) abordan los estudios y con qué grado de estratificación y participación de usuarios? |
| I | RQ2 | ¿Qué técnicas de inteligencia artificial —incluidas la inteligencia artificial generativa (GenAI) y los modelos de lenguaje grandes (LLM)— se han aplicado y con qué rol en el proceso de software? |
| C | RQ3 | ¿En qué medida la evidencia sobre accesibilidad cognitiva se contrasta con, o queda subordinada a, la accesibilidad sensorial o visual y la conformidad con las Pautas de Accesibilidad para el Contenido Web (WCAG)? |
| O | RQ4 | ¿Qué métricas de evaluación se reportan (usabilidad, accesibilidad cognitiva, legibilidad, calidad de software) y con qué grado de automatización? |
| C | RQ5 | ¿En qué fases del ciclo de vida del software (requisitos, diseño, personalización en tiempo de ejecución, pruebas, verificación y validación, y auditoría) se integra la inteligencia artificial y qué peso relativo tienen la verificación y la evaluación? |
<!-- /paper:section -->

<!-- paper:section id=palabras-clave -->
### B. Palabras clave pertinentes

Las palabras clave de cada componente combinan descriptores del tesauro del Institute of Electrical and Electronics Engineers (IEEE), en cursiva, con términos libres para los conceptos que el tesauro no recoge, como la neurodiversidad, la accesibilidad cognitiva o los modelos de lenguaje grandes.

**Tabla III — Palabras clave para la revisión sistemática**

| Componente | Palabras clave (ES) | Keywords (EN) |
|---|---|---|
| P | trastorno del espectro autista, persona autista, neurodiversidad y neurodivergencia, trastornos del neurodesarrollo, discapacidad cognitiva, discapacidad intelectual, dificultades de aprendizaje, TDAH, dislexia, accesibilidad cognitiva | *Autism*, autistic, neurodiversity, neurodivergence, neurodevelopmental, developmental disability, cognitive disability, intellectual disability, learning disability, ADHD, attention deficit, dyslexia, cognitive accessibility |
| I | inteligencia artificial, aprendizaje automático, aprendizaje profundo, procesamiento de lenguaje natural, modelos de lenguaje grandes, inteligencia artificial generativa | *Artificial intelligence*, *Machine learning*, *Deep learning*, *Natural language processing*, large language models, LLM, generative AI, ChatGPT |
| C | ceguera, sordera, discapacidad visual y auditiva, lector de pantalla, accesibilidad y pautas WCAG | *Blindness*, *Deafness*, visual impairment, visually impaired, low vision, hearing impairment, deaf, sensory impairment, screen reader, accessibility, WCAG, Web Content Accessibility Guidelines |
| O | usabilidad, métricas, métricas de legibilidad, calidad de software, experiencia de usuario, métricas de accesibilidad, lenguaje claro y lectura fácil, carga cognitiva | *Usability*, *Measurement*, *Readability metrics*, *Software quality*, user experience, accessibility metric, plain language, easy-to-read, cognitive load |
| C | ingeniería de software, ingeniería de requisitos, diseño de software, pruebas de software, pruebas automáticas, validación de sistemas, ciclo de vida del software, requisitos de accesibilidad, interfaces adaptativas y personalización en tiempo de ejecución, generación de código, pruebas automatizadas, verificación y validación, evaluación, pruebas y auditoría de accesibilidad | *Software engineering*, *Requirements engineering*, *Software design*, *Software testing*, *Automatic testing*, *System validation*, software development life cycle, software development, web development, app development, accessibility requirement, adaptive user interface, runtime personalization, runtime adaptation, code generation, automated testing, verification and validation, accessibility evaluation, accessibility testing, accessibility audit |
<!-- /paper:section -->

<!-- paper:section id=ecuacion-busqueda -->
### C. Ecuación de búsqueda

La búsqueda se hizo en Scopus y Web of Science con una ecuación de cinco bloques, uno por componente del marco. Dentro de cada bloque los términos se unen con OR y los bloques se combinan con AND, de modo que cada registro recuperado debe tocar los cinco componentes. En Scopus se buscó en el título, el resumen y las palabras clave; en Web of Science, en todos los campos. La ventana temporal, el tipo de documento y el idioma no se fijaron en la ecuación: se aplicaron durante la selección como criterios de inclusión.

**Scopus**

```text
TITLE-ABS-KEY (
  ( autism OR autistic OR "autism spectrum" OR neurodivers* OR neurodivergen* OR neurodevelopmental
    OR "cognitive disabilit*" OR "intellectual disabilit*" OR "developmental disabilit*"
    OR "learning disabilit*" OR ADHD OR "attention deficit" OR dyslexi* OR "cognitive accessibility" )
  AND
  ( "artificial intelligence" OR AI OR "machine learning" OR "machine-learning" OR "deep learning"
    OR "natural language processing" OR NLP OR "large language model*" OR LLM OR LLMs
    OR "generative AI" OR "generative artificial intelligence" OR ChatGPT )
  AND
  ( blindness OR deafness OR deaf OR "visual impairment" OR "visually impaired" OR "low vision"
    OR "hearing impairment" OR "hearing impaired" OR "sensory impairment" OR "screen reader"
    OR WCAG OR "Web Content Accessibility Guidelines" OR accessibility )
  AND
  ( usability OR "user experience" OR measurement OR metric OR metrics OR "accessibility metric"
    OR "readability metrics" OR readability OR "plain language" OR "easy-to-read"
    OR "software quality" OR "cognitive load" )
  AND
  ( "software engineering" OR "software development" OR "software development life cycle" OR SDLC
    OR "web development" OR "app development" OR "requirements engineering" OR "accessibility requirement"
    OR "software design" OR "adaptive user interface" OR "runtime personalization" OR "runtime adaptation"
    OR "code generation" OR "software testing" OR "automatic testing" OR "automated testing"
    OR "verification and validation" OR "system validation" OR "accessibility evaluation"
    OR "accessibility testing" OR "accessibility audit" )
)
```

**Web of Science**

```text
ALL=(autism OR autistic OR "autism spectrum" OR neurodivers* OR neurodivergen* OR neurodevelopmental
  OR "cognitive disabilit*" OR "intellectual disabilit*" OR "developmental disabilit*"
  OR "learning disabilit*" OR ADHD OR "attention deficit" OR dyslexi* OR "cognitive accessibility")
AND ALL=("artificial intelligence" OR AI OR "machine learning" OR "machine-learning" OR "deep learning"
  OR "natural language processing" OR NLP OR "large language model*" OR LLM OR LLMs
  OR "generative AI" OR "generative artificial intelligence" OR ChatGPT)
AND ALL=(blindness OR deafness OR deaf OR "visual impairment" OR "visually impaired" OR "low vision"
  OR "hearing impairment" OR "hearing impaired" OR "sensory impairment" OR "screen reader"
  OR WCAG OR "Web Content Accessibility Guidelines" OR accessibility)
AND ALL=(usability OR "user experience" OR measurement OR metric OR metrics OR "accessibility metric"
  OR "readability metrics" OR readability OR "plain language" OR "easy-to-read"
  OR "software quality" OR "cognitive load")
AND ALL=("software engineering" OR "software development" OR "software development life cycle" OR SDLC
  OR "web development" OR "app development" OR "requirements engineering" OR "accessibility requirement"
  OR "software design" OR "adaptive user interface" OR "runtime personalization" OR "runtime adaptation"
  OR "code generation" OR "software testing" OR "automatic testing" OR "automated testing"
  OR "verification and validation" OR "system validation" OR "accessibility evaluation"
  OR "accessibility testing" OR "accessibility audit")
```

La búsqueda se realizó el X en Scopus y Web of Science y recuperó X registros (Scopus: X; Web of Science: X).
<!-- /paper:section -->

<!-- paper:section id=criterios-seleccion -->
### D. Criterios de inclusión y exclusión

**Criterios de inclusión:**

- **CI1:** Estudios publicados entre 2020 y 2026, periodo que abarca la adopción masiva de la inteligencia artificial generativa (2023).
- **CI2:** Artículos de revista o de congreso revisados por pares, incluidas las actas publicadas como capítulos de libro, en inglés o español.
- **CI3:** Estudios dirigidos a personas con discapacidad cognitiva o neurodivergencia: TEA, TDAH, discapacidad intelectual, dislexia o dificultades de aprendizaje.
- **CI4:** Estudios en los que una técnica de inteligencia artificial identificada interviene en el software o en su proceso de desarrollo.
- **CI5:** Estudios que aplican esa técnica en requisitos, diseño, desarrollo, personalización en tiempo de ejecución, pruebas, verificación y validación o auditoría.
- **CI6:** Estudios con una evaluación empírica que reporta al menos una métrica o instrumento de evaluación.

**Criterios de exclusión:**

- **CE1:** Registros duplicados entre bases de datos o sin texto completo accesible.
- **CE2:** Revisiones sistemáticas y otros estudios secundarios; se usan solo para delimitar el vacío.
- **CE3:** Preprints, tesis, editoriales y resúmenes de congreso.
- **CE4:** Robots sociales, tutores inteligentes, cribado clínico o tecnología de rehabilitación como producto principal, sin una fase del ciclo de vida del software.
<!-- /paper:section -->

<!-- paper:section id=seleccion-prisma -->
### E. Proceso de selección — Diagrama PRISMA

La selección de estudios siguió la guía PRISMA 2020, que consta de una lista de verificación de 27 ítems y de un diagrama de flujo que registra cuántos registros entran y salen en cada etapa (Page et al., 2021, p. 1). Se eligió porque hace auditable y reproducible el paso de los registros recuperados a los estudios incluidos. Esa trazabilidad es necesaria en este tema, donde la revisión debe demostrar qué combinaciones carecen de evidencia y no solo cuáles la tienen. El proceso siguió estas etapas:

1. Registros identificados en Scopus (n = X) y en Web of Science (n = X).
2. Duplicados eliminados (n = X).
3. Excluidos por fecha de publicación (n = X).
4. Registros cribados por título y resumen (n = X); excluidos (n = X).
5. Informes buscados para su recuperación (n = X); no recuperados (n = X).
6. Informes evaluados a texto completo (n = X); excluidos según los criterios de exclusión (n = X).
7. Estudios incluidos en la revisión (n = X).

[[ AGREGAR DIAGRAMA ]]

*Fig. 1. Diagrama de flujo PRISMA 2020 del proceso de selección.*
<!-- /paper:section -->

<!-- paper:section id=referencias -->
## Referencias

Aljedaani, W., & Mollik, R. H. (2026). Large language models for web accessibility: A systematic literature review. In *Proceedings of the 23rd International Web for All Conference (W4A ’26)* (pp. 160–171). Association for Computing Machinery. https://doi.org/10.1145/3800424.3800452

Bi, T., Xia, X., Lo, D., Grundy, J., Zimmermann, T., & Ford, D. (2022). Accessibility in software practice: A practitioner’s perspective. *ACM Transactions on Software Engineering and Methodology, 31*(4), 1–26. https://doi.org/10.1145/3503508

Chemnad, K., & Othman, A. (2024). Digital accessibility in the era of artificial intelligence—Bibliometric analysis and systematic review. *Frontiers in Artificial Intelligence, 7*, Article 1349668. https://doi.org/10.3389/frai.2024.1349668

Kitchenham, B., & Charters, S. (2007). *Guidelines for performing systematic literature reviews in software engineering* (EBSE Technical Report EBSE-2007-01, Version 2.3). Keele University; University of Durham. https://www.elsevier.com/__data/promis_misc/525444systematicreviewsguide.pdf

Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., Shamseer, L., Tetzlaff, J. M., Akl, E. A., Brennan, S. E., Chou, R., Glanville, J., Grimshaw, J. M., Hróbjartsson, A., Lalu, M. M., Li, T., Loder, E. W., Mayo-Wilson, E., McDonald, S., … Moher, D. (2021). The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. *BMJ, 372*, Article n71. https://doi.org/10.1136/bmj.n71

Paiva, D. M. B., Freire, A. P., & de Mattos Fortes, R. P. (2021). Accessibility and software engineering processes: A systematic literature review. *Journal of Systems and Software, 171*, Article 110819. https://doi.org/10.1016/j.jss.2020.110819

Perry, N., Sun, C., Munro, M., Boulton, K. A., & Guastella, A. J. (2024). AI technology to support adaptive functioning in neurodevelopmental conditions in everyday environments: A systematic review. *npj Digital Medicine, 7*, Article 370. https://doi.org/10.1038/s41746-024-01355-7

World Wide Web Consortium. (2023). *Web Content Accessibility Guidelines (WCAG) 2.2* (W3C Recommendation). https://www.w3.org/TR/WCAG22/

Xu, Z., Liu, F., Xia, G., Duan, Y., & Yu, L. (2025). A scoping review of inclusive and adaptive human–AI interaction design for neurodivergent users. *Disability and Rehabilitation: Assistive Technology, 21*(4), 943–961. https://doi.org/10.1080/17483107.2025.2579822
<!-- /paper:section -->
