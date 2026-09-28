# Debate del polish — paper 2026-09-28-3

## 2026-09-28 · polish (versión nueva desde 2026-09-28-2)

**Secciones trabajadas (on):** objetivo-rsl, marco-pico, palabras-clave, ecuacion-busqueda, criterios-seleccion, seleccion-prisma (y el párrafo de apertura de II).
**Frozen copiadas sin cambios:** encabezado, contexto, problema, justificacion, organizacion.
**Agentes:** critico-rsl (con tabla Sustento, R8), defensor-rsl, impacto-social-rsl, redaccion-rsl (tabla Hilo, R7), citas-rsl.
**Motivo de la pasada:** quitar la apelación a «el lector» (la voz es la de la revisión) y sostener con citas verificadas las afirmaciones importantes del método.

### Decisiones clave

| Tema | Crítica o propuesta | Decisión |
|---|---|---|
| «El lector» en II.E | Frase «decisiones que el lector debe poder revisar» (crítico, defensor) | Reescrita como «cada una debe poder auditarse». Regla nueva en R1 del playbook y FAIL en `redaccion:lint`. |
| Repetibilidad (apertura II) | El crítico objeta que «debe llegar a los mismos estudios» excede la fuente | Atenuado a «debería llegar, en lo esencial» y citado a Kitchenham y Charters (2007, p. vi): síntesis no sesgada y repetible «en cierto grado». |
| Protocolo previo | Sin cita (Sustento) | Citado Kitchenham y Charters (2007, p. 12). |
| PICOC frente al esquema clínico | El crítico sostiene que el marco clínico ya es PICO, con comparación | Rechazado tras verificar la fuente: Kitchenham y Charters (2007, pp. 10–11) describen las guías médicas con tres puntos de vista (población, intervención, resultados) y PICOC como su extensión con comparación y contexto. Se añade la cita y «recomiendan» pasa a «retoman». |
| Palabras clave y tesauro | Decisión sin respaldo (Sustento) | Citado Kitchenham y Charters (2007, p. 14): sinónimos por componente y términos de indexación de las bases. La cita para AND/OR se omite para no sobrecitar (defensor). |
| Bloque de comparación con *accessibility* | Los estudios cognitivos que no usen esos términos quedan fuera (crítico) | Declarado como límite asumido de la búsqueda. |
| Campos asimétricos Scopus / WoS | Recuentos no comparables (crítico) | Se declara que la asimetría impide comparar recuentos pero no altera la selección. Sin fuente: decisión propia. |
| Filtros fuera de las ecuaciones | Sin cita | Citado Kitchenham y Charters (2007, p. 16): búsqueda transparente y replicable. |
| Criterios fijados en el protocolo | Sin cita | Citado Kitchenham y Charters (2007, p. 18). |
| Etapas de selección y PRISMA | Cita de Page et al. mal ubicada (defensor) | Kitchenham y Charters (2007, p. 19) para las etapas; Page et al. (2021, p. 1) movida a la frase de reporte transparente. |
| Rótulos diagnósticos | Contradicción: «solo como términos de búsqueda» frente a la RQ1 (crítico, impacto) | Se usan como términos de búsqueda y se reportan tal como los declara cada estudio, sin reclasificar. |
| Salvaguardas éticas | «el método permite comprobar» promete de más; dicotomía déficit/diferencia; consentimiento con discapacidad intelectual; CE4 parafraseado sin su condición (impacto, crítico) | Protocolo que fija salvaguardas en dos etapas; tercera opción «sin postura declarada»; dato sensible; asentimiento con apoyos y comité de ética; CE4 con «sin una fase del ciclo de vida». |
| Objetivo 4 | Sigla CI definida en el Contexto (redacción) | «qué puede verificarse en la CI». |
| Página de Kitchenham para la repetibilidad | citas-rsl: p. 1 no contiene la frase | Corregido a p. vi (glosario), verificado en el texto fuente. |

### Pendientes (no se resuelven sin fuente o sin decisión del usuario)

- **Elección de Scopus y Web of Science:** sin fuente verificada; queda como decisión propia sin justificar en el texto.
- **CI1, adopción masiva de la IA generativa (2023):** afirmación sin fuente, pero el criterio es literal del picoc; se corrige solo con rsl-picoc.
- **Ventana 2020–2026:** no se explica por qué empieza en 2020 (depende del picoc).
- **Sesgo de los datos de entrenamiento** (impacto): registrar composición e idioma de los datos de cada estudio como campo de extracción; propuesta para la fase de extracción.
- **País del estudio** (impacto): concretar qué sesgo se busca (por ejemplo, América Latina frente al norte global).
- **Título (R6):** 28 palabras con subtítulo en cascada; encabezado frozen.
- **Introducción:** frozen; cuando se descongele, más breve y centrada en lo esencial, con conectores y un propósito claro por párrafo.

### Redacción y citas

- `redaccion-rsl`: **PASS** (tabla Hilo con todos los párrafos OK; ninguna apelación a «el lector»).
- `redaccion:lint`: 0 FAIL; 20 WARN, todos en el encabezado frozen y en la pregunta general literal.
- `citas-rsl`: **PASS** tras corregir p. 1 → p. vi. `--cites`: OK, 10 referencias.
- Se corrigió un fallo de `paper:status --cites`, que no reconocía las citas con página («(Autor, 2007, p. 12)», «Autor (2007, p. 1)»); regresión en QA D18.
