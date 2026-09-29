# Rendimiento de los términos de la query (cribado 1)

Sobre 120 registros únicos (título, resumen y palabras clave). SI incluye las dudas. «Solo este término» = registros que ningún otro término de su componente recupera (se perderían si se quita).

| Comp. | Término | Registros | SI | NO | Solo este término (SI / NO) |
|---|---|---|---|---|---|
| P | `autism` | 38 | 3 | 35 | 0 / 7 |
| P | `autistic` | 8 | 0 | 8 | 0 / 0 |
| P | `autism spectrum` | 29 | 3 | 26 | 0 / 0 |
| P | `neurodivers*` | 6 | 1 | 5 | 1 / 1 |
| P | `neurodivergen*` | 7 | 2 | 5 | 2 / 2 |
| P | `neurodevelopmental` | 13 | 1 | 12 | 1 / 6 |
| P | `cognitive disabilit*` | 10 | 5 | 5 | 0 / 2 |
| P | `intellectual disabilit*` | 12 | 7 | 5 | 4 / 4 |
| P | `developmental disabilit*` | 4 | 2 | 2 | 0 / 0 |
| P | `learning disabilit*` | 7 | 4 | 3 | 1 / 2 |
| P | `adhd` | 11 | 2 | 9 | 0 / 1 |
| P | `attention deficit` | 10 | 1 | 9 | 0 / 2 |
| P | `dyslexi*` | 18 | 6 | 12 | 5 / 7 |
| P | `cognitive accessibility` | 16 | 6 | 10 | 0 / 7 |
| P | `down syndrome` | 4 | 0 | 4 | 0 / 4 |
| P | `learning disorder*` | 3 | 0 | 3 | 0 / 1 |
| P | `learning difficult*` | 3 | 0 | 3 | 0 / 2 |
| I | `artificial intelligence` | 48 | 10 | 38 | 1 / 7 |
| I | `ai` | 50 | 11 | 39 | 1 / 4 |
| I | `machine learning` | 30 | 2 | 28 | 0 / 0 |
| I | `machine-learning` | 30 | 2 | 28 | 0 / 0 |
| I | `deep learning` | 11 | 0 | 11 | 0 / 4 |
| I | `natural language processing` | 14 | 6 | 8 | 2 / 0 |
| I | `nlp` | 6 | 2 | 4 | 0 / 0 |
| I | `large language model*` | 22 | 10 | 12 | 1 / 0 |
| I | `llm` | 10 | 5 | 5 | 0 / 0 |
| I | `llms` | 11 | 4 | 7 | 0 / 0 |
| I | `generative ai` | 5 | 1 | 4 | 0 / 0 |
| I | `generative artificial intelligence` | 6 | 2 | 4 | 0 / 0 |
| I | `chatgpt` | 8 | 2 | 6 | 0 / 0 |
| I | `gpt` | 6 | 2 | 4 | 0 / 0 |
| I | `computer vision` | 4 | 0 | 4 | 0 / 0 |
| I | `chatbot` | 4 | 1 | 3 | 0 / 1 |
| I | `conversational agents` | 1 | 0 | 1 | 0 / 1 |
| I | `text simplification` | 9 | 6 | 3 | 0 / 1 |
| I | `speech recognition` | 10 | 1 | 9 | 1 / 4 |
| C | `blindness` | 3 | 0 | 3 | 0 / 2 |
| C | `deafness` | 3 | 0 | 3 | 0 / 1 |
| C | `deaf` | 6 | 1 | 5 | 0 / 1 |
| C | `visual impairment` | 2 | 0 | 2 | 0 / 0 |
| C | `visually impaired` | 2 | 1 | 1 | 0 / 0 |
| C | `low vision` | 3 | 0 | 3 | 0 / 1 |
| C | `hearing impairment` | 9 | 0 | 9 | 0 / 7 |
| C | `wcag` | 6 | 4 | 2 | 0 / 0 |
| C | `web content accessibility guidelines` | 3 | 2 | 1 | 0 / 0 |
| C | `accessibility` | 85 | 25 | 60 | 17 / 46 |
| C | `accessible interface` | 3 | 0 | 3 | 0 / 1 |
| C | `inclusive design` | 8 | 2 | 6 | 0 / 2 |
| C | `universal design` | 6 | 1 | 5 | 0 / 3 |
| O | `usability` | 32 | 9 | 23 | 7 / 15 |
| O | `user experience` | 8 | 1 | 7 | 1 / 5 |
| O | `measurement` | 12 | 0 | 12 | 0 / 10 |
| O | `metric` | 3 | 1 | 2 | 0 / 2 |
| O | `metrics` | 20 | 2 | 18 | 0 / 15 |
| O | `readability metrics` | 1 | 1 | 0 | 0 / 0 |
| O | `readability` | 13 | 6 | 7 | 3 / 2 |
| O | `plain language` | 9 | 5 | 4 | 0 / 1 |
| O | `easy-to-read` | 5 | 4 | 1 | 0 / 0 |
| O | `cognitive load` | 11 | 3 | 8 | 1 / 5 |
| O | `accessibility evaluation` | 1 | 1 | 0 | 0 / 0 |
| O | `user study` | 3 | 1 | 2 | 0 / 0 |
| O | `comprehension` | 25 | 8 | 17 | 1 / 12 |
| O | `understandability` | 3 | 1 | 2 | 0 / 0 |
| O | `user satisfaction` | 2 | 0 | 2 | 0 / 1 |

Sin registros: `asperger` (P), `intellectual developmental disorder` (P), `dyscalculia` (P), `adaptive user interface` (I), `recommender systems` (I), `natural language generation` (I), `hearing impaired` (C), `sensory impairment` (C), `screen reader` (C), `accessible design` (C), `accessibility metric` (O), `software quality` (O), `accessibility testing` (O), `accessibility audit` (O), `accessibility assessment` (O).

## Palabras clave de las fuentes que ninguna query cubre (≥ 2 registros aceptados)

| Palabra clave | SI | NO |
|---|---|---|
| students | 7 | 6 |
| language model | 6 | 3 |
| human engineering | 5 | 3 |
| prompt engineering | 4 | 0 |
| assistive technology | 4 | 6 |
| real- time | 3 | 1 |
| interactive computer systems | 3 | 2 |
| websites | 2 | 0 |
| economic and social effects | 2 | 0 |
| manual process | 2 | 0 |
| semi-automatics | 2 | 0 |
| computational linguistics | 2 | 0 |
| text processing | 2 | 1 |
| daily lives | 2 | 1 |
| cognitive loads | 2 | 1 |
