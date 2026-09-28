# Marco de búsqueda — Inteligencia artificial en el ciclo de vida del software para accesibilidad cognitiva

**Marco:** PICOC · **Vocabulario:** IEEE Thesaurus 2019 + términos libres · **Tema:** Inteligencia artificial en el ciclo de vida del software para accesibilidad cognitiva y neurodivergencia: técnicas, fases de ingeniería y métricas de evaluación — una revisión sistemática de la literatura.

Protocolo: [`playbooks/vocabulario-controlado.md`](../../../../playbooks/vocabulario-controlado.md) · Debate: [picoc-debate.md](picoc-debate.md) · Verificación: `pnpm -s picoc:lint docs/ia-inclusion-cognitiva-software`

## Pregunta general (problemática)

¿Cómo se han integrado técnicas de inteligencia artificial en las fases del ciclo de vida del software —con énfasis en diseño, personalización en runtime y, sobre todo, verificación, evaluación y auditoría— orientadas a usuarios con discapacidad cognitiva o neurodivergencia; qué métricas se reportan (incluidas orientaciones COGA frente al núcleo WCAG); y qué celdas de la matriz *condición × técnica × fase SE × métrica* permanecen vacías frente al sesgo documentado hacia la accesibilidad sensorial/visual y frente a revisiones HCI/AT o GenAI+web que no estructuran el proceso de Ingeniería de Software?

## Preguntas por componente

| RQ | Comp. | Pregunta (RQ) | Dato a extraer |
|----|-------|---------------|----------------|
| RQ1 | P | ¿Qué perfiles de discapacidad cognitiva o neurodivergencia (trastorno del espectro autista [TEA], trastorno por déficit de atención e hiperactividad [TDAH], discapacidad intelectual, dificultades de aprendizaje y dislexia) abordan los estudios y con qué grado de estratificación y participación de usuarios? | Condición declarada · estratificación (sí o no) · participación de personas con discapacidad |
| RQ2 | I | ¿Qué técnicas de inteligencia artificial —incluidas la inteligencia artificial generativa (GenAI) y los modelos de lenguaje grandes (LLM)— se han aplicado y con qué rol en el proceso de software? | Familia de técnica (aprendizaje automático, aprendizaje profundo, procesamiento de lenguaje natural, LLM o GenAI) · modelo · rol (generador, evaluador o asistente de aseguramiento de la calidad) · año de publicación |
| RQ3 | C | ¿En qué medida la evidencia sobre accesibilidad cognitiva se contrasta con, o queda subordinada a, la accesibilidad sensorial o visual y la conformidad con las Pautas de Accesibilidad para el Contenido Web (WCAG)? | Tipo de discapacidad cubierta (cognitiva o sensorial) · marco normativo (WCAG, orientaciones de accesibilidad cognitiva del W3C [COGA] o ninguno) |
| RQ4 | O | ¿Qué métricas de evaluación se reportan (usabilidad, accesibilidad cognitiva, legibilidad, calidad de software) y con qué grado de automatización? | Métrica · instrumento · grado de automatización (automatizable en integración continua, semiautomática o solo mediante validación con usuarios) |
| RQ5 | Co | ¿En qué fases del ciclo de vida del software (requisitos, diseño, personalización en tiempo de ejecución, pruebas, verificación y validación, y auditoría) se integra la inteligencia artificial y qué peso relativo tienen la verificación y la evaluación? | Fase del ciclo de vida · artefacto intervenido · combinación de condición, técnica, fase y métrica sin estudios |

## Tabla de componentes (1:1 con las queries)

