<!-- paper:section id=encabezado -->

# Inteligencia artificial en el ciclo de vida del software para accesibilidad cognitiva y neurodivergencia: técnicas, fases de ingeniería y métricas de evaluación — una revisión sistemática de la literatura

**Tema.** IA (incluidos GenAI/LLM) en el ciclo de vida del software para accesibilidad cognitiva y neurodivergencia, con énfasis en V&V/auditoría y taxonomía condición × técnica × fase SE × métrica (COGA frente a WCAG).

**Problemática.** ¿Cómo se ha integrado la inteligencia artificial en el ciclo de vida del software, del diseño y la personalización a la verificación, la evaluación y la auditoría, para usuarios con discapacidad cognitiva o neurodivergencia; qué métricas se reportan, incluidas las orientaciones COGA frente a las WCAG; y qué combinaciones de condición, técnica, fase y métrica carecen de evidencia frente al predominio de la accesibilidad sensorial?

**Objetivo.** Sintetizar evidencia primaria de IA en artefactos y procesos SE para perfiles cognitivos o neurodivergentes, y producir esa taxonomía con columna de transferibilidad (automatizable en CI / juicio experto / validación con usuarios), delimitada frente a fronteras clínicas, HCI y GenAI+web WCAG-duro.

<!-- /paper:section -->

## I. Introducción

<!-- paper:section id=contexto -->

### Contexto

La accesibilidad digital busca que las personas puedan percibir, operar y comprender el software. Las Pautas de Accesibilidad para el Contenido Web (WCAG) 2.2 concentran la conformidad verificable (World Wide Web Consortium [W3C], 2023). Las orientaciones del W3C sobre accesibilidad cognitiva y del aprendizaje (COGA), en cambio, atienden la comprensión, la memoria y la carga cognitiva (W3C, 2021), que suelen ser más difíciles de verificar de forma automática.

Por _accesibilidad cognitiva_ se entiende aquí la reducción de las barreras en esos tres planos. La _neurodivergencia_ se trata como una categoría amplia que, cuando la evidencia lo permite, se desglosa en condiciones como el trastorno del espectro autista, el trastorno por déficit de atención e hiperactividad o la dislexia, sin medicalizar a las personas. El objeto de la revisión no es la tecnología asistiva clínica. Es el modo en que la inteligencia artificial (IA), incluida la IA generativa (GenAI), se inserta en el ciclo de vida del software, desde los requisitos hasta la verificación y validación (V&V).

Las revisiones previas rodean ese objeto sin cubrirlo. Chemnad y Othman (2024) documentaron, en 43 estudios de IA y accesibilidad digital, el predominio de la discapacidad visual y un vacío en el autismo. Perry et al. (2024) sintetizaron 15 trabajos de IA para el funcionamiento adaptativo en condiciones del neurodesarrollo, con resultados de apoyo cotidiano y no de ingeniería. En 33 estudios con modelos de lenguaje para la accesibilidad web, Aljedaani y Mollik (2026) hallaron que dominan las WCAG y que las orientaciones COGA reciben poca atención, sin ordenar la evidencia por fase del ciclo de vida. En los bordes, Xu et al. (2026) cartografiaron el diseño de la interacción entre personas neurodivergentes y sistemas de IA. Paiva et al. (2021) revisaron la accesibilidad en los procesos de la Ingeniería de Software, sin centrarse en la IA ni en la dimensión cognitiva.

El estado del arte deja así tres tensiones abiertas: lo sensorial frente a lo cognitivo, el enfoque clínico o de interacción frente al proceso de ingeniería, y la automatización frente a la validación con usuarios. La última tiene consecuencias prácticas. Si la integración continua y la _Definition of Done_ (los criterios para dar por terminado un incremento) se limitan a comprobaciones WCAG automáticas, un análisis sin fallos no demuestra que el software sea inclusivo en el plano cognitivo.

<!-- /paper:section -->

<!-- paper:section id=problema -->

### El problema

De esas tensiones nace la pregunta general de esta revisión:

> ¿Cómo se ha integrado la inteligencia artificial en el ciclo de vida del software, del diseño y la personalización a la verificación, la evaluación y la auditoría, para usuarios con discapacidad cognitiva o neurodivergencia; qué métricas se reportan, incluidas las orientaciones COGA frente a las WCAG; y qué combinaciones de condición, técnica, fase y métrica carecen de evidencia frente al predominio de la accesibilidad sensorial?

