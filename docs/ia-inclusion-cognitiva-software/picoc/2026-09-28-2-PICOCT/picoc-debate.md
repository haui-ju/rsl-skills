# Debate — criterios de inclusión y exclusión

- **Fecha:** 2026-09-28 · **Modo:** criterios · **Versión base:** [2026-09-28-PICOCT](../2026-09-28-PICOCT/picoc.md) (debate completo del marco en su [picoc-debate.md](../2026-09-28-PICOCT/picoc-debate.md)).
- **Marco:** PICOCT (`formato.marco` de `config.yml`, valor por defecto). Pregunta general, preguntas por componente, tabla, palabras clave y queries sin cambios.
- **Qué cambia:** se añade la sección final `## Criterios de inclusión y exclusión`, redactada desde el alcance y las exclusiones de `topic.md` y los componentes del marco.

## Posturas

**critico-rsl**
- El criterio de métricas filtraba por tipo de métrica, que es justo lo que la RQ4 debe describir; basta exigir una evaluación con alguna métrica o instrumento.
- La lista de fases no coincidía con Co (faltaban verificación y validación, y auditoría) y no exigía que la IA interviniera en la fase.
- Tres exclusiones solo negaban una inclusión o chocaban con ella: prototipos sin evaluación, tecnología de apoyo sin ciclo de vida, y accesibilidad solo sensorial (esta última además quitaba evidencia a la RQ3).
- Las queries están en inglés y la inclusión admite español; las actas LNCS figuran como capítulos de libro en Scopus.

**defensor-rsl**
- Todos los criterios se defienden con la práctica de Kitchenham: primero los formales (año, idioma, tipo de fuente, duplicados) y luego uno por bloque del marco.
- Fusionar idioma con tipo de fuente, y duplicados con texto completo, para mantener la lista breve.
- Nombrar los perfiles de la población y exigir que la técnica de IA esté identificada, para que el cribado sea replicable.
- Propuso un umbral de calidad, defendible solo si el protocolo define la lista de verificación.

## Decisiones

| Punto | Decisión | Motivo |
|-------|----------|--------|
| Métricas | «evaluación empírica con al menos una métrica o instrumento» | No prejuzga la RQ4 y descarta demostraciones sin evaluación |
| Fases | Mismas fases que Co y la IA debe intervenir en ellas | Coherencia 1:1 con el marco |
| Idioma y tipo de fuente | Un solo criterio; actas publicadas como capítulos de libro incluidas | Brevedad; no perder congresos indexados como capítulos |
| Español | Se mantiene | Scopus indexa resúmenes en inglés de artículos en español; la búsqueda en inglés los recupera |
| Exclusiones que negaban una inclusión | Retiradas (prototipos sin evaluación, apoyo sin ciclo de vida, solo sensorial) | Ya las cubren las inclusiones; la sensorial con contraste cognitivo alimenta la RQ3 |
| Duplicados y texto completo | Un solo criterio | Brevedad |
| Umbral de calidad | No entra | El protocolo aún no define la lista de verificación |

## Queda para el usuario

- Si define una lista de verificación de calidad, añadir su umbral como exclusión en una versión nueva.
- Fijar la fecha exacta de búsqueda de 2026 al correr las queries.
