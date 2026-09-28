# Marco de búsqueda — IA en el ciclo de vida del software para accesibilidad cognitiva

**Marco:** PICOCT · **Vocabulario:** IEEE Thesaurus 2019 + términos libres · **Tema:** Inteligencia artificial en el ciclo de vida del software para accesibilidad cognitiva y neurodivergencia: técnicas, fases de ingeniería y métricas de evaluación — una revisión sistemática de la literatura.

Protocolo: [`playbooks/vocabulario-controlado.md`](../../playbooks/vocabulario-controlado.md) · Verificación: `pnpm -s picoc:lint docs/ia-inclusion-cognitiva-software/picoc.md`

## Pregunta general (problemática)

¿Cómo se han integrado técnicas de inteligencia artificial en las fases del ciclo de vida del software —con énfasis en diseño, personalización en runtime y, sobre todo, verificación, evaluación y auditoría— orientadas a usuarios con discapacidad cognitiva o neurodivergencia; qué métricas se reportan (incluidas orientaciones COGA frente al núcleo WCAG); y qué celdas de la matriz *condición × técnica × fase SE × métrica* permanecen vacías frente al sesgo documentado hacia la accesibilidad sensorial/visual?

## Preguntas por componente

| Comp. | Pregunta (RQ) | Dato a extraer |
|-------|---------------|----------------|
| P | ¿Qué perfiles de discapacidad cognitiva o neurodivergencia (TEA, TDAH, discapacidad intelectual, dificultades de aprendizaje, dislexia) abordan los estudios y con qué grado de estratificación y participación de usuarios? | Condición declarada · estratificación (sí/no) · participación de personas con discapacidad |
| I | ¿Qué técnicas de inteligencia artificial —incluidas GenAI y LLM— se han aplicado y con qué rol en el proceso de software? | Familia de técnica (ML, DL, NLP, LLM/GenAI) · modelo · rol (generador, evaluador, copiloto de QA) |
| C | ¿En qué medida la evidencia sobre accesibilidad cognitiva se contrasta con, o queda subordinada a, la accesibilidad sensorial/visual y la conformidad WCAG? | Tipo de discapacidad cubierta (cognitiva vs sensorial) · marco normativo (WCAG, COGA, ninguno) |
| O | ¿Qué métricas de evaluación se reportan (usabilidad, accesibilidad cognitiva/COGA, legibilidad, calidad de software) y con qué grado de automatización? | Métrica · instrumento · automatizable en CI / semi-automática / solo validación con usuarios |
| Co | ¿En qué fases del ciclo de vida del software (requisitos, diseño, personalización en runtime, testing, V&V, auditoría) se integra la IA y qué peso relativo tienen verificación y evaluación? | Fase SE · artefacto intervenido · celda vacía de la matriz |
| T | ¿Cómo se distribuye la producción entre 2020 y 2026, en particular antes y después de la adopción masiva de GenAI (2023), y por tipo de publicación? | Año · artículo de revista / congreso |

## Tabla de búsqueda (1:1 con las queries)

| Comp. | Concepto (ES) | Origen en el tema | Términos en la query | N | Descriptor IEEE (pág.) | Libres (justificación) |
|-------|---------------|-------------------|----------------------|---|------------------------|------------------------|
| I | Técnicas de IA, incluidas GenAI/LLM | *“técnicas de inteligencia artificial”* (problemática); *“GenAI”* (tema 1.1) | `"artificial intelligence"` · `AI` · `"machine learning"` · `"machine-learning"` · `"deep learning"` · `"natural language processing"` · `NLP` · `"large language model*"` · `LLM*` · `"generative AI"` · `"generative artificial intelligence"` | 11 | Artificial intelligence (p.30) · Machine learning (p.294) · Deep learning (p.126) · Natural language processing (p.354) | `AI`, `"machine-learning"`, `NLP`: UF oficiales. LLM/GenAI: conceptos posteriores a la edición 2019 |
| P | Usuarios con discapacidad cognitiva o neurodivergencia (TEA, TDAH, DI, dificultades de aprendizaje, dislexia) | *“usuarios con discapacidad cognitiva o neurodivergencia”* (problemática); *“orientaciones COGA”* (problemática) | `autism` · `"autism spectrum"` · `neurodivers*` · `neurodivergen*` · `"cognitive disabilit*"` · `"cognitive impairment*"` · `"intellectual disabilit*"` · `"learning disabilit*"` · `ADHD` · `"attention deficit"` · `dyslexi*` · `"cognitive accessibility"` · `COGA` | 13 | Autism (p.35) | IEEE solo codifica *Autism*; el resto de perfiles, la neurodiversidad y COGA (W3C) no tienen descriptor |
| Co | Ciclo de vida del software: requisitos, diseño, personalización en runtime, testing, V&V y auditoría | *“fases del ciclo de vida del software —diseño, personalización en runtime, verificación, evaluación y auditoría”* (problemática); *“requisitos y diseño de interfaces adaptativas”* (objeto); *“frente al núcleo WCAG”* (problemática) | `"software engineering"` · `"software development"` · `"software development life cycle"` · `SDLC` · `"requirements engineering"` · `"software design"` · `"adaptive user interface*"` · `personaliz*` · `"software testing"` · `"verification and validation"` · `"system validation"` · `"accessibility evaluation"` · `"accessibility testing"` · `"accessibility audit*"` · `WCAG` | 15 | Software engineering (p.497) · Requirements engineering (p.459) · Software design (p.497) · Software testing (p.498) · System validation (p.529) | SDLC, V&V como par, personalización, interfaces adaptativas y evaluación/auditoría de accesibilidad: sin descriptor IEEE. WCAG: estándar W3C |

