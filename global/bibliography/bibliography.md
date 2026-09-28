# Bibliografía compartida

Obras metodológicas que cualquier tema de `docs/` puede citar sin volver a buscarlas ni descargarlas. Cada obra vive en `global/bibliography/<carpeta>/` con su PDF y el MD generado por `pnpm -s rsl:source <pdf>`; el texto por página queda en `<carpeta>/_raw/`. Consultar primero con `pnpm graphify:bibliography:query "…"` y leer solo las líneas del pasaje que se cite.

El PDF se versiona en git solo si la licencia es abierta; si no, se ignora y el enlace de esta tabla permite recuperarlo. Tras agregar una obra: fila en esta tabla y `pnpm graphify:bibliography:refresh`.

| Clave | Referencia (APA 7) | DOI / URL | Carpeta | Licencia del PDF |
|---|---|---|---|---|
| kitchenham-charters-2007 | Kitchenham, B., & Charters, S. (2007). *Guidelines for performing systematic literature reviews in software engineering* (EBSE Technical Report EBSE-2007-01, Version 2.3). Keele University; University of Durham. | Sin DOI · [PDF](https://www.elsevier.com/__data/promis_misc/525444systematicreviewsguide.pdf) | `picoc/` | © Kitchenham 2007 (no versionado) |
| page-2021-prisma-2020 | Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., Shamseer, L., Tetzlaff, J. M., Akl, E. A., Brennan, S. E., Chou, R., Glanville, J., Grimshaw, J. M., Hróbjartsson, A., Lalu, M. M., Li, T., Loder, E. W., Mayo-Wilson, E., McDonald, S., . . . Moher, D. (2021). The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. *BMJ, 372*, Article n71. | [10.1136/bmj.n71](https://doi.org/10.1136/bmj.n71) · [PDF](https://eprints.whiterose.ac.uk/id/eprint/173303/1/bmj.n71.full.pdf) | `prisma/` | CC BY 4.0 (versionado) |

## Pasajes citables

La página del PDF es la del MD (`[PDF p.N]`); la página impresa es la que va en la cita.

| Clave | Pasaje | PDF p. | Página impresa | Uso |
|---|---|---|---|---|
| kitchenham-charters-2007 | Sección 5.3.2 *Question Structure*: PICOC (*Population, Intervention, Comparison, Outcome, Context*) para estructurar las preguntas de investigación, atribuido a Petticrew y Roberts [25]; el contexto indica dónde se aplica la intervención. | 19 | 11 | Justificar el marco PICOC y sus componentes. |
| kitchenham-charters-2007 | Sección 5.3.2: en ingeniería de software conviene no restringir la población al inicio porque hay pocos estudios primarios. | 19 | 11 | Justificar una población amplia. |
| page-2021-prisma-2020 | PRISMA 2020 consta de una lista de verificación de 27 ítems, una lista ampliada para el resumen y diagramas de flujo revisados. | 2 | 1 | Justificar PRISMA 2020 como guía de reporte. |
| page-2021-prisma-2020 | Fig. 1: plantilla del diagrama de flujo PRISMA 2020 (identificación, cribado, inclusión, con n por etapa). | 6 | 5 | Estructurar la selección de estudios y el diagrama. |
