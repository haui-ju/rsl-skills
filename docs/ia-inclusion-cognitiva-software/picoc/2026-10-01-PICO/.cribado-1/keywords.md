# Rendimiento de los términos de la query (cribado 1)

Sobre 125 registros únicos (título, resumen y palabras clave). SI incluye las dudas. «Solo este término» = registros que ningún otro término de su componente recupera (se perderían si se quita).

| Comp. | Término | Registros | SI | NO | Solo este término (SI / NO) |
|---|---|---|---|---|---|
| P | `autism` | 33 | 11 | 22 | 0 / 6 |
| P | `autistic` | 6 | 2 | 4 | 0 / 0 |
| P | `autism spectrum` | 22 | 9 | 13 | 0 / 0 |
| P | `neurodivers*` | 9 | 6 | 3 | 2 / 1 |
| P | `neurodivergen*` | 14 | 9 | 5 | 2 / 3 |
| P | `neurodevelopmental` | 8 | 3 | 5 | 2 / 2 |
| P | `cognitive disabilit*` | 14 | 11 | 3 | 5 / 0 |
| P | `intellectual disabilit*` | 19 | 5 | 14 | 3 / 10 |
| P | `developmental disabilit*` | 4 | 1 | 3 | 0 / 0 |
| P | `learning disabilit*` | 8 | 6 | 2 | 2 / 1 |
| P | `adhd` | 16 | 8 | 8 | 0 / 1 |
| P | `attention deficit` | 10 | 4 | 6 | 0 / 2 |
| P | `dyslexi*` | 19 | 13 | 6 | 8 / 2 |
| P | `cognitive accessibility` | 19 | 7 | 12 | 2 / 6 |
| P | `learning disorder*` | 2 | 1 | 1 | 0 / 0 |
| P | `learning difficult*` | 5 | 0 | 5 | 0 / 4 |
| P | `dysgraphia` | 1 | 1 | 0 | 0 / 0 |
| P | `reading disabilit*` | 3 | 0 | 3 | 0 / 1 |
| I | `artificial intelligence` | 55 | 27 | 28 | 3 / 4 |
| I | `ai` | 61 | 32 | 29 | 4 / 2 |
| I | `machine learning` | 22 | 4 | 18 | 0 / 6 |
| I | `natural language processing` | 14 | 6 | 8 | 0 / 2 |
| I | `nlp` | 4 | 1 | 3 | 0 / 0 |
| I | `language model` | 15 | 10 | 5 | 0 / 0 |
| I | `llm` | 13 | 9 | 4 | 0 / 0 |
| I | `llms` | 14 | 11 | 3 | 0 / 0 |
| I | `generative ai` | 11 | 7 | 4 | 0 / 0 |
| I | `generative artificial intelligence` | 8 | 7 | 1 | 0 / 0 |
| I | `chatgpt` | 11 | 7 | 4 | 0 / 0 |
| I | `gpt` | 7 | 3 | 4 | 0 / 0 |
| I | `prompt engineering` | 5 | 5 | 0 | 0 / 0 |
| I | `computer vision` | 2 | 1 | 1 | 0 / 0 |
| I | `chatbot` | 4 | 1 | 3 | 0 / 1 |
| I | `conversational agents` | 1 | 0 | 1 | 0 / 1 |
| I | `intelligent agents` | 1 | 1 | 0 | 0 / 0 |
| I | `virtual agent` | 1 | 0 | 1 | 0 / 0 |
| I | `text simplification` | 9 | 4 | 5 | 0 / 1 |
| I | `lexical simplification` | 2 | 1 | 1 | 0 / 1 |
| I | `text adaptation` | 3 | 1 | 2 | 0 / 1 |
| I | `text processing` | 4 | 4 | 0 | 1 / 0 |
| I | `text analysis` | 2 | 1 | 1 | 0 / 1 |
| I | `computational linguistics` | 2 | 1 | 1 | 0 / 0 |
| I | `speech recognition` | 10 | 3 | 7 | 1 / 3 |
| I | `generative adversarial networks` | 2 | 2 | 0 | 0 / 0 |
| I | `fuzzy logic` | 1 | 1 | 0 | 0 / 0 |
| I | `fuzzy inference` | 1 | 1 | 0 | 0 / 0 |
| I | `ambient intelligence` | 2 | 1 | 1 | 0 / 0 |
| I | `context-aware` | 5 | 4 | 1 | 2 / 1 |
| I | `reinforcement learning` | 1 | 0 | 1 | 0 / 0 |
| I | `contrastive learning` | 6 | 3 | 3 | 0 / 0 |
| C | `blindness` | 2 | 2 | 0 | 1 / 0 |
| C | `deafness` | 3 | 0 | 3 | 0 / 1 |
| C | `deaf` | 7 | 2 | 5 | 0 / 2 |
| C | `visual impairment` | 3 | 1 | 2 | 0 / 0 |
| C | `visually impaired` | 3 | 1 | 2 | 0 / 0 |
| C | `low vision` | 3 | 3 | 0 | 1 / 0 |
| C | `hearing impairment` | 4 | 1 | 3 | 0 / 2 |
| C | `screen reader` | 1 | 1 | 0 | 0 / 0 |
| C | `wcag` | 8 | 7 | 1 | 0 / 0 |
| C | `web content accessibility guidelines` | 3 | 2 | 1 | 0 / 0 |
| C | `accessibility` | 94 | 42 | 52 | 23 / 41 |
| C | `accessible interface` | 3 | 2 | 1 | 0 / 1 |
| C | `inclusive design` | 15 | 9 | 6 | 3 / 2 |
| C | `universal design` | 5 | 3 | 2 | 1 / 1 |
| C | `digital inclusion` | 4 | 2 | 2 | 1 / 1 |
| O | `usability` | 38 | 19 | 19 | 11 / 13 |
| O | `user experience` | 11 | 6 | 5 | 2 / 4 |
| O | `metric` | 2 | 0 | 2 | 0 / 1 |
| O | `metrics` | 16 | 1 | 15 | 0 / 12 |
| O | `readability metrics` | 1 | 0 | 1 | 0 / 0 |
| O | `readability` | 14 | 9 | 5 | 5 / 1 |
| O | `plain language` | 9 | 5 | 4 | 0 / 0 |
| O | `easy-to-read` | 6 | 4 | 2 | 0 / 0 |
| O | `easy read` | 3 | 0 | 3 | 0 / 2 |
| O | `cognitive load` | 9 | 5 | 4 | 2 / 2 |
| O | `accessibility evaluation` | 1 | 1 | 0 | 0 / 0 |
| O | `user study` | 3 | 2 | 1 | 0 / 0 |
| O | `comprehension` | 27 | 14 | 13 | 4 / 9 |
| O | `understandability` | 3 | 1 | 2 | 0 / 0 |
| O | `user satisfaction` | 2 | 0 | 2 | 0 / 1 |
| O | `human engineering` | 27 | 15 | 12 | 9 / 9 |
| O | `user acceptance` | 2 | 0 | 2 | 0 / 1 |
| O | `human evaluation` | 1 | 1 | 0 | 0 / 0 |

