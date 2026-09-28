# Redacción académica — informe (ficha) y paper RSL

Fuente de verdad de **forma** para todo texto entregable que produzca una skill `rsl-*`: `informe.md` / `informe-polish.md`, `paper-borrador.md` / `paper-polish.md`. El contenido (aporte, vacío, citas verificadas) lo cuidan los otros agentes; aquí se decide **cómo se lee**.

Objetivo: prosa final académica, natural y limpia, que un docente lea de corrido sin tropezar con jerga interna, siglas sueltas ni frases comprimidas. Mantener lo que funciona (estructura sólida, vacío auténtico, comparación fina con revisiones previas); no aplanar el contenido.

## Herramientas

| Uso | Comando |
|-----|---------|
| Chequeo automático de forma | `pnpm -s redaccion:lint <archivo.md>` → FAIL bloquea; WARN se corrige o se justifica |
| Citas en texto ↔ referencias | `pnpm -s paper:status docs/<slug> --cites [archivo]` |
| Revisión con juicio (naturalidad, densidad) | agente `redaccion-rsl` |

`redaccion:lint` analiza solo prosa: omite tablas, código, encabezados, comentarios y la sección Referencias.

## Reglas

### R1 — Texto final, no nota de trabajo (FAIL)

- Prohibidas las marcas editoriales: `[citar]`, `(citar)`, `TODO`, `PENDIENTE`, `TBD`, `???`. Si una cita no se puede verificar, se reformula o se quita la afirmación y se avisa en el chat; nunca se entrega la marca.
- Prohibidas las huellas del flujo interno: `topic.md`, `picoc/…/picoc.md` (salvo el enlace de la sección 2 del informe), "panel", "veredicto", `GO_*`, nombres de skills, rutas, código entre backticks, "Nota de artefacto", "ajuste previsto del protocolo".
- Nada de frases telegráficas tipo lista ("Salvaguarda ética mínima: no X; no Y; señalar Z"): se redactan como oración.

### R2 — Siglas: definir y dosificar (FAIL si no se define)

- Primera aparición = forma completa + sigla: *inteligencia artificial generativa (GenAI)*, *Definition of Done (DoD)*, *integración continua (CI)*, *orientaciones de accesibilidad cognitiva del W3C (COGA)*, *verificación y validación (V&V)*, *Ingeniería de Software (SE)*.
- En el paper, las siglas del núcleo se definen **al inicio de la Introducción** (Contexto), aunque ya aparezcan en el encabezado; en el encabezado (Tema, Problemática, Objetivo) se prefieren palabras completas.
- Dosificar: usar sigla solo si el término vuelve ≥ 3 veces; si aparece una o dos veces, escribirlo completo. Máximo 3 siglas distintas por párrafo (WARN).
- Uniformizar: una vez elegida la sigla, siempre la misma (no alternar IA / AI, GenAI / IA generativa / LLM sin criterio).

### R3 — Densidad: una idea por oración (WARN)

- Oraciones de ≤ 40 palabras (ideal 20–30). La pregunta de investigación puede ser más larga solo en la ficha y en el encabezado, y aun así sin cadenas de incisos.
- Máximo un inciso (guiones o paréntesis) por oración.
- Desempaquetar frases comprimidas: si una oración encadena tres conceptos técnicos, se parte en dos y se explica el vínculo.
- Párrafos de 2–5 oraciones con conector real al inicio.

### R4 — Sin notación de trabajo en la prosa (WARN)

| Evitar | Preferir |
|--------|----------|
| condición × técnica × fase SE × métrica | una taxonomía que cruza tipo de condición, técnica de IA, fase del ciclo de vida y métrica (definida una vez; luego "la taxonomía") |
| GenAI+web, IA+cognitivo | IA generativa aplicada a la web; IA orientada a la accesibilidad cognitiva |
| WCAG-duro / WCAG-dura | criterios WCAG verificables automáticamente |
| celda aguda, remake, gate de CI, pilot, outcomes | combinación menos estudiada, réplica, control de integración continua, piloto, resultados |
| → , / como "o" | palabras ("hacia", "o", "y") |

La notación compacta (×, →) solo se admite en tablas y figuras.

### R5 — Coherencia citas ↔ referencias (FAIL)

- Todo autor citado en el texto aparece en la lista de referencias y viceversa (paper: `--cites` PASS; ficha: cada obra citada en la prosa está en la tabla de la sección 3 o en una lista de referencias).
- Los datos (autores, año, DOI) se verifican; ver `citas-rsl`.

### R6 — Título breve y estable

- Título del paper ≤ 20 palabras, sin subtítulo en cascada (evitar "…: A, B y C — una revisión sistemática…").
- El título del paper se mantiene **cercano al título tentativo de la ficha** (sección 7); si se cambia uno, se alinea el otro.

## Ejemplos (antes → después)

| Antes (nota de trabajo) | Después (redacción final) |
|-------------------------|---------------------------|
| *(Tema final consensuado en `topic.md` tras panel `rsl-topic-panel`, veredicto GO_con_cambios.)* | *(se elimina: es trazabilidad interna)* |
| GenAI desplaza esfuerzo hacia detección y remediación a menudo WCAG-dura | La IA generativa se ha concentrado en detectar y corregir fallos que las WCAG permiten verificar automáticamente |
| escasea el cruce IA × cognitivo × fase SE × métrica | son escasas las síntesis que relacionan la IA con la accesibilidad cognitiva, la fase del ciclo de vida y la métrica empleada |
| taxonomía cuádruple con transferibilidad a DoD/CI | una taxonomía que indique qué resultados pueden incorporarse a la Definition of Done (DoD) o a la integración continua (CI) |
