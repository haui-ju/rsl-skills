# Debate del marco — 2026-09-29-2-PICO

**Fecha:** 2026-09-29 · **Versión base:** [2026-09-29-PICO](../2026-09-29-PICO/picoc.md) · **Modo:** sugerencia desde `picoc/2026-09-29-PICO/cribado-1-sugerencia.md`

La sugerencia ya se debatió en el cribado 1 (`defensor-rsl` y `critico-rsl`, modo sugerencia); esta versión solo la aplica. La búsqueda se amplía: se agregan 26 términos, se quitan 4 y se fusiona 1, con lo que la query queda en 100 keywords, el máximo de la regla R2. Los términos quitados dejan fuera 16 de los 120 registros del cribado 1, todos NO.

## Cambios

| Término | Comp. | Acción | Evidencia del cribado 1 |
|---------|-------|--------|-------------------------|
| `dysgraphia` | P | agregar | Perfil afín a la dislexia; MeSH *Agraphia* (D000381) |
| `"reading disabilit*"` | P | agregar | Perfil afín a la dislexia; MeSH *Dyslexia* (D004410) |
| `"Down syndrome"` | P | quitar | 4 registros, 0 SI, 4 NO exclusivos |
| `"language model"` | I | agregar | 7 SI y 2 NO en palabras clave; sustituye a `"large language model*"`, que incluye |
| `"large language model*"` | I | fusionar | 22 registros, 11 SI; los recupera `"language model"` |
| `"machine-learning"` | I | quitar | Redundante con `"machine learning"` (los mismos 30 registros); límite de 100 keywords |
| `"deep learning"` | I | quitar | 11 registros, 0 SI, 4 NO exclusivos |
| `"prompt engineering"` | I | agregar | 4 SI y 0 NO en palabras clave |
| `"text processing"` | I | agregar (libre) | 3 SI y 0 NO; el descriptor IEEE homónimo es tipografía |
| `"text analysis"` · `"text mining"` | I | agregar | 1 SI y 0 NO; IEEE p.539 |
| `"lexical simplification"` · `"text adaptation"` | I | agregar | Variantes de `"text simplification"` (5 SI) |
| `"computational linguistics"` | I | agregar | Afín a `"natural language processing"` (7 SI); IEEE p.95 |
| `"generative adversarial networks"` | I | agregar | 2 SI y 0 NO; IEEE p.210 |
| `"fuzzy logic"` · `"fuzzy inference"` | I | agregar | 1 SI y 0 NO; IEEE p.205 y su sinónimo |
| `"intelligent agents"` · `"virtual agent"` | I | agregar | 1 SI y 0 NO cada uno; IEEE p.261 y término libre |
| `"ambient intelligence"` | I | agregar | 2 SI y 0 NO; IEEE p.19 |
| `"context awareness"` · `"context-aware"` | I | agregar | 1 SI y 0 NO; IEEE p.106 y su variante |
| `"reinforcement learning"` | I | agregar | Término específico de *Machine learning*; IEEE p.457 |
| `"contrastive learning"` | I | agregar | 3 SI y 3 NO en palabras clave |
| `"digital inclusion"` | C | agregar | Ampliación desde el tesauro, sin evidencia en este cribado |
| `measurement` | O | quitar | 12 registros, 0 SI, 10 NO exclusivos; quedan `metric` y `metrics` |
| `ergonomics` · `"human engineering"` | O | agregar | «human engineering» 6 SI y 2 NO; IEEE p.178 y su sinónimo |
| `"easy read"` | O | agregar | Variante de `"easy-to-read"` (4 SI) |
| `"user acceptance"` · `"human evaluation"` | O | agregar | Formas de reportar la evaluación con personas, sin evidencia propia |

## Ajustes de esta versión

- **Comodines de IEEE Xplore.** El bloque P usa los 10 comodines que admite IEEE Xplore. Por eso los comodines nuevos del bloque I (`"language model*"`, `"intelligent agent*"`, `"virtual agent*"` y `"generative adversarial network*"`) pasan a frases cerradas en la tabla y en las tres queries, que deben coincidir término a término (regla R2). Scopus y Web of Science recuperan las variantes de número de las frases. *Intelligent agents* y *Generative adversarial networks* van en plural para que la etiqueta `"IEEE Terms"` use el nombre exacto del descriptor.
- **Conceptos y notas.** El concepto P ya no nombra el síndrome de Down e incorpora la disgrafía. La nota de O explica que *Measurement* se retira y que `metric` y `metrics` se conservan como términos libres. La justificación de *Neural networks* ya no remite a `"deep learning"`. La validación de Perry et al. (2024) registra que su término de O era *measurement*.
- **Keywords del paper.** Se mantienen sin cambios; ningún término nuevo representa mejor el tema.

## Queda para el usuario

- Ejecutar las nuevas queries en Scopus y Web of Science, colocar las exportaciones en `picoc/2026-09-29-2-PICO/` y correr `rsl-cribado-1`. El cribado dirá qué aportan los términos agregados sin evidencia (`dysgraphia`, `"reading disabilit*"`, `"digital inclusion"`, `"reinforcement learning"`, `"user acceptance"` y `"human evaluation"`).