## Cribado / extracción (no entran a la query)

| Comp. | Concepto (ES) | Origen en el tema | Descriptores / términos | Uso |
|-------|---------------|-------------------|-------------------------|-----|
| C | Accesibilidad sensorial/visual y conformidad WCAG | *“sesgo documentado hacia la accesibilidad sensorial/visual”* (problemática); *“sesgo visual/WCAG-duro”* (objeto) | Blindness (p.54) · Deafness (p.125) · "visual impairment" (libre) · "screen reader" (libre) | Codificar en la extracción el contraste cognitivo vs sensorial; como bloque de búsqueda recortaría justo la evidencia a contrastar |
| O | Métricas de evaluación: usabilidad, accesibilidad cognitiva, legibilidad, calidad de software | *“qué métricas se reportan (incluidas orientaciones COGA frente al núcleo WCAG)”* (problemática) | Usability (p.565) · Measurement (p.313; USE desde "metrics") · Performance evaluation (p.396) · Readability metrics (p.453) · Software quality (p.498) · "cognitive load" (libre) · "user experience" (libre) · "accessibility metric" (libre) | Cribado de títulos/resúmenes y hoja de extracción (métrica, instrumento, automatización). Fuera de la query para no exigir que el resumen nombre la métrica |

## T — Filtros

| Base | Filtro |
|------|--------|
| Scopus | `PUBYEAR > 2019` · `DOCTYPE` = `ar` (artículo) o `cp` (congreso) |
| Web of Science | `PY=(2020-2026)` · `DT=(Article OR Proceedings Paper)` |
| IEEE Xplore | Año 2020–2026 · Journals + Conferences (filtros de la interfaz) |

## Palabras clave

| Español | Inglés | Tipo | Pág. IEEE |
|---------|--------|------|-----------|
| inteligencia artificial | artificial intelligence | IEEE | p.30 |
| aprendizaje automático | machine learning | IEEE | p.294 |
| aprendizaje profundo | deep learning | IEEE | p.126 |
| procesamiento de lenguaje natural | natural language processing | IEEE | p.354 |
| modelos de lenguaje grandes | large language models | Libre | — |
| IA generativa | generative AI | Libre | — |
| trastorno del espectro autista | autism | IEEE | p.35 |
| neurodivergencia | neurodiversity / neurodivergence | Libre | — |
| discapacidad cognitiva | cognitive disability | Libre | — |
| discapacidad intelectual | intellectual disability | Libre | — |
| dificultades de aprendizaje | learning disability | Libre | — |
| TDAH | ADHD / attention deficit | Libre | — |
| dislexia | dyslexia | Libre | — |
| accesibilidad cognitiva | cognitive accessibility / COGA | Libre | — |
| ingeniería de software | software engineering | IEEE | p.497 |
| ciclo de vida del software | software development life cycle | Libre | — |
| ingeniería de requisitos | requirements engineering | IEEE | p.459 |
| diseño de software | software design | IEEE | p.497 |
| interfaces adaptativas / personalización | adaptive user interface / personalization | Libre | — |
| pruebas de software | software testing | IEEE | p.498 |
| verificación y validación | verification and validation | Libre | — |
| validación de sistemas | system validation | IEEE | p.529 |
| evaluación / auditoría de accesibilidad | accessibility evaluation / accessibility audit | Libre | — |
| WCAG | Web Content Accessibility Guidelines | Libre | — |
| usabilidad (cribado O) | usability | IEEE | p.565 |
| métricas (cribado O) | metrics → Measurement | IEEE (USE desde "metrics") | p.313 |
| métricas de legibilidad (cribado O) | readability metrics | IEEE | p.453 |
| calidad de software (cribado O) | software quality | IEEE | p.498 |

## Query Scopus

