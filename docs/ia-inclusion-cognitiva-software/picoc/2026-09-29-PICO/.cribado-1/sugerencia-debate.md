# Debate de la sugerencia de keywords (cribado 1)

## Defensor

Base: `keywords.md` (120 registros únicos, 25 SI con 14 dudas, 95 NO), `thesaurus.md` y `thesaurus:check` de los términos nuevos. Las retiradas se simularon con el mismo patrón literal de `cribado.py` sobre los 87 registros que casan con los cuatro bloques en título, resumen y palabras clave exportados: el conjunto de siete retiradas pierde 20 registros, **ninguno SI**. «Varios NO exclusivos» se lee como tres o más.

| Comp. | Término | Estado | Evidencia | Propuesta |
|---|---|---|---|---|
| P | `"intellectual disabilit*"` · `dyslexi*` · `neurodivergen*` · `neurodivers*` · `neurodevelopmental` · `"learning disabilit*"` | vale | Aportan SI exclusivos: 4, 5, 2, 1, 1 y 1 | Conservar |
| P | `"cognitive disabilit*"` · `"developmental disabilit*"` · `ADHD` · `"attention deficit"` · `"autism spectrum"` · `autistic` · `"learning disorder*"` · `"learning difficult*"` | vale | SI no exclusivos: 5, 2, 2, 1 y 3 en los cinco primeros; `autistic`, `"learning disorder*"` y `"learning difficult*"` no tienen SI, pero solo 0 a 2 NO exclusivos. Su ruido es el diagnóstico (CE5) y las revisiones (CE3), que son criterios y no problemas de vocabulario | Conservar; son perfiles que nombra CI3 |
| P | `autism` | conservar (excepción) | 0 SI exclusivos y 7 NO exclusivos; la simulación pierde 4 registros, todos NO | Conservar: es el único descriptor IEEE del bloque (p. 35) y el perfil principal de CI3. Si se quita, se pierden los estudios que escriben «autism» sin «spectrum» ni «autistic» |
| P | `"cognitive accessibility"` | conservar (excepción) | 6 SI, 0 exclusivos, 7 NO exclusivos; la simulación pierde 7, todos NO | Conservar: es el constructo del tema, keyword del picoc y ancla de RQ3 (COGA). Sus NO exclusivos son estudios sin perfil clínico (CI3) o revisiones (CE3) |
| P | `"Down syndrome"` | quitar | 4 registros, 0 SI, 4 NO exclusivos (detección prenatal por imagen, registro de pacientes); la simulación pierde 3, todos NO | Quitar; la población queda cubierta por `"intellectual disabilit*"` |
| P | `Asperger` · `"intellectual developmental disorder"` · `dyscalculia` | conservar | 0 registros; no meten ruido | Conservar por cobertura de la población (MeSH y DSM-5); coste nulo |
| I | `"artificial intelligence"` · `AI` · `"natural language processing"` · `NLP` · `"large language model*"` · `LLM` · `LLMs` · `"text simplification"` · `"speech recognition"` | vale | Concentran los SI: 10, 11, 6, 2, 10, 5, 4, 6 y 1; SI exclusivos en `"artificial intelligence"`, `AI`, `"natural language processing"`, `"large language model*"` y `"speech recognition"` | Conservar |
| I | `"generative AI"` · `"generative artificial intelligence"` · `ChatGPT` · `GPT` · `chatbot` · `"machine learning"` · `"machine-learning"` | vale | 1 o 2 SI cada uno; 0 o 1 NO exclusivo | Conservar |
| I | `"computer vision"` · `"conversational agents"` | conservar | 0 SI y 0 o 1 NO exclusivo; ruido no demostrado | Conservar (técnicas de RQ2) |
| I | `"deep learning"` | quitar | 11 registros, 0 SI, 4 NO exclusivos (clasificación y detección: CE5); la simulación pierde 3, todos NO | Quitar; los artefactos con redes neuronales ya se recuperan con `AI`, `"artificial intelligence"` y `"machine learning"` |
| I | `"adaptive user interface"` · `"recommender systems"` · `"natural language generation"` | conservar | 0 registros; no meten ruido | Conservar: personalización en tiempo de ejecución y generación de texto son fases y técnicas de RQ2 |
| I | `"language model*"` | agregar | 6 SI y 3 NO con «language model» en palabras clave, sin cubrir; en el conjunto actual casa con 25 registros, 11 SI | OR en el bloque I; término libre (ACM CCS *Language models*); recoge «neural language model» y «pretrained language model» |
| I | `"prompt engineering"` | agregar | 4 SI y 0 NO en palabras clave sin cubrir (p. ej. R024) | OR en el bloque I; término libre |
| I | `"computational linguistics"` | agregar | 2 SI y 0 NO en palabras clave sin cubrir | OR en el bloque I; descriptor IEEE *Computational linguistics* (p. 95) |
| I | `"lexical simplification"` · `"sentence simplification"` · `"text adaptation"` | agregar | «Lexical simplification» aparece en R021 (SI); «text adaptation» en 2 registros, 1 SI; son las variantes de la técnica con más SI (`"text simplification"`, 6 de 9) | OR en el bloque I; términos libres. No se usa `simplif*`, que recupera simplificación sin inteligencia artificial (CI4) |
| I | `"text processing"` · `"human engineering"` · `personali*` | no agregar | *Text processing* es tipografía en IEEE (p. 539); «human engineering» (USE *Ergonomics*) es indización de Compendex que Web of Science no tiene (5 SI, 3 NO); `personali*` casa con 15 registros y solo 3 SI | No agregar |
| C | `accessibility` · `WCAG` · `"Web Content Accessibility Guidelines"` · `"inclusive design"` | vale | `accessibility` sostiene los 25 SI (17 exclusivos); WCAG 4 SI de 6 | Conservar |
| C | `blindness` · `deafness` · `deaf` · `"visual impairment"` · `"visually impaired"` · `"low vision"` · `"accessible interface"` | conservar | 0 SI exclusivos y 0 a 2 NO exclusivos; son el contraste sensorial de RQ3 (`deaf` recupera la duda R091, sordos y neurodiversos) | Conservar |
| C | `"hearing impairment"` | quitar | 9 registros, 0 SI, 7 NO exclusivos (audiología: sinaptopatía coclear, implantes, envejecimiento auditivo); la simulación pierde 2, todos NO | Quitar; el contraste auditivo queda con `deaf` y `deafness` (descriptor IEEE) |
| C | `"universal design"` | quitar | 6 registros, 1 SI no exclusivo, 3 NO exclusivos (diseño universal para el aprendizaje, excluido por CE7); la simulación pierde 3, todos NO | Quitar; el enfoque normativo queda con `"inclusive design"` y `accessibility` |
| C | `"hearing impaired"` · `"sensory impairment"` · `"screen reader"` · `"accessible design"` | conservar | 0 registros; no meten ruido | Conservar por cobertura del contraste de RQ3 |
| O | `usability` · `readability` · `"plain language"` · `"easy-to-read"` · `comprehension` · `"cognitive load"` · `"user experience"` · `"readability metrics"` · `"accessibility evaluation"` · `"user study"` · `understandability` | vale | SI 9, 6, 5, 4, 8, 3, 1, 1, 1, 1 y 1; SI exclusivos en `usability` (7), `readability` (3), `comprehension`, `"cognitive load"` y `"user experience"` (1 cada uno) | Conservar |
| O | `measurement` | quitar | 12 registros, 0 SI, 10 NO exclusivos (medición EEG y clínica) | Quitar. El descriptor IEEE se pierde, pero en este corpus remite a medición fisiológica, no a métricas de software |
| O | `metric` · `metrics` | quitar | `metrics`: 20 registros, 2 SI no exclusivos, 15 NO exclusivos; `metric`: 0 SI exclusivos, 2 NO exclusivos. Son métricas de rendimiento de clasificadores diagnósticos (CE5). Quitar los tres términos genéricos (con `measurement`) pierde 16 registros en la simulación, ninguno SI | Quitar las palabras sueltas; RQ4 conserva las métricas con frases propias (`"accessibility metric"`, `"readability metrics"`, `usability`). Scopus y Web of Science lematizan plurales, así que quitar solo `metrics` no cambiaría nada |
| O | `"easy read"` · `"easy-to-understand"` | agregar | R094 escribe «Easy-read» y R092 «easy-to-understand», que `"easy-to-read"` no recoge (1 SI en «easy-to-understand») | OR en el bloque O; términos libres; en Scopus y Web of Science, `"easy read"` también recupera «easy-read» |
| O | `"human evaluation"` | agregar | 1 registro, 1 SI; es la forma habitual de reportar la evaluación de la simplificación y la generación de texto (CI5) | OR en el bloque O; término libre |
| O | `"user satisfaction"` · `"accessibility metric"` · `"software quality"` · `"accessibility testing"` · `"accessibility audit"` · `"accessibility assessment"` | conservar | 0 registros, o 1 NO exclusivo en `"user satisfaction"`; no meten ruido | Conservar: nombran la verificación y la auditoría que prioriza la pregunta general |
| — | `"assistive technology"` · `ASD` · `simplif*` | mantener fuera | «Assistive technology»: 4 SI y 6 NO (13 registros, 5 SI); `ASD` sigue siendo ambiguo | Mantener la exclusión del picoc |

