<!-- paper:section id=encabezado -->
# Inteligencia artificial en el ciclo de vida del software para accesibilidad cognitiva y neurodivergencia: técnicas, fases de ingeniería y métricas de evaluación — una revisión sistemática de la literatura

**Tema.** IA (incluidos GenAI/LLM) en el ciclo de vida del software para accesibilidad cognitiva y neurodivergencia, con énfasis en V&V/auditoría y taxonomía condición × técnica × fase SE × métrica (COGA frente a WCAG).

**Problemática.** ¿Cómo se han integrado técnicas de IA en las fases del ciclo de vida del software —sobre todo en verificación, evaluación y auditoría— para usuarios con discapacidad cognitiva o neurodivergencia; qué métricas se reportan (COGA frente a WCAG); y qué celdas de la matriz *condición × técnica × fase SE × métrica* quedan vacías o no transferibles a Definition of Done / CI frente al sesgo sensorial/visual y a síntesis clínicas, HCI o GenAI+web que no estructuran el proceso de Ingeniería de Software?

**Objetivo.** Sintetizar evidencia primaria de IA en artefactos y procesos SE para perfiles cognitivos o neurodivergentes, y producir esa taxonomía con columna de transferibilidad (automatizable en CI / juicio experto / validación con usuarios), delimitada frente a fronteras clínicas, HCI y GenAI+web WCAG-duro.
<!-- /paper:section -->

## I. Introducción

<!-- paper:section id=contexto -->
### Contexto

La accesibilidad digital busca que las personas puedan percibir, operar y comprender el software. En ese marco, las Pautas de Accesibilidad para el Contenido Web (WCAG) 2.2 concentran la conformidad verificable (World Wide Web Consortium [W3C], 2023). Las orientaciones del grupo de trabajo del W3C sobre accesibilidad cognitiva y del aprendizaje (COGA), en cambio, atienden otra cara del problema: la comprensión, la memoria y la carga cognitiva (W3C, 2021). Estos aspectos son, por lo general, más difíciles de verificar de forma automática.

A partir de ese matiz, por *accesibilidad cognitiva* se entiende aquí la reducción de las barreras de comprensión, memoria y carga cognitiva. Por *neurodivergencia* se entiende una categoría amplia que, cuando la evidencia lo permite, se desglosa en condiciones concretas, como el trastorno del espectro autista, el trastorno por déficit de atención e hiperactividad o la dislexia. Este uso no pretende medicalizar a las personas. En consecuencia, el objeto de esta revisión no es la tecnología asistiva clínica. Es el modo en que la inteligencia artificial (IA), incluida la IA generativa (GenAI), se inserta en el ciclo de vida del software, desde los requisitos y el diseño hasta la verificación y validación (V&V).

Este alcance obliga a revisar primero lo que ya han sintetizado las revisiones previas. Chemnad y Othman (2024), tras revisar 43 estudios de IA y accesibilidad digital, documentaron un claro predominio de la discapacidad visual y un vacío en el trastorno del espectro autista y en los trastornos neurológicos. Perry et al. (2024), por su parte, sintetizaron 15 trabajos de IA para el funcionamiento adaptativo en condiciones del neurodesarrollo, con resultados de apoyo cotidiano y no de ingeniería. En el terreno de los modelos de lenguaje, Aljedaani y Mollik (2026) analizaron 33 estudios primarios sobre su uso en la accesibilidad web. En ellos, las WCAG dominan como marco y las orientaciones COGA reciben poca atención, aunque la revisión no organiza la evidencia por fase del ciclo de vida.

En los bordes del tema se sitúan otras dos revisiones. Xu et al. (2026) cartografiaron 117 estudios sobre el diseño de la interacción entre personas neurodivergentes y sistemas de IA. Paiva et al. (2021), a su vez, revisaron 94 estudios sobre accesibilidad en los procesos de Ingeniería de Software, sin el eje de la IA ni el de la accesibilidad cognitiva.