Lo que falta no son estudios sobre el tema, sino una revisión que los reúna y los ordene. Cada revisión citada cubre solo alguna de cuatro dimensiones: la condición de los usuarios, la técnica de IA, la fase del ciclo de vida o la métrica de evaluación. Ninguna las cruza para responder, por ejemplo, qué técnica se ha usado en la fase de pruebas para evaluar la comprensión de lectura de usuarios con dislexia y con qué métrica. En este artículo, esa clasificación en cuatro dimensiones se denomina _la taxonomía_. Sin ella, un equipo de desarrollo no sabe qué parte de la accesibilidad cognitiva puede comprobar con herramientas automáticas y qué parte exige probar el software con personas. El riesgo es dar por accesible un producto que solo supera las comprobaciones automáticas.

<!-- /paper:section -->

<!-- paper:section id=justificacion -->

### Justificación

Por ello, esta revisión sistemática de la literatura (RSL) articula tres elementos: las orientaciones COGA, la IA en el ciclo de vida del software y las métricas de Ingeniería de Software. El tema tiene además respaldo normativo: la Ley N.º 29973, Ley General de la Persona con Discapacidad (Congreso de la República del Perú, 2012), reconoce derechos de accesibilidad que alcanzan a las personas con discapacidad cognitiva e intelectual. No se pretende certificar ese cumplimiento.

Para orientar la práctica, la revisión asigna a cada hallazgo uno de tres niveles: comprobable de forma automática en la integración continua, sujeto al juicio de un especialista en accesibilidad o validable solo con personas con discapacidad cognitiva o neurodivergentes. Si la combinación que se prevé menos estudiada, la V&V asistida por GenAI con criterios cognitivos, reuniera pocos estudios primarios, el aporte legítimo sería documentar ese vacío, no forzar conclusiones.

<!-- /paper:section -->

<!-- paper:section id=objetivo-rsl -->

### Objetivo de la RSL

El objetivo general es sintetizar la evidencia primaria sobre técnicas de IA aplicadas a los procesos de Ingeniería de Software cuyo producto se dirige a personas con discapacidad cognitiva o neurodivergentes. La síntesis se ordena en la taxonomía para identificar las combinaciones sin evidencia. La pregunta general (sección II.A) se desglosa en cuatro preguntas de investigación (RQ), una por componente del marco, y cada una fija un objetivo específico:

1. Caracterizar los perfiles cognitivos y neurodivergentes estudiados, su grado de estratificación y la participación de esas personas, desde sujetos de evaluación hasta codiseño.
2. Identificar las técnicas de IA, incluidas la GenAI y los modelos de lenguaje grandes (LLM), su papel y la fase del ciclo de vida en que intervienen.
3. Determinar en qué medida la evidencia sobre accesibilidad cognitiva se contrasta con la accesibilidad sensorial o visual y la conformidad con las WCAG, o queda subordinada a ellas.
4. Inventariar las métricas de evaluación y clasificarlas según los tres niveles de automatización.

Por tratarse de esta población, el protocolo fija salvaguardas éticas. La selección excluye los estudios de solo diagnóstico y los productos ajenos al ciclo de vida del software (criterios CE5 y CE8, sección II.D). La extracción registra si cada estudio trata la condición como un déficit o como una diferencia, si el sistema la deduce o almacena, si hubo consentimiento o asentimiento informado y en qué país se realizó. Estos datos se reportan con la RQ1 para exponer vacíos éticos y un posible sesgo geográfico. Los rótulos diagnósticos se reproducen tal como los declara cada estudio, y las métricas de ingeniería no se interpretan como resultados clínicos.

<!-- /paper:section -->

<!-- paper:section id=organizacion -->

### Organización del contenido de la revisión

El resto del artículo presenta el método, cuyo reporte sigue la guía _Preferred Reporting Items for Systematic Reviews and Meta-Analyses_ (PRISMA) 2020 (Page et al., 2021), y después los resultados ordenados según la taxonomía. La discusión examina qué hallazgos pueden trasladarse a la práctica de desarrollo antes de las conclusiones.