| Comp. | Concepto | RQ | Keywords | Descriptor IEEE (pág.) | Justificación |
|-------|----------|----|----------|------------------------|---------------|
| P | Usuarios con discapacidad cognitiva o neurodivergencia: autismo, TDAH, discapacidad intelectual, dificultades de aprendizaje y dislexia | RQ1 | `autism` · `autistic` · `"autism spectrum"` · `neurodivers*` · `neurodivergen*` · `neurodevelopmental` · `"cognitive disabilit*"` · `"intellectual disabilit*"` · `"developmental disabilit*"` · `"learning disabilit*"` · `ADHD` · `"attention deficit"` · `dyslexi*` · `"cognitive accessibility"` | Autism (p.35) | Procede de “usuarios con discapacidad cognitiva o neurodivergencia”. IEEE solo codifica *Autism*; los demás perfiles, la neurodiversidad y la accesibilidad cognitiva entran como términos libres. `autistic` recoge el lenguaje de identidad que prefiere la comunidad |
| I | Técnicas de inteligencia artificial, incluidas la GenAI y los LLM | RQ2 | `"artificial intelligence"` · `AI` · `"machine learning"` · `"machine-learning"` · `"deep learning"` · `"natural language processing"` · `NLP` · `"large language model*"` · `LLM` · `LLMs` · `"generative AI"` · `"generative artificial intelligence"` · `ChatGPT` | Artificial intelligence (p.30) · Machine learning (p.294) · Deep learning (p.126) · Natural language processing (p.354) | Procede de “técnicas de inteligencia artificial”. `AI`, `"machine-learning"` y `NLP` son sinónimos aceptados por el tesauro; los LLM, la GenAI y ChatGPT son posteriores a su edición de 2019, por lo que entran como términos libres |
| C | Accesibilidad sensorial o visual y conformidad normativa (WCAG), frente a las que se contrasta la accesibilidad cognitiva | RQ3 | `blindness` · `deafness` · `deaf` · `"visual impairment"` · `"visually impaired"` · `"low vision"` · `"hearing impairment"` · `"hearing impaired"` · `"sensory impairment"` · `"screen reader"` · `WCAG` · `"Web Content Accessibility Guidelines"` · `accessibility` | Blindness (p.54) · Deafness (p.125) | Procede de “sesgo documentado hacia la accesibilidad sensorial/visual” y de “frente al núcleo WCAG”. IEEE codifica la ceguera y la sordera; las demás discapacidades sensoriales, los lectores de pantalla y las WCAG, estándar del W3C, entran como términos libres. `accessibility` evita que el bloque exija nombrar una discapacidad sensorial y conserva los estudios solo cognitivos que hablan de accesibilidad |
| O | Métricas de evaluación: usabilidad, experiencia de usuario, legibilidad, carga cognitiva y calidad de software | RQ4 | `usability` · `"user experience"` · `measurement` · `metric` · `metrics` · `"accessibility metric"` · `"readability metrics"` · `readability` · `"plain language"` · `"easy-to-read"` · `"software quality"` · `"cognitive load"` | Usability (p.565) · Measurement (p.313) · Readability metrics (p.453) · Software quality (p.498) | Procede de “qué métricas se reportan”. *Metrics* es un término no preferido que el tesauro remite a *Measurement*, por eso se incluyen ambos. El lenguaje claro y la lectura fácil son la forma operativa de la legibilidad para perfiles cognitivos |
| Co | Ciclo de vida del software: requisitos, diseño, implementación, personalización en tiempo de ejecución, pruebas, verificación y validación, y auditoría | RQ5 | `"software engineering"` · `"software development"` · `"software development life cycle"` · `SDLC` · `"web development"` · `"app development"` · `"requirements engineering"` · `"accessibility requirement"` · `"software design"` · `"adaptive user interface"` · `"runtime personalization"` · `"runtime adaptation"` · `"code generation"` · `"software testing"` · `"automatic testing"` · `"automated testing"` · `"verification and validation"` · `"system validation"` · `"accessibility evaluation"` · `"accessibility testing"` · `"accessibility audit"` | Software engineering (p.497) · Requirements engineering (p.459) · Software design (p.497) · Software testing (p.498) · Automatic testing (p.36) · System validation (p.529) | Procede de “fases del ciclo de vida del software —con énfasis en diseño, personalización en runtime y, sobre todo, verificación, evaluación y auditoría”. El ciclo de vida como tal, la verificación y validación como par, la personalización y la evaluación de accesibilidad no tienen descriptor IEEE. La generación de código cubre la implementación asistida por GenAI |

