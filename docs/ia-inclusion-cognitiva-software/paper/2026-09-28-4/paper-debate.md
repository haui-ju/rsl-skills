# Debate del polish — paper 2026-09-28-4

## 2026-09-28 · polish (versión nueva; base de texto: 2026-09-28-2)

**Motivo:** el usuario rechazó la versión 3 por larga, redundante y mal conectada: la Metodología abría con «Los objetivos anteriores» y la cita del marco PICOC no decía qué aportaban los autores. Consideró mejor la versión 2. Esta versión parte del texto de la 2 y aplica solo cambios mínimos, que es lo que significa el estado `on`.
**Secciones trabajadas (on):** objetivo-rsl, apertura de II, marco-pico, palabras-clave, ecuacion-busqueda, criterios-seleccion, seleccion-prisma.
**Frozen sin cambios:** encabezado, contexto, problema, justificacion, organizacion.
**Agentes:** critico-rsl (Sustento), defensor-rsl, impacto-social-rsl, redaccion-rsl (Hilo; dos pasadas), citas-rsl (dos pasadas).

### Longitud frente a la versión 2 (palabras)

| Sección | v2 | v3 | v4 |
|---|---|---|---|
| objetivo-rsl | 360 | 426 | ≈ 375 |
| apertura de II | 109 | 139 | ≈ 90 |
| ecuacion-busqueda | 678 | 724 | ≈ 680 |
| seleccion-prisma | 218 | 252 | ≈ 220 |

### Decisiones clave

| Tema | Propuesta | Decisión |
|---|---|---|
| Apertura de la Metodología | Usuario: «Los objetivos anteriores» es un mal inicio | Empieza por el método seguido (Kitchenham y Charters, 2007) y el porqué del protocolo previo, con cita (pp. vi, 12). |
| Párrafo PICOC | Usuario: la versión 2 era clara | Texto de la versión 2 sin cambios, salvo la página (pp. 10–11), porque el esquema clínico se describe en la p. 10. |
| «El lector» (E) | Regla R1 | «decisiones sucesivas que deben quedar documentadas», con cita pp. 19–20. |
| Citas de método | Sustento (crítico) | Dentro de la oración que sostienen: p. 14 (B), p. 16 (C), p. 18 con «como recomiendan» (D). Sin oraciones nuevas. |
| Redundancias | Defensor, crítico | Eliminadas: «Los registros no pertinentes… se descartan después en el cribado» (C); «sin ajustar el criterio…» (D); la cláusula que repetía el vínculo RQ–objetivo (A); «fija… fijadas». |
| Apertura del Objetivo | redaccion-rsl: retomaba «la pregunta planteada», que no está justo antes | «El objetivo general de esta revisión es…». |
| Sigla CI en el objetivo 4 | Crítico: choca con CI1–CI6 | Se escribe «integración continua». |
| Neurodivergencia | Impacto: faltaba en el objetivo 1 y en las salvaguardas | Añadido «o neurodivergentes» en ambos. |
| Rótulos diagnósticos y CE4 | Contradicción con la RQ1; CE4 incompleto | Se reportan tal como los declara cada estudio; CE4 con «sin una fase del ciclo de vida». |
| Petticrew y Roberts | redaccion-rsl propuso quitarlos | Se mantienen: Kitchenham y Charters les atribuyen el marco (cita secundaria, sin entrada propia). |

### Pendientes (no aplicados para no alargar el texto)

- Desglosar por motivo las exclusiones a texto completo en el paso 6 de PRISMA.
- Límite del bloque de comparación: un estudio cognitivo sin ninguno de esos términos queda fuera (para Amenazas a la validez).
- Asimetría de campos Scopus / WoS y justificación de las bases: sin fuente; decisión propia.
- CI1 (2023) sin fuente; es literal del picoc y solo se corrige con rsl-picoc.
- CE4 resumido sin robots sociales ni tutores inteligentes.
- Título (R6) e Introducción (más breve): secciones frozen.

### Redacción y citas

- `redaccion-rsl`: PASS en la segunda pasada (Hilo OK en todos los párrafos cambiados).
- `redaccion:lint`: 0 FAIL; los WARN están solo en el encabezado frozen y en la pregunta general literal.
- `citas-rsl`: PASS tras corregir p. 19 → pp. 19–20. `--cites`: OK, 10 referencias.
