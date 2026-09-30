# Debate del paper — versión 2026-09-29-4

## Polish 2026-09-29 (introducción)

**Secciones trabajadas (on):** `contexto`, `problema`, `justificacion`, `objetivo-rsl`, `organizacion`. **Motivo del usuario:** las cinco secciones forman una sola introducción; debían ser más breves, claras y sin redundancia. **Agentes:** critico-rsl, defensor-rsl, impacto-social-rsl, redaccion-rsl, citas-rsl. **Resultado:** de 1511 a unas 990 palabras (contexto ≈ 385, problema ≈ 130, justificación ≈ 150, objetivo ≈ 280, organización ≈ 55).

Antes de abrir la versión se restauraron las X de `seleccion-prisma` (frozen) en 2026-09-29-3, por decisión del usuario.

### Decisiones

| Sección | Propuesta | Origen | Decisión |
|---|---|---|---|
| todas | Cada revisión previa se cita solo en Contexto; los tres niveles de automatización, solo en Justificación | Condensación | Aplicada; el objetivo 4 remite a los niveles |
| justificacion | Quitar las metas ODS 10.2 y 4.5 | Condensación; impacto social (PASS) | Aplicada: no tenían referencia |
| organizacion | Quitar el anexo y el «marco conceptual» | Condensación; defensor | Aplicada: no existen en el artículo |
| contexto | Restaurar que Aljedaani y Mollik no ordenan la evidencia por fase | Crítico (FAIL), defensor | Aceptada |
| contexto | «más difíciles de verificar» quedaba atribuido al W3C; «esas barreras» sin antecedente | Crítico (FAIL) | Aceptada: «que suelen ser…», «las barreras en esos tres planos» |
| contexto | La práctica de integración continua y *Definition of Done* sin cita | Crítico (Sustento) | Reformulada como condicional de la revisión |
| contexto | «Paiva et al. ordenaron por fase» no verificado | Citas (PENDIENTE) | Sustituido por «revisaron la accesibilidad en los procesos de la Ingeniería de Software» |
| problema | Párrafo final repetía las cuatro dimensiones | Crítico, defensor | Fundido en una oración |
| justificacion | «Una RSL es necesaria porque abundan síntesis» invertía la lógica y repetía El problema | Crítico (FAIL) | Eliminada; la RSL se define en «articula tres elementos» |
| justificacion | «la combinación menos estudiada» sin respaldo | Crítico (Sustento) | «la que se prevé menos estudiada» |
| objetivo-rsl | El objetivo 2 perdió la GenAI (contradice la RQ2 frozen) | Crítico (FAIL), defensor | Restaurada |
| objetivo-rsl | Los datos éticos perdieron su propósito de reporte | Impacto social (FAIL), defensor | Restaurado en una oración |
| objetivo-rsl | «sin reclasificar a nadie», ejemplo del texto simplificado | Defensor | Rechazada: impacto social confirma que no son FAIL |
| problema | Añadir diseño y personalización a la pregunta | Defensor (baja) | A Pendientes: la pregunta completa está en II.A |
| varias | Hilo y prosa (paréntesis en *Definition of Done*, «Para orientar la práctica», PRISMA guía el reporte) | Redacción (WARN) | Aceptadas; se conserva la sigla RSL por el título de la sección |

### Pendientes

- Citar el artículo concreto de la Ley N.º 29973 que alcanza a la discapacidad cognitiva e intelectual.
- Xu et al. (2026): confirmar año (el DOI es de 2025), volumen y páginas con el editor.
- W3C (2021): «memoria» se apoya en el objetivo COGA *Ensure processes do not rely on memory*; el corpus local solo resume «complejidad, carga cognitiva y claridad».
- ~~La pregunta de El problema abrevia la de II.A (omite diseño y personalización).~~ Resuelto: ver «Pregunta general (regla de oro)».
- El encabezado (frozen, stale) sigue con siglas, símbolo × y «GenAI+web»; conviene ponerlo en on.
- `informe-polish.md` atribuye 38 estudios a Aljedaani y Mollik; el PDF dice 33.

### Verificación

Redacción: PASS (0 FAIL; ningún aviso del lint en la introducción). Citas: PASS (13 referencias). Picoc-sync: PASS.

## Pregunta general (regla de oro)

Decisión del usuario: la pregunta de El problema, la Problemática del encabezado y la cita de la Tabla I son la pregunta general del picoc, literal. Se acortó la pregunta general (sin cambiar las RQ) y se editó en el mismo sitio, sin versión nueva: § 1.2 de `informe-polish.md`, `picoc/2026-09-29-2-PICO/picoc.md` y esta versión del paper. El cribado 1 sigue válido porque las RQ, las keywords, las queries y los criterios no cambian.

Nueva pregunta: ¿Cómo se ha integrado la inteligencia artificial en el ciclo de vida del software, del diseño y la personalización a la verificación, la evaluación y la auditoría, para usuarios con discapacidad cognitiva o neurodivergencia; qué métricas se reportan, incluidas las orientaciones COGA frente a las WCAG; y qué combinaciones de condición, técnica, fase y métrica carecen de evidencia frente al predominio de la accesibilidad sensorial?

La regla queda en `--picoc-sync` (encabezado y problema deben contener la pregunta literal) y en las skills rsl-make-paper y rsl-polish-paper. Los avisos de oración larga en la pregunta se justifican: no se parte.

Pendiente: la prosa frozen de marco-pico («matriz de condición, técnica, fase y métrica… siglas SE, HCI, AT») y el resto del encabezado (Tema, Objetivo) siguen con la redacción anterior; conviene ponerlos en on.