Así, el estado del arte deja abiertas tres tensiones que se refuerzan entre sí. La primera enfrenta lo sensorial con lo cognitivo; la segunda, el enfoque clínico o de diseño de interacción con el proceso de ingeniería; la tercera, la automatización con la validación con usuarios. Esta última tiene consecuencias prácticas. Los equipos controlan la calidad mediante la integración continua (CI), que ejecuta pruebas automáticas con cada cambio, y mediante la *Definition of Done*, el conjunto de criterios que un incremento debe cumplir para darse por terminado. Si esos controles se limitan a criterios WCAG verificables automáticamente, que un analizador no detecte fallos no basta para afirmar que el software es inclusivo en el plano cognitivo.
<!-- /paper:section -->

<!-- paper:section id=problema -->
### El problema

De esas tensiones nace la pregunta de investigación: ¿cómo se ha integrado la IA en las fases del ciclo de vida del software, sobre todo en la verificación, la evaluación y la auditoría, para personas con discapacidad cognitiva o neurodivergentes? La pregunta abarca también el diseño y la personalización. Se complementa, además, con otras dos: qué métricas se reportan y qué combinaciones de condición, técnica, fase y métrica carecen de evidencia, dado el predominio de los estudios centrados en la discapacidad sensorial.

A ello se suma una tendencia reciente. En los estudios con modelos de lenguaje, la definición, la detección y la evaluación de los problemas de accesibilidad se apoyan sobre todo en criterios WCAG, mientras que las orientaciones cognitivas reciben una atención limitada (Aljedaani & Mollik, 2026). El panorama de síntesis es, así, desigual. Abundan las revisiones con sesgo visual (Chemnad & Othman, 2024), las de apoyo al funcionamiento adaptativo (Perry et al., 2024) y las de diseño de interacción (Xu et al., 2026). Escasean, en cambio, las que relacionan a la vez el tipo de condición, la técnica de IA, la fase del ciclo de vida y la métrica; en adelante, ese cruce de cuatro dimensiones se denomina *la taxonomía*.

El vacío, entonces, no es la falta de trabajos cercanos, sino la de una síntesis que los integre. Incluso el mapa de Paiva et al. (2021), ordenado por fase, deja fuera la IA y la dimensión cognitiva. Esta fragmentación eleva el riesgo de una accesibilidad solo aparente. Falta saber, para cada combinación, qué técnica se usó, en qué fase, con qué métrica y con qué límite de automatización. Eso es lo que se propone estudiar.
<!-- /paper:section -->

<!-- paper:section id=justificacion -->
### Justificación

Por ello, esta revisión articula tres elementos: las orientaciones COGA, la IA a lo largo del ciclo de vida, con énfasis en la V&V, y las métricas propias de la Ingeniería de Software. De este modo evita replicar las síntesis existentes sobre diseño de interacción. Las revisiones previas aportan el contraste necesario, pero no un mapa por fase y métrica.

Además, la Ley N.º 29973, Ley General de la Persona con Discapacidad (Congreso de la República del Perú, 2012), reconoce derechos de accesibilidad que alcanzan a las personas con discapacidad cognitiva e intelectual. Las metas 10.2 y 4.5 de los Objetivos de Desarrollo Sostenible dan contexto, por su parte, al valor público de la revisión, sin atribuirle un impacto causal.

En la práctica, el mapa será útil si asigna a cada hallazgo uno de tres niveles. El primero reúne lo que puede comprobarse automáticamente como control de la CI. El segundo, lo que requiere el juicio de un especialista en accesibilidad, por ejemplo si un texto simplificado por un modelo de lenguaje conserva el sentido. El tercero, lo que solo puede validarse con la participación de personas con discapacidad cognitiva o neurodivergentes. La revisión no pretende certificar el cumplimiento normativo.

De ahí la necesidad de una revisión sistemática de la literatura (RSL): abundan las revisiones sobre temas vecinos y el riesgo de replicarlas es alto. Si la combinación menos estudiada, la V&V asistida por GenAI con criterios cognitivos, reuniera pocos estudios primarios, el aporte legítimo sería documentar ese vacío, no forzar conclusiones.
<!-- /paper:section -->

<!-- paper:section id=objetivo-rsl -->
### Objetivo de la RSL

