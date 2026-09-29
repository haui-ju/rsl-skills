# Rendimiento de los términos de la query (cribado 1)

Sobre 120 registros únicos (título, resumen y palabras clave). SI incluye las dudas. «Solo este término» = registros que ningún otro término de su componente recupera (se perderían si se quita).

| Comp. | Término | Registros | SI | NO | Solo este término (SI / NO) |
|---|---|---|---|---|---|
| P | `autism` | 38 | 5 | 33 | 0 / 7 |
| P | `autistic` | 8 | 1 | 7 | 0 / 0 |
| P | `autism spectrum` | 29 | 5 | 24 | 0 / 0 |
| P | `neurodivers*` | 6 | 1 | 5 | 1 / 1 |
| P | `neurodivergen*` | 7 | 2 | 5 | 2 / 2 |
| P | `neurodevelopmental` | 13 | 2 | 11 | 2 / 5 |
| P | `cognitive disabilit*` | 10 | 5 | 5 | 1 / 1 |
| P | `intellectual disabilit*` | 12 | 7 | 5 | 4 / 4 |
| P | `developmental disabilit*` | 4 | 3 | 1 | 0 / 0 |
| P | `learning disabilit*` | 7 | 5 | 2 | 2 / 1 |
| P | `adhd` | 11 | 4 | 7 | 0 / 1 |
| P | `attention deficit` | 10 | 3 | 7 | 0 / 2 |
| P | `dyslexi*` | 18 | 8 | 10 | 7 / 5 |
| P | `cognitive accessibility` | 16 | 6 | 10 | 1 / 6 |
| P | `down syndrome` | 4 | 0 | 4 | 0 / 4 |
| P | `learning disorder*` | 3 | 0 | 3 | 0 / 1 |
| P | `learning difficult*` | 3 | 0 | 3 | 0 / 2 |
| I | `artificial intelligence` | 48 | 13 | 35 | 2 / 6 |
| I | `ai` | 50 | 17 | 33 | 3 / 2 |
| I | `machine learning` | 30 | 4 | 26 | 0 / 0 |
| I | `machine-learning` | 30 | 4 | 26 | 0 / 0 |
| I | `deep learning` | 11 | 0 | 11 | 0 / 4 |
| I | `natural language processing` | 14 | 7 | 7 | 2 / 0 |
| I | `nlp` | 6 | 1 | 5 | 0 / 0 |
| I | `large language model*` | 22 | 11 | 11 | 1 / 0 |
| I | `llm` | 10 | 6 | 4 | 0 / 0 |
| I | `llms` | 11 | 5 | 6 | 0 / 0 |
| I | `generative ai` | 5 | 2 | 3 | 0 / 0 |
| I | `generative artificial intelligence` | 6 | 3 | 3 | 0 / 0 |
| I | `chatgpt` | 8 | 2 | 6 | 0 / 0 |
| I | `gpt` | 6 | 2 | 4 | 0 / 0 |
| I | `computer vision` | 4 | 0 | 4 | 0 / 0 |
| I | `chatbot` | 4 | 2 | 2 | 1 / 0 |
| I | `conversational agents` | 1 | 0 | 1 | 0 / 1 |
| I | `text simplification` | 9 | 5 | 4 | 0 / 1 |
| I | `speech recognition` | 10 | 3 | 7 | 2 / 3 |
| C | `blindness` | 3 | 0 | 3 | 0 / 2 |
| C | `deafness` | 3 | 0 | 3 | 0 / 1 |
| C | `deaf` | 6 | 1 | 5 | 0 / 1 |
| C | `visual impairment` | 2 | 0 | 2 | 0 / 0 |
| C | `visually impaired` | 2 | 1 | 1 | 0 / 0 |
| C | `low vision` | 3 | 1 | 2 | 1 / 0 |
| C | `hearing impairment` | 9 | 1 | 8 | 0 / 7 |
| C | `wcag` | 6 | 5 | 1 | 0 / 0 |
| C | `web content accessibility guidelines` | 3 | 2 | 1 | 0 / 0 |
| C | `accessibility` | 85 | 32 | 53 | 23 / 40 |
| C | `accessible interface` | 3 | 1 | 2 | 0 / 1 |
| C | `inclusive design` | 8 | 2 | 6 | 0 / 2 |
| C | `universal design` | 6 | 2 | 4 | 1 / 2 |
| O | `usability` | 32 | 16 | 16 | 12 / 10 |
| O | `user experience` | 8 | 2 | 6 | 1 / 5 |
| O | `measurement` | 12 | 0 | 12 | 0 / 10 |
| O | `metric` | 3 | 1 | 2 | 0 / 2 |
| O | `metrics` | 20 | 3 | 17 | 0 / 15 |
| O | `readability metrics` | 1 | 1 | 0 | 0 / 0 |
| O | `readability` | 13 | 6 | 7 | 3 / 2 |
| O | `plain language` | 9 | 6 | 3 | 0 / 1 |
| O | `easy-to-read` | 5 | 4 | 1 | 0 / 0 |
| O | `cognitive load` | 11 | 3 | 8 | 1 / 5 |
| O | `accessibility evaluation` | 1 | 1 | 0 | 0 / 0 |
| O | `user study` | 3 | 2 | 1 | 0 / 0 |
| O | `comprehension` | 25 | 10 | 15 | 3 / 10 |
| O | `understandability` | 3 | 1 | 2 | 0 / 0 |
| O | `user satisfaction` | 2 | 0 | 2 | 0 / 1 |

