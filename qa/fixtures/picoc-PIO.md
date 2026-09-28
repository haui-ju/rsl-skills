# Marco de búsqueda — Inteligencia artificial en el ciclo de vida del software para accesibilidad cognitiva

**Marco:** PIO · **Vocabulario:** IEEE Thesaurus 2019 + términos libres · **Tema:** Inteligencia artificial en el ciclo de vida del software para accesibilidad cognitiva y neurodivergencia: técnicas, fases de ingeniería y métricas de evaluación — una revisión sistemática de la literatura.

Protocolo: [`playbooks/vocabulario-controlado.md`](../../../../playbooks/vocabulario-controlado.md) · Debate: [picoc-debate.md](picoc-debate.md) · Verificación: `pnpm -s picoc:lint docs/<slug>`

## Pregunta general (problemática)

¿Cómo se ha integrado la inteligencia artificial en el ciclo de vida del software para usuarios con discapacidad cognitiva y qué métricas de evaluación se reportan?

## Preguntas por componente

| RQ | Comp. | Pregunta (RQ) | Dato a extraer |
|----|-------|---------------|----------------|
| RQ1 | P | ¿Qué perfiles de discapacidad cognitiva o neurodivergencia (trastorno del espectro autista [TEA], trastorno por déficit de atención e hiperactividad [TDAH], discapacidad intelectual, dificultades de aprendizaje y dislexia) abordan los estudios y con qué grado de estratificación y participación de usuarios? | Condición declarada · estratificación (sí o no) · participación de personas con discapacidad |
| RQ2 | I | ¿Qué técnicas de inteligencia artificial —incluidas la inteligencia artificial generativa (GenAI) y los modelos de lenguaje grandes (LLM)— se han aplicado y con qué rol en el proceso de software? | Familia de técnica (aprendizaje automático, aprendizaje profundo, procesamiento de lenguaje natural, LLM o GenAI) · modelo · rol (generador, evaluador o asistente de aseguramiento de la calidad) |
| RQ3 | O | ¿Qué métricas de evaluación se reportan (usabilidad, accesibilidad cognitiva, legibilidad, calidad de software) y con qué grado de automatización? | Métrica · instrumento · grado de automatización (automatizable en integración continua, semiautomática o solo mediante validación con usuarios) |

## Tabla de componentes (1:1 con las queries)

| Comp. | Concepto | RQ | Keywords | Descriptor IEEE (pág.) | Justificación |
|-------|----------|----|----------|------------------------|---------------|
| P | Usuarios con discapacidad cognitiva o neurodivergencia: autismo, TDAH, discapacidad intelectual, dificultades de aprendizaje y dislexia | RQ1 | `autism` · `autistic` · `"autism spectrum"` · `neurodivers*` · `neurodivergen*` · `neurodevelopmental` · `"cognitive disabilit*"` · `"intellectual disabilit*"` · `"developmental disabilit*"` · `"learning disabilit*"` · `ADHD` · `"attention deficit"` · `dyslexi*` · `"cognitive accessibility"` | Autism (p.35) | Procede de “usuarios con discapacidad cognitiva o neurodivergencia”. IEEE solo codifica *Autism*; los demás perfiles, la neurodiversidad y la accesibilidad cognitiva entran como términos libres. `autistic` recoge el lenguaje de identidad que prefiere la comunidad |
| I | Técnicas de inteligencia artificial, incluidas la GenAI y los LLM | RQ2 | `"artificial intelligence"` · `AI` · `"machine learning"` · `"machine-learning"` · `"deep learning"` · `"natural language processing"` · `NLP` · `"large language model*"` · `LLM` · `LLMs` · `"generative AI"` · `"generative artificial intelligence"` · `ChatGPT` | Artificial intelligence (p.30) · Machine learning (p.294) · Deep learning (p.126) · Natural language processing (p.354) | Procede de “técnicas de inteligencia artificial”. `AI`, `"machine-learning"` y `NLP` son sinónimos aceptados por el tesauro; los LLM, la GenAI y ChatGPT son posteriores a su edición de 2019, por lo que entran como términos libres |
| O | Métricas de evaluación: usabilidad, experiencia de usuario, legibilidad, carga cognitiva y calidad de software | RQ3 | `usability` · `"user experience"` · `measurement` · `metric` · `metrics` · `"accessibility metric"` · `"readability metrics"` · `readability` · `"plain language"` · `"easy-to-read"` · `"software quality"` · `"cognitive load"` | Usability (p.565) · Measurement (p.313) · Readability metrics (p.453) · Software quality (p.498) | Procede de “qué métricas se reportan”. *Metrics* es un término no preferido que el tesauro remite a *Measurement*, por eso se incluyen ambos. El lenguaje claro y la lectura fácil son la forma operativa de la legibilidad para perfiles cognitivos |