El objetivo general de esta revisión es sintetizar la evidencia primaria sobre técnicas de IA aplicadas a los procesos de Ingeniería de Software cuyo producto se dirige a personas con discapacidad cognitiva o neurodivergentes. Esa síntesis se ordenará en la taxonomía, lo que permitirá identificar también las combinaciones de condición, técnica, fase y métrica que carecen de evidencia. Para alcanzarlo, la pregunta general se desglosa en cinco preguntas de investigación (RQ), una por componente del marco que se presenta en la sección II.A, y cada una se traduce en un objetivo específico:

1. Caracterizar los perfiles cognitivos y neurodivergentes que abordan los estudios, su grado de estratificación y el nivel de participación de las personas con discapacidad o neurodivergentes, desde sujetos de evaluación hasta codiseño.
2. Identificar las técnicas de IA aplicadas, incluidas la GenAI y los modelos de lenguaje grandes, y el papel que cumplen en el proceso de software.
3. Contrastar la evidencia sobre accesibilidad cognitiva con la centrada en la accesibilidad sensorial o visual y en la conformidad con las WCAG.
4. Inventariar las métricas de evaluación y su grado de automatización: qué puede verificarse en la integración continua, qué requiere juicio experto y qué exige pruebas con usuarios.
5. Ubicar la IA en cada fase del ciclo de vida del software y medir el peso relativo de la verificación y la evaluación.

Cumplir estos objetivos exige analizar estudios sobre personas con discapacidad cognitiva o neurodivergentes, por lo que la revisión fija en el protocolo salvaguardas éticas. En la selección, el criterio de exclusión CE4 (sección II.D) deja fuera los estudios cuyo producto principal es el cribado clínico o la rehabilitación, sin una fase del ciclo de vida del software. En la extracción se registra cómo trata cada estudio la condición (como un déficit que corregir o como una diferencia que acomodar), si el sistema la deduce o almacena, si hubo consentimiento informado y el país del estudio. Esos datos se reportan como resultados, para que los vacíos éticos y el sesgo geográfico queden a la vista. Para no medicalizar a las personas, los rótulos diagnósticos se reportan tal como los declara cada estudio, sin reclasificar a nadie, y las métricas de ingeniería no se interpretan como resultados clínicos.
<!-- /paper:section -->

<!-- paper:section id=organizacion -->
### Organización del contenido de la revisión

Sobre esa base, el resto del artículo presenta el marco conceptual y el método, que sigue la guía *Preferred Reporting Items for Systematic Reviews and Meta-Analyses* (PRISMA) 2020 (Page et al., 2021). Después expone los resultados organizados según la taxonomía, con énfasis en la V&V asistida por GenAI, y señala las combinaciones sin evidencia. La discusión examina qué hallazgos pueden trasladarse a la práctica de desarrollo, y las conclusiones cierran el trabajo. En un anexo se detalla la comparación de alcance con las revisiones previas.
<!-- /paper:section -->

## II. Metodología

Esta revisión siguió las directrices de Kitchenham y Charters (2007) para revisiones sistemáticas en Ingeniería de Software, que reúnen en un protocolo previo las decisiones sobre la pregunta, la búsqueda y la selección. Fijarlas antes de conocer los resultados evita que las expectativas del investigador orienten la selección y permite que otros repitan el procedimiento (Kitchenham & Charters, 2007, pp. vi, 12). Los apartados siguientes recorren ese protocolo en su orden: la pregunta y sus componentes, las palabras clave, las ecuaciones de búsqueda, los criterios de selección y el proceso de selección.

<!-- paper:section id=marco-pico -->
### A. Pregunta PICOC y sus componentes

La primera decisión parte de la forma de la pregunta. Esta revisión no se limita a saber si la IA mejora la accesibilidad: necesita contrastar la accesibilidad cognitiva con la sensorial y situar cada intervención en una fase del ciclo de vida del software. El marco habitual de las revisiones clínicas, que solo distingue población, intervención y resultado, no deja lugar para esos dos ejes. Por eso se adoptó el marco de población, intervención, comparación, resultado y contexto (PICOC), que añade precisamente la comparación y el contexto. Kitchenham y Charters (2007, pp. 10–11) lo recomiendan para la Ingeniería de Software a partir de la propuesta de Petticrew y Roberts. En esta revisión, la comparación recoge el contraste con la accesibilidad sensorial y la conformidad con las WCAG, y el contexto corresponde a las fases del ciclo de vida.