**Límite honesto.** La simulación usa solo título, resumen y palabras clave exportados (87 de 120 casan literalmente), no la indización completa de Scopus. El beneficio de los términos nuevos solo puede medirse volviendo a correr la búsqueda. `"language model*"` añade un comodín, así que la query de IEEE Xplore (límite de 10) tendría que reservarle uno.

### Query Scopus

```text
TITLE-ABS-KEY (
  ( autism OR autistic OR "autism spectrum" OR neurodivers* OR neurodivergen*
    OR neurodevelopmental OR "cognitive disabilit*" OR "intellectual disabilit*"
    OR "developmental disabilit*" OR "learning disabilit*" OR ADHD OR "attention deficit"
    OR dyslexi* OR "cognitive accessibility" OR Asperger
    OR "intellectual developmental disorder" OR "learning disorder*"
    OR "learning difficult*" OR dyscalculia )
  AND
  ( "artificial intelligence" OR AI OR "machine learning" OR "machine-learning"
    OR "natural language processing" OR NLP OR "large language model*" OR "language model*"
    OR LLM OR LLMs OR "generative AI" OR "generative artificial intelligence" OR ChatGPT OR GPT
    OR "prompt engineering" OR "computer vision" OR chatbot OR "conversational agents"
    OR "text simplification" OR "lexical simplification" OR "sentence simplification"
    OR "text adaptation" OR "computational linguistics" OR "adaptive user interface"
    OR "speech recognition" OR "recommender systems" OR "natural language generation" )
  AND
  ( blindness OR deafness OR deaf OR "visual impairment" OR "visually impaired" OR "low vision"
    OR "hearing impaired" OR "sensory impairment" OR "screen reader"
    OR WCAG OR "Web Content Accessibility Guidelines" OR accessibility OR "accessible design"
    OR "accessible interface" OR "inclusive design" )
  AND
  ( usability OR "user experience" OR "accessibility metric"
    OR "readability metrics" OR readability OR "plain language" OR "easy-to-read" OR "easy read"
    OR "easy-to-understand" OR "software quality" OR "cognitive load" OR "accessibility evaluation"
    OR "accessibility testing" OR "user study" OR "human evaluation" OR comprehension
    OR understandability OR "user satisfaction" OR "accessibility audit" OR "accessibility assessment" )
)
AND PUBYEAR > 2020 AND PUBYEAR < 2027
AND ( LIMIT-TO ( DOCTYPE , "ar" ) )
AND ( LIMIT-TO ( LANGUAGE , "English" ) OR LIMIT-TO ( LANGUAGE , "Spanish" ) )
AND ( LIMIT-TO ( OA , "all" ) )
```