<!-- /paper:section -->

## II. Metodología

Esta revisión siguió las directrices de Kitchenham y Charters (2007) para revisiones sistemáticas en Ingeniería de Software, que reúnen en un protocolo previo las decisiones sobre la pregunta, la búsqueda y la selección. Fijarlas antes de conocer los resultados evita que las expectativas del investigador orienten la selección y permite que otros repitan el procedimiento (Kitchenham & Charters, 2007, pp. vi, 12). Los apartados siguientes recorren ese protocolo en su orden: la pregunta y sus componentes, las palabras clave, las ecuaciones de búsqueda, los criterios y el proceso de selección.

<!-- paper:section id=marco-pico -->

### A. Pregunta PICO y sus componentes

La primera decisión atañe a la forma de la pregunta. Esta revisión no se limita a saber si la IA mejora la accesibilidad: necesita contrastar la accesibilidad cognitiva con la sensorial. Las guías médicas plantean la pregunta desde la población, la intervención y el resultado, sin un componente propio para ese contraste. Kitchenham y Charters (2007, pp. 10–11) recogen la propuesta de Petticrew y Roberts, que amplía ese esquema con la comparación y el contexto. De ahí se adoptó el marco de población, intervención, comparación y resultado (PICO), en el que la comparación recoge el contraste con la accesibilidad sensorial y la conformidad con las WCAG. El contexto, que aquí serían las fases del ciclo de vida, no se incluyó como componente. Exigirlo en la búsqueda habría dejado fuera los estudios que no nombran la fase en el resumen; por eso la fase se verifica en la selección y se extrae para la RQ2.

Concretar sus componentes exigió, además, dos decisiones de alcance. Como el marco no incluye un componente temporal, la ventana de 2021 a 2026 se aplica como criterio de inclusión y como filtro de la búsqueda, y no como parte de la pregunta. La población, por su parte, reúne varios perfiles en lugar de uno solo: el trastorno del espectro autista, el trastorno por déficit de atención e hiperactividad (TDAH), la discapacidad intelectual, las dificultades de aprendizaje y la dislexia. Kitchenham y Charters (2007, p. 11) advierten que en Ingeniería de Software hay pocos estudios primarios, por lo que restringir pronto la población puede dejar la revisión sin evidencia. El mismo riesgo existe aquí, de modo que la distinción entre perfiles se hace después, en la extracción de datos de la RQ1.

Con esas decisiones, el marco queda resumido en la Tabla I. De sus cuatro componentes y de la fase del ciclo de vida se deriva la pregunta general, que se reproduce tal como quedó registrada en el protocolo. En ella, la taxonomía aparece como una matriz de condición, técnica, fase y métrica, y se emplean tres siglas del área: Ingeniería de Software (SE), interacción persona-computadora (HCI) y tecnología asistiva (AT). Por último, cada componente origina una de las preguntas de investigación (Tabla II).

**Tabla I — Marco PICO**

| P                                                                                                                                                                                   | I                                                                 | C                                                                                                                         | O                                                                                                                                                           |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Usuarios con discapacidad cognitiva o neurodivergencia: autismo, TDAH, discapacidad intelectual, dificultades de aprendizaje, dislexia, disgrafía y discalculia | Técnicas de inteligencia artificial, incluidas la GenAI y los LLM | Accesibilidad sensorial o visual y conformidad normativa (WCAG), frente a las que se contrasta la accesibilidad cognitiva | Métricas de evaluación: usabilidad, experiencia de usuario, legibilidad, comprensión, carga cognitiva, ergonomía, aceptación, evaluación de la accesibilidad y calidad de software |

**Pregunta general de investigación:**

> ¿Cómo se ha integrado la inteligencia artificial en el ciclo de vida del software, del diseño y la personalización a la verificación, la evaluación y la auditoría, para usuarios con discapacidad cognitiva o neurodivergencia; qué métricas se reportan, incluidas las orientaciones COGA frente a las WCAG; y qué combinaciones de condición, técnica, fase y métrica carecen de evidencia frente al predominio de la accesibilidad sensorial?

**Tabla II — Preguntas de investigación por componente**