## Palabras clave

| Español | Inglés | Comp. | Tipo | Pág. IEEE | Justificación |
|---------|--------|-------|------|-----------|---------------|
| trastorno del espectro autista | Autism | P | IEEE | p.35 | — |
| inteligencia artificial | Artificial intelligence | I | IEEE | p.30 | — |
| aprendizaje automático | Machine learning | I | IEEE | p.294 | — |
| aprendizaje profundo | Deep learning | I | IEEE | p.126 | — |
| procesamiento de lenguaje natural | Natural language processing | I | IEEE | p.354 | — |
| ceguera | Blindness | C | IEEE | p.54 | — |
| sordera | Deafness | C | IEEE | p.125 | — |
| usabilidad | Usability | O | IEEE | p.565 | — |
| métricas | Measurement | O | IEEE (USE desde "metrics") | p.313 | — |
| métricas de legibilidad | Readability metrics | O | IEEE | p.453 | — |
| calidad de software | Software quality | O | IEEE | p.498 | — |
| ingeniería de software | Software engineering | Co | IEEE | p.497 | — |
| ingeniería de requisitos | Requirements engineering | Co | IEEE | p.459 | — |
| diseño de software | Software design | Co | IEEE | p.497 | — |
| pruebas de software | Software testing | Co | IEEE | p.498 | — |
| pruebas automáticas | Automatic testing | Co | IEEE | p.36 | — |
| validación de sistemas | System validation | Co | IEEE | p.529 | — |
| persona autista | autistic | P | Libre | — | Lenguaje de identidad preferido por la comunidad; IEEE solo tiene *Autism* |
| neurodiversidad y neurodivergencia | neurodiversity / neurodivergence | P | Libre | — | Concepto sin descriptor en IEEE 2019 |
| trastornos del neurodesarrollo | neurodevelopmental / developmental disability | P | Libre | — | Término de grupo usado en la literatura clínica y asistiva; sin descriptor IEEE |
| discapacidad cognitiva | cognitive disability | P | Libre | — | IEEE solo codifica *Autism* entre los perfiles cognitivos |
| discapacidad intelectual | intellectual disability | P | Libre | — | Sin descriptor IEEE |
| dificultades de aprendizaje | learning disability | P | Libre | — | Sin descriptor IEEE |
| TDAH | ADHD / attention deficit | P | Libre | — | Sin descriptor IEEE |
| dislexia | dyslexia | P | Libre | — | Sin descriptor IEEE |
| accesibilidad cognitiva | cognitive accessibility | P | Libre | — | IEEE 2019 no tiene *Accessibility* |
| modelos de lenguaje grandes | large language models / LLM | I | Libre | — | Concepto posterior a la edición 2019 |
| inteligencia artificial generativa | generative AI / ChatGPT | I | Libre | — | Concepto posterior a la edición 2019 |
| discapacidad visual y auditiva | visual impairment / visually impaired / low vision / hearing impairment / deaf / sensory impairment | C | Libre | — | IEEE solo tiene los casos extremos (*Blindness*, *Deafness*) |
| lector de pantalla | screen reader | C | Libre | — | Tecnología de apoyo sin descriptor IEEE |
| accesibilidad y pautas WCAG | accessibility / WCAG / Web Content Accessibility Guidelines | C | Libre | — | IEEE 2019 no tiene *Accessibility*; las WCAG son un estándar del W3C |
| experiencia de usuario | user experience | O | Libre | — | Sin descriptor IEEE (*Quality of experience* pertenece a redes y no es equivalente) |
| métricas de accesibilidad | accessibility metric | O | Libre | — | IEEE 2019 no tiene *Accessibility* |
| lenguaje claro y lectura fácil | plain language / easy-to-read | O | Libre | — | Vocabulario operativo de la legibilidad cognitiva; sin descriptor IEEE |
| carga cognitiva | cognitive load | O | Libre | — | Sin descriptor IEEE |
| ciclo de vida del software | software development life cycle / software development / web development / app development | Co | Libre | — | Sin descriptor IEEE para el ciclo de vida ni para el desarrollo como actividad |
| requisitos de accesibilidad | accessibility requirement | Co | Libre | — | IEEE 2019 no tiene *Accessibility* |
| interfaces adaptativas y personalización en tiempo de ejecución | adaptive user interface / runtime personalization / runtime adaptation | Co | Libre | — | Sin descriptor IEEE |
| generación de código | code generation | Co | Libre | — | Sin descriptor IEEE |
| pruebas automatizadas | automated testing | Co | Libre | — | Variante de uso común de *Automatic testing* que el tesauro no registra |
| verificación y validación | verification and validation | Co | Libre | — | IEEE solo tiene *System validation*, no el par |
| evaluación, pruebas y auditoría de accesibilidad | accessibility evaluation / accessibility testing / accessibility audit | Co | Libre | — | IEEE 2019 no tiene *Accessibility* |

