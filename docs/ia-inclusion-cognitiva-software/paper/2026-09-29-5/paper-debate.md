# Debate del paper — versión 2026-09-29-5

## Polish 2026-09-29 (introducción y metodología, prosa con voz)

**Secciones trabajadas (on):** `encabezado` (solo el Objetivo; el Tema no se toca por decisión del usuario y la Problemática es la pregunta general literal), `contexto`, `problema`, `justificacion`, `objetivo-rsl`, `organizacion`, `marco-pico`, `palabras-clave`, `ecuacion-busqueda`, `criterios-seleccion`, `seleccion-prisma`. `calidad` pasó a `off` por decisión del usuario (falta `RSL/seleccion`).

**Motivo del usuario:** la versión 4 era correcta pero seca: frases troceadas, antecedentes en catálogo, ideas repetidas y descargos. El polish debe leerse de corrido, con hilo y voz, y explicar cada idea una sola vez. Antes de esta corrida se afinaron las reglas R3, R7 y R9 del playbook de redacción, el agente `redaccion-rsl`, las skills del paper y el lint (avisos de ritmo monótono y contraste troceado).

**Agentes:** critico-rsl, defensor-rsl, impacto-social-rsl, redaccion-rsl (lectura de corrido), citas-rsl (vía `--cites`).

**Espejo del picoc:** la pregunta general (encabezado, El problema y II.A), las Tablas I a III, la nota de vocabularios, los bloques Scopus y Web of Science y las viñetas CI/CE quedan idénticos a `picoc/2026-09-29-2-PICO/picoc.md`. Los marcadores `n = X` y `[[ … ]]` se conservan.

### Decisiones

| Sección | Propuesta | Origen | Decisión |
|---|---|---|---|
| contexto | Frases troceadas («No es X. Es Y.»), antecedentes en catálogo, apertura cargada de siglas | Usuario; lint (contraste troceado) | Reescrito: contraste en una oración, recorrido del más general al más cercano, siglas repartidas |
| contexto / problema | El riesgo del escáner se explicaba en Contexto y otra vez en Problema | Crítico, defensor | La imagen del escáner «en verde» se explica en Contexto; en Problema solo se nombra |
| problema | Quitar la pregunta de El problema y remitir a II.A | Defensor | Rechazada: regla de oro, la pregunta va literal en El problema |
| problema | La taxonomía se presentaba como lo que decide qué se automatiza (idea de los tres niveles) | Redacción (FAIL) | Reescrito: sin la taxonomía no se sabe qué se ha probado, con qué perfil y en qué fase |
| justificacion | «No se pretende certificar ese cumplimiento» | Impacto social, defensor | Retirado (descargo que ninguna RSL necesita) |
| justificacion | El vacío en la V&V con GenAI entraba sin puente | Redacción (FAIL) | Puente: «Esa utilidad no depende de que abunde la evidencia» |
| encabezado | Objetivo con ×, «GenAI+web», «esa taxonomía» sin antecedente y siglas sueltas | Crítico, defensor, impacto social | Reescrito en palabras completas, con los tres niveles |
| objetivo-rsl | CE8 citado como salvaguarda ética (es de alcance) | Crítico, impacto social | Solo CE5; la extracción ética se conserva completa |
| marco-pico | «se emplean tres siglas del área (SE, HCI, AT)» que no están en la pregunta | Crítico (error de hecho), defensor | Retirado |
| marco-pico | La prosa enumeraba cinco perfiles y la Tabla I siete | Defensor | La prosa remite a la Tabla I |
| marco-pico / palabras-clave | Las citas no decían qué recomiendan Kitchenham y Charters | Redacción (FAIL) | «recomiendan para la Ingeniería de Software el esquema de Petticrew y Roberts»; «recomiendan apoyar la búsqueda en términos de indexación controlados» |
| ecuacion-busqueda | «las tres revisiones sistemáticas del tema» sin identificar; «falta probar» como nota de trabajo | Crítico, defensor | Se nombran (verificadas en la validación del picoc); la prueba con [[n]] estudios queda en futuro |
| ecuacion-busqueda | «para no excluir» exageraba el efecto de _accessibility_ | Crítico | «para reducir la pérdida» |
| ecuacion-busqueda | Replicabilidad y descarte en el cribado se reexplicaban | Redacción (FAIL) | Retirados; viven en la apertura de la Metodología y en II.D |
| criterios / prisma | La fase no es parte del marco PICO; «registro» con dos sentidos | Redacción | «el marco y la fase del ciclo de vida»; «quedar por escrito», «Esa constancia» |

### Pendientes

- Riesgo ético sugerido por impacto social: registrar si los datos de entrenamiento o evaluación de la IA incluyeron a la población destinataria. Es un cambio del protocolo de extracción: decidirlo antes de escribirlo en el paper.
- PRISMA: el paso «Excluidos por fecha de publicación» convive con el filtro de año de las ecuaciones; justificarlo (por ejemplo, registros de acceso anticipado) o retirarlo al tener los conteos.
- Citar la afirmación de que las orientaciones COGA son más difíciles de verificar automáticamente (el crítico sugiere Aljedaani y Mollik, 2026, pp. 6–7; sin verificar).
- Xu et al. (2026) y Paiva et al. (2021): no están en el corpus del tema; confirmar sus descripciones y el año de Xu (el DOI es de 2025).
- Ley N.º 29973: citar el artículo que alcanza a la discapacidad cognitiva e intelectual.
- Tema del encabezado (no editable por decisión del usuario): conserva ×, siglas y «GenAI+web». Título de 28 palabras (R6 pide ≤ 20).

### Verificación

Redacción: PASS (0 FAIL; WARN solo en el Tema no editable y en la pregunta literal). Citas: PASS (13 referencias). Picoc-sync: PASS. Picoc-lint: OK.