| Componente | Código | Pregunta                                                                                                                                                                                                                                                                                                            |
| ---------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| P          | RQ1    | ¿Qué perfiles de discapacidad cognitiva o neurodivergencia (trastorno del espectro autista [TEA], trastorno por déficit de atención e hiperactividad [TDAH], discapacidad intelectual, dificultades de aprendizaje y dislexia) abordan los estudios y con qué grado de estratificación y participación de usuarios? |
| I          | RQ2    | ¿Qué técnicas de inteligencia artificial —incluidas la inteligencia artificial generativa (GenAI) y los modelos de lenguaje grandes (LLM)— se han aplicado, con qué rol y en qué fase del ciclo de vida del software?                                                                                               |
| C          | RQ3    | ¿En qué medida la evidencia sobre accesibilidad cognitiva se contrasta con, o queda subordinada a, la accesibilidad sensorial o visual y la conformidad con las Pautas de Accesibilidad para el Contenido Web (WCAG)?                                                                                               |
| O          | RQ4    | ¿Qué métricas de evaluación se reportan (usabilidad, experiencia de usuario, legibilidad, carga cognitiva, calidad de software y accesibilidad cognitiva) y con qué grado de automatización?                                                                                                                        |

<!-- /paper:section -->

<!-- paper:section id=palabras-clave -->

### B. Palabras clave pertinentes

Una vez fijados los componentes, cada uno se tradujo en un conjunto de palabras clave en español y en inglés (Tabla III); la búsqueda se ejecutó con los términos en inglés. Para usar términos de indexación controlados (Kitchenham & Charters, 2007, p. 14), se priorizaron los descriptores del IEEE Thesaurus (Institute of Electrical and Electronics Engineers [IEEE], 2019). Donde el tesauro no ofrece un descriptor, como ocurre con casi todos los perfiles de la población, la accesibilidad o los modelos de lenguaje, se añadieron términos libres.

**Tabla III — Palabras clave para la revisión sistemática**

| Componente | Palabras clave (ES)                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Keywords (EN)                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| P          | autismo, autista, espectro autista, neurodiversidad, neurodivergencia, del neurodesarrollo, discapacidad cognitiva, discapacidad intelectual, discapacidad del desarrollo, dificultades de aprendizaje, TDAH, déficit de atención, dislexia, accesibilidad cognitiva, síndrome de Asperger, trastorno del desarrollo intelectual, trastornos del aprendizaje, dificultades del aprendizaje, discalculia, disgrafía, dificultades lectoras | _autism_, autistic, "autism spectrum", neurodivers\*, neurodivergen\*, neurodevelopmental, "cognitive disabilit\*", "intellectual disabilit\*", "developmental disabilit\*", "learning disabilit\*", ADHD, "attention deficit", dyslexi\*, "cognitive accessibility", Asperger, "intellectual developmental disorder", "learning disorder\*", "learning difficult\*", dyscalculia, dysgraphia, "reading disabilit\*" |
| I          | inteligencia artificial, IA, aprendizaje automático, procesamiento de lenguaje natural, PLN, modelo de lenguaje, LLM, LLM (plural), IA generativa, inteligencia artificial generativa, ChatGPT, GPT, ingeniería de instrucciones, visión por computador, chatbot, agentes conversacionales, agentes inteligentes, agente virtual, simplificación automática de textos, simplificación léxica, adaptación de textos, procesamiento de textos, análisis de textos, minería de textos, lingüística computacional, interfaz de usuario adaptativa, reconocimiento de voz, sistemas de recomendación, generación de lenguaje natural, redes generativas antagónicas, lógica difusa, inferencia difusa, inteligencia ambiental, computación sensible al contexto, sensible al contexto, aprendizaje por refuerzo, aprendizaje contrastivo | _"artificial intelligence"_, AI, _"machine learning"_, _"natural language processing"_, NLP, "language model", LLM, LLMs, "generative AI", "generative artificial intelligence", ChatGPT, GPT, "prompt engineering", _"computer vision"_, chatbot, "conversational agents", _"intelligent agents"_, "virtual agent", "text simplification", "lexical simplification", "text adaptation", "text processing", _"text analysis"_, _"text mining"_, _"computational linguistics"_, "adaptive user interface", _"speech recognition"_, _"recommender systems"_, "natural language generation", _"generative adversarial networks"_, _"fuzzy logic"_, "fuzzy inference", _"ambient intelligence"_, _"context awareness"_, "context-aware", _"reinforcement learning"_, "contrastive learning" |
| C          | ceguera, sordera, persona sorda, discapacidad visual, persona con discapacidad visual, baja visión, discapacidad auditiva, persona con discapacidad auditiva, discapacidad sensorial, lector de pantalla, WCAG, Pautas de Accesibilidad para el Contenido Web, accesibilidad, diseño accesible, interfaz accesible, diseño inclusivo, diseño universal, inclusión digital | _blindness_, _deafness_, deaf, "visual impairment", "visually impaired", "low vision", "hearing impairment", "hearing impaired", "sensory impairment", "screen reader", WCAG, "Web Content Accessibility Guidelines", accessibility, "accessible design", "accessible interface", "inclusive design", "universal design", "digital inclusion" |
| O          | usabilidad, experiencia de usuario, métrica, métricas, métrica de accesibilidad, métricas de legibilidad, legibilidad, lenguaje claro, lectura fácil, lectura fácil (variante sin guiones), calidad de software, carga cognitiva, evaluación de la accesibilidad, pruebas de accesibilidad, estudio con usuarios, comprensión, comprensibilidad, satisfacción del usuario, auditoría de accesibilidad, valoración de la accesibilidad, ergonomía, ingeniería humana, aceptación del usuario, evaluación humana | _usability_, "user experience", metric, metrics, "accessibility metric", _"readability metrics"_, readability, "plain language", "easy-to-read", "easy read", _"software quality"_, "cognitive load", "accessibility evaluation", "accessibility testing", "user study", comprehension, understandability, "user satisfaction", "accessibility audit", "accessibility assessment", _ergonomics_, "human engineering", "user acceptance", "human evaluation" |