## Keywords

| Keyword (EN) | Palabra clave (ES) | Comp. |
|--------------|--------------------|-------|
| cognitive accessibility | accesibilidad cognitiva | P |
| neurodiversity | neurodiversidad | P |
| Artificial intelligence | inteligencia artificial | I |
| WCAG | pautas WCAG | C |
| accessibility metric | métricas de accesibilidad | O |
| accessibility evaluation | evaluación de accesibilidad | Co |

## Query Scopus

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

## Query Web of Science

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

## Query IEEE Xplore

```text
( "IEEE Terms":"Autism" OR autistic OR "autism spectrum" OR neurodivers* OR neurodivergen* OR neurodevelopmental
  OR "cognitive disabilit*" OR "intellectual disabilit*" OR "developmental disabilit*"
  OR "learning disabilit*" OR ADHD OR "attention deficit" OR dyslexi* OR "cognitive accessibility" )
AND
( "IEEE Terms":"Artificial intelligence" OR AI OR "IEEE Terms":"Machine learning" OR "machine-learning"
  OR "IEEE Terms":"Deep learning" OR "IEEE Terms":"Natural language processing" OR NLP
  OR "large language model*" OR LLM OR LLMs OR "generative AI" OR "generative artificial intelligence" OR ChatGPT )
AND
( "IEEE Terms":"Blindness" OR "IEEE Terms":"Deafness" OR deaf OR "visual impairment" OR "visually impaired" OR "low vision"
  OR "hearing impairment" OR "hearing impaired" OR "sensory impairment" OR "screen reader"
  OR WCAG OR "Web Content Accessibility Guidelines" OR accessibility )
AND
( "IEEE Terms":"Usability" OR "user experience" OR "IEEE Terms":"Measurement" OR metric OR metrics OR "accessibility metric"
  OR "IEEE Terms":"Readability metrics" OR readability OR "plain language" OR "easy-to-read"
  OR "IEEE Terms":"Software quality" OR "cognitive load" )
AND
( "IEEE Terms":"Software engineering" OR "software development" OR "software development life cycle" OR SDLC
  OR "web development" OR "app development" OR "IEEE Terms":"Requirements engineering" OR "accessibility requirement"
  OR "IEEE Terms":"Software design" OR "adaptive user interface" OR "runtime personalization" OR "runtime adaptation"
  OR "code generation" OR "IEEE Terms":"Software testing" OR "IEEE Terms":"Automatic testing" OR "automated testing"
  OR "verification and validation" OR "IEEE Terms":"System validation" OR "accessibility evaluation"
  OR "accessibility testing" OR "accessibility audit" )
```

*Nota:* la query usa 8 comodines, por debajo del límite de 10 de IEEE Xplore; los comodines se reservan para el bloque P, donde las variantes morfológicas son muchas. Scopus y Web of Science recuperan los plurales de las frases sin comodín.

## Búsqueda auxiliar — localizar revisiones afines (Scopus, sin filtro de año; no es el corpus primario)

