# Redacción académica — informe (ficha) y paper RSL

Fuente de verdad de **forma** para todo texto entregable que produzca una skill `rsl-*`: `informe.md` / `informe-polish.md`, `paper-borrador.md` / `paper-polish.md`. El contenido (aporte, vacío, citas verificadas) lo cuidan los otros agentes; aquí se decide **cómo se lee**.

Objetivo: prosa final académica, natural y limpia, que un docente lea de corrido sin tropezar con jerga interna, siglas sueltas ni frases comprimidas. Mantener lo que funciona (estructura sólida, vacío auténtico, comparación fina con revisiones previas); no aplanar el contenido.

## Herramientas

| Uso | Comando |
|-----|---------|
| Chequeo automático de forma | `pnpm -s redaccion:lint <archivo.md>` → FAIL bloquea; WARN se corrige o se justifica |
| Citas en texto ↔ referencias | `pnpm -s paper:status docs/<slug> --cites [archivo]` |
| Revisión con juicio (naturalidad, densidad, hilo entre oraciones y párrafos) | agente `redaccion-rsl` (tabla Hilo, R7) |
| Afirmaciones importantes sin fuente (R8) | agente `critico-rsl` (tabla Sustento) |

`redaccion:lint` analiza solo prosa: omite tablas, código, encabezados, comentarios y la sección Referencias.

## Reglas

### R1 — Texto final, no nota de trabajo (FAIL)

- Prohibidas las marcas editoriales: `[citar]`, `(citar)`, `TODO`, `PENDIENTE`, `TBD`, `???`. Si una cita no se puede verificar, se reformula o se quita la afirmación y se avisa en el chat; nunca se entrega la marca.
- Prohibidas las huellas del flujo interno: `topic.md`, `picoc/…/picoc.md` (salvo el enlace de la sección 2 del informe), "panel", "veredicto", `GO_*`, nombres de skills, rutas, código entre backticks, "Nota de artefacto", "ajuste previsto del protocolo".
- La voz es la de la revisión, no la de quien lee: nada de "el lector", "como lector", "al lector" ni apelaciones a quien lee. Se escribe en impersonal o con la revisión como sujeto (*se documenta*, *esta revisión*, *la selección debe poder auditarse*).
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

### R7 — Coherencia y progresión: cada párrafo transmite algo y conduce al siguiente (FAIL)

El lint no lo ve; lo juzga `redaccion-rsl` con la tabla Hilo. Un texto con siglas definidas y oraciones cortas puede fallar aquí.

- **Una intención por párrafo, anunciada en su primera oración.** Si el párrafo no se resume en una línea ("este párrafo explica por qué se eligió PICOC"), está mal construido.
- **Cada oración retoma algo de la anterior** (de lo conocido a lo nuevo). Prohibidas las cadenas de oraciones sueltas en las que cada punto define una cosa distinta.
- **Transición entre párrafos y entre secciones.** El párrafo B se engancha con lo que dejó A: consecuencia (*por eso*, *de ahí que*), contraste (*sin embargo*), siguiente paso (*con esas palabras clave…*) o precisión (*esa decisión implica…*). No se salta de un tema a otro sin puente.
- **Primero la necesidad, después la herramienta.** No se abre un apartado con el nombre de la herramienta y su definición ("La selección se reporta conforme a PRISMA 2020, una guía de 27 ítems…"); primero se plantea qué problema resuelve.
- **Sin redundancia.** Cada argumento se dice una vez; si ya está en otro párrafo o sección, no se repite con otras palabras. Un texto más corto y conectado es mejor que uno largo que insiste.
- **Apertura de sección.** Una sección se abre con su propio asunto; la Metodología empieza por lo que hizo la revisión (el método seguido), no resumiendo la Introducción ("Los objetivos anteriores…").
- **Las citas dicen qué aporta el autor** con un verbo de contenido (*recomiendan*, *proponen*, *advierten*), no con fórmulas vagas ("lo retoman", "según").
- **Decisiones de método, patrón fijo:** necesidad del estudio → por qué no basta la alternativa obvia → decisión → qué aporta según la fuente (cita) → cómo se aplica en esta revisión.

