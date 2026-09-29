# Marco de búsqueda — Inteligencia artificial en el ciclo de vida del software para accesibilidad cognitiva

**Marco:** PICO · **Vocabulario:** IEEE Thesaurus (IEEE, 2019) y términos libres; los términos de informática se contrastan con la ACM Computing Classification System (ACM, 2012) y los perfiles clínicos con los Medical Subject Headings (NLM, 2026) · **Tema:** Inteligencia artificial en el ciclo de vida del software para accesibilidad cognitiva y neurodivergencia: técnicas, fases de ingeniería y métricas de evaluación — una revisión sistemática de la literatura.

Protocolo: [`playbooks/vocabulario-controlado.md`](../../../../playbooks/vocabulario-controlado.md) · Debate: [picoc-debate.md](picoc-debate.md) · Verificación: `pnpm -s picoc:lint docs/ia-inclusion-cognitiva-software`

## Pregunta general (problemática)

¿Cómo se han integrado técnicas de inteligencia artificial en las fases del ciclo de vida del software —con énfasis en diseño, personalización en runtime y, sobre todo, verificación, evaluación y auditoría— orientadas a usuarios con discapacidad cognitiva o neurodivergencia; qué métricas se reportan (incluidas orientaciones COGA frente al núcleo WCAG); y qué celdas de la matriz *condición × técnica × fase SE × métrica* permanecen vacías frente al sesgo documentado hacia la accesibilidad sensorial/visual y frente a revisiones HCI/AT o GenAI+web que no estructuran el proceso de Ingeniería de Software?

## Preguntas por componente

| RQ | Comp. | Pregunta (RQ) | Dato a extraer |
|----|-------|---------------|----------------|
| RQ1 | P | ¿Qué perfiles de discapacidad cognitiva o neurodivergencia (trastorno del espectro autista [TEA], trastorno por déficit de atención e hiperactividad [TDAH], discapacidad intelectual, dificultades de aprendizaje y dislexia) abordan los estudios y con qué grado de estratificación y participación de usuarios? | Condición declarada · estratificación (sí o no) · participación de personas con discapacidad |
| RQ2 | I | ¿Qué técnicas de inteligencia artificial —incluidas la inteligencia artificial generativa (GenAI) y los modelos de lenguaje grandes (LLM)— se han aplicado, con qué rol y en qué fase del ciclo de vida del software? | Familia de técnica (aprendizaje automático, aprendizaje profundo, procesamiento de lenguaje natural, LLM o GenAI) · modelo · rol (generador, evaluador o asistente de aseguramiento de la calidad) · fase del ciclo de vida (requisitos, diseño, desarrollo, personalización en tiempo de ejecución, pruebas, verificación y validación o auditoría) · año de publicación |
| RQ3 | C | ¿En qué medida la evidencia sobre accesibilidad cognitiva se contrasta con, o queda subordinada a, la accesibilidad sensorial o visual y la conformidad con las Pautas de Accesibilidad para el Contenido Web (WCAG)? | Tipo de discapacidad cubierta (cognitiva o sensorial) · marco normativo (WCAG, orientaciones de accesibilidad cognitiva del World Wide Web Consortium [COGA] o ninguno) |
| RQ4 | O | ¿Qué métricas de evaluación se reportan (usabilidad, experiencia de usuario, legibilidad, carga cognitiva, calidad de software y accesibilidad cognitiva) y con qué grado de automatización? | Métrica · instrumento · grado de automatización (automatizable en integración continua, semiautomática o solo mediante validación con usuarios) |

## Tabla de componentes (1:1 con las queries)

