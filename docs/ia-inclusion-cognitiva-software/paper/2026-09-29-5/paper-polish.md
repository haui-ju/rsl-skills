<!-- paper:section id=encabezado -->
# Inteligencia artificial en el ciclo de vida del software para accesibilidad cognitiva y neurodivergencia: técnicas, fases de ingeniería y métricas de evaluación — una revisión sistemática de la literatura

**Tema.** IA (incluidos GenAI/LLM) en el ciclo de vida del software para accesibilidad cognitiva y neurodivergencia, con énfasis en verificación, validación y auditoría y taxonomía por condición, técnica, fase de ingeniería de software y métrica (COGA frente a WCAG).

**Problemática.** ¿Cómo se ha integrado la inteligencia artificial en el ciclo de vida del software, del diseño y la personalización a la verificación, la evaluación y la auditoría, para usuarios con discapacidad cognitiva o neurodivergencia; qué métricas se reportan, incluidas las orientaciones COGA frente a las WCAG; y qué combinaciones de condición, técnica, fase y métrica carecen de evidencia frente al predominio de la accesibilidad sensorial?

**Objetivo.** Sintetizar la evidencia primaria sobre la inteligencia artificial en los procesos de Ingeniería de Software cuyo producto se dirige a personas con discapacidad cognitiva o neurodivergentes. La síntesis se ordena por condición, técnica, fase y métrica, y distingue lo que se comprueba automáticamente, lo que requiere juicio experto y lo que solo se valida con usuarios.
<!-- /paper:section -->

## I. Introducción

<!-- paper:section id=contexto -->
### Contexto

La accesibilidad digital busca que cualquier persona pueda percibir, operar y comprender el software. Para la conformidad verificable existe una referencia consolidada: las Pautas de Accesibilidad para el Contenido Web (WCAG) 2.2 (World Wide Web Consortium [W3C], 2023). Comprender es otra cosa. Depende de la memoria y de la carga cognitiva que impone cada interfaz, y de ello se ocupan las orientaciones sobre accesibilidad cognitiva y del aprendizaje (COGA) del W3C (2021), más difíciles de verificar de forma automática.

Desde esa diferencia se delimita esta revisión. Por *accesibilidad cognitiva* se entiende la reducción de las barreras de comprensión, memoria y carga. La *neurodivergencia* se trata como una categoría amplia, que se desglosa en condiciones como el autismo, el trastorno por déficit de atención e hiperactividad o la dislexia cuando la evidencia lo permite, sin medicalizar a las personas. Lo que interesa, así, no es la tecnología asistiva clínica, sino cómo la inteligencia artificial (IA), incluida la IA generativa (GenAI), se inserta en el ciclo de vida del software, de los requisitos a la verificación y la validación.

Ese recorte exige situar lo ya sintetizado. Chemnad y Othman (2024) reunieron 43 estudios de IA y accesibilidad digital y encontraron que predomina la discapacidad visual, con un vacío en el autismo. Perry et al. (2024) sí se centraron en las condiciones del neurodesarrollo, pero sus 15 trabajos miden el apoyo en la vida cotidiana, no la ingeniería del software. Más cerca aún, Aljedaani y Mollik (2026) revisaron 33 estudios con modelos de lenguaje para la accesibilidad web: dominan las WCAG, las orientaciones COGA reciben poca atención y la evidencia no se ordena por fase del ciclo de vida. En los bordes, Xu et al. (2026) cartografiaron el diseño de la interacción de personas neurodivergentes con la IA; Paiva et al. (2021), la accesibilidad en los procesos de Ingeniería de Software, sin mirar la IA ni lo cognitivo.

Leídas juntas, estas revisiones dejan tres tensiones abiertas: lo sensorial frente a lo cognitivo, el enfoque clínico o de interacción frente al proceso de ingeniería, y la automatización frente a la validación con usuarios. La última es la que más pesa en la práctica. Si la integración continua y la *Definition of Done*, los criterios con que un equipo da por terminado un incremento, solo ejecutan comprobaciones WCAG automáticas, un escáner «en verde» no garantiza que una persona con discapacidad cognitiva comprenda el software.
<!-- /paper:section -->

