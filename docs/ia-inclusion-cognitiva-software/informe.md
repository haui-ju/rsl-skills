# Informe RSL — IA en el ciclo de vida del software para accesibilidad cognitiva

## 1. Tema de la investigación elegido para la RSL

### 1.1 Tema

Inteligencia artificial en el ciclo de vida del software para accesibilidad cognitiva y neurodivergencia: técnicas, fases de ingeniería y métricas de evaluación — una revisión sistemática de la literatura.

*(Tema final consensuado en `topic.md` tras panel `rsl-topic-panel`, veredicto GO_con_cambios.)*

### 1.2 Problemática

¿Cómo se han integrado técnicas de inteligencia artificial en las fases del ciclo de vida del software (con énfasis en diseño, personalización y, sobre todo, verificación/evaluación) orientadas a usuarios con discapacidad cognitiva o neurodivergencia, qué métricas de evaluación se emplean, y qué vacíos metodológicos persisten frente al sesgo de la literatura y la práctica hacia la accesibilidad sensorial/visual y frente a revisiones HCI/AT ya existentes?

### 1.3 Objeto de estudio

Síntesis de evidencia primaria sobre técnicas de IA aplicadas a artefactos y procesos de Ingeniería de Software (requisitos/diseño de interfaces adaptativas, personalización en runtime, testing/V&V/auditoría de accesibilidad) para perfiles cognitivos o neurodivergentes, con el fin de producir una taxonomía **condición × técnica de IA × fase SE × métrica de evaluación**, contrastada explícitamente con el sesgo visual/WCAG-duro y delimitada frente a intervenciones HCI/AT clínicas o educativas sin componente de proceso SE.

## 2. Palabras clave

Las palabras clave, el marco PICOCT y las queries se encuentran en [picoc.md](picoc.md).

## 3. Artículos de revisión de literatura relacionados con el tema de investigación

*(Mínimo 2 artículos de revisión; meta: 3 RSL. De no existir revisiones, mínimo 5 artículos originales con antigüedad menor a 5 años.)*

| Referencia bibliográfica (APA) | DOI / URL | Razón | PDF |
|--------------------------------|-----------|-------|-----|
| Chemnad, K., & Othman, A. (2024). Digital accessibility in the era of artificial intelligence—Bibliometric analysis and systematic review. *Frontiers in Artificial Intelligence, 7*, 1349668. | https://doi.org/10.3389/frai.2024.1349668 | RSL OA que documenta el **predominio de la discapacidad visual** en IA+accesibilidad digital y el vacío en TEA/cognitivo/motor; justifica el contraste “vs sesgo visual”. | `RSL/PDF/chemnad-othman-2024-digital-accessibility-ai.pdf` |
| Perry, N., et al. (2024). AI technology to support adaptive functioning in neurodevelopmental conditions in everyday environments: A systematic review. *npj Digital Medicine, 7*. | https://doi.org/10.1038/s41746-024-01355-7 | RSL clínica/asistiva sobre IA y condiciones del neurodesarrollo; delimita lo que **no** es el aporte SE (outcomes clínicos vs fases/métricas de ingeniería). | `RSL/PDF/perry-etal-2024-ai-neurodevelopmental.pdf` |
| Aljedaani, W., & Mollik, R. H. (2026). Large language models for web accessibility: A systematic literature review. In *Proceedings of the 23rd International Web for All Conference (W4A ’26)* (pp. 160–171). ACM. | https://doi.org/10.1145/3800424.3800452 (también https://arxiv.org/abs/2605.13873) | RSL de 38 estudios sobre LLM en accesibilidad web: WCAG como marco dominante y **poca consideración de COGA**; delimita la frontera GenAI+a11y web sin taxonomía **fase SE × métrica** para perfiles cognitivos/neurodivergentes. | `RSL/PDF/aljedaani-mollik-2026-llm-web-accessibility.pdf` |

**Queries Scopus para completar / localizar las RSL anteriores y afines:**

```
TITLE-ABS-KEY ( "digital accessibility" AND "artificial intelligence" AND "systematic review" ) AND PUBYEAR > 2022

TITLE-ABS-KEY ( ( "large language model*" OR LLM ) AND ( "web accessibility" OR WCAG OR COGA ) AND ( "systematic review" OR "systematic literature review" ) ) AND PUBYEAR > 2022

TITLE-ABS-KEY ( ( neurodiverg* OR "neurodevelopmental" ) AND ( "artificial intelligence" OR "machine learning" ) AND ( "systematic review" OR "scoping review" ) ) AND PUBYEAR > 2019
```