_Nota._ En cursiva, descriptores del IEEE Thesaurus (IEEE, 2019). Los demás son términos libres; los de informática se contrastaron con la ACM Computing Classification System (Association for Computing Machinery [ACM], 2012) y los perfiles clínicos con los Medical Subject Headings (National Library of Medicine [NLM], 2026).

<!-- /paper:section -->

<!-- paper:section id=ecuacion-busqueda -->

### C. Ecuación de búsqueda

Con esas palabras clave se construyó una ecuación de búsqueda para Scopus y otra para Web of Science, ambas con cuatro bloques, uno por componente del marco. Los términos de un mismo bloque se unen con OR y los bloques se combinan con AND, de modo que cada registro debe responder a todos los componentes. Esa exigencia obligó a cuidar el bloque de comparación, que incluye el término general _accessibility_ para no excluir los estudios centrados solo en lo cognitivo. En consecuencia, el contraste con la accesibilidad sensorial que plantea la RQ3 no se exige en la búsqueda, sino que se analiza en la extracción de datos.

Como exigir los cuatro bloques ya restringe la recuperación, los campos se eligieron amplios: en Scopus, el título, el resumen y las palabras clave; en Web of Science, todos los campos. Los registros no pertinentes que esa amplitud añade se descartan en el cribado. Los límites de los criterios de inclusión, en cambio, van dentro de las ecuaciones: el periodo, el tipo de documento, el idioma y, en Scopus, el acceso abierto. En Web of Science, sin etiqueta de campo para ello, el acceso abierto se aplica con el filtro de la interfaz (Tabla IV). Así, la búsqueda queda documentada y otros pueden repetirla (Kitchenham & Charters, 2007, p. 16).

Kitchenham y Charters (2007, p. 14) recomiendan probar la ecuación con estudios ya conocidos. Como primer contraste, los términos se compararon con las tres revisiones sistemáticas del tema. Ninguna reúne los cuatro componentes en su título, resumen y palabras clave, y a dos de ellas las deja fuera un solo bloque, el de comparación o el de resultado. Por ello, falta probar la ecuación con un conjunto de control de [[n]] estudios primarios tomados de las referencias de esas revisiones, de los que deberá recuperar [[n]].

**Scopus**