<!-- paper:section id=problema -->
### El problema

De esas tensiones nace la pregunta general de esta revisión:

> ¿Cómo se ha integrado la inteligencia artificial en el ciclo de vida del software, del diseño y la personalización a la verificación, la evaluación y la auditoría, para usuarios con discapacidad cognitiva o neurodivergencia; qué métricas se reportan, incluidas las orientaciones COGA frente a las WCAG; y qué combinaciones de condición, técnica, fase y métrica carecen de evidencia frente al predominio de la accesibilidad sensorial?

Responderla exige una síntesis que todavía no existe: no faltan estudios cercanos, sino una revisión que los reúna y los ordene. Cada una de las revisiones citadas mira alguna de cuatro dimensiones, la condición de los usuarios, la técnica de IA, la fase del ciclo de vida o la métrica de evaluación, pero ninguna las cruza. Con ellas no puede saberse, por ejemplo, qué técnica se ha usado en la fase de pruebas para evaluar la comprensión lectora de usuarios con dislexia, ni con qué métrica.

En adelante, ese cruce de cuatro dimensiones se denomina *la taxonomía*. Sin ella, un equipo de desarrollo no puede saber qué se ha probado, con qué perfil y en qué fase, y el escáner en verde acaba confundiéndose con la inclusión.
<!-- /paper:section -->

<!-- paper:section id=justificacion -->
### Justificación

Por eso esta revisión sistemática de la literatura (RSL) articula tres campos que las revisiones previas tratan por separado: las orientaciones COGA, la IA en el ciclo de vida del software y las métricas de la Ingeniería de Software. El tema no es solo académico. En el Perú, la Ley N.º 29973, Ley General de la Persona con Discapacidad (Congreso de la República del Perú, 2012), reconoce derechos de accesibilidad que alcanzan a las personas con discapacidad cognitiva e intelectual.

Para que la síntesis sirva a quien desarrolla software, cada hallazgo se ubicará en uno de tres niveles de automatización. El primero reúne lo que puede comprobarse de forma automática en la integración continua; el segundo, lo que requiere el juicio de un especialista en accesibilidad; el tercero, lo que solo se valida con personas con discapacidad cognitiva o neurodivergentes. Esa utilidad no depende de que abunde la evidencia: si la combinación que se prevé menos estudiada, la verificación y validación asistida por GenAI con criterios cognitivos, reúne pocos estudios primarios, el vacío se reportará como un resultado.
<!-- /paper:section -->

<!-- paper:section id=objetivo-rsl -->
### Objetivo de la RSL

Así planteado, el objetivo general es sintetizar la evidencia primaria sobre técnicas de IA aplicadas a los procesos de Ingeniería de Software cuyo producto se dirige a personas con discapacidad cognitiva o neurodivergentes. Ordenada en la taxonomía, esa síntesis permitirá localizar las combinaciones sin evidencia. La pregunta general se desglosa en tres preguntas de investigación (RQ), una por componente del marco (sección II.A), y de cada una se deriva un objetivo específico:

1. Caracterizar los perfiles cognitivos y neurodivergentes estudiados, su grado de estratificación y la participación de esas personas, desde sujetos de evaluación hasta codiseño.
2. Identificar las técnicas de IA, incluidas la GenAI y los modelos de lenguaje grandes (LLM), su papel y la fase del ciclo de vida en que intervienen.
3. Inventariar las métricas de evaluación y los marcos normativos reportados (incluidas las orientaciones COGA frente a las WCAG), contrastar la evaluación cognitiva con la sensorial y clasificar el grado de automatización de cada métrica.

Trabajar con evidencia sobre esta población exige, además, cuidados que el protocolo fija desde el inicio. La selección excluye los estudios en los que la IA solo diagnostica o detecta la condición (criterio de exclusión CE1, sección II.D). La extracción registra si cada estudio trata la condición como una diferencia o como un déficit, si el sistema la deduce o la almacena, si hubo consentimiento o asentimiento informado y en qué país se realizó. Esos datos se reportan con la RQ1, de modo que queden a la vista los vacíos éticos y un posible sesgo geográfico. Los rótulos diagnósticos se reproducen tal como los declara cada estudio, y las métricas de ingeniería no se leen como resultados clínicos.
<!-- /paper:section -->