### Query Web of Science

```text
ALL=(autism OR autistic OR "autism spectrum" OR neurodivers* OR neurodivergen*
  OR neurodevelopmental OR "cognitive disabilit*" OR "intellectual disabilit*"
  OR "developmental disabilit*" OR "learning disabilit*" OR ADHD OR "attention deficit"
  OR dyslexi* OR "cognitive accessibility" OR Asperger OR "intellectual developmental disorder"
  OR "learning disorder*" OR "learning difficult*" OR dyscalculia)
AND ALL=("artificial intelligence" OR AI OR "machine learning" OR "machine-learning"
  OR "natural language processing" OR NLP OR "large language model*" OR "language model*"
  OR LLM OR LLMs OR "generative AI" OR "generative artificial intelligence" OR ChatGPT OR GPT
  OR "prompt engineering" OR "computer vision" OR chatbot OR "conversational agents"
  OR "text simplification" OR "lexical simplification" OR "sentence simplification"
  OR "text adaptation" OR "computational linguistics" OR "adaptive user interface"
  OR "speech recognition" OR "recommender systems" OR "natural language generation")
AND ALL=(blindness OR deafness OR deaf OR "visual impairment" OR "visually impaired"
  OR "low vision" OR "hearing impaired" OR "sensory impairment"
  OR "screen reader" OR WCAG OR "Web Content Accessibility Guidelines" OR accessibility
  OR "accessible design" OR "accessible interface" OR "inclusive design")
AND ALL=(usability OR "user experience" OR "accessibility metric" OR "readability metrics"
  OR readability OR "plain language" OR "easy-to-read" OR "easy read" OR "easy-to-understand"
  OR "software quality" OR "cognitive load" OR "accessibility evaluation"
  OR "accessibility testing" OR "user study" OR "human evaluation" OR comprehension
  OR understandability OR "user satisfaction" OR "accessibility audit" OR "accessibility assessment")
AND PY=(2021-2026) AND DT=(Article) AND LA=(English OR Spanish)
```

