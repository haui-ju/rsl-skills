# Debate de pulido — paper 2026-10-01

## 2026-10-01 — Alineación PICO `2026-10-01-PICO` + cribado 1

**Motivo (usuario):** pulir el paper según el picoc nuevo (marco PICO, queries, criterios y cifras PRISMA del cribado de título/resumen).

**Secciones trabajadas:** encabezado, contexto, problema, justificacion, objetivo-rsl, organizacion, marco-pico, palabras-clave, ecuacion-busqueda, criterios-seleccion, seleccion-prisma, referencias.

**Agentes:** critico-rsl y defensor-rsl no relanzados en esta pasada (continuación tras edición manual); redaccion-rsl sustituido por correcciones de forma directas hasta `redaccion:lint` OK.

### Decisiones clave

| Tema | Decisión |
|------|----------|
| Marco | PICO (4 RQ); eliminadas RQ5/RQ6 del borrador PICOCT; objetivo y organización acordes |
| Espejo picoc | Tablas, keywords, queries Scopus/WoS y CI/CE copiados de `picoc/2026-10-01-PICO/picoc.md`; `--picoc-sync` PASS |
| Criterios en paper | Viñetas `**CIn:**` con texto que incluye el prefijo `CIn.` del picoc (requerido por el comparador de sync) |
| CE4 / siglas | Párrafo introductorio define KDD y CICIDS sin alterar el texto espejo de CE4 |
| PRISMA | Cifras del cribado 1: 111 Scopus + 250 WoS, 69 duplicados, 292 cribados, 70 excluidos, 222 a recuperación; fechas y recuperación en marcadores `X` / `[[ … ]]` |
| Pendientes | Congelar secciones validadas en `config.yml`; completar fechas de búsqueda y diagrama PRISMA; cribado 2 sobre los 222 SI |

### Redacción

`redaccion:lint` sobre `paper-polish.md`: **PASS** (0 FAIL; WARN en pregunta literal y oraciones largas heredadas).

### Citas

`paper:status --cites`: **PASS** (10 referencias, apa7).

### Picoc-sync

`paper:status --picoc-sync`: **PASS**.
