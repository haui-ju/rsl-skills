# Debate del polish — paper 2026-09-29

## 2026-09-29 · re-sincronización con el picoc (versión nueva; base: 2026-09-28-5)

**Motivo:** el paper no copiaba el último picoc (`picoc/2026-09-28-7-PICO/`). La Tabla III resumía conceptos en lugar de listar los términos de la query (faltaban, entre otros, `neurodivers*`, `"autism spectrum"`, `AI`, `NLP`, `metric`, `readability`), y las queries, la Tabla I y la exclusión de intervenciones pedagógicas venían de un picoc anterior. `marco-pico`, `palabras-clave` y `ecuacion-busqueda` están frozen, por lo que el polish anterior las copió sin cambios.
**Regla nueva:** tablas, keywords, queries y criterios se copian del último picoc aunque la sección esté frozen; la prosa frozen no se toca. Lo verifica `pnpm -s paper:status docs/ia-inclusion-cognitiva-software --picoc-sync`.
**Base:** paper-polish.md de 2026-09-28-5 tal como quedó registrado (la copia de trabajo había perdido los marcadores de sección al formatearse).
**Agentes:** ninguno; solo el espejo del picoc y el ajuste mínimo de las secciones `on` que lo citan.

### Decisiones clave

| Sección | Cambio | Origen |
|---|---|---|
| marco-pico (frozen) | Tabla I: conceptos P y O del picoc (síndrome de Down, discalculia, comprensión, evaluación de la accesibilidad) | picoc |
| palabras-clave (frozen) | Tabla III: columna EN = términos exactos de cada bloque de la query (20 P, 22 I, 17 C, 20 O), comodín escapado `\*`; columna ES con una traducción por término | picoc; usuario |
| ecuacion-busqueda (frozen) | Bloques de Scopus y Web of Science copiados literal del picoc | picoc |
| criterios-seleccion (on) | CE7 nuevo (intervenciones pedagógicas sin artefacto de software); robots pasa a CE8; la apertura lo menciona | picoc |
| objetivo-rsl (on) | La referencia a la exclusión de robots pasa de CE7 a CE8 | coherencia con criterios-seleccion |

**Redacción:** `redaccion:lint` 0 FAIL (20 avisos, los mismos de 2026-09-28-5, en el encabezado frozen y en la pregunta general literal). **Citas:** PASS (11 referencias). **Picoc:** `--picoc-sync` PASS.

### Pendientes (prosa frozen que ya no encaja con el picoc; descongelar para alinearla)

- `marco-pico`: la prosa enumera la población sin el síndrome de Down ni la discalculia, que ahora están en la Tabla I.
- `palabras-clave`: la nota bajo la Tabla III no explica el comodín `*` (truncamiento) ni las comillas (frase exacta).
- Siguen stale: `encabezado`, `problema`, `justificacion`, `organizacion` y `seleccion-prisma`.