```text
TITLE-ABS-KEY (
  ( "systematic literature review" OR "scoping review" OR "systematic mapping" )
  AND
  ( "artificial intelligence" OR "machine learning" OR "deep learning" OR "natural language processing"
    OR "large language model*" OR LLM* OR "generative AI" )
  AND
  ( accessibility OR WCAG OR COGA OR autism OR neurodivers* OR "cognitive accessibility" OR "intellectual disabilit*" )
)
```

## Descriptores revisados y excluidos

- *Neural networks* (p.358) y `chatbot*`: no nacen del tema; *Deep learning* ya cubre las redes neuronales y los chatbots quedan cubiertos por los términos de LLM y GenAI.
- *User centered design* (p.566): el tema habla de diseño de interfaces adaptativas y personalización, no del diseño centrado en el usuario como método; incluirlo atraería estudios de interacción persona-computador sin componente de ingeniería de software.
- *Formal verification* (p.199): verificación matemática de programas, ajena a la verificación y validación de accesibilidad del tema.
- *System testing* (p.529): término específico de *System validation*; es un nivel de prueba ya cubierto por *Software testing*.
- *Performance evaluation* (p.396): en el corpus de software remite al rendimiento del sistema (tiempo, carga), no a métricas de accesibilidad o usabilidad.
- *Auditory system* (p.35): anatomía de la audición; el concepto del tema es la discapacidad auditiva, cubierta por *Deafness* y términos libres.
- *Standards* (p.509): demasiado amplio; la conformidad normativa del tema se busca con WCAG y `accessibility`.
- *Assistive technology* (p.32): el alcance excluye la tecnología de apoyo sin relación con el proceso de ingeniería de software.
- *Mental disorders* (p.320) y *Dementia* (p.128): se excluyen para evitar un enfoque medicalizado y porque quedan fuera de los perfiles estratificados. Por la misma razón se retiró `"cognitive impairment*"`, que recupera sobre todo estudios de diagnóstico de deterioro cognitivo y demencia.
- *Cognition* (p.85): demasiado amplio (ciencia cognitiva, inteligencia artificial «cognitiva»).
- *User interfaces*: término genérico que reabriría el corpus de interacción persona-computador; el tema se refiere a interfaces adaptativas, que se buscan como término libre.
- `COGA` como sigla suelta: coincide con un estudio genético sobre alcoholismo de amplio corpus biomédico; la accesibilidad cognitiva se busca con `"cognitive accessibility"`.
- `blind` y `personaliz*`: recuperan ruido ajeno al tema (ensayos doble ciego, medicina y aprendizaje personalizados); se sustituyen por `blindness`, `"visually impaired"` y las frases de personalización en tiempo de ejecución.

## Criterios de inclusión y exclusión

### Inclusión

- Estudios publicados entre 2020 y 2026, periodo que abarca la adopción masiva de la inteligencia artificial generativa (2023).
- Artículos de revista o de congreso revisados por pares, incluidas las actas publicadas como capítulos de libro, en inglés o español.
- Estudios dirigidos a personas con discapacidad cognitiva o neurodivergencia: TEA, TDAH, discapacidad intelectual, dislexia o dificultades de aprendizaje.
- Estudios en los que una técnica de inteligencia artificial identificada interviene en el software o en su proceso de desarrollo.
- Estudios que aplican esa técnica en requisitos, diseño, desarrollo, personalización en tiempo de ejecución, pruebas, verificación y validación o auditoría.
- Estudios con una evaluación empírica que reporta al menos una métrica o instrumento de evaluación.

### Exclusión

- Registros duplicados entre bases de datos o sin texto completo accesible.
- Revisiones sistemáticas y otros estudios secundarios; se usan solo para delimitar el vacío.
- Preprints, tesis, editoriales y resúmenes de congreso.
- Robots sociales, tutores inteligentes, cribado clínico o tecnología de rehabilitación como producto principal, sin una fase del ciclo de vida del software.
