# Informe RSL — IA en el ciclo de vida del software para accesibilidad cognitiva

## 1. Tema de la investigación elegido para la RSL

### 1.1 Tema

Inteligencia artificial en el ciclo de vida del software para accesibilidad cognitiva y neurodivergencia: técnicas, fases de ingeniería y métricas de evaluación — una revisión sistemática de la literatura.

*(Tema final consensuado en `topic.md` tras panel `rsl-topic-panel`, veredicto GO_con_cambios. Énfasis defendible: celda V&V / GenAI / orientaciones COGA dentro del ciclo de vida.)*

### 1.2 Problemática

¿Cómo se han integrado técnicas de inteligencia artificial en las fases del ciclo de vida del software —con énfasis en diseño, personalización en runtime y, sobre todo, verificación, evaluación y auditoría— orientadas a usuarios con discapacidad cognitiva o neurodivergencia; qué métricas se reportan (incluidas orientaciones COGA frente al núcleo WCAG); y qué celdas de la matriz *condición × técnica × fase SE × métrica* permanecen vacías frente al sesgo documentado hacia la accesibilidad sensorial/visual y frente a revisiones HCI/AT o GenAI+web que no estructuran el proceso de Ingeniería de Software?

### 1.3 Objeto de estudio

Síntesis de evidencia primaria sobre técnicas de IA aplicadas a artefactos y procesos de Ingeniería de Software (requisitos y diseño de interfaces adaptativas, personalización en runtime, testing, V&V y auditoría de accesibilidad) para perfiles cognitivos o neurodivergentes, con el fin de producir una taxonomía **condición × técnica de IA × fase SE × métrica de evaluación**, contrastada explícitamente con el sesgo visual/WCAG-duro y **excluyendo** intervenciones clínicas, educativas o de tecnología asistiva sin componente explícito de proceso o de calidad de software.

## 2. Palabras clave

Las palabras clave, el marco PICOCT (población, intervención, comparación, resultado, contexto y tiempo), las queries y los criterios de inclusión y exclusión se encuentran en [picoc/2026-09-28-2-PICOCT/picoc.md](picoc/2026-09-28-2-PICOCT/picoc.md).

## 3. Artículos de revisión de literatura relacionados con el tema de investigación

*(Mínimo 2 artículos de revisión; meta: 3 RSL ancla. Adicionalmente se declaran fronteras de solapamiento exigidas por el panel.)*

| Referencia bibliográfica (APA) | DOI / URL | Razón | PDF |
|--------------------------------|-----------|-------|-----|
| Chemnad, K., & Othman, A. (2024). Digital accessibility in the era of artificial intelligence—Bibliometric analysis and systematic review. *Frontiers in Artificial Intelligence, 7*, Article 1349668. | https://doi.org/10.3389/frai.2024.1349668 | RSL (≈43 estudios) sobre IA y accesibilidad digital; documenta el **predominio de la discapacidad visual** y cobertura insuficiente de TEA/cognitivo/motor; justifica el contraste “vs sesgo visual”, sin taxonomía de fases SE. | `RSL/PDF/chemnad-othman-2024-digital-accessibility-ai.pdf` |
| Perry, N., et al. (2024). AI technology to support adaptive functioning in neurodevelopmental conditions in everyday environments: A systematic review. *npj Digital Medicine, 7*, Article 370. | https://doi.org/10.1038/s41746-024-01355-7 | RSL (15 estudios) clínico-asistiva sobre IA y neurodesarrollo en entornos cotidianos; delimita lo que **no** es el aporte SE (outcomes clínicos vs fases/métricas de ingeniería). | `RSL/PDF/perry-etal-2024-ai-neurodevelopmental.pdf` |
| Aljedaani, W., & Mollik, R. H. (2026). Large language models for web accessibility: A systematic literature review. In *Proceedings of the 23rd International Web for All Conference (W4A ’26)* (pp. 160–171). ACM. | https://doi.org/10.1145/3800424.3800452 · espejo OA: https://arxiv.org/abs/2605.13873 | RSL de 38 estudios LLM×accesibilidad web; WCAG como marco dominante y **limitada consideración de COGA**; frontera GenAI+web sin matriz **fase SE × métrica** para perfiles cognitivos/neurodivergentes. | `RSL/PDF/aljedaani-mollik-2026-llm-web-accessibility.pdf` |

**Fronteras de solapamiento (no sustituyen a las tres RSL ancla):**

| Frontera | DOI | Uso en el protocolo |
|----------|-----|---------------------|
| Xu et al. (2025). Scoping review de diseño HAI inclusivo/adaptativo para usuarios neurodivergentes (*Disabil. Rehabil. Assist. Technol.*). | https://doi.org/10.1080/17483107.2025.2579822 | **Exclusión / diferenciación HCI-AT**: diseño/interacción/ética; no taxonomía condición × técnica × **fase SE** × métrica de proceso. Mantener tabla RQ-propia vs temas Xu en el protocolo. |
| Paiva, D. M. B., Freire, A. P., & Fortes, R. P. M. (2021). Accessibility and software engineering processes: A systematic literature review. *Journal of Systems and Software, 171*, 110819. | https://doi.org/10.1016/j.jss.2020.110819 | **Exclusión / diferenciación SE sin IA cognitiva**: a11y en procesos SE (94 estudios); el aporte propio añade **IA + cognitivo/neurodivergencia + métricas** (énfasis V&V/COGA). |