Sin registros: `asperger` (P), `intellectual developmental disorder` (P), `dyscalculia` (P), `adaptive user interface` (I), `recommender systems` (I), `natural language generation` (I), `hearing impaired` (C), `sensory impairment` (C), `screen reader` (C), `accessible design` (C), `accessibility metric` (O), `software quality` (O), `accessibility testing` (O), `accessibility audit` (O), `accessibility assessment` (O).

## Palabras clave de las fuentes que ninguna query cubre (≥ 1 registro aceptado y al menos tantos SI como NO)

| Palabra clave | SI | NO |
|---|---|---|
| students | 8 | 5 |
| language model | 7 | 2 |
| human engineering | 6 | 2 |
| automation | 4 | 0 |
| prompt engineering | 4 | 0 |
| interactive computer systems | 4 | 1 |
| diseases | 4 | 4 |
| text processing | 3 | 0 |
| software design | 3 | 0 |
| real- time | 3 | 1 |
| inclusive education | 3 | 2 |
| contrastive learning | 3 | 3 |
| ambient intelligence | 2 | 0 |
| smart homes | 2 | 0 |
| serious games | 2 | 0 |
| websites | 2 | 0 |
| generative adversarial networks | 2 | 0 |
| economic and social effects | 2 | 0 |
| manual process | 2 | 0 |
| semi-automatics | 2 | 0 |
| mobile applications | 2 | 0 |
| information systems | 2 | 0 |
| information use | 2 | 0 |
| daily lives | 2 | 1 |
| cognitive loads | 2 | 1 |
| emotion recognition | 2 | 2 |
| education computing | 2 | 2 |
| educational technology | 2 | 2 |
| engineering education | 2 | 2 |
| automated text analysis | 1 | 0 |
| fuzzy logic systems | 1 | 0 |
| mobile web applications | 1 | 0 |
| computational complexity | 1 | 0 |
| fuzzy inference | 1 | 0 |
| automated text analyze | 1 | 0 |
| fuzzy logic system | 1 | 0 |
| mobile web | 1 | 0 |
| support systems | 1 | 0 |
| support technology | 1 | 0 |
| text analysis | 1 | 0 |
| regulatory compliance | 1 | 0 |
| text integration | 1 | 0 |
| skills | 1 | 0 |
| ability | 1 | 0 |
| ambient assisted living | 1 | 0 |
| context and user awareness | 1 | 0 |
| distributed sensor networks | 1 | 0 |
| osgi | 1 | 0 |
| domestic appliances | 1 | 0 |
| intelligent buildings | 1 | 0 |
| kitchens | 1 | 0 |
| sensor networks | 1 | 0 |
| handicapped persons | 1 | 0 |
| online gaming | 1 | 0 |
| virtual agents | 1 | 0 |
| online systems | 1 | 0 |
| social networking (online) | 1 | 0 |
| agent based | 1 | 0 |
| digital technologies | 1 | 0 |
| egyptians | 1 | 0 |
