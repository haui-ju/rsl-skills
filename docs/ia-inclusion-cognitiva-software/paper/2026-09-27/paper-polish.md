<!-- paper:section id=encabezado -->
# Inteligencia artificial en el ciclo de vida del software para accesibilidad cognitiva y neurodivergencia: técnicas, fases de ingeniería y métricas de evaluación — una revisión sistemática de la literatura

**Tema.** IA (incluidos GenAI/LLM) en el ciclo de vida del software para accesibilidad cognitiva y neurodivergencia, con énfasis en V&V/auditoría y taxonomía condición × técnica × fase SE × métrica (COGA frente a WCAG).

**Problemática.** ¿Cómo se han integrado técnicas de IA en las fases del ciclo de vida del software —sobre todo en verificación, evaluación y auditoría— para usuarios con discapacidad cognitiva o neurodivergencia; qué métricas se reportan (COGA frente a WCAG); y qué celdas de la matriz *condición × técnica × fase SE × métrica* quedan vacías o no transferibles a Definition of Done / CI frente al sesgo sensorial/visual y a síntesis clínicas, HCI o GenAI+web que no estructuran el proceso de Ingeniería de Software?

**Objetivo.** Sintetizar evidencia primaria de IA en artefactos y procesos SE para perfiles cognitivos o neurodivergentes, y producir esa taxonomía con columna de transferibilidad (automatizable en CI / juicio experto / validación con usuarios), delimitada frente a fronteras clínicas, HCI y GenAI+web WCAG-duro.
<!-- /paper:section -->

## I. Introducción

<!-- paper:section id=contexto -->
### Contexto

La accesibilidad digital busca que las personas puedan percibir, operar y comprender el software. En ese marco, las Pautas de Accesibilidad para el Contenido Web (WCAG) 2.2 concentran la conformidad verificable (World Wide Web Consortium [W3C], 2023). Las orientaciones del grupo de trabajo del W3C sobre accesibilidad cognitiva y del aprendizaje (COGA), en cambio, atienden otra cara del problema: la comprensión, la memoria y la carga cognitiva (W3C, 2021). Estos aspectos son, por lo general, más difíciles de verificar de forma automática.

A partir de ese matiz, por *accesibilidad cognitiva* se entiende aquí la reducción de las barreras de comprensión, memoria y carga cognitiva. Por *neurodivergencia* se entiende una categoría amplia que, cuando la evidencia lo permite, se desglosa en condiciones concretas, como el trastorno del espectro autista, el trastorno por déficit de atención e hiperactividad o la dislexia. Este uso no pretende medicalizar a las personas. En consecuencia, el objeto de esta revisión no es la tecnología asistiva clínica. Es el modo en que la inteligencia artificial (IA), incluida la IA generativa (GenAI), se inserta en el ciclo de vida del software, desde los requisitos y el diseño hasta la verificación y validación (V&V).

Este alcance obliga a revisar primero lo que ya han sintetizado las revisiones previas. Chemnad y Othman (2024), tras revisar 43 estudios de IA y accesibilidad digital, documentaron un claro predominio de la discapacidad visual y un vacío en el trastorno del espectro autista y en los trastornos neurológicos. Perry et al. (2024), por su parte, sintetizaron 15 trabajos de IA para el funcionamiento adaptativo en condiciones del neurodesarrollo, con resultados de apoyo cotidiano y no de ingeniería. En el terreno de los modelos de lenguaje, Aljedaani y Mollik (2026) analizaron 33 estudios primarios sobre su uso en la accesibilidad web. En ellos, las WCAG dominan como marco y las orientaciones COGA reciben poca atención, aunque la revisión no organiza la evidencia por fase del ciclo de vida.

En los bordes del tema se sitúan otras dos revisiones. Xu et al. (2026) cartografiaron 117 estudios sobre el diseño de la interacción entre personas neurodivergentes y sistemas de IA. Paiva et al. (2021), a su vez, revisaron 94 estudios sobre accesibilidad en los procesos de Ingeniería de Software, sin el eje de la IA ni el de la accesibilidad cognitiva.

