# Debate del marco — 2026-09-28-5-PICO

**Fecha:** 2026-09-28 · **Modo:** completo (cambió `formato.marco` de PICOC a PICO) · **Base:** `2026-09-28-4-PICOC` · **Agentes:** critico-rsl, defensor-rsl, redaccion-rsl

## Decisiones del usuario (no se debaten)

- Marco PICO: se retira el bloque de contexto (ciclo de vida del software) y RQ5. La fase del ciclo de vida pasa a criterio de inclusión y a dato a extraer de RQ2.
- Bloques P, I, C y O: los de la query de Scopus que el usuario ejecutó, sin cambios.
- Filtros de inclusión dentro de las queries: 2021–2026 (cinco años completos y el año en curso), solo artículos de revista, inglés y español, acceso abierto. En Web of Science el acceso abierto es filtro de la interfaz (no tiene etiqueta de campo).

## Posiciones

**critico-rsl** (riesgo de rechazo alto)
- La validación no recupera ninguna de las tres revisiones conocidas; dos quedan fuera por un solo bloque (O en Chemnad y Othman, C en Perry et al.). Propone unir C y O con OR: P AND I AND (C OR O).
- Sin el bloque de contexto entra ruido clínico (diagnóstico de TEA o TDAH con EEG, resonancia, seguimiento ocular); `measurement`, `metric` y `metrics` casi no discriminan. Propone términos de O más específicos y probar una poda por título (`AND NOT TITLE(diagnos* OR screening OR …)`) midiendo lo que se gana y se pierde.
- Keywords genéricas (*Artificial intelligence*, *Software quality*, *WCAG*).
- Faltan términos en I (`chatbot*`, `"conversational agent*"`, `"neural network*"`, `"computer vision"`, `GPT*`, `transformer*`) y en P (`"Down syndrome"`, `"learning difficult*"`, `ASD`).
- Sintaxis: `ALL=` en Web of Science es más amplio que `TITLE-ABS-KEY`; propone `TS=`. En Scopus `DOCTYPE ar` no garantiza revista; propone `SRCTYPE j`.
- Criterios de fase y de evaluación empírica poco operativos; la validación se interpretaba como confirmación del vacío.
- Amenazas a declarar: sesgo del acceso abierto y pérdida de los trabajos de congreso (ASSETS, CHI, W4A).

**defensor-rsl**
- El marco PICO se sostiene: la identidad de ingeniería de software sigue en RQ2 (fase) y RQ4 (automatización); la matriz se reconstruye en la extracción.
- C y O recortan por lo que dice el resumen; como alternativa a unirlos, propone añadir `evaluation`, `"accessibility evaluation"` y `"accessibility testing"` al bloque O.
- *Software quality* sirve como keyword del paper (identidad de ingeniería de software), pero no sustituye a `accessibility evaluation` para recuperar estudios.
- Faltan dos exclusiones explícitas: IA solo para diagnóstico y accesibilidad solo sensorial.
- Excluir congresos tiene un coste que debe declararse.

**redaccion-rsl** (FAIL en la versión inicial)
- Siglas sin definir en los criterios (TEA, TDAH) y en RQ3 (W3C); nota de trabajo «Pendiente del usuario»; oración de 57 palabras en la viñeta del bloque de contexto; dos criterios en una viñeta; listas de métricas y fases que no coincidían entre RQ4, RQ2 y los criterios.

## Decisiones

| Propuesta | Decisión | Motivo |
|---|---|---|
| Unir C y O con OR, o añadir `evaluation` y `accessibility evaluation` a O | Para el usuario | Cambia la query que el usuario ejecutó; se decide con los conteos en Scopus |
| Términos nuevos en I y P | Para el usuario | Idem; pasarlos por `thesaurus:check` antes de añadirlos |
| Poda por título del ruido de diagnóstico | Para el usuario | Requiere medir en Scopus lo que se gana y se pierde |
| `TS=` en lugar de `ALL=` (Web of Science); `SRCTYPE j` (Scopus) | Para el usuario | Cambia los conteos de la búsqueda ya ejecutada |
| Keywords: conservar *Software quality* y *Artificial intelligence* | Aplicada | *Software quality* conserva la identidad de ingeniería de software tras retirar el bloque de contexto (defensor); *Artificial intelligence* es el término del título |
| Exclusiones: IA solo para diagnóstico; accesibilidad solo sensorial | Aplicada | Ambos agentes; hacen explícito el ruido que traen P AND I y el bloque C |
| Criterio de fase operativo (uno solo, con la lista de fases alineada con RQ2) | Aplicada | Crítico y redacción; se quitó el criterio duplicado |
| Evaluación empírica «con usuarios o automática» | Aplicada | Crítico: la evaluación automática alimenta RQ4 |
| Periodo justificado como «cinco últimos años completos y el año en curso» | Aplicada | El motivo de la adopción de GenAI (2023) no justificaba empezar en 2021 |
| Validación: columna sobre términos, sin concluir el vacío | Aplicada | Crítico: no recuperar estudios afines es señal sobre la búsqueda, no confirmación del vacío |
| Siglas, nota de trabajo, oración larga, viñetas separadas, listas alineadas | Aplicada | redaccion-rsl |

## Queda para el usuario

- Decidir sobre los bloques C y O (unir con OR o ampliar O) con los conteos de Scopus, y sobre los términos nuevos de I y P.
- Formar el conjunto de control de 3 a 5 estudios primarios (de las referencias de Chemnad y Othman, 2024, y Perry et al., 2024) y comprobar la recuperación bloque a bloque.
- Registrar la fecha de búsqueda y los conteos con y sin filtros (para el paso de PRISMA «excluidos por los filtros de la base de datos»).
- Declarar en amenazas a la validez el sesgo del acceso abierto y la pérdida de los trabajos de congreso.