<!-- paper:section id=organizacion -->
### Organización del contenido de la revisión

Tras esta introducción, la sección II presenta el método, cuyo reporte se ajusta a la guía *Preferred Reporting Items for Systematic Reviews and Meta-Analyses* (PRISMA) 2020 (Page et al., 2021). Después, los resultados se ordenan según la taxonomía, y la discusión examina qué hallazgos pueden llevarse a la práctica del desarrollo antes de cerrar con las conclusiones.
<!-- /paper:section -->

## II. Metodología

Esta revisión siguió las directrices de Kitchenham y Charters (2007) para revisiones sistemáticas en Ingeniería de Software, que reúnen en un protocolo previo las decisiones sobre la pregunta, la búsqueda y la selección. Fijarlas antes de conocer los resultados evita que las expectativas del investigador orienten la selección y permite que otros repitan el procedimiento (Kitchenham & Charters, 2007, pp. vi, 12). Los apartados siguientes recorren ese protocolo en su orden: la pregunta y sus componentes, las palabras clave, las ecuaciones de búsqueda, los criterios y el proceso de selección.

<!-- paper:section id=marco-pico -->
### A. Pregunta PIO y sus componentes

La primera decisión atañe a la forma de la pregunta. Esta revisión necesita contrastar la accesibilidad cognitiva con la sensorial y con las WCAG, pero también situar la inteligencia artificial en el ciclo de vida del software. Un marco clínico de población, intervención y resultado no reserva un lugar explícito para ese contraste ni para las métricas de ingeniería; por eso se adoptó el esquema de población, intervención y resultado (PIO) de Petticrew y Roberts, recomendado en Ingeniería de Software por Kitchenham y Charters (2007, pp. 10–11). La ventana 2021–2026 no forma parte del marco: se aplica como criterio de inclusión y como filtro de la búsqueda. La fase del ciclo de vida no es un bloque AND de la ecuación —exigirla en el resumen habría excluido estudios pertinentes—, sino un criterio verificable (CI4) y un dato de la RQ2.

Kitchenham y Charters (2007, p. 11) advierten que en Ingeniería de Software hay pocos estudios primarios; la población reúne varios perfiles en lugar de uno solo y la estratificación se reserva a la extracción (RQ1). En la Tabla I, la población incluye trastorno por déficit de atención e hiperactividad (TDAH).

**Tabla I — Marco PIO**

| P | I | O |
| --- | --- | --- |
| Usuarios con discapacidad cognitiva o neurodivergencia: autismo, TDAH, discapacidad intelectual, dificultades de aprendizaje, dislexia, disgrafía y discalculia | Técnicas de inteligencia artificial, incluidas la GenAI y los LLM | Métricas de evaluación, instrumentos y marcos normativos (WCAG, COGA) reportados en los estudios |

_Nota._ Elaboración propia según el protocolo de la revisión. P, población; I, intervención (técnicas de IA); O, resultado (métricas, instrumentos y marcos normativos).

**Pregunta general de investigación:**

> ¿Cómo se ha integrado la inteligencia artificial en el ciclo de vida del software, del diseño y la personalización a la verificación, la evaluación y la auditoría, para usuarios con discapacidad cognitiva o neurodivergencia; qué métricas se reportan, incluidas las orientaciones COGA frente a las WCAG; y qué combinaciones de condición, técnica, fase y métrica carecen de evidencia frente al predominio de la accesibilidad sensorial?

**Tabla II — Preguntas de investigación por componente**