| Comp. | Concepto | RQ | Keywords | Descriptor IEEE (pág.) | Justificación |
|-------|----------|----|----------|------------------------|---------------|
| P | Usuarios con discapacidad cognitiva o neurodivergencia: autismo, TDAH, discapacidad intelectual, dificultades de aprendizaje, dislexia, disgrafía y discalculia | RQ1 | `autism` · `autistic` · `"autism spectrum"` · `neurodivers*` · `neurodivergen*` · `neurodevelopmental` · `"cognitive disabilit*"` · `"intellectual disabilit*"` · `"developmental disabilit*"` · `"learning disabilit*"` · `ADHD` · `"attention deficit"` · `dyslexi*` · `"cognitive accessibility"` · `Asperger` · `"intellectual developmental disorder"` · `"learning disorder*"` · `"learning difficult*"` · `dyscalculia` · `dysgraphia` · `"reading disabilit*"` | Autism (p.35) | Procede de “usuarios con discapacidad cognitiva o neurodivergencia”. IEEE solo codifica *Autism*; los demás perfiles, la neurodiversidad y la accesibilidad cognitiva entran como términos libres, y los perfiles clínicos se verifican en los Medical Subject Headings (MeSH), cuyo descriptor e identificador figuran en la tabla de palabras clave. `autistic` recoge el lenguaje de identidad que prefiere la comunidad, `"learning difficult*"` es la variante británica de las dificultades de aprendizaje, y la disgrafía y las dificultades lectoras son perfiles afines a la dislexia |
| I | Técnicas de inteligencia artificial, incluidas la GenAI y los LLM | RQ2 | `"artificial intelligence"` · `AI` · `"machine learning"` · `"natural language processing"` · `NLP` · `"language model"` · `LLM` · `LLMs` · `"generative AI"` · `"generative artificial intelligence"` · `ChatGPT` · `GPT` · `"prompt engineering"` · `"computer vision"` · `chatbot` · `"conversational agents"` · `"intelligent agents"` · `"virtual agent"` · `"text simplification"` · `"lexical simplification"` · `"text adaptation"` · `"text processing"` · `"text analysis"` · `"text mining"` · `"computational linguistics"` · `"adaptive user interface"` · `"speech recognition"` · `"recommender systems"` · `"natural language generation"` · `"generative adversarial networks"` · `"fuzzy logic"` · `"fuzzy inference"` · `"ambient intelligence"` · `"context awareness"` · `"context-aware"` · `"reinforcement learning"` · `"contrastive learning"` | Artificial intelligence (p.30) · Machine learning (p.294) · Natural language processing (p.354) · Computer vision (p.101) · Intelligent agents (p.261) · Text analysis (p.539) · Text mining (p.539) · Computational linguistics (p.95) · Speech recognition (p.506) · Recommender systems (p.454) · Generative adversarial networks (p.210) · Fuzzy logic (p.205) · Ambient intelligence (p.19) · Context awareness (p.106) · Reinforcement learning (p.457) | Procede de “técnicas de inteligencia artificial”. `AI`, `NLP` y `"fuzzy inference"` son sinónimos aceptados por el tesauro; los modelos de lenguaje, la GenAI, ChatGPT, GPT y la ingeniería de instrucciones son posteriores a su edición de 2019, por lo que entran como términos libres. Los agentes conversacionales y virtuales, la simplificación y adaptación automática de textos y las interfaces de usuario adaptativas figuran entre las técnicas más frecuentes en las herramientas de apoyo a personas con perfiles cognitivos. El procesamiento, el análisis y la minería de textos, la lingüística computacional, la inteligencia ambiental, la computación sensible al contexto y los aprendizajes por refuerzo y contrastivo se incorporan desde las palabras clave de los registros aceptados en el cribado 1 y desde el tesauro |
| C | Accesibilidad sensorial o visual y conformidad normativa (WCAG), frente a las que se contrasta la accesibilidad cognitiva | RQ3 | `blindness` · `deafness` · `deaf` · `"visual impairment"` · `"visually impaired"` · `"low vision"` · `"hearing impairment"` · `"hearing impaired"` · `"sensory impairment"` · `"screen reader"` · `WCAG` · `"Web Content Accessibility Guidelines"` · `accessibility` · `"accessible design"` · `"accessible interface"` · `"inclusive design"` · `"universal design"` · `"digital inclusion"` | Blindness (p.54) · Deafness (p.125) | Procede de “sesgo documentado hacia la accesibilidad sensorial/visual” y de “frente al núcleo WCAG”. IEEE codifica la ceguera y la sordera; las demás discapacidades sensoriales, los lectores de pantalla y las WCAG, estándar del World Wide Web Consortium (W3C), entran como términos libres. `accessibility` evita que el bloque exija nombrar una discapacidad sensorial y conserva los estudios centrados solo en la accesibilidad cognitiva; el diseño accesible, el inclusivo y el universal, junto con la inclusión digital, son los enfoques normativos con los que se contrasta la accesibilidad cognitiva |
| O | Métricas de evaluación: usabilidad, experiencia de usuario, legibilidad, comprensión, carga cognitiva, ergonomía, aceptación, evaluación de la accesibilidad y calidad de software | RQ4 | `usability` · `"user experience"` · `metric` · `metrics` · `"accessibility metric"` · `"readability metrics"` · `readability` · `"plain language"` · `"easy-to-read"` · `"easy read"` · `"software quality"` · `"cognitive load"` · `"accessibility evaluation"` · `"accessibility testing"` · `"user study"` · `comprehension` · `understandability` · `"user satisfaction"` · `"accessibility audit"` · `"accessibility assessment"` · `ergonomics` · `"human engineering"` · `"user acceptance"` · `"human evaluation"` | Usability (p.565) · Readability metrics (p.453) · Software quality (p.498) · Ergonomics (p.178) | Procede de “qué métricas se reportan”. `metric` y `metrics` se conservan como términos libres; el tesauro remite *Metrics* a *Measurement*, que se retira tras el cribado 1 porque solo recuperaba mediciones clínicas. `"human engineering"` es sinónimo de *Ergonomics* en el tesauro. El lenguaje claro y la lectura fácil son la forma operativa de la legibilidad para perfiles cognitivos; la comprensión es el resultado que persigue la accesibilidad cognitiva; la evaluación y las pruebas de accesibilidad, los estudios con usuarios, la aceptación y la evaluación humana recogen la verificación que prioriza la pregunta general |

