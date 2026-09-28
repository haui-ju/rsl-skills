<!-- paper:section id=encabezado -->
# Inteligencia artificial en el ciclo de vida del software para accesibilidad cognitiva y neurodivergencia: técnicas, fases de ingeniería y métricas de evaluación — una revisión sistemática de la literatura

**Tema.** IA (incluidos GenAI/LLM) en el ciclo de vida del software para accesibilidad cognitiva y neurodivergencia, con énfasis en V&V/auditoría y taxonomía condición × técnica × fase SE × métrica (COGA frente a WCAG).

**Problemática.** ¿Cómo se han integrado técnicas de IA en las fases del ciclo de vida del software —sobre todo en verificación, evaluación y auditoría— para usuarios con discapacidad cognitiva o neurodivergencia; qué métricas se reportan (COGA frente a WCAG); y qué celdas de la matriz *condición × técnica × fase SE × métrica* quedan vacías o no transferibles a Definition of Done / CI frente al sesgo sensorial/visual y a síntesis clínicas, HCI o GenAI+web que no estructuran el proceso de Ingeniería de Software?

**Objetivo.** Sintetizar evidencia primaria de IA en artefactos y procesos SE para perfiles cognitivos o neurodivergentes, y producir esa taxonomía con columna de transferibilidad (automatizable en CI / juicio experto / validación con usuarios), delimitada frente a fronteras clínicas, HCI y GenAI+web WCAG-duro.
<!-- /paper:section -->

## I. Introducción

<!-- paper:section id=contexto -->
### Contexto

La accesibilidad digital busca que las personas puedan percibir, operar y comprender el software. En ese marco, WCAG 2.2 concentra la conformidad verificable (World Wide Web Consortium [W3C], 2023); no obstante, las orientaciones COGA atienden otra cara del problema —comprensión, memoria y carga cognitiva—, por lo general menos automatizable.

A partir de ese matiz, por *accesibilidad cognitiva* se entiende aquí la reducción de dichas barreras, y por *neurodivergencia* una categoría que se estratifica cuando la evidencia lo permite (p. ej. TEA, TDAH o dislexia), sin medicalizar perfiles. En consecuencia, el objeto de esta revisión no es la tecnología asistiva clínica, sino el modo en que la IA —incluidos GenAI y LLM— se inserta en el ciclo de vida del software.

Ese recorte exige situar lo ya sintetizado. Chemnad y Othman (2024), tras revisar 43 estudios de IA y accesibilidad digital, documentaron un claro predominio de la discapacidad visual; en una línea distinta, Perry et al. (2024) sintetizaron 15 trabajos de apoyo cotidiano en neurodesarrollo y dejaron, por tanto, una frontera clínica más que de ingeniería. Más cerca del GenAI, Aljedaani y Mollik (2026) examinaron 38 estudios de LLM en accesibilidad web y hallaron WCAG dominante junto con una consideración limitada de COGA, aunque sin organizar la evidencia por fase del ciclo de vida.

Así, el estado del arte deja abiertas al menos tres tensiones que se refuerzan entre sí: lo sensorial frente a lo cognitivo, lo clínico o HCI frente al proceso de Ingeniería de Software, y la automatización frente a la validación con usuarios. De ahí que un escáner WCAG “en verde” no baste para hablar de inclusión cognitiva, incluso cuando la regulación empuja conformidad WCAG y no un mandato COGA.
<!-- /paper:section -->

<!-- paper:section id=problema -->
### El problema

Es precisamente desde esas tensiones desde donde se formula la pregunta de investigación: ¿cómo se ha usado la IA —en especial en verificación, evaluación y auditoría— para accesibilidad cognitiva o neurodivergencia; con qué métricas; y qué celdas de la matriz SE quedan vacías o no pasan a DoD/CI?

A ello se suma una tendencia reciente: GenAI desplaza esfuerzo hacia detección y remediación a menudo WCAG-dura (Aljedaani & Mollik, 2026), al tiempo que la regulación refuerza checklists automatizables. Por eso abunda la síntesis con sesgo visual (Chemnad & Othman, 2024) y la de carácter clínico o HCI (Perry et al., 2024; Xu et al., 2025), mientras escasea el cruce IA × cognitivo × fase SE × métrica.

