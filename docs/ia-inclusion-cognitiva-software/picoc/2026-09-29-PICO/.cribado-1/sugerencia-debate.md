# Debate de la sugerencia de keywords (cribado 1)

## Defensor

Base: 120 registros únicos del cribado 1 (`keywords.md`), tesauro revisado (`thesaurus.md`, más `thesaurus:check` de *Text processing*, *Contrastive learning*, *Emotion recognition*, *Interactive computer systems*, *Automation*, *Students* y *Websites*) y el picoc `2026-09-29-PICO`. No hay un cribado anterior de este tema con términos retirados por evidencia; los retirados del picoc (`"cognitive impairment*"`, `ASD`, `blind`, `accessible`, `COGA`, `"assistive technology"`) salieron por debate y ruido documentado, no por un cribado, y no se reintroducen.

Regla de retiro aplicada: 0 SI en total (las dudas cuentan como SI) y al menos 3 NO exclusivos. Solo la cumplen `"Down syndrome"` (0 SI, 4 NO exclusivos), `"deep learning"` (0 SI, 4 NO exclusivos) y `measurement` (0 SI, 10 NO exclusivos).

### Términos actuales

| Comp. | Término | Estado | Evidencia | Propuesta |
|---|---|---|---|---|
| P | `autism` · `autistic` · `"autism spectrum"` · `neurodivers*` · `neurodivergen*` · `neurodevelopmental` · `"cognitive disabilit*"` · `"intellectual disabilit*"` · `"developmental disabilit*"` · `"learning disabilit*"` · `ADHD` · `"attention deficit"` · `dyslexi*` · `"cognitive accessibility"` | vale | Todos con SI; `dyslexi*` (7 SI exclusivos), `"intellectual disabilit*"` (4) y `neurodivergen*`, `neurodevelopmental`, `"learning disabilit*"` (2 cada uno) sostienen recall propio | Se quedan |
| P | `"Down syndrome"` | quitar | 4 registros, 0 SI, 4 NO exclusivos | Retirar del bloque P; los estudios de síndrome de Down que nombran la discapacidad intelectual siguen entrando por `"intellectual disabilit*"` |
| P | `"learning disorder*"` · `"learning difficult*"` | no aporta | 0 SI; solo 1 y 2 NO exclusivos | Se quedan (no alcanzan 3 NO exclusivos) |
| P | `Asperger` · `"intellectual developmental disorder"` · `dyscalculia` | no aporta | 0 registros | Se quedan (sin coste de ruido) |
| I | `"artificial intelligence"` · `AI` · `"machine learning"` · `"machine-learning"` · `"natural language processing"` · `NLP` · `"large language model*"` · `LLM` · `LLMs` · `"generative AI"` · `"generative artificial intelligence"` · `ChatGPT` · `GPT` · `chatbot` · `"text simplification"` · `"speech recognition"` | vale | Todos con SI; `AI` (3 SI exclusivos), `"artificial intelligence"`, `"natural language processing"` y `"speech recognition"` (2 cada uno) | Se quedan |
| I | `"deep learning"` | quitar | 11 registros, 0 SI, 4 NO exclusivos (clasificación y diagnóstico, CE5) | Retirar; *Deep learning* es NT de *Machine learning* (p.294), que sigue en el bloque |
| I | `"computer vision"` · `"conversational agents"` | no aporta | 0 SI; 0 y 1 NO exclusivos | Se quedan |
| I | `"adaptive user interface"` · `"recommender systems"` · `"natural language generation"` | no aporta | 0 registros | Se quedan |
| C | `deaf` · `"visually impaired"` · `"low vision"` · `"hearing impairment"` · `WCAG` · `"Web Content Accessibility Guidelines"` · `accessibility` · `"accessible interface"` · `"inclusive design"` · `"universal design"` | vale | Todos con SI; `accessibility` sostiene 23 SI exclusivos | Se quedan |
| C | `blindness` · `deafness` · `"visual impairment"` | no aporta | 0 SI; 2, 1 y 0 NO exclusivos | Se quedan (sostienen la RQ3) |
| C | `"hearing impaired"` · `"sensory impairment"` · `"screen reader"` · `"accessible design"` | no aporta | 0 registros | Se quedan |
| O | `usability` · `"user experience"` · `metric` · `metrics` · `"readability metrics"` · `readability` · `"plain language"` · `"easy-to-read"` · `"cognitive load"` · `"accessibility evaluation"` · `"user study"` · `comprehension` · `understandability` | vale | Todos con SI; `usability` (12 SI exclusivos), `readability` y `comprehension` (3 cada uno) | Se quedan |
| O | `measurement` | quitar | 12 registros, 0 SI, 10 NO exclusivos (mediciones clínicas y de sensores) | Retirar; *Metrics*, UF de *Measurement* (p.313), sigue como `metric` y `metrics` con 4 SI |
| O | `"user satisfaction"` | no aporta | 0 SI; 1 NO exclusivo | Se queda |
| O | `"accessibility metric"` · `"software quality"` · `"accessibility testing"` · `"accessibility audit"` · `"accessibility assessment"` | no aporta | 0 registros | Se quedan (`"software quality"` conserva la identidad de ingeniería de software) |