Así, el estado del arte deja abiertas tres tensiones que se refuerzan entre sí. La primera enfrenta lo sensorial con lo cognitivo; la segunda, el enfoque clínico o de diseño de interacción con el proceso de ingeniería; la tercera, la automatización con la validación con usuarios. Esta última tiene consecuencias prácticas. Los equipos controlan la calidad mediante la integración continua (CI), que ejecuta pruebas automáticas con cada cambio, y mediante la *Definition of Done*, el conjunto de criterios que un incremento debe cumplir para darse por terminado. Si esos controles se limitan a criterios WCAG verificables automáticamente, que un analizador no detecte fallos no basta para afirmar que el software es inclusivo en el plano cognitivo.
<!-- /paper:section -->

<!-- paper:section id=problema -->
### El problema

De esas tensiones nace la pregunta de investigación: ¿cómo se ha integrado la IA en las fases del ciclo de vida del software, sobre todo en la verificación, la evaluación y la auditoría, para personas con discapacidad cognitiva o neurodivergentes? La pregunta abarca también el diseño y la personalización. Se complementa, además, con otras dos: qué métricas se reportan y qué combinaciones de condición, técnica, fase y métrica carecen de evidencia, dado el predominio de los estudios centrados en la discapacidad sensorial.

A ello se suma una tendencia reciente. En los estudios con modelos de lenguaje, la definición, la detección y la evaluación de los problemas de accesibilidad se apoyan sobre todo en criterios WCAG, mientras que las orientaciones cognitivas reciben una atención limitada (Aljedaani & Mollik, 2026). El panorama de síntesis es, así, desigual. Abundan las revisiones con sesgo visual (Chemnad & Othman, 2024), las de apoyo al funcionamiento adaptativo (Perry et al., 2024) y las de diseño de interacción (Xu et al., 2026). Escasean, en cambio, las que relacionan a la vez el tipo de condición, la técnica de IA, la fase del ciclo de vida y la métrica; en adelante, ese cruce de cuatro dimensiones se denomina *la taxonomía*.

El vacío, entonces, no es la falta de trabajos cercanos, sino la de una síntesis que los integre. Incluso el mapa de Paiva et al. (2021), ordenado por fase, deja fuera la IA y la dimensión cognitiva. Esta fragmentación eleva el riesgo de una accesibilidad solo aparente. Falta saber, para cada combinación, qué técnica se usó, en qué fase, con qué métrica y con qué límite de automatización. Eso es lo que se propone estudiar.
<!-- /paper:section -->

<!-- paper:section id=justificacion -->
### Justificación

Por ello, esta revisión articula tres elementos: las orientaciones COGA, la IA a lo largo del ciclo de vida, con énfasis en la V&V, y las métricas propias de la Ingeniería de Software. De este modo evita replicar las síntesis existentes sobre diseño de interacción. Las revisiones previas aportan el contraste necesario, pero no un mapa por fase y métrica.

Además, la Ley N.º 29973, Ley General de la Persona con Discapacidad (Congreso de la República del Perú, 2012), reconoce derechos de accesibilidad que alcanzan a las personas con discapacidad cognitiva e intelectual. Las metas 10.2 y 4.5 de los Objetivos de Desarrollo Sostenible dan contexto, por su parte, al valor público de la revisión, sin atribuirle un impacto causal.

En la práctica, el mapa será útil si asigna a cada hallazgo uno de tres niveles. El primero reúne lo que puede comprobarse automáticamente como control de la CI. El segundo, lo que requiere el juicio de un especialista en accesibilidad, por ejemplo si un texto simplificado por un modelo de lenguaje conserva el sentido. El tercero, lo que solo puede validarse con la participación de personas con discapacidad cognitiva o neurodivergentes. La revisión no pretende certificar el cumplimiento normativo.

De ahí la necesidad de una revisión sistemática de la literatura (RSL): abundan las revisiones sobre temas vecinos y el riesgo de replicarlas es alto. Si la combinación menos estudiada, la V&V asistida por GenAI con criterios cognitivos, reuniera pocos estudios primarios, el aporte legítimo sería documentar ese vacío, no forzar conclusiones.
<!-- /paper:section -->

<!-- paper:section id=objetivo-rsl -->
### Objetivo de la RSL

