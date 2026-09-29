# Sugerencia de búsqueda — cribado 1

<!-- cribado:sugerencia picoc=2026-09-29-2-PICO -->

Basada en 115 registros únicos de Scopus y Web of Science (SI 41, NO 74). No reemplaza la búsqueda: la amplía.

**Efecto esperado:** 4 términos agregados, 6 quitados; los términos quitados dejan fuera 4 de los 115 registros actuales (0 SI). Cinco de los seis retiros son frases que otro término del mismo bloque ya contiene, por lo que no cambian los registros recuperados; solo liberan cupo bajo el máximo de 100 keywords. La query pasa de 100 a 98 keywords (P 19, I 36, C 20, O 23).

## Keywords

Evidencia: registros totales, SI y NO (SI incluye las dudas); entre paréntesis, registros que solo ese término recupera en su bloque (SI / NO).

| Comp. | Término | Estado | Evidencia | Vocabulario | Decisión |
|---|---|---|---|---|---|
| P | `autism` | vale | 30: 6 SI, 24 NO (1 / 3) | IEEE *Autism* (p.35) | Se queda |
| P | `autistic` | vale | 5: 1 SI, 4 NO (0 / 0) | Libre | Se queda |
| P | `"autism spectrum"` | no aporta | 22: 5 SI, 17 NO (0 / 0) | Libre | Se quita por el máximo de 100: `autism` ya recupera toda frase que lo contiene |
| P | `neurodivers*` | vale | 9: 2 SI, 7 NO (1 / 2) | Libre | Se queda |
| P | `neurodivergen*` | vale | 14: 6 SI, 8 NO (3 / 2) | Libre | Se queda |
| P | `neurodevelopmental` | vale | 8: 1 SI, 7 NO (1 / 3) | Libre | Se queda |
| P | `"cognitive disabilit*"` | vale | 14: 7 SI, 7 NO (2 / 3) | Libre | Se queda |
| P | `"intellectual disabilit*"` | vale | 17: 8 SI, 9 NO (5 / 6) | Libre (MeSH) | Se queda |
| P | `"developmental disabilit*"` | vale | 4: 3 SI, 1 NO (0 / 0) | Libre (MeSH) | Se queda |
| P | `"learning disabilit*"` | vale | 8: 4 SI, 4 NO (1 / 2) | Libre (MeSH) | Se queda |
| P | `ADHD` | vale | 15: 6 SI, 9 NO (0 / 0) | Libre (MeSH) | Se queda |
| P | `"attention deficit"` | vale | 9: 4 SI, 5 NO (0 / 1) | Libre (MeSH) | Se queda |
| P | `dyslexi*` | vale | 18: 9 SI, 9 NO (8 / 2) | Libre (MeSH) | Se queda |
| P | `"cognitive accessibility"` | vale | 18: 7 SI, 11 NO (1 / 6) | Libre | Se queda |
| P | `Asperger` | revisar | 0 registros | Libre (MeSH) | Se queda |
| P | `"intellectual developmental disorder"` | revisar | 0 registros | Libre | Se queda |
| P | `"learning disorder*"` | revisar | 2: 0 SI, 2 NO (0 / 0) | Libre | Se queda: no cumple la regla de retiro |
| P | `"learning difficult*"` | no aporta | 5: 0 SI, 5 NO (0 / 4) | Libre | Se quita: 0 SI y 4 NO exclusivos |
| P | `dyscalculia` | revisar | 0 registros | Libre (MeSH) | Se queda |
| P | `dysgraphia` | revisar | 1: 0 SI, 1 NO (0 / 0) | Libre | Se queda |
| P | `"reading disabilit*"` | revisar | 1: 0 SI, 1 NO (0 / 0) | Libre | Se queda |
| I | `"artificial intelligence"` | vale | 52: 15 SI, 37 NO (1 / 4) | IEEE *Artificial intelligence* (p.30) | Se queda |
| I | `AI` | vale | 59: 20 SI, 39 NO (1 / 4) | IEEE, UF de *Artificial intelligence* | Se queda |
| I | `"machine learning"` | vale | 22: 4 SI, 18 NO (0 / 6) | IEEE *Machine learning* (p.294) | Se queda |
| I | `"natural language processing"` | vale | 13: 7 SI, 6 NO (1 / 1) | IEEE *Natural language processing* (p.354) | Se queda |
| I | `NLP` | vale | 3: 2 SI, 1 NO (0 / 0) | IEEE, UF de *Natural language processing* | Se queda |
| I | `"language model"` | vale | 15: 9 SI, 6 NO (0 / 0) | Libre | Se queda |
| I | `LLM` | vale | 13: 7 SI, 6 NO (0 / 0) | Libre | Se queda |
| I | `LLMs` | vale | 14: 6 SI, 8 NO (0 / 0) | Libre | Se queda |
| I | `"generative AI"` | no aporta | 11: 2 SI, 9 NO (0 / 0) | Libre | Se quita por el máximo de 100: `AI` ya recupera toda frase que lo contiene |
| I | `"generative artificial intelligence"` | no aporta | 7: 2 SI, 5 NO (0 / 0) | Libre | Se quita por el máximo de 100: `"artificial intelligence"` ya la recupera |
| I | `ChatGPT` | vale | 11: 2 SI, 9 NO (0 / 0) | Libre | Se queda |
| I | `GPT` | vale | 6: 2 SI, 4 NO (0 / 0) | Libre | Se queda |
| I | `"prompt engineering"` | vale | 5: 4 SI, 1 NO (0 / 0) | Libre | Se queda |
| I | `"computer vision"` | vale | 3: 1 SI, 2 NO (0 / 0) | IEEE *Computer vision* (p.101) | Se queda |
| I | `chatbot` | vale | 4: 2 SI, 2 NO (1 / 0) | Libre | Se queda |
| I | `"conversational agents"` | revisar | 1: 0 SI, 1 NO (0 / 1) | Libre | Se queda |
| I | `"intelligent agents"` | vale | 1: 1 SI, 0 NO (0 / 0) | IEEE *Intelligent agents* (p.261) | Se queda |
| I | `"virtual agent"` | vale | 1: 1 SI, 0 NO (0 / 0) | Libre | Se queda; recupera también el plural |
| I | `"text simplification"` | vale | 9: 6 SI, 3 NO (0 / 1) | Libre | Se queda |
| I | `"lexical simplification"` | vale | 1: 1 SI, 0 NO (0 / 0) | Libre | Se queda |
| I | `"text adaptation"` | vale | 2: 1 SI, 1 NO (0 / 1) | Libre | Se queda |
| I | `"text processing"` | vale | 4: 4 SI, 0 NO (1 / 0) | Libre | Se queda |
| I | `"text analysis"` | vale | 1: 1 SI, 0 NO (0 / 0) | IEEE *Text analysis* (p.539) | Se queda |
| I | `"text mining"` | revisar | 0 registros | IEEE *Text mining* (p.539) | Se queda |
| I | `"computational linguistics"` | vale | 2: 2 SI, 0 NO (0 / 0) | IEEE *Computational linguistics* (p.95) | Se queda |
| I | `"adaptive user interface"` | revisar | 0 registros | Libre | Se queda |
| I | `"speech recognition"` | vale | 10: 4 SI, 6 NO (3 / 1) | IEEE *Speech recognition* (p.506) | Se queda |
| I | `"recommender systems"` | revisar | 0 registros | IEEE *Recommender systems* (p.454) | Se queda |
| I | `"natural language generation"` | revisar | 0 registros | Libre | Se queda |
| I | `"generative adversarial networks"` | vale | 2: 1 SI, 1 NO (0 / 0) | IEEE *Generative adversarial networks* (p.210) | Se queda |
| I | `"fuzzy logic"` | vale | 1: 1 SI, 0 NO (0 / 0) | IEEE *Fuzzy logic* (p.205) | Se queda |
| I | `"fuzzy inference"` | vale | 1: 1 SI, 0 NO (0 / 0) | IEEE, UF de *Fuzzy logic* | Se queda |
| I | `"ambient intelligence"` | vale | 1: 1 SI, 0 NO (0 / 0) | IEEE *Ambient intelligence* (p.19) | Se queda |
| I | `"context awareness"` | revisar | 0 registros | IEEE *Context awareness* (p.106) | Se queda |
| I | `"context-aware"` | vale | 5: 2 SI, 3 NO (1 / 2) | Libre | Se queda |
| I | `"reinforcement learning"` | vale | 1: 1 SI, 0 NO (0 / 0) | IEEE *Reinforcement learning* (p.457) | Se queda |
| I | `"contrastive learning"` | vale | 5: 3 SI, 2 NO (0 / 0) | Libre | Se queda |
| I | `"cognitive systems"` | agregar | Palabra clave de 3 SI y 2 NO, sin cubrir | IEEE *Cognitive systems* (p.86), NT de *Artificial intelligence*, UF *Cognitive computing* | Se agrega |
| C | `blindness` | vale | 2: 2 SI, 0 NO (1 / 0) | IEEE *Blindness* (p.54) | Se queda |
| C | `deafness` | revisar | 3: 0 SI, 3 NO (0 / 1) | IEEE *Deafness* (p.125) | Se queda: no cumple la regla de retiro |
| C | `deaf` | vale | 8: 1 SI, 7 NO (0 / 3) | Libre | Se queda |
| C | `"visual impairment"` | revisar | 3: 0 SI, 3 NO (0 / 0) | Libre | Se queda |
| C | `"visually impaired"` | vale | 2: 1 SI, 1 NO (0 / 0) | Libre | Se queda |
| C | `"low vision"` | vale | 3: 2 SI, 1 NO (1 / 0) | Libre | Se queda |
| C | `"hearing impairment"` | vale | 4: 1 SI, 3 NO (0 / 2) | Libre | Se queda |
| C | `"hearing impaired"` | revisar | 0 registros | Libre | Se queda |
| C | `"sensory impairment"` | revisar | 0 registros | Libre | Se queda |
| C | `"screen reader"` | revisar | 1: 0 SI, 1 NO (0 / 0) | Libre | Se queda |
| C | `WCAG` | vale | 8: 6 SI, 2 NO (0 / 0) | Libre | Se queda |
| C | `"Web Content Accessibility Guidelines"` | no aporta | 3: 2 SI, 1 NO (0 / 0) | Libre | Se quita por el máximo de 100: `accessibility` ya la recupera |
| C | `accessibility` | vale | 87: 34 SI, 53 NO (23 / 36) | Libre | Se queda |
| C | `"accessible design"` | revisar | 0 registros | Libre | Se queda |
| C | `"accessible interface"` | vale | 3: 2 SI, 1 NO (1 / 0) | Libre | Se queda |
| C | `"inclusive design"` | vale | 14: 4 SI, 10 NO (2 / 3) | Libre | Se queda |
| C | `"universal design"` | vale | 6: 1 SI, 5 NO (0 / 3) | Libre | Se queda |
| C | `"digital inclusion"` | vale | 3: 2 SI, 1 NO (1 / 1) | Libre | Se queda |
| C | `"co-design"` | agregar | «co-design», «co-designs» y «co-designing»: 5 SI y 3 NO, sin cubrir | Libre (sin descriptor IEEE) | Se agrega |
| C | `"user centered design"` | agregar | Palabra clave de 2 SI y 1 NO, sin cubrir | IEEE *User centered design* (p.566), UF *User-centred design* | Se agrega; revisa la exclusión previa del picoc |
| C | `pictograms` | agregar | Palabra clave de 2 SI y 0 NO, sin cubrir | Libre (sin descriptor IEEE) | Se agrega |
| O | `usability` | vale | 30: 20 SI, 10 NO (12 / 5) | IEEE *Usability* (p.565) | Se queda |
| O | `"user experience"` | vale | 9: 3 SI, 6 NO (1 / 4) | Libre | Se queda |
| O | `metric` | vale | 3: 1 SI, 2 NO (0 / 2) | Libre | Se queda |
| O | `metrics` | vale | 15: 3 SI, 12 NO (0 / 11) | Libre | Se queda |
| O | `"accessibility metric"` | no aporta | 0 registros | Libre | Se quita por el máximo de 100: `metric` ya la recupera |
| O | `"readability metrics"` | vale | 1: 1 SI, 0 NO (0 / 0) | IEEE *Readability metrics* (p.453) | Se queda |
| O | `readability` | vale | 14: 6 SI, 8 NO (3 / 3) | Libre | Se queda |
| O | `"plain language"` | vale | 9: 6 SI, 3 NO (0 / 0) | Libre | Se queda |
| O | `"easy-to-read"` | vale | 6: 4 SI, 2 NO (0 / 0) | Libre | Se queda |
| O | `"easy read"` | revisar | 3: 0 SI, 3 NO (0 / 2) | Libre | Se queda: no cumple la regla de retiro |
| O | `"software quality"` | revisar | 0 registros | IEEE *Software quality* (p.498) | Se queda |
| O | `"cognitive load"` | vale | 11: 4 SI, 7 NO (1 / 4) | Libre | Se queda |
| O | `"accessibility evaluation"` | vale | 1: 1 SI, 0 NO (0 / 0) | Libre | Se queda |
| O | `"accessibility testing"` | revisar | 0 registros | Libre | Se queda |
| O | `"user study"` | vale | 3: 2 SI, 1 NO (0 / 0) | Libre | Se queda |
| O | `comprehension` | vale | 25: 9 SI, 16 NO (1 / 10) | Libre | Se queda |
| O | `understandability` | vale | 3: 1 SI, 2 NO (0 / 0) | Libre | Se queda |
| O | `"user satisfaction"` | vale | 2: 1 SI, 1 NO (0 / 1) | Libre | Se queda |
| O | `"accessibility audit"` | revisar | 0 registros | Libre | Se queda |
| O | `"accessibility assessment"` | revisar | 0 registros | Libre | Se queda |
| O | `ergonomics` | vale | 1: 1 SI, 0 NO (1 / 0) | IEEE *Ergonomics* (p.178) | Se queda |
| O | `"human engineering"` | vale | 26: 9 SI, 17 NO (3 / 14) | IEEE, UF de *Ergonomics* | Se queda |
| O | `"user acceptance"` | revisar | 2: 0 SI, 2 NO (0 / 1) | Libre | Se queda |
| O | `"human evaluation"` | vale | 1: 1 SI, 0 NO (0 / 0) | Libre | Se queda |

