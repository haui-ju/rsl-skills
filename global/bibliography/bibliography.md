# Bibliografía compartida

Obras metodológicas que cualquier tema de `docs/` puede citar sin volver a buscarlas ni descargarlas. Cada obra vive en `global/bibliography/<carpeta>/` con su PDF y el MD generado por `pnpm -s rsl:source <pdf>`; el texto por página queda en `<carpeta>/_raw/`. Consultar primero con `pnpm graphify:bibliography:query "…"` y leer solo las líneas del pasaje que se cite.

El PDF se versiona en git solo si la licencia es abierta; si no, se ignora y el enlace de esta tabla permite recuperarlo. Tras agregar una obra: fila en esta tabla y `pnpm graphify:bibliography:refresh`.

| Clave | Referencia (APA 7) | DOI / URL | Carpeta | Licencia del PDF |
|---|---|---|---|---|
| kitchenham-charters-2007 | Kitchenham, B., & Charters, S. (2007). *Guidelines for performing systematic literature reviews in software engineering* (EBSE Technical Report EBSE-2007-01, Version 2.3). Keele University; University of Durham. | Sin DOI · [PDF](https://www.elsevier.com/__data/promis_misc/525444systematicreviewsguide.pdf) | `picoc/` | © Kitchenham 2007 (no versionado) |
| page-2021-prisma-2020 | Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., Shamseer, L., Tetzlaff, J. M., Akl, E. A., Brennan, S. E., Chou, R., Glanville, J., Grimshaw, J. M., Hróbjartsson, A., Lalu, M. M., Li, T., Loder, E. W., Mayo-Wilson, E., McDonald, S., . . . Moher, D. (2021). The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. *BMJ, 372*, Article n71. | [10.1136/bmj.n71](https://doi.org/10.1136/bmj.n71) · [PDF](https://eprints.whiterose.ac.uk/id/eprint/173303/1/bmj.n71.full.pdf) | `prisma/` | CC BY 4.0 (versionado) |
| ieee-2019-thesaurus | Institute of Electrical and Electronics Engineers. (2019). *2019 IEEE thesaurus* (Version 1.0). | Sin DOI · [Acceso oficial](https://www.ieee.org/publications/services/thesaurus-access-page.html) | `../thesaurus/` (`IEEE.pdf`) | CC BY-NC-ND 4.0 |
| acm-ccs-2012 | Association for Computing Machinery. (2012). *The 2012 ACM computing classification system*. | Sin DOI · [SKOS](https://dl.acm.org/pb-assets/dl_ccs/acm_ccs2012-1626988337597.xml) | `../thesaurus/acm-ccs/` (`acm-ccs-2012.xml`) | Uso libre educativo y de investigación (© ACM) |

## Pasajes citables

La página del PDF es la del MD (`[PDF p.N]`); la página impresa es la que va en la cita.

| Clave | Pasaje | PDF p. | Página impresa | Uso |
|---|---|---|---|---|
| kitchenham-charters-2007 | Sección 5.3.2 *Question Structure*: PICOC (*Population, Intervention, Comparison, Outcome, Context*) para estructurar las preguntas de investigación, atribuido a Petticrew y Roberts [25]; el contexto indica dónde se aplica la intervención. | 19 | 11 | Justificar el marco PICOC y sus componentes. |
| kitchenham-charters-2007 | Sección 5.3.2: en ingeniería de software conviene no restringir la población al inicio porque hay pocos estudios primarios. | 19 | 11 | Justificar una población amplia. |
| kitchenham-charters-2007 | Glosario: la revisión sistemática identifica, analiza e interpreta la evidencia disponible de forma no sesgada y (en cierto grado) repetible. | 7 | vi | Justificar el método por su repetibilidad. |
| kitchenham-charters-2007 | Sección 5.3.2: las guías médicas plantean la pregunta desde población, intervención y resultados; PICOC las extiende con comparación y contexto. | 18–19 | 10–11 | Contrastar PICOC con el esquema clínico. |
| kitchenham-charters-2007 | Sección 5.4: un protocolo predefinido reduce el sesgo del investigador; sin él, la selección puede guiarse por sus expectativas. | 20 | 12 | Justificar el protocolo previo. |
| kitchenham-charters-2007 | Sección 6.1: descomponer la pregunta en sus componentes, listar sinónimos y variantes, usar los términos de indexación de las bases y combinar con AND y OR. | 22 | 14 | Justificar palabras clave, tesauro y ecuación. |
| kitchenham-charters-2007 | Sección 6.1.4: la búsqueda debe ser transparente y replicable y documentarse con detalle suficiente. | 24 | 16 | Justificar la documentación de la búsqueda. |
| kitchenham-charters-2007 | Sección 6.2.1: los criterios de selección se deciden al definir el protocolo para reducir el sesgo. | 26 | 18 | Justificar criterios fijados de antemano. |
| kitchenham-charters-2007 | Sección 6.2.2: la selección es un proceso en varias etapas (título y resumen, luego texto completo). | 27 | 19 | Justificar las etapas de selección. |
| kitchenham-charters-2007 | Sección 6.2.2: se recomienda mantener una lista de estudios excluidos con el motivo de cada exclusión. | 28 | 20 | Justificar que la selección quede documentada. |
| kitchenham-charters-2007 | Sección 6.2.3: un investigador único discute los estudios incluidos y excluidos con su asesor o aplica test-retest sobre una muestra aleatoria para comprobar la consistencia de sus decisiones. | 28 | 20 | Justificar la verificación de la selección con un solo revisor. |
| kitchenham-charters-2007 | Sección 6.1.2: el sesgo de publicación (los resultados positivos se publican más) puede sesgar la revisión si no se controla. | 23 | 15 | Declarar limitaciones de la evidencia. |
| kitchenham-charters-2007 | Tabla 8: estructura del reporte de una revisión sistemática (título, resumen estructurado, antecedentes, preguntas, métodos, estudios incluidos y excluidos, resultados, discusión, conclusiones). | 50–51 | 42–43 | Estructurar el paper. |
| page-2021-prisma-2020 | Resumen: PRISMA 2020 ayuda a informar de forma transparente por qué se hizo la revisión, qué se hizo y qué se encontró. | 2 | 1 | Justificar el reporte con PRISMA. |
| page-2021-prisma-2020 | PRISMA 2020 consta de una lista de verificación de 27 ítems, una lista ampliada para el resumen y diagramas de flujo revisados. | 2 | 1 | Justificar PRISMA 2020 como guía de reporte. |
| page-2021-prisma-2020 | Tabla 1, ítems 8 y 16b: cuántos revisores cribaron cada registro, si trabajaron de forma independiente y qué herramientas usaron; estudios que parecían cumplir los criterios pero se excluyeron. | 5 | 4 | Reportar el proceso de selección. |
| page-2021-prisma-2020 | Tabla 1, ítems 23b–23c y 24a–27: limitaciones de la evidencia y del proceso; registro y protocolo, financiamiento, conflictos de intereses y disponibilidad de datos. | 5 | 4 | Amenazas a la validez y declaraciones. |
| page-2021-prisma-2020 | Tabla 2: lista para el resumen estructurado (objetivo, criterios, fuentes, riesgo de sesgo, síntesis, estudios incluidos, resultados, limitaciones, interpretación, financiamiento, registro). | 6 | 5 | Estructurar el resumen. |
| page-2021-prisma-2020 | Fig. 1: plantilla del diagrama de flujo PRISMA 2020 (identificación, cribado, inclusión, con n por etapa). | 6 | 5 | Estructurar la selección de estudios y el diagrama. |