Filtro de la interfaz: Open Access (Web of Science no tiene etiqueta de campo para el acceso abierto).

## Crítico

| Comp. | Término | Propuesta | Tu posición | Motivo |
|---|---|---|---|---|
| P | `"Down syndrome"` | quitar | conservar | Su ruido (4 NO, detección prenatal) es CE5, el mismo argumento con que se conserva `autism` (7 NO). El concepto P nombra el síndrome de Down y hay estudios que no escriben «intellectual disability». |
| I | `"deep learning"` | quitar | conservar | Es un descriptor IEEE (p. 126) y una familia de RQ2; su ruido de 4 NO es CE5, igual que en `autism`. Si se quita, cae la razón para excluir *Neural networks*. |
| O | `measurement` | quitar | conservar al menos `"IEEE Terms":"Measurement"` en IEEE Xplore | Es el descriptor preferido (UF *Metrics*, p. 313). El ruido EEG viene de texto libre de Scopus y no se traslada a la indización IEEE. La validación de Perry et al. solo cubre O con él. |
| O | `metric` · `metrics` | quitar | quitar solo si se agrega `"evaluation metric"` | La validación del picoc ya muestra que O recorta estudios afines. Si se quitan los genéricos sin sustituto, RQ4 queda sin forma de recuperar métricas automáticas (SARI, BLEU, legibilidad). |
| I | `"language model*"` | agregar | agregar sustituyendo a `"large language model*"` | Lo subsume. Si se suma sin retirar el otro, IEEE Xplore llega a 11 comodines (límite de 10). La rama ACM *Language models* es de recuperación de información, no de procesamiento de lenguaje natural. |
| I | `"computational linguistics"` | agregar | agregar como descriptor IEEE y medir el ruido al volver a correr la búsqueda | La evidencia viene de indización de Compendex, el mismo motivo por el que se rechazó `"human engineering"`. Su NT *Sentiment analysis* abre la puerta al análisis emocional con fines diagnósticos (CE5). |
| O | `"easy-to-understand"` | agregar | agregar a prueba; retirarlo si aporta más de 2 NO exclusivos | Solo 1 SI lo respalda. Es un adjetivo habitual en resúmenes de inteligencia artificial explicable para diagnóstico (CE5), a diferencia de `"easy read"`, que es un término de lectura fácil. |

- Query de IEEE Xplore: no está en la propuesta. Hay que reescribirla con los cambios. Si se retiran `"deep learning"` y `measurement`, pierde los descriptores `"IEEE Terms":"Deep learning"` y `"IEEE Terms":"Measurement"`. Con `"language model*"` pasa a 11 comodines.
- Queries de Scopus y Web of Science: conservan todos los términos salvo las retiradas declaradas (`"Down syndrome"`, `"deep learning"`, `"hearing impairment"`, `"universal design"`, `measurement`, `metric` y `metrics`). La sintaxis y los filtros son idénticos a los del picoc. `"large language model*"` queda redundante junto a `"language model*"`.
- Tabla igual a query: aplicar la propuesta obliga a cambiar la tabla de componentes y las palabras clave. Afecta al concepto P («incluido el síndrome de Down»), a la justificación de O («se incluyen ambos», *Metrics* y *Measurement*), a la de C («el universal»), a las filas IEEE *Deep learning* y *Measurement* y a la exclusión de *Neural networks*. Si no, `picoc:lint` y la regla de tabla y query 1:1 fallan.