| Componente | Código | Pregunta |
| ---------- | ------ | -------- |
| P | RQ1 | ¿Qué perfiles de discapacidad cognitiva o neurodivergencia (trastorno del espectro autista [TEA], trastorno por déficit de atención e hiperactividad [TDAH], discapacidad intelectual, dificultades de aprendizaje y dislexia) abordan los estudios y con qué grado de estratificación y participación de usuarios? |
| I | RQ2 | ¿Qué técnicas de inteligencia artificial —incluidas la inteligencia artificial generativa (GenAI) y los modelos de lenguaje grandes (LLM)— se han aplicado, con qué rol y en qué fase del ciclo de vida del software? |
| O | RQ3 | ¿Qué métricas de evaluación y qué marcos normativos reportan los estudios —usabilidad, experiencia de usuario, legibilidad, carga cognitiva, calidad de software y accesibilidad cognitiva, incluidas las orientaciones de accesibilidad cognitiva del World Wide Web Consortium (COGA) frente a las Pautas de Accesibilidad para el Contenido Web (WCAG)— y con qué grado de automatización? ¿En qué medida, además, la evaluación contrasta usuarios con discapacidad cognitiva o neurodivergencia con la accesibilidad sensorial? |

_Nota._ Elaboración propia. Cada fila enlaza un componente del marco PIO (Tabla I) con la pregunta de investigación que lo operacionaliza.
<!-- /paper:section -->

<!-- paper:section id=palabras-clave -->
### B. Palabras clave pertinentes

Una vez fijados los componentes, cada uno se tradujo en un conjunto de palabras clave en español y en inglés, recogidos en la Tabla III, y la búsqueda se ejecutó con los términos en inglés. Kitchenham y Charters (2007, p. 14) recomiendan apoyar la búsqueda en términos de indexación controlados; por eso se priorizaron los descriptores del IEEE Thesaurus (Institute of Electrical and Electronics Engineers [IEEE], 2019). Donde el tesauro no ofrece un descriptor, se añadieron términos libres.

**Tabla III — Palabras clave para la revisión sistemática**

| Componente | Palabras clave (ES) | Keywords (EN) |
| ---------- | ------------------- | ------------- |
| P | trastorno del espectro autista, persona autista, trastorno del espectro autista, neurodivers, neurodivergen, neurodevelopmental, cognitive disabilit, intellectual disabilit, developmental disabilit, learning disabilit, ADHD, attention deficit, dyslexi, accesibilidad cognitiva, síndrome de Asperger, trastorno del desarrollo intelectual, learning disorder, learning difficult, discalculia, disgrafía, reading disabilit | _autism_, _autistic_, _autism spectrum_, _neurodivers*_, _neurodivergen*_, _neurodevelopmental_, _cognitive disabilit*_, _intellectual disabilit*_, _developmental disabilit*_, _learning disabilit*_, _ADHD_, _attention deficit_, _dyslexi*_, _cognitive accessibility_, _Asperger_, _intellectual developmental disorder_, _learning disorder*_, _learning difficult*_, _dyscalculia_, _dysgraphia_, _reading disabilit*_ |
| I | inteligencia artificial, AI, aprendizaje automático, procesamiento de lenguaje natural, NLP, language model, LLM, LLMs, generative AI, generative artificial intelligence, ChatGPT, GPT, ingeniería de instrucciones, visión por computador, chatbot, conversational agents, agentes inteligentes, virtual agent, text simplification, lexical simplification, text adaptation, procesamiento de textos, análisis de textos, minería de textos, lingüística computacional, interfaz de usuario adaptativa, reconocimiento de voz, sistemas de recomendación, generación de lenguaje natural, redes generativas antagónicas, lógica difusa, fuzzy inference, inteligencia ambiental, computación sensible al contexto, computación sensible al contexto, aprendizaje por refuerzo, aprendizaje contrastivo | _artificial intelligence_, _AI_, _machine learning_, _natural language processing_, _NLP_, _language model_, _LLM_, _LLMs_, _generative AI_, _generative artificial intelligence_, _ChatGPT_, _GPT_, _prompt engineering_, _computer vision_, _chatbot_, _conversational agents_, _intelligent agents_, _virtual agent_, _text simplification_, _lexical simplification_, _text adaptation_, _text processing_, _text analysis_, _text mining_, _computational linguistics_, _adaptive user interface_, _speech recognition_, _recommender systems_, _natural language generation_, _generative adversarial networks_, _fuzzy logic_, _fuzzy inference_, _ambient intelligence_, _context awareness_, _context-aware_, _reinforcement learning_, _contrastive learning_ |
| O | usabilidad, experiencia de usuario, metric, metrics, métricas de accesibilidad, métricas de legibilidad, readability, plain language, easy-to-read, easy read, calidad de software, carga cognitiva, accessibility evaluation, accessibility testing, estudio con usuarios, comprehension, understandability, satisfacción del usuario, accessibility audit, accessibility assessment, ergonomía, human engineering, user acceptance, human evaluation, WCAG, Web Content Accessibility Guidelines, accessibility, accessible design, accessible interface, inclusive design, universal design, inclusión digital | _usability_, _user experience_, _metric_, _metrics_, _accessibility metric_, _readability metrics_, _readability_, _plain language_, _easy-to-read_, _easy read_, _software quality_, _cognitive load_, _accessibility evaluation_, _accessibility testing_, _user study_, _comprehension_, _understandability_, _user satisfaction_, _accessibility audit_, _accessibility assessment_, _ergonomics_, _human engineering_, _user acceptance_, _human evaluation_, _WCAG_, _Web Content Accessibility Guidelines_, _accessibility_, _accessible design_, _accessible interface_, _inclusive design_, _universal design_, _digital inclusion_ |

