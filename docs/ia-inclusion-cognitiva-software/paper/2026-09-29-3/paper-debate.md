# Debate del paper — versión 2026-09-29-3

## Polish 2026-09-29

**Secciones trabajadas:** `objetivo-rsl`, `criterios-seleccion`, `palabras-clave` y `ecuacion-busqueda` (on; las dos últimas pasaron de frozen a on en config.yml durante la corrida). **Re-sincronizadas con el picoc 2026-09-29-2-PICO:** `marco-pico` (frozen: conceptos P y O de la Tabla I), Tabla III y las ecuaciones de Scopus y Web of Science. **Agentes:** critico-rsl, defensor-rsl, impacto-social-rsl, redaccion-rsl; citas verificadas con `paper:status --cites`.

### Decisiones

| Sección | Propuesta | Origen | Decisión |
|---|---|---|---|
| objetivo-rsl | El párrafo ético atribuía al CE8 la exclusión del diagnóstico; separar CE5 (diagnóstico sin artefacto evaluado) y CE8 (robots, tutores, rehabilitación) | Crítico, impacto social (FAIL) | Aceptada, en dos oraciones para no pasar de 40 palabras |
| objetivo-rsl | «el sesgo geográfico» da por probado un sesgo sin cita | Crítico (FAIL) | Aceptada: «un posible sesgo geográfico» |
| objetivo-rsl | Objetivo 3 no recogía la subordinación de la RQ3; objetivo 2 omitía la auditoría de la pregunta general | Crítico (FAIL) | Aceptada |
| objetivo-rsl | «Para no medicalizar a las personas» repite el contexto | Crítico | Aceptada: se quita el inciso |
| objetivo-rsl | Fundir CE5 y CE8 en «productos asistivos» | Defensor | Rechazada: pierde la precisión que pedía el FAIL |
| objetivo-rsl | Adelanto de «la pregunta general», población repetida, «se reportan» doble | Redacción (WARN) | Aceptada |
| criterios-seleccion | Solo CI1 y CI2 repiten filtros de la ecuación | Crítico, defensor | Aceptada |
| criterios-seleccion | La prosa repetía la lista CE1–CE8 | Crítico, defensor | Aceptada: «formales (CE1 a CE4) y de alcance (CE5 a CE8)» |
| criterios-seleccion | Definir CI y CE; «traducir a» | Redacción (WARN) | Aceptada |

| palabras-clave (on durante la corrida) | Los ejemplos de términos libres no reflejaban el picoc (`"language model"`, `accessibility`) | Crítico | Aceptada: «casi todos los perfiles de la población, la accesibilidad o los modelos de lenguaje» |
| ecuacion-busqueda (on durante la corrida) | El acceso abierto no va dentro de la ecuación de Web of Science | Crítico, defensor (FAIL) | Aceptada |
| ecuacion-busqueda | La prueba con [[n]] estudios conocidos se presentaba como hecha; el picoc dice que aún no hay conjunto de control | Crítico (FAIL) | Aceptada: se reporta el contraste con las tres revisiones y la prueba pendiente, con los marcadores [[n]] intactos |
| ecuacion-busqueda | Párrafo con dos intenciones (campos y límites; validación) | Redacción (FAIL de hilo) | Aceptada: dos párrafos; se descarta la paráfrasis «apoyarse en revisiones previas» por no estar verificada en la p. 14 |

### Pendientes

- Campos distintos por base: Scopus usa `TITLE-ABS-KEY` y Web of Science `ALL=`; la equivalente sería `TS=`. Se decide en el picoc.
- La query de IEEE Xplore del picoc no figura en el paper ni en la Tabla IV.
- «LLM (plural)» y «lectura fácil (variante sin guiones)» en la Tabla III son notas de trabajo heredadas del picoc; se corrigen con rsl-picoc.
- _accessibility_ en cursiva en la prosa puede leerse como descriptor IEEE según la nota de la Tabla III.

- CI3 y RQ1 no nombran la disgrafía ni la discalculia, que sí están en la P de la Tabla I y en la query; se corrige en el picoc con rsl-picoc.
- En la justificación (frozen), «control de la CI» significa integración continua y choca con los códigos CI1–CI5; desarrollar la sigla al descongelarla.
- Registrar también el idioma de la intervención junto al país (sesgo lingüístico).
- Aclarar en el método que la prosa propia no reproduce el lenguaje clínico de los rótulos.
- «Carecen de evidencia» se entiende dentro del corpus recuperado; matizarlo en amenazas a la validez.

### Frozen desalineadas con el picoc (no editadas)

- `seleccion-prisma`, `encabezado`, `problema`, `justificacion` y `organizacion` siguen stale.

### Verificación

Redacción: PASS (0 FAIL; los 20 avisos del lint están en el encabezado frozen y en la pregunta general, copia literal del picoc). Citas: PASS (13 referencias). Picoc-sync: PASS.