### Términos nuevos

| Comp. | Término | Estado | Evidencia | Propuesta |
|---|---|---|---|---|
| I | `"language model*"` | agregar | 7 SI y 2 NO con «language model» en palabras clave, sin cubrir | OR en el bloque I; término libre (ACM CCS *Language models*); recoge modelos de lenguaje que no se declaran «large» |
| I | `"prompt engineering"` | agregar | 4 SI y 0 NO, sin cubrir | OR en el bloque I; término libre (sin descriptor IEEE) |
| I | `"text processing"` | agregar | 3 SI y 0 NO, sin cubrir | OR en el bloque I; IEEE *Text processing* (p.539) |
| I | `"text analysis"` · `"text mining"` | agregar | «text analysis» y «automated text analysis» con 1 SI y 0 NO cada una | OR en el bloque I; IEEE *Text analysis* (p.539) y *Text mining* (p.539) |
| I | `"lexical simplification"` · `"text adaptation"` | agregar | Variantes de la simplificación de textos (5 SI); ampliación desde el tesauro | OR en el bloque I; términos libres (sin descriptor IEEE) |
| I | `"computational linguistics"` | agregar | Afín a *Natural language processing* (7 SI); ampliación desde el tesauro | OR en el bloque I; IEEE *Computational linguistics* (p.95) |
| I | `"generative adversarial network*"` | agregar | 2 SI y 0 NO, sin cubrir | OR en el bloque I; IEEE *Generative adversarial networks* (p.210), UF GAN (la sigla suelta no se usa por ambigua) |
| I | `"fuzzy logic"` · `"fuzzy inference"` | agregar | «fuzzy logic system(s)» y «fuzzy inference» con 1 SI y 0 NO | OR en el bloque I; IEEE *Fuzzy logic* (p.205), UF *Fuzzy inference* |
| I | `"intelligent agent*"` · `"virtual agent*"` | agregar | «virtual agents» y «agent based» con 1 SI y 0 NO | OR en el bloque I; IEEE *Intelligent agents* (p.261) y término libre; complementan `chatbot` |
| I | `"ambient intelligence"` | agregar | 2 SI y 0 NO, sin cubrir | OR en el bloque I; IEEE *Ambient intelligence* (p.19) |
| I | `"context awareness"` · `"context-aware"` | agregar | «context and user awareness» 1 SI y 0 NO; NT de *Artificial intelligence* | OR en el bloque I; IEEE *Context awareness* (p.106); cubre la personalización en tiempo de ejecución |
| I | `"reinforcement learning"` | agregar | NT de *Machine learning*; ampliación desde el tesauro | OR en el bloque I; IEEE *Reinforcement learning* (p.457); técnica habitual en interfaces adaptativas |
| I | `"contrastive learning"` | agregar | 3 SI y 3 NO, sin cubrir | OR en el bloque I; término libre (sin descriptor IEEE) |
| I | `"affective computing"` · `"emotion recognition"` | agregar | «emotion recognition» 2 SI y 2 NO; *Affective computing* es NT de *Artificial intelligence* | OR en el bloque I; IEEE *Affective computing* (p.14) y *Emotion recognition* (p.171); vigilar CE5 en el cribado |
| P | `"special needs"` | agregar | Ampliación desde el tesauro (incluye «special educational needs») | OR en el bloque P; término libre (sin descriptor IEEE) |
| P | `dysgraphia` · `"reading disabilit*"` | agregar | Perfiles afines a la dislexia (8 SI); ampliación desde el tesauro | OR en el bloque P; términos libres (sin descriptor IEEE) |
| C | `"digital inclusion"` | agregar | «digital technologies» y «economic and social effects» con SI sin NO; ampliación desde el tesauro | OR en el bloque C; término libre (sin descriptor IEEE) |
| O | `ergonomics` · `"human engineering"` | agregar | «human engineering» 6 SI y 2 NO, sin cubrir | OR en el bloque O; IEEE *Ergonomics* (p.178), UF *Human engineering* |
| O | `"easy read"` | agregar | Variante de `"easy-to-read"` (4 SI); ampliación desde el tesauro | OR en el bloque O; término libre (sin descriptor IEEE) |
| O | `"user acceptance"` · `"human evaluation"` | agregar | Formas de reportar la evaluación con usuarios; ampliación desde el tesauro | OR en el bloque O; términos libres (sin descriptor IEEE) |
| — | `students` · `"inclusive education"` · `"educational technology"` | descartar | 8/5, 3/2 y 2/2 SI/NO | Abren a estudiantes típicos y a pedagogía sin software (CE7) |
| — | `"smart homes"` · `"ambient assisted living"` | descartar | 2/0 y 1/0 SI/NO | Tecnología de apoyo y domótica como producto principal (CE8; *Assistive technology* ya excluido en el picoc) |
| — | `automation` · `"interactive computer systems"` · `"software design"` · `"mobile applications"` · `"serious games"` · `websites` | descartar | 4/0, 4/1, 3/0, 2/0, 2/0 y 2/0 SI/NO | No son técnicas de IA ni encajan en P, C u O; en el bloque I dejarían entrar software sin IA (contra CI4). `"cognitive loads"` y «automatic speech recognition» ya los cubren `"cognitive load"` y `"speech recognition"` |