## Palabras clave

| Español | Inglés | Comp. | Tipo | Pág. IEEE | Justificación |
|---------|--------|-------|------|-----------|---------------|
| trastorno del espectro autista | Autism | P | IEEE | p.35 | — |
| inteligencia artificial | Artificial intelligence | I | IEEE | p.30 | — |
| aprendizaje automático | Machine learning | I | IEEE | p.294 | — |
| procesamiento de lenguaje natural | Natural language processing | I | IEEE | p.354 | — |
| visión por computador | Computer vision | I | IEEE | p.101 | — |
| agentes inteligentes | Intelligent agents | I | IEEE | p.261 | — |
| análisis de textos | Text analysis | I | IEEE | p.539 | — |
| minería de textos | Text mining | I | IEEE | p.539 | — |
| lingüística computacional | Computational linguistics | I | IEEE | p.95 | — |
| reconocimiento de voz | Speech recognition | I | IEEE | p.506 | — |
| sistemas de recomendación | Recommender systems | I | IEEE | p.454 | — |
| redes generativas antagónicas | Generative adversarial networks | I | IEEE | p.210 | — |
| lógica difusa | Fuzzy logic | I | IEEE (USE desde "fuzzy inference") | p.205 | — |
| inteligencia ambiental | Ambient intelligence | I | IEEE | p.19 | — |
| computación sensible al contexto | Context awareness | I | IEEE | p.106 | — |
| aprendizaje por refuerzo | Reinforcement learning | I | IEEE | p.457 | — |
| ceguera | Blindness | C | IEEE | p.54 | — |
| sordera | Deafness | C | IEEE | p.125 | — |
| usabilidad | Usability | O | IEEE | p.565 | — |
| métricas de legibilidad | Readability metrics | O | IEEE | p.453 | — |
| calidad de software | Software quality | O | IEEE | p.498 | — |
| ergonomía | Ergonomics | O | IEEE (USE desde "human engineering") | p.178 | — |
| persona autista | autistic | P | Libre | — | Lenguaje de identidad preferido por la comunidad; IEEE solo tiene *Autism* |
| neurodiversidad y neurodivergencia | neurodiversity / neurodivergence | P | Libre | — | Concepto sin descriptor en IEEE 2019 |
| trastornos del neurodesarrollo | neurodevelopmental / developmental disability | P | Libre | — | Sin descriptor IEEE; MeSH *Neurodevelopmental Disorders* (D065886) y *Developmental Disabilities* (D002658) |
| discapacidad cognitiva | cognitive disability | P | Libre | — | IEEE solo codifica *Autism* entre los perfiles cognitivos |
| discapacidad intelectual | intellectual disability | P | Libre | — | Sin descriptor IEEE; MeSH *Intellectual Disability* (D008607) |
| dificultades de aprendizaje | learning disability | P | Libre | — | Sin descriptor IEEE; MeSH *Learning Disabilities* (D007859) |
| TDAH | ADHD / attention deficit | P | Libre | — | Sin descriptor IEEE; MeSH *Attention Deficit Disorder with Hyperactivity* (D001289), que registra ADHD como sinónimo |
| dislexia | dyslexia | P | Libre | — | Sin descriptor IEEE; MeSH *Dyslexia* (D004410) |
| accesibilidad cognitiva | cognitive accessibility | P | Libre | — | IEEE 2019 no tiene *Accessibility* |
| trastornos y dificultades del aprendizaje | learning disorder / learning difficulties | P | Libre | — | Sin descriptor IEEE; el descriptor MeSH *Learning Disabilities* (D007859) registra «learning disorders» como sinónimo, y MeSH incluye además *Specific Learning Disorder* (D000067559) |
| discalculia | dyscalculia | P | Libre | — | Sin descriptor IEEE; MeSH *Dyscalculia* (D060705) |
| síndrome de Asperger | Asperger | P | Libre | — | Sin descriptor IEEE; MeSH *Asperger Syndrome* (D020817). La clasificación clínica vigente integra esta etiqueta en el trastorno del espectro autista, pero parte de la literatura la conserva |
| trastorno del desarrollo intelectual | intellectual developmental disorder | P | Libre | — | Sin descriptor IEEE ni MeSH; es la denominación que el Manual diagnóstico y estadístico de los trastornos mentales, quinta edición (DSM-5), da a la discapacidad intelectual |
| disgrafía | dysgraphia | P | Libre | — | Sin descriptor IEEE; MeSH la registra como sinónimo de *Agraphia* (D000381) |
| dificultades lectoras | reading disability | P | Libre | — | Sin descriptor IEEE; MeSH registra «Reading Disability, Developmental» como sinónimo de *Dyslexia* (D004410) |
| modelos de lenguaje | language model / LLM | I | Libre | — | Concepto posterior a la edición 2019; concepto ACM CCS *Language models*. La frase `"language model"` recupera también los modelos de lenguaje grandes |
| ingeniería de instrucciones | prompt engineering | I | Libre | — | Técnica propia de los modelos de lenguaje, posterior a la edición 2019; 4 registros aceptados en el cribado 1 la usan como palabra clave |
| inteligencia artificial generativa | generative AI / ChatGPT / GPT | I | Libre | — | Concepto posterior a la edición 2019 |
| agentes conversacionales y virtuales | chatbot / conversational agents / virtual agent | I | Libre | — | Sin descriptor IEEE; interfaz frecuente en las herramientas de apoyo a personas con autismo o dislexia |
| simplificación y adaptación automática de textos | text simplification / lexical simplification / text adaptation | I | Libre | — | Técnica de procesamiento de lenguaje natural central en la accesibilidad cognitiva; sin descriptor IEEE |
| procesamiento de textos | text processing | I | Libre | — | El descriptor IEEE *Text processing* remite a la tipografía; se usa como término libre porque la indización de las bases lo asigna al procesamiento de lenguaje natural (3 registros aceptados en el cribado 1) |
| computación sensible al contexto | context-aware | I | Libre | — | Variante adjetiva de *Context awareness* |
| aprendizaje contrastivo | contrastive learning | I | Libre | — | Sin descriptor IEEE; técnica de aprendizaje automático presente en 3 registros aceptados en el cribado 1 |
| generación de lenguaje natural | natural language generation | I | Libre | — | Sin descriptor IEEE; concepto ACM CCS *Natural language generation* (Artificial intelligence → Natural language processing) |
| interfaz de usuario adaptativa | adaptive user interface | I | Libre | — | Personalización de la interfaz según el perfil del usuario; sin descriptor IEEE (*User interfaces*, p.566, es más amplio) |
| discapacidad visual y auditiva | visual impairment / visually impaired / low vision / hearing impairment / deaf / sensory impairment | C | Libre | — | IEEE solo tiene los casos extremos (*Blindness*, *Deafness*) |
| lector de pantalla | screen reader | C | Libre | — | Tecnología de apoyo sin descriptor IEEE |
| accesibilidad y pautas WCAG | accessibility / WCAG / Web Content Accessibility Guidelines | C | Libre | — | El IEEE Thesaurus 2019 no incluye *Accessibility*, que sí es un concepto de la ACM CCS, dentro de *Human-centered computing*; las Web Content Accessibility Guidelines (WCAG) son un estándar del W3C |
| diseño accesible, inclusivo y universal | accessible design / accessible interface / inclusive design / universal design | C | Libre | — | Enfoques normativos de la accesibilidad sin descriptor IEEE; se usan frases cerradas en lugar del adjetivo `accessible`, que recupera «publicly accessible dataset» |
| inclusión digital | digital inclusion | C | Libre | — | Enfoque de política y diseño afín a la accesibilidad; sin descriptor IEEE |
| experiencia de usuario | user experience | O | Libre | — | Sin descriptor IEEE (*Quality of experience* pertenece a redes y no es equivalente) |
| métricas de accesibilidad | accessibility metric | O | Libre | — | IEEE 2019 no tiene *Accessibility* |
| métricas | metric / metrics | O | Libre | — | El tesauro remite *Metrics* a *Measurement*, que se retira tras el cribado 1; las formas libres se conservan porque aportan registros aceptados |
| lenguaje claro y lectura fácil | plain language / easy-to-read / easy read | O | Libre | — | Vocabulario operativo de la legibilidad cognitiva; sin descriptor IEEE |
| carga cognitiva | cognitive load | O | Libre | — | Sin descriptor IEEE |
| evaluación, pruebas y auditoría de accesibilidad | accessibility evaluation / accessibility testing / accessibility audit / accessibility assessment | O | Libre | — | IEEE 2019 no tiene *Accessibility*; concepto ACM CCS *Accessibility design and evaluation methods*. Es la verificación que la pregunta prioriza |
| estudio con usuarios | user study | O | Libre | — | Sin descriptor IEEE; forma habitual de reportar la evaluación con personas; respaldado por el concepto ACM CCS *User studies* (Human-centered computing → HCI design and evaluation methods) |
| comprensión y comprensibilidad | comprehension / understandability | O | Libre | — | Resultado propio de la accesibilidad cognitiva; sin descriptor IEEE |
| satisfacción del usuario | user satisfaction | O | Libre | — | Medida frecuente en las evaluaciones con usuarios; sin descriptor IEEE |
| aceptación y evaluación humana | user acceptance / human evaluation | O | Libre | — | Formas de reportar la evaluación con personas, incluida la evaluación humana de la simplificación de textos; sin descriptor IEEE |

