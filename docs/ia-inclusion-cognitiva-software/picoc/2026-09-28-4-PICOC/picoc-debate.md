# Debate — cambio de marco a PICOC

- **Fecha:** 2026-09-28 · **Modo:** completo, solo las filas que cambian · **Versión base:** [2026-09-28-3-PICOCT](../2026-09-28-3-PICOCT/picoc.md).
- **Marco:** PICOC (`formato.marco` de `config.yml`, elegido por el usuario): población, intervención, comparación, resultado y contexto.
- **Qué cambia:** sale la fila T y su RQ6; las queries de Scopus, Web of Science e IEEE Xplore pierden el filtro de año. Pregunta general, bloques P, I, C, O y Co, palabras clave y keywords sin cambios.

## Posturas

**critico-rsl**
- Sin T, mantener «publicados entre 2020 y 2026» reintroduce el corte por la puerta de atrás; el corte solo se justificaba por la RQ6. Propone eliminar el criterio y registrar el año solo como dato bibliográfico.
- No añadir el año a la RQ2: sería la RQ6 encubierta. Si se añade, la discusión solo describe la tendencia, sin conclusiones causales sobre 2023.
- La búsqueda auxiliar puede conservar 2020–2026 como verificación de novedad.

**defensor-rsl**
- El PICOC de Petticrew y Roberts no tiene tiempo y Kitchenham trata la fecha como criterio de selección: mantener 2020–2026 en el cribado, con su justificación dentro del criterio, y contar las exclusiones por fecha en PRISMA.
- Conservar el año como dato a extraer y cruzarlo con la familia de técnica de la RQ2 (2020–2022 frente a 2023–2026).
- Quitar el filtro de año de la búsqueda auxiliar: sin T no hay filtro de año, y las revisiones anteriores a 2020 ayudan a delimitar el vacío.

## Decisiones

| Punto | Decisión | Motivo |
|-------|----------|--------|
| Fila T y RQ6 | Eliminadas; queries sin filtro de año | Marco PICOC del usuario; regla del protocolo |
| Ventana 2020–2026 | Se mantiene como criterio de inclusión, con su justificación | Contiene el volumen y sigue la práctica de Kitchenham; el criterio explica el corte |
| Año de publicación | Dato a extraer en la RQ2, solo descriptivo | Conserva la lectura antes y después de 2023 sin una RQ temporal |
| Búsqueda auxiliar | Sin filtro de año | Coherente con el marco sin T; revisiones anteriores a 2020 delimitan el vacío |

## Queda para el usuario

- Si prefiere la postura del crítico (sin ventana temporal), quitar el criterio de año en una versión nueva con `Usa rsl-picoc sobre docs/ia-inclusion-cognitiva-software/`; esperar más registros previos a 2020.
- Las exclusiones por fecha se hacen en el cribado: registrarlas en el diagrama PRISMA (`RSL/seleccion/`).