En respuesta a la pregunta planteada, el objetivo general es sintetizar la evidencia primaria sobre IA en los procesos de Ingeniería de Software dirigidos a personas con discapacidad cognitiva o neurodivergentes. Esa evidencia se organizará en la taxonomía, que indicará para cada combinación si su resultado puede verificarse automáticamente en la CI, si requiere juicio experto o si exige pruebas con usuarios.

De él se derivan seis objetivos específicos, uno por cada pregunta del protocolo. Los tres primeros buscan caracterizar los perfiles estudiados y su grado de participación, identificar las técnicas de IA y su papel en el proceso, y contrastar la evidencia cognitiva con la sensorial y con la conformidad WCAG. Los dos siguientes buscan inventariar las métricas y su grado de automatización, y ubicar la IA en cada fase del ciclo de vida. El último describe la evolución de la producción entre 2020 y 2026, antes y después de la adopción masiva de la GenAI.

La revisión adopta, además, salvaguardas éticas explícitas. No medicaliza la neurodivergencia, no sustituye la evidencia clínica por métricas de ingeniería y señala cuándo los estudios omiten la participación de personas con discapacidad. Tampoco confunde un analizador WCAG sin errores con la inclusión cognitiva.
<!-- /paper:section -->

<!-- paper:section id=organizacion -->
### Organización del contenido de la revisión

Sobre esa base, el resto del artículo presenta el marco conceptual y el método, que sigue la guía *Preferred Reporting Items for Systematic Reviews and Meta-Analyses* (PRISMA) 2020 (Page et al., 2021). Después expone los resultados organizados según la taxonomía, con énfasis en la V&V asistida por GenAI, y señala las combinaciones sin evidencia. La discusión examina qué hallazgos pueden trasladarse a la práctica de desarrollo, y las conclusiones cierran el trabajo. En un anexo se detalla la comparación de alcance con las revisiones previas.
<!-- /paper:section -->

<!-- paper:section id=referencias -->
## Referencias

Aljedaani, W., & Mollik, R. H. (2026). Large language models for web accessibility: A systematic literature review. In *Proceedings of the 23rd International Web for All Conference (W4A ’26)* (pp. 160–171). Association for Computing Machinery. https://doi.org/10.1145/3800424.3800452

Chemnad, K., & Othman, A. (2024). Digital accessibility in the era of artificial intelligence—Bibliometric analysis and systematic review. *Frontiers in Artificial Intelligence, 7*, Article 1349668. https://doi.org/10.3389/frai.2024.1349668

Congreso de la República del Perú. (2012). *Ley N.º 29973, Ley General de la Persona con Discapacidad*. Diario Oficial El Peruano.

Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., Shamseer, L., Tetzlaff, J. M., Akl, E. A., Brennan, S. E., Chou, R., Glanville, J., Grimshaw, J. M., Hróbjartsson, A., Lalu, M. M., Li, T., Loder, E. W., Mayo-Wilson, E., McDonald, S., . . . Moher, D. (2021). The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. *BMJ, 372*, Article n71. https://doi.org/10.1136/bmj.n71

Paiva, D. M. B., Freire, A. P., & de Mattos Fortes, R. P. (2021). Accessibility and software engineering processes: A systematic literature review. *Journal of Systems and Software, 171*, Article 110819. https://doi.org/10.1016/j.jss.2020.110819

Perry, N., Sun, C., Munro, M., Boulton, K. A., & Guastella, A. J. (2024). AI technology to support adaptive functioning in neurodevelopmental conditions in everyday environments: A systematic review. *npj Digital Medicine, 7*, Article 370. https://doi.org/10.1038/s41746-024-01355-7

World Wide Web Consortium. (2021). *Making content usable for people with cognitive and learning disabilities* (W3C Working Group Note). https://www.w3.org/TR/coga-usable/

World Wide Web Consortium. (2023). *Web Content Accessibility Guidelines (WCAG) 2.2* (W3C Recommendation). https://www.w3.org/TR/WCAG22/

Xu, Z., Liu, F., Xia, G., Duan, Y., & Yu, L. (2026). A scoping review of inclusive and adaptive human–AI interaction design for neurodivergent users. *Disability and Rehabilitation: Assistive Technology, 21*(4), 943–961. https://doi.org/10.1080/17483107.2025.2579822
<!-- /paper:section -->
