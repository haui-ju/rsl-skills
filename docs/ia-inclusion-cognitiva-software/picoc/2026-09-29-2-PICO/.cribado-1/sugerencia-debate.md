# Debate de la sugerencia de keywords (cribado 1, 2026-09-29-2-PICO)

## Defensor

La query vigente ya tiene 100 keywords (P 21, I 37, C 18, O 24), así que cada término nuevo exige liberar un hueco. Solo un término cumple la regla de retirada (0 SI y al menos 3 NO exclusivos); los otros cinco huecos salen de variantes que otro término del mismo bloque ya recupera en Scopus y Web of Science (0 registros exclusivos, no se pierde ningún SI).

### Rendimiento y propuesta

| Comp. | Término | Estado | Evidencia | Propuesta |
|---|---|---|---|---|
| P | `dyslexi*` | vale | 9 SI, 8 SI exclusivos | Se queda |
| P | `"intellectual disabilit*"` | vale | 8 SI, 5 SI exclusivos | Se queda |
| P | `neurodivergen*` · `"cognitive disabilit*"` · `"learning disabilit*"` · `"cognitive accessibility"` · `neurodevelopmental` · `neurodivers*` · `autism` | vale | Cada uno aporta al menos 1 SI exclusivo | Se quedan |
| P | `adhd` · `"attention deficit"` · `autistic` · `"developmental disabilit*"` | vale | SI > 0, sin SI exclusivos | Se quedan |
| P | `"learning difficult*"` | quitar | 0 SI, 4 NO exclusivos | Retirar (cumple la regla) |
| P | `"autism spectrum"` | quitar (redundante) | 5 SI, 0 exclusivos; toda frase «autism spectrum» contiene `autism` | Retirar por el máximo de 100; en IEEE Xplore cambiar `"IEEE Terms":"Autism"` por `autism` en texto libre para no perder la frase |
| P | `"learning disorder*"` · `dysgraphia` · `"reading disabilit*"` | no aporta | 0 SI, menos de 3 NO exclusivos | Se quedan (no cumplen la regla de retirada) |
| P | `Asperger` · `"intellectual developmental disorder"` · `dyscalculia` | no aporta | 0 registros | Se quedan |
| I | `ai` · `"artificial intelligence"` · `"natural language processing"` · `"speech recognition"` · `chatbot` · `"text processing"` · `"context-aware"` | vale | Cada uno aporta al menos 1 SI exclusivo | Se quedan |
| I | `"language model"` · `llm` · `llms` · `"prompt engineering"` · `"text simplification"` · `"contrastive learning"` y demás con SI > 0 | vale | SI > 0, sin exclusivos | Se quedan |
| I | `"generative artificial intelligence"` | quitar (redundante) | 2 SI, 0 exclusivos; contiene `"artificial intelligence"` | Retirar por el máximo de 100 |
| I | `"generative AI"` | quitar (redundante) | 2 SI, 0 exclusivos; contiene `AI` | Retirar por el máximo de 100 |
| I | `"conversational agents"` | no aporta | 0 SI, 1 NO exclusivo | Se queda |
| I | `"text mining"` · `"adaptive user interface"` · `"recommender systems"` · `"natural language generation"` · `"context awareness"` | no aporta | 0 registros | Se quedan |
| I | `"cognitive systems"` | agregar | 3 SI y 2 NO con «cognitive systems» en palabras clave, sin cubrir; NT de *Artificial intelligence* | OR en el bloque I; IEEE *Cognitive systems* (p.86), UF *Cognitive computing* |
| I | `automation` | agregar | 3 SI y 0 NO, sin cubrir (junto con «semi-automatics» y «manual process», 2 SI y 0 NO cada una); su NT *Automatic testing* es la verificación automatizada que prioriza la pregunta | OR en el bloque I; IEEE *Automation* (p.36) |
| I | `"large language models"` · `"language models"` · `"virtual agents"` | ya cubierto | 5 SI, 2 SI y 1 SI; el análisis los marca sin cubrir por coincidencia literal, pero `"language model"` y `"virtual agent"` recuperan el plural en ambas bases | No agregar |
| C | `accessibility` | vale | 34 SI, 23 SI exclusivos | Se queda |
| C | `"inclusive design"` · `blindness` · `"low vision"` · `"accessible interface"` · `"digital inclusion"` | vale | Al menos 1 SI exclusivo | Se quedan |
| C | `wcag` · `"visually impaired"` · `deaf` · `"hearing impairment"` · `"universal design"` | vale | SI > 0 | Se quedan |
| C | `"Web Content Accessibility Guidelines"` | quitar (redundante) | 2 SI, 0 exclusivos; contiene `accessibility` | Retirar por el máximo de 100 |
| C | `deafness` · `"visual impairment"` · `"screen reader"` | no aporta | 0 SI, menos de 3 NO exclusivos | Se quedan |
| C | `"hearing impaired"` · `"sensory impairment"` · `"accessible design"` | no aporta | 0 registros | Se quedan |
| C | `"co-design"` | agregar | «co-design», «co-designs» y «co-designing» suman 5 SI y 3 NO, sin cubrir | OR en el bloque C, junto al diseño inclusivo; término libre (sin descriptor IEEE) |
| C | `"user centered design"` | agregar | 2 SI y 1 NO, sin cubrir | OR en el bloque C; IEEE *User centered design* (p.566), UF *User-centred design*. Revisa la exclusión previa: el bloque C ya incluye `"inclusive design"` y el ciclo de vida se exige como criterio, no como bloque |
| C | `pictograms` | agregar | 2 SI y 0 NO, sin cubrir; soporte de accesibilidad cognitiva afín a la lectura fácil | OR en el bloque C; término libre (sin descriptor IEEE) |
| C | `"augmentative and alternative communication"` | agregar | 1 SI y 0 NO, sin cubrir; formato de comunicación central en autismo y discapacidad intelectual | OR en el bloque C; término libre (sin descriptor IEEE). Riesgo: dispositivos de apoyo, que se filtran por el CE de tecnología de apoyo |
| O | `usability` | vale | 20 SI, 12 SI exclusivos | Se queda |
| O | `readability` · `"human engineering"` · `"user experience"` · `"cognitive load"` · `comprehension` · `ergonomics` | vale | Al menos 1 SI exclusivo | Se quedan |
| O | `"plain language"` · `"easy-to-read"` · `metrics` · `metric` · `"user study"` y demás con SI > 0 | vale | SI > 0 | Se quedan |
| O | `"accessibility metric"` | quitar (redundante) | 0 registros; `metric` ya lo recupera | Retirar por el máximo de 100 |
| O | `"easy read"` · `"user acceptance"` | no aporta | 0 SI, 2 y 1 NO exclusivos | Se quedan |
| O | `"software quality"` · `"accessibility testing"` · `"accessibility audit"` · `"accessibility assessment"` | no aporta | 0 registros | Se quedan |