Concretar sus componentes exigió, además, dos decisiones de alcance. Como el marco no incluye un componente temporal, la ventana de 2020 a 2026 se aplica como criterio de inclusión y no como parte de la pregunta. La población, por su parte, reúne varios perfiles en lugar de uno solo: el trastorno del espectro autista (TEA), el trastorno por déficit de atención e hiperactividad (TDAH), la discapacidad intelectual, las dificultades de aprendizaje y la dislexia. Kitchenham y Charters (2007, p. 11) advierten que en Ingeniería de Software hay pocos estudios primarios, por lo que restringir pronto la población puede dejar la revisión sin evidencia. El mismo riesgo existe aquí, de modo que la distinción entre perfiles se hace después, en la extracción de datos de la RQ1.

Con esas decisiones, el marco queda resumido en la Tabla I. De sus cinco componentes se deriva la pregunta general, que se reproduce tal como quedó registrada en el protocolo. En ella, la taxonomía aparece como una matriz de condición, técnica, fase y métrica, y se emplean tres siglas del área: Ingeniería de Software (SE), interacción persona-computadora (HCI) y tecnología asistiva (AT). Por último, cada componente origina una de las preguntas de investigación (Tabla II).

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

Una vez fijados los componentes, cada uno se tradujo en un conjunto de palabras clave en español y en inglés (Tabla III); la búsqueda se ejecutó con los términos en inglés. Para usar el vocabulario con el que las bases indexan los trabajos (Kitchenham & Charters, 2007, p. 14), se priorizaron los descriptores del tesauro del Institute of Electrical and Electronics Engineers, que aparecen en cursiva en la columna en inglés. Donde el tesauro no ofrece un descriptor, como ocurre con la neurodiversidad, la accesibilidad cognitiva o los modelos de lenguaje grandes, se añadieron términos libres.

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

Con esas palabras clave se construyó una ecuación de búsqueda para Scopus y otra para Web of Science, ambas con cinco bloques, uno por componente del marco. Los términos de un mismo bloque se unen con OR y los bloques se combinan con AND, de modo que cada registro debe responder a todos los componentes. Esa exigencia obligó a cuidar el bloque de comparación, que incluye el término general *accessibility* para no excluir los estudios centrados solo en lo cognitivo. En consecuencia, el contraste con la accesibilidad sensorial que plantea la RQ3 no se exige en la búsqueda, sino que se analiza en la extracción de datos.

Exigir los cinco bloques a la vez ya restringe mucho la recuperación, por lo que otras dos decisiones de la búsqueda dejaron parte del filtrado para etapas posteriores. La primera afecta a los campos: en Scopus se buscó en el título, el resumen y las palabras clave, y en Web of Science, en todos los campos, para no perder exhaustividad. La segunda afecta a los filtros, que se dejaron fuera de las ecuaciones para que cada exclusión quede contada en el flujo de selección, como exige una búsqueda documentada y replicable (Kitchenham & Charters, 2007, p. 16). Así, la ventana temporal se aplicó después de la búsqueda, y el tipo de documento y el idioma, durante el cribado.

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

Los registros recuperados todavía mezclan estudios pertinentes con otros que solo comparten vocabulario con la pregunta. Para separarlos se aplicaron criterios de inclusión y exclusión que, como recomiendan Kitchenham y Charters (2007, p. 18), se definieron en el protocolo. Los de inclusión traducen el marco en condiciones verificables: el periodo, el tipo de documento, la población, la técnica, la fase del ciclo de vida y la presencia de una evaluación empírica. Los de exclusión descartan lo que la búsqueda recupera sin responder a la pregunta: duplicados, estudios secundarios, literatura no revisada por pares y productos clínicos o asistivos ajenos al ciclo de vida del software.

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

