# Debate del marco — 2026-09-28-7-PICO

**Fecha:** 2026-09-28 · **Modo:** completo (ampliación de los cuatro bloques) · **Base:** `2026-09-28-6-PICO` · **Agentes:** critico-rsl, defensor-rsl, redaccion-rsl

## Decisión del usuario (no se debate)

- Incorporar un segundo vocabulario controlado de informática y añadir unos cuantos términos más; con esta versión se cierra la ampliación del marco.
- Sin cambios en el marco, las preguntas de investigación, las keywords del paper ni los filtros de inclusión.

## Vocabulario añadido

Se incorporó la ACM Computing Classification System 2012 (ACM CCS), descargada en SKOS desde la biblioteca digital de ACM a `global/thesaurus/acm-ccs/`, con su grafo de Graphify. `thesaurus:check` muestra ahora una columna ACM CCS junto al estado IEEE. La ACM CCS cubre el vacío principal del IEEE Thesaurus 2019 en este tema, la accesibilidad (*Human-centered computing → Accessibility*), y respalda términos libres; el tipo de esos términos sigue siendo Libre. Los perfiles clínicos siguen verificándose en los Medical Subject Headings (MeSH).

## Propuesta inicial

11 términos: en P, `Asperger` (MeSH D020817) e `"intellectual developmental disorder"` (DSM-5); en I, `"speech recognition"` (IEEE p.506), `"recommender systems"` (IEEE p.454) y `"natural language generation"` (ACM CCS); en C, `"Section 508"` y `"EN 301 549"`; en O, `"System Usability Scale"`, `"user satisfaction"`, `"accessibility audit"` y `"accessibility assessment"`.

## Posiciones

**critico-rsl**
- Riesgo de rechazo bajo; ninguno de los términos daña la búsqueda.
- `"Section 508"` y `"EN 301 549"` no pueden sumar registros, porque el bloque C ya contiene `accessibility`: quitarlos.
- `"speech recognition"` trae cribado de autismo por la voz, pero ese ruido ya entra por `"machine learning"`; lo nuevo que aporta, la entrada por voz, es pertinente.
- `"recommender systems"` trae aprendizaje electrónico genérico: mantenerlo y excluir las intervenciones educativas sin contribución al software.
- Mantener los dos perfiles de P, la generación de lenguaje natural y los resultados de O.

**defensor-rsl**
- Asperger e `"intellectual developmental disorder"` no quedan cubiertos por los términos existentes y casi no traen ruido.
- `"natural language generation"` es el añadido de intervención mejor justificado: complementa la simplificación de textos y la lectura fácil.
- `"accessibility audit"`, `"accessibility assessment"` y `"user satisfaction"` aportan recall propio.
- `"System Usability Scale"` queda absorbido por `usability`, igual que las dos normas por `accessibility`.

**redaccion-rsl**
- Cuatro ajustes aplicados literalmente: el encabezado sin «+», la etiqueta Asperger en la clasificación vigente, la sigla DSM-5 desarrollada y la fila de accesibilidad con las WCAG desarrolladas. Los dos restantes se refieren a filas retiradas o fusionadas.

## Decisiones

| Punto | Decisión | Motivo |
|---|---|---|
| `"Section 508"`, `"EN 301 549"` | Se retiran y pasan a descriptores excluidos | Sin recall marginal: `accessibility` ya los cubre (ambos agentes) |
| `"System Usability Scale"` | Se retira | `usability` coincide dentro de la frase |
| `"recommender systems"` | Se mantiene sin comodín | IEEE Xplore ya usa sus 10 comodines; Scopus y Web of Science recuperan el singular |
| `Asperger` | Se mantiene sin comodín | Mismo límite de comodines |
| Recomendadores educativos | Se amplía el criterio de exclusión de intervenciones pedagógicas | Contiene el ruido de aprendizaje electrónico sin artefacto de software |
| Diagnóstico por voz | Sin criterio nuevo | El criterio de exclusión de estudios de solo diagnóstico ya lo cubre |

Resultado: 79 términos (52 en la versión 5 y 71 en la 6). La validación con las tres revisiones conocidas no cambia.

## Queda para el usuario

- Ejecutar la query en Scopus y comparar el número de registros con los de la versión 6. Si el volumen crece demasiado, retirar primero `"speech recognition"` y `"recommender systems"`.
- Ambos agentes señalan que el volumen depende sobre todo de los filtros de acceso abierto y de tipo de documento, y de que los bloques C y O sean obligatorios, más que de los sinónimos.