## 4. Estado del conocimiento y necesidad de una nueva RSL

La literatura reciente ya consolidó frentes que no deben confundirse con el aporte propuesto. Por un lado, Chemnad y Othman (2024) sintetizan aplicaciones de IA a la accesibilidad digital y evidencian un sesgo estructural hacia la discapacidad visual, junto con escasa cobertura de TEA, trastornos neurológicos y otras condiciones, además de débil adhesión a estándares. Por otro, Perry et al. (2024) revisan tecnologías de IA para el funcionamiento adaptativo en condiciones del neurodesarrollo en entornos cotidianos, con énfasis en outcomes clínicos y de apoyo, no en artefactos del ciclo de vida del software. En paralelo, Aljedaani y Mollik (2026) revisan sistemáticamente el uso de LLM en accesibilidad web (38 estudios) y muestran que las tareas predominantes son text-céntricas y estructuralmente explícitas, con WCAG como marco principal y **limitada consideración de las orientaciones de accesibilidad cognitiva (COGA)**, además de evaluaciones heterogéneas y poca participación directa de usuarios con discapacidad; tampoco construyen una taxonomía condición × técnica × **fase de ingeniería de software** × **métrica de evaluación de calidad/accesibilidad en el proceso**.

En consecuencia, persiste la necesidad de una RSL anclada en Ingeniería de Software que, partiendo de esas fronteras, organice cómo la IA interviene en diseño, personalización y, especialmente, verificación/evaluación para accesibilidad cognitiva y neurodivergencia, explicitando métricas (incluidas COGA frente al núcleo WCAG) y vacíos metodológicos. Dicha síntesis permitiría delimitar con rigor lo que ya cubren las revisiones de accesibilidad digital, de apoyo clínico/neurodesarrollo y de LLM+web, evitando un remake de esos frentes y alineando el aporte con el consenso del panel (`topic.md`).

*(≈ 290 palabras)*

## 5. Línea(s) de investigación de la UTP

La investigación propuesta responde, en primer lugar, a la línea **«Computación Científica»**, transversal a los programas de Ingeniería de la Facultad de Ingeniería de la UTP, cuyo objetivo es elaborar y desarrollar soluciones computacionales vinculadas a modelos y técnicas para analizar procesos de ingeniería. En ese sentido, al centrarse en modelos y técnicas de inteligencia artificial —y en su evaluación mediante métricas— aplicados al ciclo de vida del software inclusivo cognitivo, el estudio se alinea de modo directo con dicha línea.

De forma complementaria, se vincula con la línea **«Aplicaciones TIC, electrónicas, robóticas y de telecomunicaciones para la competitividad, salud, educación y seguridad ciudadana»**, orientada a desarrollar aplicaciones informáticas que mejoren la competitividad y el bienestar en ámbitos como educación y servicios ciudadanos. La accesibilidad cognitiva de plataformas digitales —relevante para educación inclusiva y gobierno digital accesible en el Perú— sitúa la síntesis propuesta como insumo técnico para ese propósito, sin desplazar el núcleo metodológico de la Computación Científica y de la Ingeniería de Software.

## 6. Competencias de la carrera

El tema se relaciona, en primer término, con la competencia de **desarrollo de software**, en tanto exige dominio del ciclo de vida y de los entregables por fase (requisitos, diseño, verificación y evaluación), precisamente el eje analítico de la RSL. Asimismo, conecta con **tecnologías de vanguardia** y el área de **desarrollo con IA**, al examinar cómo la inteligencia artificial —incluido el GenAI— se incorpora a prácticas y herramientas de ingeniería. De igual modo, dialoga con el **desarrollo frontend** y el análisis de sistemas, dado el peso de interfaces adaptativas, usabilidad y modelado de requisitos de accesibilidad cognitiva. Finalmente, la lectura de métricas y evidencia cuantitativa/cualitativa de evaluación refuerza habilidades afines al análisis de datos para la toma de decisiones de calidad del producto, sin reducir el trabajo a Business Intelligence operativo.

## 7. Título tentativo de la RSL

Inteligencia artificial en el ciclo de vida del software para accesibilidad cognitiva y neurodivergencia: técnicas, fases de ingeniería y métricas de evaluación — una revisión sistemática de la literatura