_Nota._ En cursiva, descriptores del IEEE Thesaurus (IEEE, 2019). Los demás son términos libres; los de informática se contrastaron con la ACM Computing Classification System (Association for Computing Machinery [ACM], 2012) y los perfiles clínicos con los Medical Subject Headings (National Library of Medicine [NLM], 2026).
<!-- /paper:section -->

<!-- paper:section id=ecuacion-busqueda -->
### C. Ecuación de búsqueda

Con esas palabras clave se construyó una ecuación para Scopus y otra para Web of Science, cada una con tres bloques, uno por componente del marco. Dentro de un bloque los términos se unen con OR; entre bloques, con AND. El contraste entre accesibilidad cognitiva y sensorial no se impone como bloque de comparación en la búsqueda: las métricas, los marcos WCAG y los términos de accesibilidad integran el bloque O, y el contraste se analiza en la extracción (RQ3). Los campos se eligieron amplios (título, resumen y palabras clave en Scopus; todos los campos en Web of Science). Los límites de CI1 y CI2 van dentro de las ecuaciones o en los filtros de interfaz, según resume la Tabla IV.

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
  ( usability OR "user experience" OR metric OR metrics OR "accessibility metric"
    OR "readability metrics" OR readability OR "plain language" OR "easy-to-read"
    OR "easy read" OR "software quality" OR "cognitive load" OR "accessibility evaluation"
    OR "accessibility testing" OR "user study" OR comprehension OR understandability
    OR "user satisfaction" OR "accessibility audit" OR "accessibility assessment"
    OR ergonomics OR "human engineering" OR "user acceptance" OR "human evaluation"
    OR WCAG OR "Web Content Accessibility Guidelines" OR accessibility
    OR "accessible design" OR "accessible interface" OR "inclusive design"
    OR "universal design" OR "digital inclusion" )
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
AND ALL=(usability OR "user experience" OR metric OR metrics OR "accessibility metric"
  OR "readability metrics" OR readability OR "plain language" OR "easy-to-read"
  OR "easy read" OR "software quality" OR "cognitive load" OR "accessibility evaluation"
  OR "accessibility testing" OR "user study" OR comprehension OR understandability
  OR "user satisfaction" OR "accessibility audit" OR "accessibility assessment"
  OR ergonomics OR "human engineering" OR "user acceptance" OR "human evaluation"
  OR WCAG OR "Web Content Accessibility Guidelines" OR accessibility
  OR "accessible design" OR "accessible interface" OR "inclusive design"
  OR "universal design" OR "digital inclusion")