Aplicar esos criterios a un conjunto amplio de registros exige decisiones sucesivas que deben quedar documentadas (Kitchenham & Charters, 2007, pp. 19–20). Esto pesa especialmente en una revisión que busca señalar qué combinaciones carecen de evidencia, porque una ausencia solo es creíble si se sabe qué se buscó y qué se descartó en cada paso. Por esa razón, la selección se documenta según PRISMA 2020 (Page et al., 2021, p. 1), una guía de reporte que combina una lista de 27 ítems con un diagrama de flujo. Ese diagrama muestra cuántos registros entran y salen en cada etapa; en esta revisión, las etapas fueron las siguientes:

1. Registros identificados en Scopus (n = X) y en Web of Science (n = X).
2. Duplicados eliminados (n = X).
3. Excluidos por fecha de publicación (n = X).
4. Registros cribados por título y resumen (n = X); excluidos (n = X).
5. Informes buscados para su recuperación (n = X); no recuperados (n = X).
6. Informes evaluados a texto completo (n = X); excluidos por no cumplir un criterio de inclusión o por cumplir uno de exclusión (n = X).
7. Estudios incluidos en la revisión (n = X).

[[ AGREGAR DIAGRAMA ]]

*Fig. 1. Diagrama de flujo PRISMA 2020 del proceso de selección.*
<!-- /paper:section -->

<!-- paper:section id=referencias -->
## Referencias

Aljedaani, W., & Mollik, R. H. (2026). Large language models for web accessibility: A systematic literature review. In *Proceedings of the 23rd International Web for All Conference (W4A ’26)* (pp. 160–171). Association for Computing Machinery. https://doi.org/10.1145/3800424.3800452

Chemnad, K., & Othman, A. (2024). Digital accessibility in the era of artificial intelligence—Bibliometric analysis and systematic review. *Frontiers in Artificial Intelligence, 7*, Article 1349668. https://doi.org/10.3389/frai.2024.1349668

Congreso de la República del Perú. (2012). *Ley N.º 29973, Ley General de la Persona con Discapacidad*. Diario Oficial El Peruano.

Kitchenham, B., & Charters, S. (2007). *Guidelines for performing systematic literature reviews in software engineering* (EBSE Technical Report EBSE-2007-01, Version 2.3). Keele University; University of Durham. https://www.elsevier.com/__data/promis_misc/525444systematicreviewsguide.pdf

Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., Shamseer, L., Tetzlaff, J. M., Akl, E. A., Brennan, S. E., Chou, R., Glanville, J., Grimshaw, J. M., Hróbjartsson, A., Lalu, M. M., Li, T., Loder, E. W., Mayo-Wilson, E., McDonald, S., . . . Moher, D. (2021). The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. *BMJ, 372*, Article n71. https://doi.org/10.1136/bmj.n71

Paiva, D. M. B., Freire, A. P., & de Mattos Fortes, R. P. (2021). Accessibility and software engineering processes: A systematic literature review. *Journal of Systems and Software, 171*, Article 110819. https://doi.org/10.1016/j.jss.2020.110819

Perry, N., Sun, C., Munro, M., Boulton, K. A., & Guastella, A. J. (2024). AI technology to support adaptive functioning in neurodevelopmental conditions in everyday environments: A systematic review. *npj Digital Medicine, 7*, Article 370. https://doi.org/10.1038/s41746-024-01355-7

World Wide Web Consortium. (2021). *Making content usable for people with cognitive and learning disabilities* (W3C Working Group Note). https://www.w3.org/TR/coga-usable/

World Wide Web Consortium. (2023). *Web Content Accessibility Guidelines (WCAG) 2.2* (W3C Recommendation). https://www.w3.org/TR/WCAG22/

Xu, Z., Liu, F., Xia, G., Duan, Y., & Yu, L. (2026). A scoping review of inclusive and adaptive human–AI interaction design for neurodivergent users. *Disability and Rehabilitation: Assistive Technology, 21*(4), 943–961. https://doi.org/10.1080/17483107.2025.2579822
<!-- /paper:section -->