| Antes (oraciones sueltas, empieza por la herramienta) | Después (hilo: necesidad → decisión → fuente → aplicación) |
|---|---|
| *Kitchenham y Charters (2007, p. 11) adoptan PICOC para la Ingeniería de Software a partir de la propuesta de Petticrew y Roberts. El marco suma dos componentes a la pregunta clínica de población, intervención y resultado: la comparación […] y el contexto […]. Se eligió porque esos dos componentes son centrales en este tema.* | *La pregunta de esta revisión no se limita a saber si la inteligencia artificial mejora la accesibilidad: exige además contrastarla con la accesibilidad sensorial y situar cada intervención en una fase del ciclo de vida. El marco clínico de población, intervención y resultado no deja lugar para esos dos ejes. Por eso se adoptó PICOC, que Kitchenham y Charters (2007, p. 11) recomiendan para la Ingeniería de Software y que añade precisamente la comparación y el contexto.* |
| *La selección se reporta conforme a PRISMA 2020, una guía de 27 ítems con un diagrama de flujo que registra cuántos registros entran y salen en cada etapa (Page et al., 2021, p. 1).* | *Las ecuaciones recuperan muchos registros, y buena parte no responderá a la pregunta. Pasar de ese conjunto a los estudios incluidos exige decisiones que deben quedar documentadas. Por eso la selección se documenta según PRISMA 2020 (Page et al., 2021, p. 1).* |

### R8 — Sustento: lo importante se cita (FAIL)

Una RSL sostiene lo que dice con fuentes. No todo va citado, pero sí lo que un revisor preguntaría "¿de dónde sale?". El lint no lo ve; lo juzgan `critico-rsl` (tabla Sustento) y `citas-rsl`.

- **Lleva cita:** datos y cifras; tendencias o afirmaciones sobre el estado de la literatura ("pocos estudios…", "la mayoría…"); definiciones de marcos, normas y guías (PICOC, PRISMA, WCAG); la justificación de una decisión de método (por qué ese marco, esas bases, ese periodo, ese criterio); comparaciones con revisiones previas.
- **No lleva cita:** lo que esta revisión decidió o hizo (la ecuación usada, los criterios fijados, los pasos seguidos), las transiciones y lo que se deduce de lo ya citado en el mismo párrafo.
- En la mayoría de los párrafos de Introducción y en cada decisión de Metodología hay al menos una cita; un párrafo sin ninguna debe ser puramente descriptivo de lo que hizo la revisión.
- **Nunca se inventa una fuente.** Solo se cita lo verificado: el corpus del tema (`RSL/MD/`, grafo del tema), el catálogo `global/bibliography/bibliography.md` o las referencias ya comprobadas. Si no hay fuente verificable, la afirmación se reformula como decisión propia o se retira, y la falta se anota en el debate.

## Ejemplos (antes → después)

| Antes (nota de trabajo) | Después (redacción final) |
|-------------------------|---------------------------|
| *(Tema final consensuado en `topic.md` tras panel `rsl-topic-panel`, veredicto GO_con_cambios.)* | *(se elimina: es trazabilidad interna)* |
| GenAI desplaza esfuerzo hacia detección y remediación a menudo WCAG-dura | La IA generativa se ha concentrado en detectar y corregir fallos que las WCAG permiten verificar automáticamente |
| escasea el cruce IA × cognitivo × fase SE × métrica | son escasas las síntesis que relacionan la IA con la accesibilidad cognitiva, la fase del ciclo de vida y la métrica empleada |
| taxonomía cuádruple con transferibilidad a DoD/CI | una taxonomía que indique qué resultados pueden incorporarse a la Definition of Done (DoD) o a la integración continua (CI) |