## 4. Estado del conocimiento y necesidad de una nueva RSL

La literatura reciente consolidó tres frentes que este trabajo no pretende repetir. Chemnad y Othman (2024) sintetizan IA aplicada a accesibilidad digital y documentan un predominio estructural de la discapacidad visual, junto con cobertura insuficiente de TEA y otras condiciones y débil adhesión a estándares; su marco no organiza el ciclo de vida SE ni métricas de evaluación por fase para accesibilidad cognitiva. Perry et al. (2024) revisan IA para funcionamiento adaptativo en condiciones del neurodesarrollo en entornos cotidianos, con énfasis en outcomes clínicos y de apoyo, frontera explícita respecto de artefactos y procesos de ingeniería. Aljedaani y Mollik (2026) revisan 38 estudios sobre LLM en accesibilidad web y muestran tareas predominantemente text-céntricas, WCAG como marco dominante y limitada consideración de COGA, sin construir una taxonomía condición × técnica × fase SE × métrica de calidad. Frente a ello, Xu et al. (2025) y Paiva et al. (2021) se tratan como fronteras de solapamiento: HCI/AT neurodivergente y a11y en SE sin eje IA+cognitivo, respectivamente.

En consecuencia, persiste la necesidad de una RSL anclada en Ingeniería de Software que organice cómo la IA interviene en diseño, personalización y, sobre todo, verificación/evaluación para accesibilidad cognitiva y neurodivergencia, explicitando métricas (COGA frente a WCAG-duro) y celdas vacías. El entregable mínimo no es solo la síntesis bibliográfica, sino una taxonomía exportable a Definition of Done / gate de CI (automatizable, semi-automático o solo validación con usuarios). En el Perú, la Ley 29973 (arts. 15–23) y la Resolución N.º 001-2025-PCM/SGTD (WCAG 2.2 para la Administración Pública) hacen visible el riesgo de accesibilidad de fachada si se omite la dimensión cognitiva. Salvaguarda ética mínima: no medicalizar la neurodivergencia; no sustituir evidencia clínica por métricas de ingeniería; señalar omisiones de participación de personas con discapacidad; situar ODS 10.2 y 4.5/4.a como horizonte de valor público, no como impacto causal automático del mapeo.

*(≈ 295 palabras)*

## 5. Línea(s) de investigación de la UTP

La investigación responde, en primer lugar, a la línea **«Computación Científica»**, transversal a los programas de Ingeniería de la Facultad de Ingeniería de la UTP, cuyo objetivo es elaborar y desarrollar soluciones computacionales vinculadas a modelos y técnicas para analizar procesos de ingeniería. Al centrarse en modelos y técnicas de inteligencia artificial —y en su evaluación mediante métricas— aplicados al ciclo de vida del software inclusivo cognitivo, el estudio se alinea de modo directo con dicha línea.

De forma complementaria, se vincula con la línea **«Aplicaciones TIC, electrónicas, robóticas y de telecomunicaciones para la competitividad, salud, educación y seguridad ciudadana»**. La síntesis interesa al gobierno digital peruano en tanto la Resolución N.º 001-2025-PCM/SGTD exige WCAG 2.2 y la Ley 29973 obliga a facilitar el uso de servicios web a distintos tipos de discapacidad; el aporte de la RSL es organizar evidencia SE/IA para accesibilidad cognitiva, **no** certificar cumplimiento normativo.

## 6. Competencias de la carrera

El tema se relaciona con la competencia de **desarrollo de software**, al exigir dominio del ciclo de vida y de los entregables por fase (requisitos, diseño, verificación y evaluación), eje analítico de la RSL. Conecta con **tecnologías de vanguardia** y **desarrollo con IA**, al examinar cómo la inteligencia artificial —incluido el GenAI— se incorpora a prácticas y herramientas de ingeniería. Dialoga con el **desarrollo frontend** y el análisis de sistemas, dado el peso de interfaces adaptativas, usabilidad y requisitos de accesibilidad cognitiva. La lectura crítica de métricas y de vacíos de participación de usuarios con discapacidad refuerza un desarrollo responsable, evitando reducir “inclusión” a automatismos GenAI o a checklists WCAG sin dimensión cognitiva.

## 7. Título tentativo de la RSL

Inteligencia artificial en el ciclo de vida del software para accesibilidad cognitiva y neurodivergencia: técnicas, fases de ingeniería y métricas de evaluación — una revisión sistemática de la literatura

**Nota de artefacto (ajuste previsto del protocolo):** la taxonomía resultante incluirá columna de transferibilidad a Definition of Done / CI y señalará qué puede cubrir GenAI en V&V frente a lo que exige validación con usuarios COGA; se excluirá como “éxito industrial” cualquier celda que no traduzca la métrica a criterio de aceptación o a ítem de backlog priorizable por costo/riesgo regulatorio (p. ej. EAA / EN 301 549, criterio de cognición limitada).