### Candidatos descartados

| Término | Evidencia | Motivo |
|---|---|---|
| `"mobile applications"` (IEEE p.336) · `"software design"` (IEEE p.497) | 3 SI y 0 NO cada uno | El mejor indicio de artefacto de software, pero no encaja en ningún bloque del PICO: el bloque de contexto se retiró y en I, C u O abriría a aplicaciones sin IA. Se recomienda usarlos como dato de extracción, no en la query |
| `"user profile"` · `"interactive computer systems"` · `"real-time"` | 3 SI y 0 NO; 4 SI y 2 NO; 3 SI y 1 NO | Sin bloque natural; indizadores genéricos de Scopus |
| `"serious games"` (USE *Games*) | 2 SI y 0 NO | Abre a la pedagogía sin artefacto evaluado (CE) y no es técnica de IA |
| `"emotion recognition"` (IEEE p.171) | 2 SI y 2 NO | Ya excluido: abre a la detección emocional y a los robots sociales |
| `diseases` · `"cognitive behavioral therapy"` | 4 SI y 2 NO; 2 SI y 0 NO | Abren a diagnóstico y terapia clínica (CE) |
| `"human factors"` (IEEE p.232, UF de *Ergonomics* por *Human factors engineering*) | Tesauro | `"human engineering"` ya trae 14 NO exclusivos frente a 3 SI; su sinónimo más frecuente multiplicaría el ruido |
| *Deep learning*, *Measurement*, `"Down syndrome"`, `"machine-learning"` | Retirados en el cribado anterior (4, 10 y 4 NO exclusivos; el último, duplicado) | Se mantienen fuera: la evidencia de ruido sigue vigente |
| *Sentiment analysis*, *Affective computing* (NT del tesauro) | Tesauro | Abren a la detección emocional |

### Query Scopus propuesta (100 keywords)

```text
TITLE-ABS-KEY (
  ( autism OR autistic OR neurodivers* OR neurodivergen*
    OR neurodevelopmental OR "cognitive disabilit*" OR "intellectual disabilit*"
    OR "developmental disabilit*" OR "learning disabilit*" OR ADHD OR "attention deficit"
    OR dyslexi* OR "cognitive accessibility" OR Asperger
    OR "intellectual developmental disorder" OR "learning disorder*"
    OR dyscalculia OR dysgraphia OR "reading disabilit*" )
  AND
  ( "artificial intelligence" OR AI OR "machine learning" OR "natural language processing"
    OR NLP OR "language model" OR LLM OR LLMs OR ChatGPT OR GPT OR "prompt engineering"
    OR "computer vision" OR chatbot OR "conversational agents" OR "intelligent agents"
    OR "virtual agent" OR "text simplification" OR "lexical simplification"
    OR "text adaptation" OR "text processing" OR "text analysis" OR "text mining"
    OR "computational linguistics" OR "adaptive user interface" OR "speech recognition"
    OR "recommender systems" OR "natural language generation"
    OR "generative adversarial networks" OR "fuzzy logic" OR "fuzzy inference"
    OR "ambient intelligence" OR "context awareness" OR "context-aware"
    OR "reinforcement learning" OR "contrastive learning" OR "cognitive systems"
    OR automation )
  AND
  ( blindness OR deafness OR deaf OR "visual impairment" OR "visually impaired"
    OR "low vision" OR "hearing impairment" OR "hearing impaired" OR "sensory impairment"
    OR "screen reader" OR WCAG OR accessibility OR "accessible design"
    OR "accessible interface" OR "inclusive design" OR "universal design"
    OR "digital inclusion" OR "co-design" OR "user centered design" OR pictograms
    OR "augmentative and alternative communication" )
  AND
  ( usability OR "user experience" OR metric OR metrics
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

### Query Web of Science propuesta (100 keywords)

```text
ALL=(autism OR autistic OR neurodivers* OR neurodivergen*
  OR neurodevelopmental OR "cognitive disabilit*" OR "intellectual disabilit*"
  OR "developmental disabilit*" OR "learning disabilit*" OR ADHD OR "attention deficit"
  OR dyslexi* OR "cognitive accessibility" OR Asperger
  OR "intellectual developmental disorder" OR "learning disorder*"
  OR dyscalculia OR dysgraphia OR "reading disabilit*")