## Keywords

| Keyword (EN) | Palabra clave (ES) | Comp. |
|--------------|--------------------|-------|
| cognitive accessibility | accesibilidad cognitiva | P |
| neurodiversity | neurodiversidad | P |
| Artificial intelligence | inteligencia artificial | I |
| WCAG | pautas WCAG | C |
| accessibility metric | métricas de accesibilidad | O |
| Software quality | calidad de software | O |

## Query Scopus

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

## Query Web of Science

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

Filtro de la interfaz: Open Access (Web of Science no tiene etiqueta de campo para el acceso abierto).

## Query IEEE Xplore

```text
( "IEEE Terms":"Autism" OR autistic OR "autism spectrum" OR neurodivers* OR neurodivergen*
  OR neurodevelopmental OR "cognitive disabilit*" OR "intellectual disabilit*"
  OR "developmental disabilit*" OR "learning disabilit*" OR ADHD OR "attention deficit"
  OR dyslexi* OR "cognitive accessibility" OR Asperger
  OR "intellectual developmental disorder" OR "learning disorder*" OR "learning difficult*"
  OR dyscalculia OR dysgraphia OR "reading disabilit*" )
AND
( "IEEE Terms":"Artificial intelligence" OR AI OR "IEEE Terms":"Machine learning"
  OR "IEEE Terms":"Natural language processing" OR NLP OR "language model" OR LLM OR LLMs
  OR "generative AI" OR "generative artificial intelligence" OR ChatGPT OR GPT
  OR "prompt engineering" OR "IEEE Terms":"Computer vision" OR chatbot
  OR "conversational agents" OR "IEEE Terms":"Intelligent agents" OR "virtual agent"
  OR "text simplification" OR "lexical simplification" OR "text adaptation"
  OR "text processing" OR "IEEE Terms":"Text analysis" OR "IEEE Terms":"Text mining"
  OR "IEEE Terms":"Computational linguistics" OR "adaptive user interface"
  OR "IEEE Terms":"Speech recognition" OR "IEEE Terms":"Recommender systems"
  OR "natural language generation" OR "IEEE Terms":"Generative adversarial networks"
  OR "IEEE Terms":"Fuzzy logic" OR "fuzzy inference" OR "IEEE Terms":"Ambient intelligence"
  OR "IEEE Terms":"Context awareness" OR "context-aware"
  OR "IEEE Terms":"Reinforcement learning" OR "contrastive learning" )
AND
( "IEEE Terms":"Blindness" OR "IEEE Terms":"Deafness" OR deaf OR "visual impairment"
  OR "visually impaired" OR "low vision" OR "hearing impairment" OR "hearing impaired"
  OR "sensory impairment" OR "screen reader" OR WCAG
  OR "Web Content Accessibility Guidelines" OR accessibility OR "accessible design"
  OR "accessible interface" OR "inclusive design" OR "universal design"
  OR "digital inclusion" )
AND
( "IEEE Terms":"Usability" OR "user experience" OR metric OR metrics
  OR "accessibility metric" OR "IEEE Terms":"Readability metrics" OR readability
  OR "plain language" OR "easy-to-read" OR "easy read" OR "IEEE Terms":"Software quality"
  OR "cognitive load" OR "accessibility evaluation" OR "accessibility testing"
  OR "user study" OR comprehension OR understandability OR "user satisfaction"
  OR "accessibility audit" OR "accessibility assessment" OR "IEEE Terms":"Ergonomics"
  OR "human engineering" OR "user acceptance" OR "human evaluation" )
```

