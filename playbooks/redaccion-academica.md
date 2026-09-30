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

**Principio:** las reglas son un mínimo, no la meta. Un texto puede pasar el lint y la tabla Hilo y seguir mal escrito. La meta es R9: prosa con sentido, precisa, económica y elegante, juzgada por sí misma, sin depender de otras versiones. Un párrafo que ya cumple R9 no se toca.

**Borrador y polish.** El borrador (`paper-borrador.md`, `informe.md`) y el debate admiten todo: matices, correcciones, discusiones entre agentes. El polish es la versión destilada, con voz propia: se lee de corrido, cada idea se explica una sola vez y cada párrafo conduce al siguiente. La meta no es la longitud: un texto puede ser corto o largo, pero nunca seco ni repetido. Pulir es quitar la reexplicación y el relleno, no el hilo que une las ideas.

### R1 — Texto final, no nota de trabajo (FAIL)

- Prohibidas las marcas editoriales: `[citar]`, `(citar)`, `TODO`, `PENDIENTE`, `TBD`, `???`. Si una cita no se puede verificar, se reformula o se quita la afirmación y se avisa en el chat; nunca se entrega la marca.
- Prohibidas las huellas del flujo interno: `topic.md`, `picoc/…/picoc.md` (salvo el enlace de la sección 2 del informe), "panel", "veredicto", `GO_*`, nombres de skills, rutas, código entre backticks, "Nota de artefacto", "ajuste previsto del protocolo".
- La voz es la de la revisión, no la de quien lee: nada de "el lector", "como lector", "al lector" ni apelaciones a quien lee. Se escribe en impersonal o con la revisión como sujeto (*se documenta*, *esta revisión*, *la selección debe poder auditarse*).
- Nada de frases telegráficas tipo lista ("Salvaguarda ética mínima: no X; no Y; señalar Z"): se redactan como oración.

### R2 — Siglas: definir y dosificar (FAIL si no se define)

- Primera aparición = forma completa + sigla: *inteligencia artificial generativa (GenAI)*, *Definition of Done (DoD)*, *integración continua (CI)*, *orientaciones de accesibilidad cognitiva del W3C (COGA)*, *verificación y validación (V&V)*, *Ingeniería de Software (SE)*.
- En el paper, las siglas del núcleo se definen **al inicio de la Introducción** (Contexto), aunque ya aparezcan en el encabezado; en el encabezado (Tema, Problemática, Objetivo) se prefieren palabras completas. En la apertura se definen solo las siglas que vuelven a usarse, repartidas en las oraciones donde hacen falta, sin amontonar expansiones en la primera frase.
- Dosificar: usar sigla solo si el término vuelve ≥ 3 veces; si aparece una o dos veces, escribirlo completo. Máximo 3 siglas distintas por párrafo (WARN).
- Uniformizar: una vez elegida la sigla, siempre la misma (no alternar IA / AI, GenAI / IA generativa / LLM sin criterio).

### R3 — Densidad: una idea por oración (WARN)

- Oraciones de ≤ 40 palabras, de longitud variada: frases largas bien construidas alternan con frases cortas de remate. La pregunta general se copia literal aunque pase el límite (WARN justificado).
- Máximo un inciso (guiones o paréntesis) por oración.
- Desempaquetar frases comprimidas: si una oración encadena tres conceptos técnicos, se reescribe y se explica el vínculo.
- **Reescribir, no trocear.** Una frase larga se arregla con subordinación o con un contraste en una sola oración («no es X, sino Y»), no partiéndola en frases cortas del mismo molde («No es X. Es Y.»).
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
- **Transición entre párrafos y entre secciones.** El párrafo B abre con un puente explícito hacia lo que dejó A: consecuencia (*por eso*, *de ahí que*), contraste (*sin embargo*), siguiente paso (*con esas palabras clave…*), precisión (*esa decisión implica…*) o retoma (*ese recorte exige…*). No se salta de un tema a otro sin puente, y un enlace que solo se adivina no cuenta. Una frase puente que no aporta datos no sobra: lleva el hilo.
- **Argumento, no lista.** Cada sección se resume en un argumento de tres pasos (de dónde parte, qué tensión plantea, adónde lleva). Los antecedentes forman un recorrido que se acerca al vacío (del más general al más cercano, y lo que a cada uno le falta), no un catálogo de «X (año) hizo Y» repetido.
- **Primero la necesidad, después la herramienta.** No se abre un apartado con el nombre de la herramienta y su definición ("La selección se reporta conforme a PRISMA 2020, una guía de 27 ítems…"); primero se plantea qué problema resuelve.
- **Sin redundancia: se explica una vez, después se nombra.** Cada idea se explica en un solo lugar del documento; después solo se nombra («la taxonomía», «esos tres niveles»), sin volver a explicarla con otras palabras. Un texto más corto y conectado es mejor que uno largo que insiste.
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

### R9 — Prosa con sentido y elegancia (FAIL)

El estándar es el de un artículo publicado: se lee de corrido, cada oración aporta y el tono es profesional. `redaccion-rsl` lo juzga párrafo por párrafo en su tabla **Calidad de prosa**; un párrafo falla si incumple cualquiera de estos cuatro criterios.