### Query Scopus propuesta

```text
TITLE-ABS-KEY (
  ( autism OR autistic OR "autism spectrum" OR neurodivers* OR neurodivergen*
    OR neurodevelopmental OR "cognitive disabilit*" OR "intellectual disabilit*"
    OR "developmental disabilit*" OR "learning disabilit*" OR ADHD OR "attention deficit"
    OR dyslexi* OR "cognitive accessibility" OR Asperger
    OR "intellectual developmental disorder" OR "learning disorder*"
    OR "learning difficult*" OR dyscalculia OR "special needs" OR dysgraphia
    OR "reading disabilit*" )
  AND
  ( "artificial intelligence" OR AI OR "machine learning" OR "machine-learning"
    OR "natural language processing" OR NLP OR "large language model*" OR LLM
    OR LLMs OR "language model*" OR "generative AI" OR "generative artificial intelligence"
    OR ChatGPT OR GPT OR "prompt engineering" OR "computer vision" OR chatbot
    OR "conversational agents" OR "intelligent agent*" OR "virtual agent*"
    OR "text simplification" OR "lexical simplification" OR "text adaptation"
    OR "text processing" OR "text analysis" OR "text mining" OR "computational linguistics"
    OR "adaptive user interface" OR "speech recognition" OR "recommender systems"
    OR "natural language generation" OR "generative adversarial network*"
    OR "fuzzy logic" OR "fuzzy inference" OR "ambient intelligence" OR "context awareness"
    OR "context-aware" OR "reinforcement learning" OR "contrastive learning"
    OR "affective computing" OR "emotion recognition" )
  AND
  ( blindness OR deafness OR deaf OR "visual impairment" OR "visually impaired" OR "low vision"
    OR "hearing impairment" OR "hearing impaired" OR "sensory impairment" OR "screen reader"
    OR WCAG OR "Web Content Accessibility Guidelines" OR accessibility OR "accessible design"
    OR "accessible interface" OR "inclusive design" OR "universal design"
    OR "digital inclusion" )
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

### Query Web of Science propuesta

```text
ALL=(autism OR autistic OR "autism spectrum" OR neurodivers* OR neurodivergen*
  OR neurodevelopmental OR "cognitive disabilit*" OR "intellectual disabilit*"
  OR "developmental disabilit*" OR "learning disabilit*" OR ADHD OR "attention deficit"
  OR dyslexi* OR "cognitive accessibility" OR Asperger OR "intellectual developmental disorder"
  OR "learning disorder*" OR "learning difficult*" OR dyscalculia OR "special needs"
  OR dysgraphia OR "reading disabilit*")
AND ALL=("artificial intelligence" OR AI OR "machine learning" OR "machine-learning"
  OR "natural language processing" OR NLP OR "large language model*" OR LLM OR LLMs
  OR "language model*" OR "generative AI" OR "generative artificial intelligence" OR ChatGPT
  OR GPT OR "prompt engineering" OR "computer vision" OR chatbot OR "conversational agents"
  OR "intelligent agent*" OR "virtual agent*" OR "text simplification"
  OR "lexical simplification" OR "text adaptation" OR "text processing" OR "text analysis"
  OR "text mining" OR "computational linguistics" OR "adaptive user interface"
  OR "speech recognition" OR "recommender systems" OR "natural language generation"
  OR "generative adversarial network*" OR "fuzzy logic" OR "fuzzy inference"
  OR "ambient intelligence" OR "context awareness" OR "context-aware"
  OR "reinforcement learning" OR "contrastive learning" OR "affective computing"
  OR "emotion recognition")