Filtros de la interfaz: 2021–2026 · Journals · Open Access; el idioma, si la interfaz no lo ofrece, se aplica en el cribado.

*Nota:* la query usa 10 comodines, el límite de IEEE Xplore; los comodines se reservan para el bloque P, donde las variantes morfológicas son muchas. Fuera de P, las tres bases usan frases cerradas (`"language model"`, `"intelligent agents"`, `"virtual agent"`, `"generative adversarial networks"`): Scopus y Web of Science recuperan las variantes de número, y `"language model"` recupera también «large language model».

## Validación de la búsqueda

Kitchenham y Charters (2007, p. 14) recomiendan probar la ecuación con estudios relevantes ya conocidos. El corpus del tema aún no tiene estudios primarios; se prueba con las tres revisiones sistemáticas ya recopiladas, según los términos de su resumen y sus palabras clave. Son estudios secundarios, que la exclusión deja fuera, y Scopus los clasifica por tipo de documento: la prueba mide si los términos cubren el tema, no los filtros.

| Estudio conocido | DOI | Fuente | ¿Cubren los términos su título, resumen y palabras clave? |
|---|---|---|---|
| Chemnad y Othman (2024) | 10.3389/frai.2024.1349668 | `RSL/MD/chemnad-othman-2024-digital-accessibility-ai.md` | No por su resumen: cubre P (*autism*), I (*AI*) y C (*accessibility*, *visual impairment*), pero no nombra métricas (O) |
| Perry et al. (2024) | 10.1038/s41746-024-01355-7 | `RSL/MD/perry-etal-2024-ai-neurodevelopmental.md` | No por su resumen: cubre P (*neurodevelopmental*) e I (*AI*), pero no la accesibilidad (C); su término de O era *measurement*, que esta versión retira |
| Aljedaani y Mollik (2026) | 10.1145/3800424.3800452 | `RSL/MD/aljedaani-mollik-2026-llm-web-accessibility.md` | No: cubre I (*LLMs*) y C (*accessibility*), sin perfiles cognitivos (P) ni métricas (O); además es de congreso |

