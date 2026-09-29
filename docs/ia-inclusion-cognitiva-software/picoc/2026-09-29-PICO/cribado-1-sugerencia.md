# Sugerencia de búsqueda — cribado 1

<!-- cribado:sugerencia picoc=2026-09-29-PICO -->

Basada en 120 registros únicos de Scopus (92) y Web of Science (61), después de quitar 33 duplicados: SI 25 (de ellos 14 dudas) y NO 95. No reemplaza la búsqueda: la mejora. Se conserva todo término que recupere un estudio aceptado o que cubra población o técnica del marco con poco ruido. Solo se retira un término cuando trae únicamente registros rechazados que ningún otro término de su componente recupera («exclusivos», columna de `.cribado-1/keywords.md`) y su contenido queda cubierto por otro término. Los términos nuevos se validaron con `thesaurus:check`.

## Keywords

| Comp. | Término | Estado | Evidencia (registros · SI · exclusivos SI/NO) | Vocabulario | Decisión |
|---|---|---|---|---|---|
| P | `"intellectual disabilit*"` · `dyslexi*` · `neurodivergen*` · `neurodivers*` · `neurodevelopmental` · `"learning disabilit*"` | vale | SI exclusivos: 4, 5, 2, 1, 1 y 1 | Según picoc | Conservar |
| P | `autism` · `"autism spectrum"` · `autistic` · `"cognitive disabilit*"` · `"cognitive accessibility"` · `"developmental disabilit*"` · `ADHD` · `"attention deficit"` | vale | SI no exclusivos; `autism` y `"cognitive accessibility"` tienen 7 NO exclusivos, casi todos diagnóstico (CE5) o revisiones (CE3), que el cribado filtra | IEEE *Autism* (picoc) | Conservar: perfiles que nombra el criterio de población y constructo central del tema |
| P | `"Down syndrome"` · `"learning disorder*"` · `"learning difficult*"` | revisar | 0 SI; 0/4, 0/1 y 0/2 exclusivos | Según picoc | Conservar: el concepto P nombra el síndrome de Down; retirar solo si la próxima búsqueda repite 0 SI |
| P | `Asperger` · `"intellectual developmental disorder"` · `dyscalculia` | no aporta | 0 registros, sin ruido | MeSH / DSM-5 (picoc) | Conservar |
| I | `"artificial intelligence"` · `AI` · `"natural language processing"` · `NLP` · `LLM` · `LLMs` · `"text simplification"` · `"speech recognition"` · `"generative AI"` · `"generative artificial intelligence"` · `ChatGPT` · `GPT` · `chatbot` · `"machine learning"` · `"machine-learning"` · `"computer vision"` · `"conversational agents"` | vale | Concentran los SI (hasta 11 por término) | Según picoc | Conservar |
| I | `"deep learning"` | revisar | 11 registros, 0 SI; 0/4 exclusivos (clasificadores de diagnóstico, CE5) | IEEE *Deep learning* (p. 126) | Conservar: familia de técnica de la pregunta del componente I; ruido bajo |
| I | `"adaptive user interface"` · `"recommender systems"` · `"natural language generation"` | no aporta | 0 registros, sin ruido | IEEE / ACM CCS (picoc) | Conservar |
| I | `"large language model*"` → `"language model*"` | revisar | 22 registros y 10 SI; «language model» aparece en 6 SI sin cobertura | Libre | Sustituir: lo incluye y no suma comodines en IEEE Xplore |
| I | `"prompt engineering"` | agregar | Palabra clave de 4 SI y 0 NO, sin cobertura | Libre | Agregar |
| I | `"lexical simplification"` · `"sentence simplification"` · `"text adaptation"` | agregar | La simplificación de textos es la técnica más precisa (6 SI de 9); «text adaptation» en 2 registros, 1 SI | Libre | Agregar |
| I | `"computational linguistics"` | agregar a prueba | Palabra clave de 2 SI y 0 NO | IEEE *Computational linguistics* (p. 95) | Agregar y medir el ruido en la próxima búsqueda (su NT *Sentiment analysis* puede traer diagnóstico emocional) |
| I | `"text processing"` · `"human engineering"` · `personali*` | no agregar | *Text processing* es tipografía en IEEE; «human engineering» es indización de Compendex; `personali*` 15 registros y solo 3 SI | — | No agregar |
| C | `accessibility` · `WCAG` · `"Web Content Accessibility Guidelines"` · `"inclusive design"` | vale | `accessibility` recupera los 25 SI (17 exclusivos) | Según picoc | Conservar |
| C | `blindness` · `deafness` · `deaf` · `"visual impairment"` · `"visually impaired"` · `"low vision"` · `"hearing impaired"` · `"sensory impairment"` · `"screen reader"` · `"accessible design"` · `"accessible interface"` | vale | 0 a 2 NO exclusivos | Según picoc | Conservar: contraste sensorial de la pregunta del componente C |
| C | `"hearing impairment"` | no aporta | 9 registros, 0 SI; 0/7 exclusivos (audiología, CE6) | IEEE (picoc) | Retirar: `deaf` y `deafness` cubren el contraste auditivo |
| C | `"universal design"` | no aporta | 6 registros, 1 SI no exclusivo; 0/3 exclusivos (diseño universal para el aprendizaje, CE7) | Según picoc | Retirar: lo cubren `"inclusive design"` y `accessibility` |
| O | `usability` · `readability` · `"plain language"` · `"easy-to-read"` · `comprehension` · `"cognitive load"` · `"user experience"` · `"readability metrics"` · `"accessibility evaluation"` · `"user study"` · `understandability` | vale | SI exclusivos en `usability` (7) y `readability` (3) | Según picoc | Conservar |
| O | `measurement` | no aporta en texto libre | 12 registros, 0 SI; 0/10 exclusivos (medición EEG y clínica) | IEEE *Measurement* (UF *Metrics*, p. 313) | Retirar de Scopus y Web of Science; en IEEE Xplore se conserva como descriptor (`"IEEE Terms"`), donde no trae ese ruido |
| O | `metric` · `metrics` → `"evaluation metric"` · `"evaluation metrics"` | revisar | 3 y 20 registros, SI no exclusivos; 0/2 y 0/15 exclusivos (métricas de clasificadores de diagnóstico) | Libre | Sustituir por la frase, que conserva las métricas automáticas de la pregunta del componente O |
| O | `"easy read"` | agregar | Forma europea de lectura fácil (`"easy-to-read"`: 4 SI de 5) | Libre | Agregar |
| O | `"easy-to-understand"` | agregar a prueba | Respaldado por 1 SI; es un adjetivo frecuente en resúmenes de IA explicable para diagnóstico | Libre | Agregar; retirar si trae más de 2 NO exclusivos |
| O | `"human evaluation"` | agregar | Forma habitual de reportar la evaluación de la simplificación (CI5) | Libre | Agregar |
| O | `"software quality"` · `"accessibility metric"` · `"accessibility testing"` · `"accessibility audit"` · `"accessibility assessment"` · `"user satisfaction"` | no aporta | 0 a 2 registros, sin ruido | Según picoc | Conservar: verificación y auditoría de la pregunta general |
| — | `"assistive technology"` | no agregar | Palabra clave de 4 SI y 6 NO | IEEE *Assistive technology* (p. 32) | Mantener fuera, como decidió el picoc |