AND PY=(2021-2026) AND DT=(Article) AND LA=(English OR Spanish)
```

Filtro de la interfaz: acceso abierto (Web of Science no tiene etiqueta de campo para el acceso abierto).

**Tabla IV — Búsqueda por base de datos**

| Base           | Fecha de búsqueda | Años      | Campos                           | Filtros                                                            | Registros                  |
| -------------- | ----------------- | --------- | -------------------------------- | ------------------------------------------------------------------ | -------------------------- |
| Scopus         | X                 | 2021–2026 | Título, resumen y palabras clave | Artículo; inglés o español; acceso abierto                         | n = 761 (sin filtros: n = X) |
| Web of Science | X                 | 2021–2026 | Todos los campos                 | Artículo; inglés o español; acceso abierto (filtro de la interfaz) | n = 532 (sin filtros: n = X) |

_Nota._ Elaboración propia. La fecha de búsqueda y el total sin filtros (X) se completarán al cerrar la recuperación en cada base.
<!-- /paper:section -->

<!-- paper:section id=criterios-seleccion -->
### D. Criterios de inclusión y exclusión

La amplitud de la búsqueda tiene un precio: los registros recuperados mezclan estudios pertinentes con otros que solo comparten vocabulario con la pregunta. Para separarlos, los criterios de inclusión (CI) y exclusión (CE) se fijaron en el protocolo antes de la búsqueda, como recomiendan Kitchenham y Charters (2007, p. 18). CI1 y CI2 repiten los límites de las ecuaciones; CI3 y CI4 traducen el marco PIO y la fase del ciclo de vida a condiciones verificables. Las revisiones sistemáticas de la literatura (RSL) y, en inglés, las *systematic literature reviews* (SLR) quedan fuera del corpus primario (CE6).

**Criterios de inclusión:**

- **CI1:** CI1. Estudios publicados entre 2021 y 2026, los cinco últimos años completos y el año en curso.
- **CI2:** CI2. Artículos de revista revisados por pares, de acceso abierto, en inglés o español.
- **CI3:** CI3. Población con discapacidad cognitiva o neurodivergencia (autismo, TDAH, discapacidad intelectual, dislexia o dificultades de aprendizaje).
- **CI4:** CI4. Estudios en los que la IA interviene en una fase del ciclo de vida del software: requisitos, diseño, desarrollo, personalización, pruebas, verificación o auditoría.

**Criterios de exclusión:**

- **CE1:** CE1. Estudios en los que la inteligencia artificial solo diagnostica o detecta la condición, sin un artefacto de software evaluado.
- **CE2:** CE2. Estudios de accesibilidad solo sensorial, sin población con discapacidad cognitiva o neurodivergencia.
- **CE3:** CE3. Robots sociales, tutores inteligentes o tecnología de rehabilitación como producto principal, que no intervienen en ninguna fase del ciclo de vida del software.
- **CE4:** CE4. Artículos de revisión, mapeos o síntesis secundarias sin estudio empírico primario en el texto.
- **CE5:** CE5. Actas de congreso, comunicaciones cortas, editoriales, preprints o tesis.
- **CE6:** CE6. El estudio es una revisión sistemática de la literatura (RSL o SLR).
<!-- /paper:section -->

<!-- paper:section id=seleccion-prisma -->
### E. Proceso de selección — Diagrama PRISMA

Aplicar esos criterios a un conjunto amplio de registros exige decisiones sucesivas que deben quedar por escrito (Kitchenham & Charters, 2007, pp. 19–20). Por esa razón, la selección se documenta según PRISMA 2020 (Page et al., 2021, p. 1). El diagrama de flujo resume las etapas siguientes, con los conteos obtenidos al cerrar el cribado a texto completo (octubre de 2026):

1. Registros identificados en Scopus (n = 761) y en Web of Science (n = 532).
2. Duplicados eliminados (n = 327).
3. Registros cribados por título y resumen (n = 966); excluidos (n = 833).
4. Informes buscados para su recuperación (n = 133); no recuperados (n = 12).
5. Informes evaluados a texto completo (n = 120); excluidos por no cumplir un criterio de inclusión o por cumplir uno de exclusión (n = 47).
6. Estudios incluidos en la revisión (n = 73).

La Fig. 1 condensa esas etapas en un diagrama de flujo.

**Fig. 1**

_Diagrama de flujo PRISMA 2020 del proceso de selección._

[[AGREGAR DIAGRAMA]]

_Nota._ Elaboración propia con los conteos de los pasos numerados de esta sección. Adaptado de la estructura del diagrama de flujo PRISMA 2020 (Page et al., 2021, p. 5).
<!-- /paper:section -->

<!-- paper:section id=referencias -->
## Referencias
Aljedaani, W., & Mollik, R. H. (2026). Large language models for web accessibility: A systematic literature review. In *Proceedings of the 23rd International Web for All Conference (W4A ’26)* (pp. 160–171). Association for Computing Machinery. [https://doi.org/10.1145/3800424.3800452](https://doi.org/10.1145/3800424.3800452)

Association for Computing Machinery. (2012). *The 2012 ACM computing classification system*. [https://dl.acm.org/pb-assets/dl_ccs/acm_ccs2012-1626988337597.xml](https://dl.acm.org/pb-assets/dl_ccs/acm_ccs2012-1626988337597.xml)

Chemnad, K., & Othman, A. (2024). Digital accessibility in the era of artificial intelligence—Bibliometric analysis and systematic review. *Frontiers in Artificial Intelligence, 7*, Article 1349668. [https://doi.org/10.3389/frai.2024.1349668](https://doi.org/10.3389/frai.2024.1349668)

Congreso de la República del Perú. (2012). *Ley N.º 29973, Ley General de la Persona con Discapacidad*. Diario Oficial El Peruano.

Institute of Electrical and Electronics Engineers. (2019). *2019 IEEE thesaurus* (Version 1.0). [https://www.ieee.org/publications/services/thesaurus-access-page.html](https://www.ieee.org/publications/services/thesaurus-access-page.html)

Kitchenham, B., & Charters, S. (2007). *Guidelines for performing systematic literature reviews in software engineering* (EBSE Technical Report EBSE-2007-01, Version 2.3). Keele University; University of Durham. [https://www.elsevier.com/__data/promis_misc/525444systematicreviewsguide.pdf](https://www.elsevier.com/__data/promis_misc/525444systematicreviewsguide.pdf)

National Library of Medicine. (2026). *Medical subject headings* [Base de datos]. [https://www.nlm.nih.gov/mesh/meshhome.html](https://www.nlm.nih.gov/mesh/meshhome.html)

Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., Shamseer, L., Tetzlaff, J. M., Akl, E. A., Brennan, S. E., Chou, R., Glanville, J., Grimshaw, J. M., Hróbjartsson, A., Lalu, M. M., Li, T., Loder, E. W., Mayo-Wilson, E., McDonald, S., . . . Moher, D. (2021). The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. *BMJ, 372*, Article n71. [https://doi.org/10.1136/bmj.n71](https://doi.org/10.1136/bmj.n71)

Paiva, D. M. B., Freire, A. P., & de Mattos Fortes, R. P. (2021). Accessibility and software engineering processes: A systematic literature review. *Journal of Systems and Software, 171*, Article 110819. [https://doi.org/10.1016/j.jss.2020.110819](https://doi.org/10.1016/j.jss.2020.110819)

Perry, N., Sun, C., Munro, M., Boulton, K. A., & Guastella, A. J. (2024). AI technology to support adaptive functioning in neurodevelopmental conditions in everyday environments: A systematic review. *npj Digital Medicine, 7*, Article 370. [https://doi.org/10.1038/s41746-024-01355-7](https://doi.org/10.1038/s41746-024-01355-7)

World Wide Web Consortium. (2021). *Making content usable for people with cognitive and learning disabilities* (W3C Working Group Note). [https://www.w3.org/TR/coga-usable/](https://www.w3.org/TR/coga-usable/)

World Wide Web Consortium. (2023). *Web Content Accessibility Guidelines (WCAG) 2.2* (W3C Recommendation). [https://www.w3.org/TR/WCAG22/](https://www.w3.org/TR/WCAG22/)

Xu, Z., Liu, F., Xia, G., Duan, Y., & Yu, L. (2026). A scoping review of inclusive and adaptive human–AI interaction design for neurodivergent users. *Disability and Rehabilitation: Assistive Technology, 21*(4), 943–961. [https://doi.org/10.1080/17483107.2025.2579822](https://doi.org/10.1080/17483107.2025.2579822)
<!-- /paper:section -->