AND ALL=("artificial intelligence" OR AI OR "machine learning"
  OR "natural language processing" OR NLP OR "language model" OR LLM OR LLMs
  OR ChatGPT OR GPT OR "prompt engineering" OR "computer vision" OR chatbot
  OR "conversational agents" OR "intelligent agents" OR "virtual agent"
  OR "text simplification" OR "lexical simplification" OR "text adaptation"
  OR "text processing" OR "text analysis" OR "text mining" OR "computational linguistics"
  OR "adaptive user interface" OR "speech recognition" OR "recommender systems"
  OR "natural language generation" OR "generative adversarial networks" OR "fuzzy logic"
  OR "fuzzy inference" OR "ambient intelligence" OR "context awareness" OR "context-aware"
  OR "reinforcement learning" OR "contrastive learning" OR "cognitive systems"
  OR automation)
AND ALL=(blindness OR deafness OR deaf OR "visual impairment" OR "visually impaired"
  OR "low vision" OR "hearing impairment" OR "hearing impaired" OR "sensory impairment"
  OR "screen reader" OR WCAG OR accessibility OR "accessible design"
  OR "accessible interface" OR "inclusive design" OR "universal design"
  OR "digital inclusion" OR "co-design" OR "user centered design" OR pictograms
  OR "augmentative and alternative communication")
AND ALL=(usability OR "user experience" OR metric OR metrics
  OR "readability metrics" OR readability OR "plain language" OR "easy-to-read"
  OR "easy read" OR "software quality" OR "cognitive load" OR "accessibility evaluation"
  OR "accessibility testing" OR "user study" OR comprehension OR understandability
  OR "user satisfaction" OR "accessibility audit" OR "accessibility assessment"
  OR ergonomics OR "human engineering" OR "user acceptance" OR "human evaluation")
AND PY=(2021-2026) AND DT=(Article) AND LA=(English OR Spanish)
```

Filtro de la interfaz: Open Access. Recuento: P 19, I 37, C 21, O 23 (100 keywords).

### Límite honesto de la defensa

- `automation` y `"cognitive systems"` pueden traer automatización sin IA; el CI de IA los filtra en el cribado, pero subirá la carga de NO.
- `"user centered design"` revierte una exclusión del picoc con solo 3 registros de evidencia; si el crítico prioriza la precisión, es el primer candidato a caer.
- La redundancia de las cinco variantes retiradas se apoya en que la frase contiene el término corto; en IEEE Xplore esto solo vale si `autism` pasa a texto libre.
- Los candidatos con más evidencia (`"mobile applications"`, `"software design"`) no caben en ningún bloque del PICO sin reintroducir el bloque de contexto que se retiró.

## Crítico

| Comp. | Término | Propuesta | Tu posición | Motivo |
|---|---|---|---|---|
| P | `"autism spectrum"` | quitar (redundante) | no quitar | 5 SI; incumple la regla (0 SI y 3 NO exclusivos) y obliga a tocar el descriptor IEEE *Autism* |
| I | `"generative AI"` | quitar (redundante) | no quitar | 2 SI; incumple la regla de retirada. Que no pierda registros no la convierte en retirable |
| I | `"generative artificial intelligence"` | quitar (redundante) | no quitar | 2 SI; incumple la regla de retirada |
| C | `"Web Content Accessibility Guidelines"` | quitar (redundante) | no quitar | 2 SI; incumple la regla de retirada |
| O | `"accessibility metric"` | quitar (redundante) | no quitar | 0 registros, 0 NO exclusivos: no llega a 3 NO |
| I | `automation` | agregar | no agregar | No es técnica de IA (fuera de I); reintroduce *Automatic testing*, del bloque de contexto retirado, y abre a la domótica asistiva |
| C | `"augmentative and alternative communication"` | agregar | no agregar | Tecnología de apoyo, excluida en el picoc; solo 1 SI de evidencia |
| C·I | `"co-design"` · `"user centered design"` · `pictograms` · `"cognitive systems"` | agregar | con 1 hueco (solo `"learning difficult*"`): solo `"co-design"` | 5 SI, la mayor evidencia. Aplazar el resto hasta que haya cupo que cumpla la regla |