Los términos añadidos en las últimas versiones, incluida la ampliación tras el cribado 1, no cambian el resultado: ninguna revisión reúne los cuatro componentes. En dos de ellas, un solo bloque (C u O) las deja fuera. La prueba indica que los bloques C y O, unidos con AND, pueden recortar estudios afines. Queda por formar un conjunto de control de 3 a 5 estudios primarios, tomados de las referencias de estas revisiones, y comprobar en Scopus, bloque a bloque, que la ecuación los recupera.

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

- *User centered design* (p.566): el tema habla de diseño de interfaces adaptativas y personalización, no del diseño centrado en el usuario como método; incluirlo atraería estudios de interacción persona-computador sin componente de ingeniería de software.
- *Performance evaluation* (p.396): en el corpus de software remite al rendimiento del sistema (tiempo, carga), no a métricas de accesibilidad o usabilidad.
- *Auditory system* (p.35): anatomía de la audición; el concepto del tema es la discapacidad auditiva, cubierta por *Deafness* y términos libres.
- *Standards* (p.509): demasiado amplio; la conformidad normativa del tema se busca con WCAG y `accessibility`.
- *Assistive technology* (p.32): el alcance excluye la tecnología de apoyo sin relación con el proceso de ingeniería de software.
- *Mental disorders* (p.320) y *Dementia* (p.128): se excluyen para evitar un enfoque medicalizado y porque quedan fuera de los perfiles estratificados. Por la misma razón se retiró `"cognitive impairment*"`, que recupera sobre todo estudios de diagnóstico de deterioro cognitivo y demencia, y no se usa el descriptor MeSH *Cognition Disorders* (D003072).
- *Neural networks* (p.358) y la sigla `ASD`: las redes neuronales ya se recuperan con `"machine learning"`, y los resúmenes desarrollan la sigla del autismo, que además coincide con Auto-Sklearn y con la comunicación interauricular (*atrial septal defect*).
- El adjetivo `accessible` suelto y `"assistive technology"`: el primero recupera frases como «publicly accessible dataset»; la tecnología de apoyo queda fuera del alcance, como *Assistive technology*.
- `"Section 508"`, `"EN 301 549"` y `"System Usability Scale"`: no suman registros, porque todo resumen que los nombra ya contiene `accessibility` o `usability`, presentes en los mismos bloques.
- Retirados tras el cribado 1 por no aportar registros aceptados (0 SI y al menos 3 NO exclusivos): *Measurement* (p.313), con 10 NO exclusivos, que recuperaba mediciones clínicas; *Deep learning* (p.126), con 4 NO exclusivos, cuyos estudios pertinentes ya recupera `"machine learning"`; y `"Down syndrome"` (MeSH *Down Syndrome*, D004314), con 4 NO exclusivos, cuya población pertinente ya recupera `"intellectual disabilit*"`.
- `"machine-learning"`: se retira por el máximo de 100 keywords; las bases tratan el guion como espacio y recuperaba los mismos 30 registros que `"machine learning"`. `"large language model*"` se sustituye por `"language model"`, que lo incluye.
- *Emotion recognition* (p.171), *Affective computing* (p.14) y `"special needs"`: no se añaden; los dos primeros abren a la detección emocional y a los robots sociales, y el tercero a la educación especial y la discapacidad física sin perfil cognitivo, casos que el alcance excluye.
- *Cognition* (p.85): demasiado amplio (ciencia cognitiva, inteligencia artificial «cognitiva»).
- `COGA` como sigla suelta: coincide con un estudio genético sobre alcoholismo de amplio corpus biomédico; la accesibilidad cognitiva se busca con `"cognitive accessibility"`.
- `blind`: recupera ruido ajeno al tema (ensayos doble ciego); se sustituye por `blindness` y `"visually impaired"`.
- Bloque de contexto (ciclo de vida del software): se retira al pasar a PICO. Como bloque AND, recortaba los estudios que no nombran la fase en el resumen. Sus descriptores eran *Software engineering* (p.497), *Requirements engineering* (p.459), *Software design* (p.497), *Software testing* (p.498), *Automatic testing* (p.36) y *System validation* (p.529), junto con sus términos libres. La fase del ciclo de vida pasa a criterio de inclusión y a dato a extraer de RQ2.

