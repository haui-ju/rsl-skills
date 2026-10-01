# Sugerencia de búsqueda — cribado 1

<!-- cribado:sugerencia picoc=2026-10-01-PICO -->

Basada en 125 registros únicos de Scopus y Web of Science (SI 52, NO 73). No reemplaza la búsqueda: la amplía.

**Efecto esperado:** 3 términos agregados, 3 quitados; los términos quitados dejan fuera 28 de los 125 registros actuales (0 SI).

## Keywords

| Comp. | Término | Estado | Evidencia | Vocabulario | Decisión |
|---|---|---|---|---|---|
| P | `learning difficult*` | no aporta | 0 SI, 4 NO exclusivos | Libre | Se quita |
| P | `neurodevelopmental` | no aporta | 0 SI, 4 NO exclusivos | Libre | Se quita |
| C | `inclusive design` | no aporta | 0 SI, 5 NO exclusivos | Libre | Se quita |
| I | `software prototyping` | agregar | Prototipos en SI (NeuRoam) | IEEE *Software prototyping* (p.498) | Se agrega |
| I | `accessible content generation` | agregar | Palabras clave de aceptados | Libre | Se agrega |
| I | `interactive computer systems` | agregar | 4 SI en índice, sin cubrir | Libre | Se agrega |
| P–O | Resto de la query vigente | vale / revisar | Ver `.cribado-1/keywords.md` | — | Sin cambio |

## Query Scopus

```text
TITLE-ABS-KEY (
  ( autism OR autistic OR "autism spectrum" OR neurodivers* OR neurodivergen*
    OR "cognitive disabilit*" OR "intellectual disabilit*"
    OR "developmental disabilit*" OR "learning disabilit*" OR ADHD OR "attention deficit"
    OR dyslexi* OR "cognitive accessibility" OR Asperger
    OR "intellectual developmental disorder" OR "learning disorder*"
    OR dyscalculia OR dysgraphia OR "reading disabilit*" )
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
    OR "reinforcement learning" OR "contrastive learning"
    OR "software prototyping" OR "accessible content generation" OR "interactive computer systems" )
  AND
  ( blindness OR deafness OR deaf OR "visual impairment" OR "visually impaired"
    OR "low vision" OR "hearing impairment" OR "hearing impaired" OR "sensory impairment"
    OR "screen reader" OR WCAG OR "Web Content Accessibility Guidelines" OR accessibility
    OR "accessible design" OR "accessible interface"
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
AND ( LIMIT-TO ( DOCTYPE , "ar" ) OR LIMIT-TO ( DOCTYPE , "cp" ) )
AND ( LIMIT-TO ( LANGUAGE , "English" ) OR LIMIT-TO ( LANGUAGE , "Spanish" ) )
AND ( LIMIT-TO ( OA , "all" ) )
```

## Query Web of Science

```text
ALL=(autism OR autistic OR "autism spectrum" OR neurodivers* OR neurodivergen*
  OR "cognitive disabilit*" OR "intellectual disabilit*"
  OR "developmental disabilit*" OR "learning disabilit*" OR ADHD OR "attention deficit"
  OR dyslexi* OR "cognitive accessibility" OR Asperger
  OR "intellectual developmental disorder" OR "learning disorder*"
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
  OR "reinforcement learning" OR "contrastive learning"
  OR "software prototyping" OR "accessible content generation" OR "interactive computer systems")
AND ALL=(blindness OR deafness OR deaf OR "visual impairment" OR "visually impaired"
  OR "low vision" OR "hearing impairment" OR "hearing impaired" OR "sensory impairment"
  OR "screen reader" OR WCAG OR "Web Content Accessibility Guidelines" OR accessibility
  OR "accessible design" OR "accessible interface"
  OR "universal design" OR "digital inclusion")
AND ALL=(usability OR "user experience" OR metric OR metrics OR "accessibility metric"
  OR "readability metrics" OR readability OR "plain language" OR "easy-to-read"
  OR "easy read" OR "software quality" OR "cognitive load" OR "accessibility evaluation"
  OR "accessibility testing" OR "user study" OR comprehension OR understandability
  OR "user satisfaction" OR "accessibility audit" OR "accessibility assessment"
  OR ergonomics OR "human engineering" OR "user acceptance" OR "human evaluation")
AND PY=(2021-2026) AND DT=(Article OR "Proceedings Paper") AND LA=(English OR Spanish)
```

Filtro de la interfaz: Open Access.

## Debate

- Sin CE de revisiones ni e-learning, el cribado 1 admite más SI con duda; la sugerencia de keywords no cambia de criterio.
- Retiros: `learning difficult*`, `neurodevelopmental`, `inclusive design` (regla 0 SI y ≥3 NO exclusivos).
- Agregados en I: `software prototyping`, `accessible content generation`, `interactive computer systems`.