```text
TITLE-ABS-KEY (
  ( autism OR autistic OR "autism spectrum" OR neurodivers* OR neurodivergen*
    OR neurodevelopmental OR "cognitive disabilit*" OR "intellectual disabilit*"
    OR "developmental disabilit*" OR "learning disabilit*" OR ADHD OR "attention deficit"
    OR dyslexi* OR "cognitive accessibility" OR Asperger
    OR "intellectual developmental disorder" OR "learning disorder*"
    OR "learning difficult*" OR dyscalculia OR dysgraphia OR "reading disabilit*" )
  AND
  ( "artificial intelligence" OR AI OR "machine learning" OR "natural language processing"
    OR NLP OR "language model" OR LLM OR LLMs OR "generative AI"
    OR "generative artificial intelligence" OR ChatGPT OR GPT OR "prompt engineering"
    OR "computer vision" OR chatbot OR "conversational agents" OR "intelligent agents"
    OR "virtual agent" OR "text simplification" OR "lexical simplification"
    OR "text adaptation" OR "text processing" OR "text analysis" OR "text mining"
    OR "computational linguistics" OR "adaptive user interface" OR "speech recognition"
    OR "recommender systems" OR "natural language generation"
    OR "generative adversarial networks" OR "fuzzy logic" OR "fuzzy inference"
    OR "ambient intelligence" OR "context awareness" OR "context-aware"
    OR "reinforcement learning" OR "contrastive learning" )
  AND
  ( blindness OR deafness OR deaf OR "visual impairment" OR "visually impaired"
    OR "low vision" OR "hearing impairment" OR "hearing impaired" OR "sensory impairment"
    OR "screen reader" OR WCAG OR "Web Content Accessibility Guidelines" OR accessibility
    OR "accessible design" OR "accessible interface" OR "inclusive design"
    OR "universal design" OR "digital inclusion" )
  AND
  ( usability OR "user experience" OR metric OR metrics OR "accessibility metric"
    OR "readability metrics" OR readability OR "plain language" OR "easy-to-read"
    OR "easy read" OR "software quality" OR "cognitive load" OR "accessibility evaluation"
    OR "accessibility testing" OR "user study" OR comprehension OR understandability
    OR "user satisfaction" OR "accessibility audit" OR "accessibility assessment"
    OR ergonomics OR "human engineering" OR "user acceptance" OR "human evaluation" )
)
AND PUBYEAR > 2020 AND PUBYEAR < 2027
AND ( LIMIT-TO ( DOCTYPE , "ar" ) )
AND ( LIMIT-TO ( LANGUAGE , "English" ) OR LIMIT-TO ( LANGUAGE , "Spanish" ) )
AND ( LIMIT-TO ( OA , "all" ) )
```

**Web of Science**

```text
ALL=(autism OR autistic OR "autism spectrum" OR neurodivers* OR neurodivergen*
  OR neurodevelopmental OR "cognitive disabilit*" OR "intellectual disabilit*"
  OR "developmental disabilit*" OR "learning disabilit*" OR ADHD OR "attention deficit"
  OR dyslexi* OR "cognitive accessibility" OR Asperger
  OR "intellectual developmental disorder" OR "learning disorder*" OR "learning difficult*"
  OR dyscalculia OR dysgraphia OR "reading disabilit*")
AND ALL=("artificial intelligence" OR AI OR "machine learning"
  OR "natural language processing" OR NLP OR "language model" OR LLM OR LLMs
  OR "generative AI" OR "generative artificial intelligence" OR ChatGPT OR GPT
  OR "prompt engineering" OR "computer vision" OR chatbot OR "conversational agents"
  OR "intelligent agents" OR "virtual agent" OR "text simplification"
  OR "lexical simplification" OR "text adaptation" OR "text processing" OR "text analysis"
  OR "text mining" OR "computational linguistics" OR "adaptive user interface"
  OR "speech recognition" OR "recommender systems" OR "natural language generation"
  OR "generative adversarial networks" OR "fuzzy logic" OR "fuzzy inference"
  OR "ambient intelligence" OR "context awareness" OR "context-aware"
  OR "reinforcement learning" OR "contrastive learning")
AND ALL=(blindness OR deafness OR deaf OR "visual impairment" OR "visually impaired"
  OR "low vision" OR "hearing impairment" OR "hearing impaired" OR "sensory impairment"
  OR "screen reader" OR WCAG OR "Web Content Accessibility Guidelines" OR accessibility
  OR "accessible design" OR "accessible interface" OR "inclusive design"
  OR "universal design" OR "digital inclusion")
AND ALL=(usability OR "user experience" OR metric OR metrics OR "accessibility metric"
  OR "readability metrics" OR readability OR "plain language" OR "easy-to-read"
  OR "easy read" OR "software quality" OR "cognitive load" OR "accessibility evaluation"
  OR "accessibility testing" OR "user study" OR comprehension OR understandability
  OR "user satisfaction" OR "accessibility audit" OR "accessibility assessment"
  OR ergonomics OR "human engineering" OR "user acceptance" OR "human evaluation")
AND PY=(2021-2026) AND DT=(Article) AND LA=(English OR Spanish)
```