## Criterios de inclusión y exclusión

### Inclusión

- Artículos publicados entre 2021 y 2026, los cinco últimos años completos y el año en curso.
- Artículos de revista revisados por pares, de acceso abierto, en inglés o español.
- Estudios dirigidos a personas con autismo, trastorno por déficit de atención e hiperactividad, discapacidad intelectual, dislexia o dificultades de aprendizaje.
- Estudios en los que la inteligencia artificial interviene en una fase del ciclo de vida del software: requisitos, diseño, desarrollo, personalización, pruebas, verificación o auditoría.
- Estudios con una evaluación empírica, con usuarios o automática, que reporta al menos una métrica o instrumento de evaluación.

### Exclusión

- Registros duplicados entre bases de datos.
- Estudios sin texto completo accesible.
- Revisiones sistemáticas y otros estudios secundarios; se usan solo para delimitar el vacío.
- Preprints, tesis, editoriales y trabajos de congreso.
- Estudios en los que la inteligencia artificial solo diagnostica o detecta la condición, sin un artefacto de software evaluado.
- Estudios de accesibilidad solo sensorial, sin población con discapacidad cognitiva o neurodivergencia.
- Intervenciones pedagógicas o de aprendizaje electrónico, como el diseño universal para el aprendizaje o los recomendadores educativos, sin un artefacto de software evaluado.
- Robots sociales, tutores inteligentes o tecnología de rehabilitación como producto principal, que no intervienen en ninguna fase del ciclo de vida del software.
