# Debate del marco de búsqueda — 2026-09-28 · PICOCT

- **Marco:** PICOCT (`formato.marco` de `config.yml`, valor por defecto).
- **Versión base:** `picoc.md` anterior, sin versionar (estructura antigua con cribado de C y O y filtros de T); se eliminó del tema y queda en el historial de git.
- **Cambios de estructura pedidos por el usuario:**
  - los 6 componentes van en la tabla y P, I, C, O y Co entran como bloques AND;
  - T pasa a ser solo el filtro 2020–2026;
  - sin cribado ni tipo de documento;
  - palabras clave IEEE primero y libres al final;
  - pregunta general copiada literal de la § 1.2 de `informe-polish.md`.
- **Agentes:** `critico-rsl`, `defensor-rsl`, `redaccion-rsl`.

## critico-rsl (riesgo alto → resuelto en parte)

- **Bloque C en AND.** Exige nombrar la discapacidad sensorial o WCAG, por lo que excluye los estudios solo cognitivos. Eso vuelve circular la RQ3: el sesgo que quiere medir lo fabricaría la propia búsqueda.
  - Propone añadir `accessibility` a C.
  - Pide correr la query en Scopus con y sin C y anotar los dos conteos.
- **Términos con ruido:**
  - `"cognitive impairment*"`: trae el corpus de demencia y contradice la exclusión de *Dementia*;
  - `COGA`: es también un estudio genético del alcoholismo;
  - `blind`: recupera ensayos doble ciego;
  - `personaliz*`: recupera medicina y aprendizaje personalizados.
- **Huecos morfológicos:** faltan `autistic`, `deaf`, `"visually impaired"`, `"hearing impaired"` y `"low vision"`.
- **IEEE Xplore:** la query tenía 17 comodines y el límite es 10, así que no se podía ejecutar.
- **Bloque O:** `measurement` y `metric*` casi no filtran. Faltan métricas de accesibilidad.
- **Bloque Co:** *Automatic testing* (p.36) cubre la verificación automatizada. `"code generation"` cubre el rol generador de la GenAI.

## defensor-rsl

- Defiende que el cruce de los cinco bloques no existe en revisiones afines:
  - Chemnad y Othman (2024) no tienen bloque de ingeniería de software ni de perfil cognitivo;
  - Paiva et al. (2021) cubren hasta 2019 y no incluyen IA;
  - Teixeira et al. (2024) no incluyen IA;
  - Zastudil et al. (2025) trabajan en educación en computación.
- Coincide con el crítico en `autistic`, `neurodevelopmental` y en quitar `blind`.
- Añade candidatos:
  - `"developmental disabilit*"`;
  - términos de estándares en C, que quedan subsumidos por `accessibility`;
  - `"plain language"` y `"easy-to-read"` para la legibilidad cognitiva;
  - `"accessibility requirement"`, `"web development"` y `"app development"`, tomados de las cadenas de Teixeira et al. (2024);
  - `ChatGPT`.
- Pide mantener *Neural networks* fuera, midiendo su costo de recall, y conservar `AI` como sigla.

## redaccion-rsl (FAIL → corregido)

- Siglas sin definir en las RQ: TEA, TDAH, GenAI, LLM, WCAG, COGA y V&V.
- Notación de trabajo: «vs», barras usadas como «o», «runtime», «celda vacía», «anti-medicalización».
- Jerga del tesauro sin explicar: UF, USE, NT.
- Viñetas telegráficas en los descriptores excluidos.
- La pregunta general no se tocó, porque es copia literal de la ficha.

## Decisiones

| Bloque | Cambio | Motivo |
|--------|--------|--------|
| P | + `autistic`, `neurodevelopmental`, `"developmental disabilit*"` | Consenso crítico y defensor; todos son términos libres validados |
| P | − `"cognitive impairment*"`, − `COGA` | Ruido clínico y sigla ambigua; `"cognitive accessibility"` cubre COGA |
| I | `LLM*` → `LLM` · `LLMs`; + `ChatGPT` | Libera comodines; ChatGPT cubre estudios GenAI que no nombran los LLM |
| C | − `blind`, − `"web accessibility"`; + `deaf`, `"visually impaired"`, `"low vision"`, `"hearing impaired"`, `accessibility`; sin comodines | Menos ruido y cobertura de las variantes. `accessibility` evita que C exija nombrar una discapacidad sensorial |
| O | `metric*` → `metric` · `metrics`; + `"accessibility metric"`, `"plain language"`, `"easy-to-read"` | Métricas de la RQ4 y legibilidad cognitiva; libera comodines |
| Co | `personaliz*` → `"runtime personalization"` · `"runtime adaptation"`; + `"automatic testing"` (IEEE p.36), `"automated testing"`, `"code generation"`, `"accessibility requirement"`, `"web development"`, `"app development"`; sin comodines | Énfasis del tema en la verificación; frases del objeto de estudio |
| T | 2020–2026 como `PUBYEAR > 2019 AND PUBYEAR < 2027` · `PY=(2020-2026)` · filtro de interfaz | Sin tipo de documento (lo decide el usuario) |
| IEEE Xplore | 8 comodines, todos en P | Límite de 10 por búsqueda |
| Excluidos | + *Standards* (p.509), `COGA` suelta, `blind`, `personaliz*`, `"cognitive impairment*"` | Motivos en la sección del picoc |
| No adoptado | *Neural networks*, `"System Usability Scale"`, `"NASA-TLX"`, `"text simplification"` | *Deep learning* y `usability` los cubren; la simplificación de texto es una técnica, no una métrica |

## Pendiente para el usuario

- Correr la query de Scopus con y sin el bloque C, y con y sin el bloque O, y decidir si alguno se retira. El marco los mantiene porque así se decidió, pero el crítico advierte que el corpus final puede quedar en decenas de registros.
- El encabezado del paper (frozen) tiene una Problemática distinta de la pregunta general de la § 1.2 (`picoc:lint` lo avisa). Para alinearlo hay que ponerlo en `on`.