## Query Scopus

```text
TITLE-ABS-KEY (
  ( autism OR autistic OR "autism spectrum" OR neurodivers* OR neurodivergen*
    OR neurodevelopmental OR "cognitive disabilit*" OR "intellectual disabilit*"
    OR "developmental disabilit*" OR "learning disabilit*" OR ADHD OR "attention deficit"
    OR dyslexi* OR "cognitive accessibility" OR Asperger
    OR "intellectual developmental disorder" OR "Down syndrome" OR "learning disorder*"
    OR "learning difficult*" OR dyscalculia )
  AND
  ( "artificial intelligence" OR AI OR "machine learning" OR "machine-learning"
    OR "deep learning" OR "natural language processing" OR NLP OR "language model*"
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
  ( usability OR "user experience" OR "evaluation metric" OR "evaluation metrics"
    OR "accessibility metric" OR "readability metrics" OR readability OR "plain language"
    OR "easy-to-read" OR "easy read" OR "easy-to-understand" OR "software quality"
    OR "cognitive load" OR "accessibility evaluation" OR "accessibility testing"
    OR "user study" OR "human evaluation" OR comprehension OR understandability
    OR "user satisfaction" OR "accessibility audit" OR "accessibility assessment" )
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
  OR dyslexi* OR "cognitive accessibility" OR Asperger OR "intellectual developmental disorder"
  OR "Down syndrome" OR "learning disorder*" OR "learning difficult*" OR dyscalculia)
AND ALL=("artificial intelligence" OR AI OR "machine learning" OR "machine-learning"
  OR "deep learning" OR "natural language processing" OR NLP OR "language model*"
  OR LLM OR LLMs OR "generative AI" OR "generative artificial intelligence" OR ChatGPT OR GPT
  OR "prompt engineering" OR "computer vision" OR chatbot OR "conversational agents"
  OR "text simplification" OR "lexical simplification" OR "sentence simplification"
  OR "text adaptation" OR "computational linguistics" OR "adaptive user interface"
  OR "speech recognition" OR "recommender systems" OR "natural language generation")
AND ALL=(blindness OR deafness OR deaf OR "visual impairment" OR "visually impaired"
  OR "low vision" OR "hearing impaired" OR "sensory impairment" OR "screen reader"
  OR WCAG OR "Web Content Accessibility Guidelines" OR accessibility OR "accessible design"
  OR "accessible interface" OR "inclusive design")
AND ALL=(usability OR "user experience" OR "evaluation metric" OR "evaluation metrics"
  OR "accessibility metric" OR "readability metrics" OR readability OR "plain language"
  OR "easy-to-read" OR "easy read" OR "easy-to-understand" OR "software quality"
  OR "cognitive load" OR "accessibility evaluation" OR "accessibility testing"
  OR "user study" OR "human evaluation" OR comprehension OR understandability
  OR "user satisfaction" OR "accessibility audit" OR "accessibility assessment")
AND PY=(2021-2026) AND DT=(Article) AND LA=(English OR Spanish)
```