**Tabla IV — Búsqueda por base de datos**

| Base           | Fecha de búsqueda | Años      | Campos                           | Filtros                                                            | Registros                  |
| -------------- | ----------------- | --------- | -------------------------------- | ------------------------------------------------------------------ | -------------------------- |
| Scopus         | X                 | 2021–2026 | Título, resumen y palabras clave | Artículo; inglés o español; acceso abierto                         | n = X (sin filtros: n = X) |
| Web of Science | X                 | 2021–2026 | Todos los campos                 | Artículo; inglés o español; acceso abierto (filtro de la interfaz) | n = X (sin filtros: n = X) |

<!-- /paper:section -->

<!-- paper:section id=criterios-seleccion -->

### D. Criterios de inclusión y exclusión

Los registros recuperados todavía mezclan estudios pertinentes con otros que solo comparten vocabulario con la pregunta. Para separarlos, los criterios de inclusión (CI) y exclusión (CE) se fijaron en el protocolo antes de la búsqueda, como recomiendan Kitchenham y Charters (2007, p. 18). CI1 y CI2 repiten los límites que ya aplican las ecuaciones, y CI3 a CI5 traducen el marco a condiciones verificables: la población, la técnica, la fase del ciclo de vida y una evaluación empírica. Los de exclusión se dividen en formales (CE1 a CE4) y de alcance (CE5 a CE8).

**Criterios de inclusión:**

- **CI1:** Artículos publicados entre 2021 y 2026, los cinco últimos años completos y el año en curso.
- **CI2:** Artículos de revista revisados por pares, de acceso abierto, en inglés o español.
- **CI3:** Estudios dirigidos a personas con autismo, trastorno por déficit de atención e hiperactividad, discapacidad intelectual, dislexia o dificultades de aprendizaje.
- **CI4:** Estudios en los que la inteligencia artificial interviene en una fase del ciclo de vida del software: requisitos, diseño, desarrollo, personalización, pruebas, verificación o auditoría.
- **CI5:** Estudios con una evaluación empírica, con usuarios o automática, que reporta al menos una métrica o instrumento de evaluación.

**Criterios de exclusión:**

- **CE1:** Registros duplicados entre bases de datos.
- **CE2:** Estudios sin texto completo accesible.
- **CE3:** Revisiones sistemáticas y otros estudios secundarios; se usan solo para delimitar el vacío.
- **CE4:** Preprints, tesis, editoriales y trabajos de congreso.
- **CE5:** Estudios en los que la inteligencia artificial solo diagnostica o detecta la condición, sin un artefacto de software evaluado.
- **CE6:** Estudios de accesibilidad solo sensorial, sin población con discapacidad cognitiva o neurodivergencia.
- **CE7:** Intervenciones pedagógicas o de aprendizaje electrónico, como el diseño universal para el aprendizaje o los recomendadores educativos, sin un artefacto de software evaluado.
- **CE8:** Robots sociales, tutores inteligentes o tecnología de rehabilitación como producto principal, que no intervienen en ninguna fase del ciclo de vida del software.
<!-- /paper:section -->

<!-- paper:section id=seleccion-prisma -->

### E. Proceso de selección — Diagrama PRISMA