- **Sentido.** Quien no conoce el proyecto entiende qué se dice y por qué. Cada cita deja claro qué afirman los autores y para qué se trae (*Kitchenham y Charters (2007, p. 11) lo recomiendan para la Ingeniería de Software*), no una mención suelta que obliga a adivinar.
- **Precisión.** Palabra exacta y afirmación que se puede sostener; ni vaguedades ("aspectos", "diversos elementos") ni promesas mayores que el método ("otro investigador debe llegar a los mismos estudios").
- **Economía.** Ninguna oración sobra: si al quitarla el párrafo no pierde nada, se quita. Lo que se recorta es la reexplicación de una idea ya dicha, lo obvio, los matices que no cambian la conclusión y los descargos repetidos («no se pretende…», «sin…»: una vez, y en positivo cuando se pueda). Los puentes entre ideas no se recortan: al quitarlos el párrafo pierde el hilo.
- **Elegancia.** Orden natural (sujeto, verbo, complemento, sin inversiones forzadas como "fija en el protocolo salvaguardas éticas"); ritmo variado, nunca más de tres oraciones seguidas con la misma estructura y longitud; subordinación en lugar de oraciones yuxtapuestas; conectores variados, sin repetir mecánicamente el mismo; vocabulario académico sobrio, sin coloquialismos. Se admite una imagen por sección si se entiende sin contexto y aclara la idea (un escáner automático «en verde», una accesibilidad «de fachada»); la jerga interna de R4 sigue prohibida. Un párrafo que se lee como una lista de afirmaciones sueltas falla, aunque cada oración sea correcta.

Al incorporar una observación de otro agente (una cita, un matiz, una corrección), se **reescribe la oración** para que la integre con naturalidad; no se pegan cláusulas al final ni se añaden oraciones que interrumpen el hilo.

| Mal escrito (pasa el lint) | Bien escrito |
|---|---|
| *El esquema de las guías médicas, que ordena la pregunta en población, intervención y resultado, no deja un lugar explícito para esos dos ejes. Por eso se adoptó el marco (PICOC), que amplía ese esquema precisamente con la comparación y el contexto. Kitchenham y Charters (2007, pp. 10–11) lo retoman de Petticrew y Roberts para la Ingeniería de Software.* (la cita no dice qué aportan los autores) | *El marco habitual de las revisiones clínicas, que solo distingue población, intervención y resultado, no deja lugar para esos dos ejes. Por eso se adoptó el marco PICOC, que añade precisamente la comparación y el contexto. Kitchenham y Charters (2007, pp. 10–11) lo recomiendan para la Ingeniería de Software a partir de la propuesta de Petticrew y Roberts.* |
| *Las revisiones previas rodean ese objeto sin cubrirlo. Chemnad y Othman (2024) documentaron el predominio de la discapacidad visual. Perry et al. (2024) sintetizaron 15 trabajos de apoyo cotidiano. Aljedaani y Mollik (2026) hallaron que dominan las WCAG.* (catálogo: cada oración es «X (año) hizo Y» y nada las une) | *Ese recorte exige situar lo ya sintetizado. Chemnad y Othman (2024) documentaron el predominio de la discapacidad visual en la IA para la accesibilidad; Perry et al. (2024) sí se centraron en el neurodesarrollo, pero midieron el apoyo cotidiano y no la ingeniería. Más cerca de este tema, Aljedaani y Mollik (2026) hallaron que dominan las WCAG, sin ordenar la evidencia por fase.* (recorrido: cada revisión se acerca más al vacío y deja ver lo que le falta) |
| *El objeto de la revisión no es la tecnología asistiva clínica. Es el modo en que la IA se inserta en el ciclo de vida del software.* (frases troceadas del mismo molde) | *El objeto de la revisión no es la tecnología asistiva clínica, sino el modo en que la IA se inserta en el ciclo de vida del software.* (el contraste en una sola oración) |
| *Si la integración continua se limita a comprobaciones WCAG automáticas, un análisis sin fallos no demuestra que el software sea inclusivo en el plano cognitivo.* (correcto, pero sin vida) | *Si la integración continua solo ejecuta comprobaciones WCAG automáticas, un escáner «en verde» no garantiza que una persona con discapacidad cognitiva comprenda el software.* (una imagen clara que se entiende sin contexto) |
| *Los objetivos anteriores incluyen señalar qué combinaciones carecen de evidencia, y esa conclusión solo es sólida si…* (abre la Metodología resumiendo la Introducción) | *Esta revisión siguió las directrices de Kitchenham y Charters (2007) para revisiones sistemáticas en Ingeniería de Software, que reúnen en un protocolo previo las decisiones sobre la pregunta, la búsqueda y la selección.* |

## Ejemplos (antes → después)

| Antes (nota de trabajo) | Después (redacción final) |
|-------------------------|---------------------------|
| *(Tema final consensuado en `topic.md` tras panel `rsl-topic-panel`, veredicto GO_con_cambios.)* | *(se elimina: es trazabilidad interna)* |
| GenAI desplaza esfuerzo hacia detección y remediación a menudo WCAG-dura | La IA generativa se ha concentrado en detectar y corregir fallos que las WCAG permiten verificar automáticamente |
| escasea el cruce IA × cognitivo × fase SE × métrica | son escasas las síntesis que relacionan la IA con la accesibilidad cognitiva, la fase del ciclo de vida y la métrica empleada |
| taxonomía cuádruple con transferibilidad a DoD/CI | una taxonomía que indique qué resultados pueden incorporarse a la Definition of Done (DoD) o a la integración continua (CI) |