En Web of Science, el acceso abierto se aplica con el filtro Open Access de la interfaz. La query de IEEE Xplore la ajusta `rsl-picoc` (modo sugerencia) con los mismos cambios. Al sustituir `"large language model*"` por `"language model*"` se mantiene en 10 comodines, y conserva los descriptores `"IEEE Terms":"Deep learning"` y `"IEEE Terms":"Measurement"`. La tabla de componentes debe reflejar las retiradas: el diseño universal en C, y *Metrics* y *Measurement* en la justificación de O.

## Debate

- De acuerdo: sustituir `"large language model*"` por `"language model*"`; agregar `"prompt engineering"`, las variantes de simplificación, `"text adaptation"`, `"easy read"` y `"human evaluation"`; retirar `"hearing impairment"` y `"universal design"`; no agregar `"text processing"`, `"human engineering"` ni `personali*`.
- `"Down syndrome"` y `"deep learning"`: el defensor proponía quitarlos y el crítico conservarlos. Se conservan en «revisar», porque su ruido es diagnóstico (CE5), el mismo que el de `autism`, y cubren población y técnica del marco.
- `measurement`: el defensor proponía quitarlo y el crítico conservarlo como descriptor IEEE. Sale de Scopus y Web of Science, donde solo trae 10 rechazos exclusivos, y queda como descriptor en IEEE Xplore.
- `metric` y `metrics`: se sustituyen por `"evaluation metric"` y `"evaluation metrics"`, como pidió el crítico, para no dejar sin cobertura las métricas automáticas.
- `"computational linguistics"` y `"easy-to-understand"`: entran a prueba; se revisan con la próxima búsqueda.
- Límite: la evidencia sale de registros que la búsqueda ya recupera. Lo que aportan los términos nuevos solo se sabrá al correr las queries.