Aplicar esos criterios a un conjunto amplio de registros exige decisiones sucesivas que deben quedar registradas (Kitchenham & Charters, 2007, pp. 19–20). Esto pesa especialmente en una revisión que busca señalar qué combinaciones carecen de evidencia, porque una ausencia solo es creíble si se sabe qué se buscó y qué se descartó en cada paso. Por esa razón, la selección se documenta según PRISMA 2020 (Page et al., 2021, p. 1), una guía de reporte que combina una lista de 27 ítems con un diagrama de flujo. Ese diagrama muestra cuántos registros entran y salen en cada una de las etapas, que en esta revisión fueron las siguientes:

1. Registros identificados en Scopus (n = X) y en Web of Science (n = X).
2. Duplicados eliminados (n = X).
3. Excluidos por fecha de publicación (n = X).
4. Registros cribados por título y resumen (n = X); excluidos (n = X).
5. Informes buscados para su recuperación (n = X); no recuperados (n = X).
6. Informes evaluados a texto completo (n = X); excluidos por no cumplir un criterio de inclusión o por cumplir uno de exclusión (n = X).
7. Estudios incluidos en la revisión (n = X).

[[AGREGAR DIAGRAMA]]

_Fig. 1. Diagrama de flujo PRISMA 2020 del proceso de selección._

<!-- /paper:section -->

<!-- paper:section id=referencias -->

## Referencias

Aljedaani, W., & Mollik, R. H. (2026). Large language models for web accessibility: A systematic literature review. In _Proceedings of the 23rd International Web for All Conference (W4A ’26)_ (pp. 160–171). Association for Computing Machinery. https://doi.org/10.1145/3800424.3800452

Association for Computing Machinery. (2012). _The 2012 ACM computing classification system_. https://dl.acm.org/pb-assets/dl_ccs/acm_ccs2012-1626988337597.xml

Chemnad, K., & Othman, A. (2024). Digital accessibility in the era of artificial intelligence—Bibliometric analysis and systematic review. _Frontiers in Artificial Intelligence, 7_, Article 1349668. https://doi.org/10.3389/frai.2024.1349668

Congreso de la República del Perú. (2012). _Ley N.º 29973, Ley General de la Persona con Discapacidad_. Diario Oficial El Peruano.

Institute of Electrical and Electronics Engineers. (2019). _2019 IEEE thesaurus_ (Version 1.0). https://www.ieee.org/publications/services/thesaurus-access-page.html

Kitchenham, B., & Charters, S. (2007). _Guidelines for performing systematic literature reviews in software engineering_ (EBSE Technical Report EBSE-2007-01, Version 2.3). Keele University; University of Durham. https://www.elsevier.com/__data/promis_misc/525444systematicreviewsguide.pdf

National Library of Medicine. (2026). _Medical subject headings_ [Base de datos]. https://www.nlm.nih.gov/mesh/meshhome.html

Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., Shamseer, L., Tetzlaff, J. M., Akl, E. A., Brennan, S. E., Chou, R., Glanville, J., Grimshaw, J. M., Hróbjartsson, A., Lalu, M. M., Li, T., Loder, E. W., Mayo-Wilson, E., McDonald, S., . . . Moher, D. (2021). The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. _BMJ, 372_, Article n71. https://doi.org/10.1136/bmj.n71

Paiva, D. M. B., Freire, A. P., & de Mattos Fortes, R. P. (2021). Accessibility and software engineering processes: A systematic literature review. _Journal of Systems and Software, 171_, Article 110819. https://doi.org/10.1016/j.jss.2020.110819

Perry, N., Sun, C., Munro, M., Boulton, K. A., & Guastella, A. J. (2024). AI technology to support adaptive functioning in neurodevelopmental conditions in everyday environments: A systematic review. _npj Digital Medicine, 7_, Article 370. https://doi.org/10.1038/s41746-024-01355-7

World Wide Web Consortium. (2021). _Making content usable for people with cognitive and learning disabilities_ (W3C Working Group Note). https://www.w3.org/TR/coga-usable/

World Wide Web Consortium. (2023). _Web Content Accessibility Guidelines (WCAG) 2.2_ (W3C Recommendation). https://www.w3.org/TR/WCAG22/

Xu, Z., Liu, F., Xia, G., Duan, Y., & Yu, L. (2026). A scoping review of inclusive and adaptive human–AI interaction design for neurodivergent users. _Disability and Rehabilitation: Assistive Technology, 21_(4), 943–961. https://doi.org/10.1080/17483107.2025.2579822

<!-- /paper:section -->