AND ALL=(blindness OR deafness OR deaf OR "visual impairment" OR "visually impaired"
  OR "low vision" OR "hearing impairment" OR "hearing impaired" OR "sensory impairment"
  OR "screen reader" OR WCAG OR "Web Content Accessibility Guidelines" OR accessibility
  OR "accessible design" OR "accessible interface" OR "inclusive design" OR "universal design"
  OR "digital inclusion")
AND ALL=(usability OR "user experience" OR metric OR metrics
  OR "accessibility metric" OR "readability metrics" OR readability OR "plain language"
  OR "easy-to-read" OR "easy read" OR "software quality" OR "cognitive load"
  OR "accessibility evaluation" OR "accessibility testing" OR "user study" OR comprehension
  OR understandability OR "user satisfaction" OR "accessibility audit"
  OR "accessibility assessment" OR ergonomics OR "human engineering" OR "user acceptance"
  OR "human evaluation")
AND PY=(2021-2026) AND DT=(Article) AND LA=(English OR Spanish)
```

Filtro de la interfaz: Open Access (Web of Science no tiene etiqueta de campo para el acceso abierto).

### Límite honesto de la defensa

- Los términos nuevos que vienen del tesauro (`"reinforcement learning"`, `"lexical simplification"`, `"text adaptation"`, `"computational linguistics"`, `"special needs"`, `dysgraphia`, `"reading disabilit*"`, `"digital inclusion"`, `"easy read"`, `"user acceptance"`, `"human evaluation"`) no tienen evidencia en este cribado, porque la query actual no podía traerlos; su valor solo se mide al correr la query propuesta.
- `"emotion recognition"`, `"affective computing"` y `"contrastive learning"` tienen tantos NO como SI o riesgo de CE5; son los primeros candidatos a retirar si el volumen de NO crece.
- `"special needs"` y `ergonomics` amplían bastante el universo; el AND con los otros tres bloques acota el ruido, pero conviene comparar el número de registros con los 120 actuales.
- La query de IEEE Xplore no se reescribe: los comodines nuevos (`"reading disabilit*"`, `"language model*"`, `"intelligent agent*"`, `"virtual agent*"`, `"generative adversarial network*"`) superarían el límite de 10; habría que pasarlos a frases cerradas.

## Crítico

| Comp. | Término | Propuesta | Tu posición | Motivo |
|---|---|---|---|---|
| I | `"text processing"` | agregar | no agregar | IEEE p.539: UF *Word processing*, BT *Data processing*; no es técnica de IA (CI4), igual que `automation` |
| I | `"emotion recognition"` · `"affective computing"` | agregar | no agregar | En autismo abre a detección emocional y robots sociales (CE5, CE8); 2 SI/2 NO; BT *User interfaces* |
| I | `"virtual agent*"` | agregar | no agregar | Agentes virtuales para entrenamiento de habilidades sociales: tutor como producto (CE8); evidencia 1 SI solamente |
| I | `"reinforcement learning"` | agregar | no agregar | Sin evidencia; en autismo domina robótica social y terapia adaptativa (CE8); `"machine learning"` ya cubre el resto |
| I | `"text mining"` | agregar | no agregar | Sin evidencia propia; minería de historias clínicas y redes para detectar la condición (CE5); `"text analysis"` basta |
| P | `"special needs"` | agregar | no agregar | Abre a educación especial y discapacidad física sin artefacto (CE7); no nombra un perfil cognitivo de RQ1 |
| C | `"digital inclusion"` | agregar (evidencia: «digital technologies», «economic and social effects») | agregar solo por tesauro | Esas palabras clave no son inclusión digital; evidencia mal atribuida, declarar «sin evidencia» |
| P | `"Down syndrome"` | quitar | quitar y actualizar picoc | Cumple la regla, pero el concepto P dice «incluido el síndrome de Down»: reescribir concepto y fila MeSH |
| I | `"deep learning"` | quitar | quitar y actualizar picoc | Cumple la regla; romper la justificación de *Neural networks* («ya se recuperan con deep learning»); retirar descriptor p.126 |
| O | `measurement` | quitar | quitar y actualizar picoc | Cumple la regla; quedan `metric`/`metrics` (UF) sin su preferido: reescribir «se incluyen ambos» y la fila USE |
| — | Query IEEE Xplore | no se reescribe | reescribir | La tabla debe ser 1:1 con todas las queries; pasar comodines nuevos a frases cerradas y retirar `"IEEE Terms":"Deep learning"`/`"Measurement"` |
| I | `"language model*"` · `"large language model*"` | ambos | dejar solo `"language model*"` | Error de query menor: la frase con comodín ya recupera «large language model(s)»; redundante en Scopus y WoS |

Sintaxis de Scopus y Web of Science: paréntesis balanceados, comodines en frase válidos en ambas bases, filtros correctos; sin errores bloqueantes.