## Query Scopus

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
    OR "reinforcement learning" OR "contrastive learning" OR "cognitive systems" )
  AND
  ( blindness OR deafness OR deaf OR "visual impairment" OR "visually impaired"
    OR "low vision" OR "hearing impairment" OR "hearing impaired" OR "sensory impairment"
    OR "screen reader" OR WCAG OR accessibility OR "accessible design"
    OR "accessible interface" OR "inclusive design" OR "universal design"
    OR "digital inclusion" OR "co-design" OR "user centered design" OR pictograms )
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

## Query Web of Science

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
  OR "reinforcement learning" OR "contrastive learning" OR "cognitive systems")
AND ALL=(blindness OR deafness OR deaf OR "visual impairment" OR "visually impaired"
  OR "low vision" OR "hearing impairment" OR "hearing impaired" OR "sensory impairment"
  OR "screen reader" OR WCAG OR accessibility OR "accessible design"
  OR "accessible interface" OR "inclusive design" OR "universal design"
  OR "digital inclusion" OR "co-design" OR "user centered design" OR pictograms)
AND ALL=(usability OR "user experience" OR metric OR metrics
  OR "readability metrics" OR readability OR "plain language" OR "easy-to-read"
  OR "easy read" OR "software quality" OR "cognitive load" OR "accessibility evaluation"
  OR "accessibility testing" OR "user study" OR comprehension OR understandability
  OR "user satisfaction" OR "accessibility audit" OR "accessibility assessment"
  OR ergonomics OR "human engineering" OR "user acceptance" OR "human evaluation")
