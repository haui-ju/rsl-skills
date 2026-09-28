# Debate del polish — paper 2026-09-28-5

## 2026-09-28 · polish (versión nueva; base: 2026-09-28-4)

**Motivo:** el usuario cambió el marco a PICO y puso los filtros de inclusión dentro de la búsqueda (2021–2026, artículos de revista, inglés y español, acceso abierto). El marco se regeneró con rsl-picoc (`picoc/2026-09-28-5-PICO/`). Además, las skills se alinearon con Kitchenham y Charters (2007) y PRISMA 2020 (`playbooks/estandares-rsl.md`), y se añadió la cita del IEEE Thesaurus.
**Secciones trabajadas (on):** objetivo-rsl, apertura de II, marco-pico, palabras-clave, ecuacion-busqueda, criterios-seleccion.
**Frozen sin cambios (verificado byte a byte):** encabezado, contexto, problema, justificacion, organizacion, seleccion-prisma.
**Agentes:** critico-rsl (Sustento y estándares), defensor-rsl, impacto-social-rsl, redaccion-rsl (Hilo y Calidad de prosa; dos pasadas), citas-rsl.
**Procedimiento:** como el picoc cambió de marco, primero se llevaron a las secciones `on` los cambios que exige (PICO, cuatro RQ, filtros, Tabla IV, criterios nuevos) con cambio mínimo en el resto; los agentes revisaron ese texto.

### Decisiones clave

| Sección | Cambio | Origen |
|---|---|---|
| objetivo-rsl | Cuatro RQ; el objetivo 2 absorbe la fase del ciclo de vida (antes objetivo 5); se define LLM | picoc; redaccion-rsl |
| objetivo-rsl | Salvaguardas: CE5 (IA solo para diagnóstico o detección) y CE7 (robots sociales, tutores, rehabilitación); «consentimiento o asentimiento»; los datos éticos y geográficos se reportan junto a la RQ1 | picoc; impacto-social-rsl; critico-rsl |
| marco-pico | PICO en lugar de PICOC: las guías médicas plantean la pregunta desde población, intervención y resultado; Kitchenham y Charters (pp. 10–11) recogen la propuesta de Petticrew y Roberts, que añade comparación y contexto; el contexto no se incluye porque habría dejado fuera los estudios que no nombran la fase | picoc; critico-rsl; citas-rsl (atribución a Petticrew y Roberts) |
| marco-pico | Tabla I con cuatro componentes; Tabla II con cuatro RQ (RQ2 y RQ4 del picoc nuevo); la pregunta general se deriva de los cuatro componentes y de la fase | picoc; critico-rsl |
| palabras-clave | Cita del IEEE Thesaurus (IEEE, 2019) y nota bajo la Tabla III; «términos de indexación controlados» (Scopus y Web of Science no indexan con el tesauro IEEE); sin fila de contexto | usuario; critico-rsl |
| ecuacion-busqueda | Cuatro bloques con los filtros dentro; acceso abierto en Web of Science como filtro de la interfaz; prueba con estudios conocidos con marcadores `[[ n ]]`; Tabla IV por base con conteos con y sin filtros (`n = X`) | picoc; critico-rsl (estándares: p. 14 y p. 16) |
| criterios-seleccion | CI1–CI5 y CE1–CE7 del picoc; la apertura ya no repite el argumento del protocolo de la apertura de II; incluye los trabajos de congreso | picoc; redaccion-rsl; critico-rsl |
| Referencias | Entrada del IEEE Thesaurus (APA 7, autor corporativo; sin editorial repetida) | citas-rsl |

### Pendientes (no aplicados para no alargar el texto o porque dependen del usuario)

- **Amenazas a la validez (cuando se active `amenazas`):** sesgo del acceso abierto (puede sobrerrepresentar a grupos con financiamiento y subrepresentar la producción latinoamericana; la distribución por país se leerá como propia de la muestra); pérdida de los trabajos de congreso (ASSETS, CHI, W4A); el filtro de español casi no aporta registros porque los términos están en inglés; sesgo de publicación; la revisión no incluye a personas neurodivergentes en la interpretación.
- **Búsqueda (decide el usuario en rsl-picoc):** los bloques C y O, unidos con AND, dejan fuera dos de las tres revisiones conocidas; opciones: unirlos con OR o ampliar O (`evaluation`, `"accessibility evaluation"`). `TS=` en lugar de `ALL=` en Web of Science y `SRCTYPE j` en Scopus.
- **Validación de la búsqueda:** formar 3–5 estudios primarios de control y completar los marcadores `[[ n ]]`.
- **Datos del usuario:** fecha de búsqueda, conteos con y sin filtros por base (Tabla IV) y registro del protocolo (sección `declaraciones`, hoy `off`).
- **Stale (frozen):** `seleccion-prisma` aún dice «Excluidos por fecha de publicación» y no tiene el párrafo del proceso con los revisores; `encabezado`, `problema`, `justificacion` y `organizacion` dependen del picoc o del informe anterior. Descongelarlas (`on`) para alinearlas con PICO y la nueva plantilla.
- **Observado en frozen:** la sigla CI significa integración continua en Contexto y Justificación, y también nombra los criterios de inclusión; el título tiene unas 30 palabras (R6 pide brevedad) y no dice «revisión sistemática» de forma breve.

### Redacción y citas

- **redaccion-rsl:** primera pasada FAIL (párrafo 2 de la ecuación y apertura de los criterios; siglas CE y LLM); segunda pasada PASS en los siete párrafos cambiados. `redaccion:lint`: 0 FAIL; los 20 avisos están en el encabezado (frozen) y en la pregunta general (literal del picoc).
- **citas-rsl:** `--cites` PASS con 11 referencias; dos correcciones aplicadas (atribución de la propuesta a Petticrew y Roberts; editorial repetida en la entrada del IEEE).