Sin registros: `asperger` (P), `intellectual developmental disorder` (P), `dyscalculia` (P), `text mining` (I), `adaptive user interface` (I), `recommender systems` (I), `natural language generation` (I), `context awareness` (I), `hearing impaired` (C), `sensory impairment` (C), `accessible design` (C), `accessibility metric` (O), `software quality` (O), `accessibility testing` (O), `accessibility audit` (O), `accessibility assessment` (O), `ergonomics` (O).

## Palabras clave de las fuentes que ninguna query cubre (≥ 1 registro aceptado y al menos tantos SI como NO)

| Palabra clave | SI | NO |
|---|---|---|
| human computer interaction | 11 | 7 |
| students | 10 | 7 |
| large language models | 9 | 2 |
| assistive technology | 8 | 4 |
| user interfaces | 5 | 2 |
| behavioral research | 5 | 4 |
| inclusive education | 4 | 0 |
| augmented reality | 4 | 2 |
| literature review | 3 | 0 |
| websites | 3 | 0 |
| user centered design | 3 | 0 |
| digital libraries | 3 | 0 |
| user profile | 3 | 0 |
| real- time | 3 | 1 |
| disability | 3 | 1 |
| virtual reality | 3 | 1 |
| human-computer interaction | 3 | 2 |
| educational technology | 3 | 2 |
| cognitive systems | 3 | 2 |
| interactive computer systems | 3 | 3 |
| engineering education | 3 | 3 |
| support systems | 2 | 0 |
| support technology | 2 | 0 |
| reviews | 2 | 0 |
| down's syndrome | 2 | 0 |
| natural languages | 2 | 0 |
| scoping review | 2 | 0 |
| equity | 2 | 0 |
| multi-modal | 2 | 0 |
| accessible interfaces | 2 | 0 |
| employment | 2 | 0 |
| language models | 2 | 0 |
| education | 2 | 0 |
| reading skills | 2 | 0 |
| manual process | 2 | 0 |
| semi-automatics | 2 | 0 |
| software prototyping | 2 | 0 |
| adaptive learning | 2 | 0 |
| higher education students | 2 | 0 |
| down syndrome | 2 | 1 |
| literature reviews | 2 | 1 |
| design and evaluations | 2 | 1 |
| mobile applications | 2 | 1 |
| interactive computer graphics | 2 | 1 |
| 'current | 2 | 1 |
| open systems | 2 | 1 |
| software design | 2 | 1 |
| cognitive loads | 2 | 1 |
| systematic literature review | 2 | 2 |
| systematic review | 2 | 2 |
| daily lives | 2 | 2 |
| mobile web applications | 1 | 0 |
| computational complexity | 1 | 0 |
| automated text analyze | 1 | 0 |
| mobile web | 1 | 0 |
| regulatory compliance | 1 | 0 |
| conversational voice user interfaces | 1 | 0 |
| commercial applications | 1 | 0 |
| conversational voice user interface | 1 | 0 |
| user groups | 1 | 0 |