## Palabras clave

| Español | Inglés | Comp. | Tipo | Pág. IEEE | Justificación |
|---------|--------|-------|------|-----------|---------------|
| trastorno del espectro autista | Autism | P | IEEE | p.35 | — |
| inteligencia artificial | Artificial intelligence | I | IEEE | p.30 | — |
| aprendizaje automático | Machine learning | I | IEEE | p.294 | — |
| aprendizaje profundo | Deep learning | I | IEEE | p.126 | — |
| procesamiento de lenguaje natural | Natural language processing | I | IEEE | p.354 | — |
| usabilidad | Usability | O | IEEE | p.565 | — |
| métricas | Measurement | O | IEEE (USE desde "metrics") | p.313 | — |
| métricas de legibilidad | Readability metrics | O | IEEE | p.453 | — |
| calidad de software | Software quality | O | IEEE | p.498 | — |
| persona autista | autistic | P | Libre | — | Lenguaje de identidad preferido por la comunidad; IEEE solo tiene *Autism* |
| neurodivergencia | neurodiversity / neurodivergence | P | Libre | — | Concepto sin descriptor en IEEE 2019 |
| trastornos del neurodesarrollo | neurodevelopmental / developmental disability | P | Libre | — | Término de grupo usado en la literatura clínica y asistiva; sin descriptor IEEE |
| discapacidad cognitiva | cognitive disability | P | Libre | — | IEEE solo codifica *Autism* entre los perfiles cognitivos |
| discapacidad intelectual | intellectual disability | P | Libre | — | Sin descriptor IEEE |
| dificultades de aprendizaje | learning disability | P | Libre | — | Sin descriptor IEEE |
| TDAH | ADHD / attention deficit | P | Libre | — | Sin descriptor IEEE |
| dislexia | dyslexia | P | Libre | — | Sin descriptor IEEE |
| accesibilidad cognitiva | cognitive accessibility | P | Libre | — | IEEE 2019 no tiene *Accessibility* |
| modelos de lenguaje grandes | large language models / LLM | I | Libre | — | Concepto posterior a la edición 2019 |
| inteligencia artificial generativa | generative AI / ChatGPT | I | Libre | — | Concepto posterior a la edición 2019 |
| experiencia de usuario | user experience | O | Libre | — | Sin descriptor IEEE (*Quality of experience* pertenece a redes y no es equivalente) |
| métricas de accesibilidad | accessibility metric | O | Libre | — | IEEE 2019 no tiene *Accessibility* |
| lenguaje claro y lectura fácil | plain language / easy-to-read | O | Libre | — | Vocabulario operativo de la legibilidad cognitiva; sin descriptor IEEE |
| carga cognitiva | cognitive load | O | Libre | — | Sin descriptor IEEE |

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
  ( usability OR "user experience" OR measurement OR metric OR metrics OR "accessibility metric"
    OR "readability metrics" OR readability OR "plain language" OR "easy-to-read"
    OR "software quality" OR "cognitive load" )
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
AND ALL=(usability OR "user experience" OR measurement OR metric OR metrics OR "accessibility metric"
  OR "readability metrics" OR readability OR "plain language" OR "easy-to-read"
  OR "software quality" OR "cognitive load")
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
( "IEEE Terms":"Usability" OR "user experience" OR "IEEE Terms":"Measurement" OR metric OR metrics OR "accessibility metric"
  OR "IEEE Terms":"Readability metrics" OR readability OR "plain language" OR "easy-to-read"
  OR "IEEE Terms":"Software quality" OR "cognitive load" )
```


*Nota:* la query usa 8 comodines, por debajo del límite de 10 de IEEE Xplore; los comodines se reservan para el bloque P, donde las variantes morfológicas son muchas. Scopus y Web of Science recuperan los plurales de las frases sin comodín.

## Búsqueda auxiliar — localizar revisiones afines (Scopus; no es el corpus primario)

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

- Artículos de revista o de congreso revisados por pares, en inglés o español.
- Estudios dirigidos a personas con discapacidad cognitiva o neurodivergencia.

### Exclusión

- Registros duplicados entre bases de datos o sin texto completo accesible.
- Revisiones sistemáticas y otros estudios secundarios.