```text
TITLE-ABS-KEY (
  ( "artificial intelligence" OR AI OR "machine learning" OR "machine-learning" OR "deep learning"
    OR "natural language processing" OR NLP OR "large language model*" OR LLM*
    OR "generative AI" OR "generative artificial intelligence" )
  AND
  ( autism OR "autism spectrum" OR neurodivers* OR neurodivergen* OR "cognitive disabilit*"
    OR "cognitive impairment*" OR "intellectual disabilit*" OR "learning disabilit*"
    OR ADHD OR "attention deficit" OR dyslexi* OR "cognitive accessibility" OR COGA )
  AND
  ( "software engineering" OR "software development" OR "software development life cycle" OR SDLC
    OR "requirements engineering" OR "software design" OR "adaptive user interface*" OR personaliz*
    OR "software testing" OR "verification and validation" OR "system validation"
    OR "accessibility evaluation" OR "accessibility testing" OR "accessibility audit*" OR WCAG )
)
AND PUBYEAR > 2019
AND ( LIMIT-TO ( DOCTYPE , "ar" ) OR LIMIT-TO ( DOCTYPE , "cp" ) )
```

## Query Web of Science

```text
(ALL=("artificial intelligence" OR AI OR "machine learning" OR "machine-learning" OR "deep learning"
  OR "natural language processing" OR NLP OR "large language model*" OR LLM*
  OR "generative AI" OR "generative artificial intelligence"))
AND ALL=(autism OR "autism spectrum" OR neurodivers* OR neurodivergen* OR "cognitive disabilit*"
  OR "cognitive impairment*" OR "intellectual disabilit*" OR "learning disabilit*"
  OR ADHD OR "attention deficit" OR dyslexi* OR "cognitive accessibility" OR COGA)
AND ALL=("software engineering" OR "software development" OR "software development life cycle" OR SDLC
  OR "requirements engineering" OR "software design" OR "adaptive user interface*" OR personaliz*
  OR "software testing" OR "verification and validation" OR "system validation"
  OR "accessibility evaluation" OR "accessibility testing" OR "accessibility audit*" OR WCAG)
AND PY=(2020-2026)
AND DT=(Article OR Proceedings Paper)
```

## Query IEEE Xplore

```text
( "IEEE Terms":"Artificial intelligence" OR AI OR "IEEE Terms":"Machine learning" OR "machine-learning"
  OR "IEEE Terms":"Deep learning" OR "IEEE Terms":"Natural language processing" OR NLP
  OR "large language model*" OR LLM* OR "generative AI" OR "generative artificial intelligence" )
AND
( "IEEE Terms":"Autism" OR "autism spectrum" OR neurodivers* OR neurodivergen* OR "cognitive disabilit*"
  OR "cognitive impairment*" OR "intellectual disabilit*" OR "learning disabilit*"
  OR ADHD OR "attention deficit" OR dyslexi* OR "cognitive accessibility" OR COGA )
AND
( "IEEE Terms":"Software engineering" OR "software development" OR "software development life cycle" OR SDLC
  OR "IEEE Terms":"Requirements engineering" OR "IEEE Terms":"Software design" OR "adaptive user interface*" OR personaliz*
  OR "IEEE Terms":"Software testing" OR "verification and validation" OR "IEEE Terms":"System validation"
  OR "accessibility evaluation" OR "accessibility testing" OR "accessibility audit*" OR WCAG )
```

*Nota:* IEEE Xplore limita el número de comodines por consulta; si la rechaza, dividirla por bloque P y unir resultados, sin quitar términos.

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
AND PUBYEAR > 2019
```

## Descriptores revisados y excluidos

- *Neural networks* (p.358), `chatbot*`: no nacen del tema; *Deep learning* ya cubre las redes neuronales y los chatbots quedan dentro de LLM/GenAI.
- *User centered design* (p.566): el tema habla de diseño de interfaces adaptativas y personalización, no de UCD como método; arrastraría corpus HCI puro.
- *Formal verification* (p.199): verificación matemática de programas, ajena a la V&V de accesibilidad del tema.
- *System testing* (p.529): NT de *System validation*; nivel de prueba específico ya cubierto por *Software testing*.
- *Software quality* (p.498): movido a O (cribado); es resultado, no fase del ciclo de vida.
- *Assistive technology* (p.32): el alcance excluye tecnología asistiva sin componente de proceso SE.
- *Mental disorders* (p.320), *Dementia* (p.128): salvaguarda anti-medicalización; fuera de la estratificación.
- *Cognition* (p.85): demasiado amplio (ciencia cognitiva, IA “cognitiva”).
- *User interfaces*: genérico; reabre el corpus HCI (el concepto del tema es interfaz **adaptativa**, libre).

## Términos libres (sin descriptor IEEE)

- **P:** neurodivergencia, discapacidad cognitiva/intelectual, dificultades de aprendizaje, TDAH, dislexia, accesibilidad cognitiva, COGA — IEEE 2019 solo codifica *Autism*.
- **I:** LLM, GenAI — conceptos posteriores a la edición 2019.
- **Co:** SDLC, desarrollo de software, V&V como par, personalización, interfaces adaptativas, evaluación/pruebas/auditoría de accesibilidad, WCAG — sin descriptor IEEE; WCAG es estándar W3C.
- Se reportan como texto libre en el protocolo, nunca como descriptores IEEE.