El vacío, entonces, no consiste en afirmar que no existan papers adyacentes, sino en reconocer que falta un mapa centrado en Ingeniería de Software. Hoy la evidencia aparece fragmentada y el riesgo de accesibilidad de fachada es alto; lo deseable, en cambio, es saber por celda qué técnica se usó, en qué fase, con qué métrica y con qué límite de automatización. Eso es, en suma, lo que se propone estudiar.
<!-- /paper:section -->

<!-- paper:section id=justificacion -->
### Justificación

Por esa razón se eligió un tema que articula COGA, IA en el ciclo de vida —sobre todo en V&V— y métricas propias de Ingeniería de Software, sin caer en un remake de síntesis HCI. Las tres anclas aportan el contraste necesario —sesgo visual, frontera clínica y COGA débil en GenAI+web—, pero no el entregable que aquí se busca.

Además, los titulares de derecho son personas con discapacidad cognitiva e intelectual (Ley 29973), y los ODS 10.2 y 4.5/4.a orientan un horizonte de valor público sin atribuir a la revisión un impacto causal. En la práctica, el mapa solo resulta útil si discrimina qué puede ir a un gate de CI, qué exige juicio experto y qué no cierra sin usuarios COGA, sin pretender certificar EAA ni PCM.

De ahí la necesidad de una RSL: el campo está saturado de fronteras adyacentes y el riesgo de remake es alto. Si la celda V&V × GenAI × COGA resultara fina, el aporte legítimo será documentar vacíos, no inventar densidad.
<!-- /paper:section -->

<!-- paper:section id=objetivo-rsl -->
### Objetivo de la RSL

En respuesta directa a la pregunta planteada, el objetivo primario es sintetizar evidencia primaria de IA en procesos de Ingeniería de Software para perfiles cognitivos o neurodivergentes y producir la taxonomía cuádruple con transferibilidad a DoD/CI.

Como complemento, se contrastará el sesgo visual documentado por Chemnad y Othman (2024) y la debilidad COGA en GenAI+web mostrada por Aljedaani y Mollik (2026), y se delimitará lo clínico (Perry et al., 2024) frente a lo HCI o SE sin eje IA+cognitivo (Xu et al., 2025; Paiva et al., 2021). En todo caso, no se medicaliza la neurodivergencia ni se confunde un escáner WCAG con inclusión cognitiva.
<!-- /paper:section -->

<!-- paper:section id=organizacion -->
### Organización del contenido de la revisión

Con ese marco, el resto del trabajo avanza del marco conceptual al método tipo PRISMA, luego a los resultados por celda —con énfasis en V&V × GenAI × COGA—, a la discusión y a las conclusiones. La tabla de solapamiento frente a las tres anclas y el piloto de la celda aguda se recogen, finalmente, en anexo.
<!-- /paper:section -->

<!-- paper:section id=referencias -->
## Referencias

Aljedaani, W., & Mollik, R. H. (2026). Large language models for web accessibility: A systematic literature review. In *Proceedings of the 23rd International Web for All Conference (W4A ’26)* (pp. 160–171). Association for Computing Machinery. https://doi.org/10.1145/3800424.3800452

Chemnad, K., & Othman, A. (2024). Digital accessibility in the era of artificial intelligence—Bibliometric analysis and systematic review. *Frontiers in Artificial Intelligence, 7*, Article 1349668. https://doi.org/10.3389/frai.2024.1349668

Paiva, D. M. B., Freire, A. P., & de Mattos Fortes, R. P. (2021). Accessibility and software engineering processes: A systematic literature review. *Journal of Systems and Software, 171*, Article 110819. https://doi.org/10.1016/j.jss.2020.110819

Perry, N., Sun, C., Munro, M., Boulton, K. A., & Guastella, A. J. (2024). AI technology to support adaptive functioning in neurodevelopmental conditions in everyday environments: A systematic review. *npj Digital Medicine, 7*, Article 370. https://doi.org/10.1038/s41746-024-01355-7

World Wide Web Consortium. (2023). *Web Content Accessibility Guidelines (WCAG) 2.2* (W3C Recommendation). https://www.w3.org/TR/WCAG22/

Xu, Z., Liu, F., Xia, G., Duan, Y., & Yu, L. (2025). A scoping review of inclusive and adaptive human–AI interaction design for neurodivergent users. *Disability and Rehabilitation: Assistive Technology, 21*(4), 943–961. https://doi.org/10.1080/17483107.2025.2579822
<!-- /paper:section -->