AND PY=(2021-2026) AND DT=(Article) AND LA=(English OR Spanish)
```

Filtro de la interfaz: Open Access (Web of Science no tiene etiqueta de campo para el acceso abierto).

## Debate

- `"autism spectrum"`, `"generative AI"`, `"generative artificial intelligence"`, `"Web Content Accessibility Guidelines"` y `"accessibility metric"`: el crítico pedía conservarlos porque no cumplen la regla de retiro. Se quitan: cada frase contiene otro término del mismo bloque unido por OR, así que la retirada no cambia los registros recuperados, y la regla del máximo de 100 permite descartar primero las variantes que las bases ya recuperan. El descriptor IEEE *Autism* no se toca.
- `automation`: se descarta, como pedía el crítico. No es una técnica de inteligencia artificial y reintroduciría las pruebas automáticas del bloque de ciclo de vida ya retirado.
- `"augmentative and alternative communication"`: se descarta, como pedía el crítico. Es tecnología de apoyo, excluida en el picoc, y solo tiene 1 SI de evidencia.
- `"co-design"`, `"user centered design"`, `pictograms` y `"cognitive systems"`: el crítico solo admitía `"co-design"` porque contaba con un único hueco libre. Al liberarse seis huecos entran los cuatro. `"user centered design"` revisa la exclusión previa: el diseño es una fase del ciclo de vida exigida por el CI4 y el término entra en el bloque C, junto al diseño inclusivo, no como bloque obligatorio.
- `"mobile applications"` y `"software design"` (3 SI y 0 NO cada uno): ninguno de los dos los propone, porque no encajan en ningún bloque del PICO sin reintroducir el bloque de contexto. Quedan como dato a extraer.
- *Deep learning*, *Measurement* y `"Down syndrome"`: siguen fuera, por acuerdo de ambos; la evidencia de ruido del cribado anterior no se contradice en este.
