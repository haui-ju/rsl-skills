# Debate del marco — 2026-09-28-6-PICO

**Fecha:** 2026-09-28 · **Modo:** completo (ampliación de los cuatro bloques) · **Base:** `2026-09-28-5-PICO` · **Agentes:** critico-rsl, defensor-rsl, redaccion-rsl

## Decisión del usuario (no se debate)

- Ampliar el vocabulario de forma moderada, siempre alineado al tema, porque la query de Scopus con los filtros de inclusión devuelve poco más de 100 registros.
- Sin cambios en el marco, las preguntas de investigación, las keywords del paper ni los filtros de inclusión.

## Vocabulario externo

IEEE 2019 no codifica los perfiles clínicos de la población. Se verificaron en los Medical Subject Headings (MeSH) de la National Library of Medicine, mediante su API pública (`id.nlm.nih.gov/mesh/lookup`), sin descargar el tesauro completo ni actualizar Graphify: la verificación término a término basta, y Scopus indexa los descriptores MeSH en los registros de MEDLINE. Los términos siguen siendo de tipo Libre; la justificación cita el descriptor y su identificador.

## Propuesta inicial

19 términos nuevos: en P, `ASD`, `"Down syndrome"`, `"learning disorder*"`, `"learning difficult*"` y `dyscalculia`; en I, `GPT`, `"neural networks"`, `"computer vision"`, `chatbot`, `"conversational agents"` y `"text simplification"`; en C, `accessible`, `"inclusive design"` y `"universal design"`; en O, `"accessibility evaluation"`, `"accessibility testing"`, `"user study"`, `comprehension` y `understandability`.

## Posiciones

**critico-rsl**
- `accessible` vacía el bloque C: recupera «publicly accessible dataset» y deja pasar la clasificación clínica del autismo con aprendizaje profundo.
- `ASD` apenas suma recall, porque los resúmenes desarrollan la sigla, y añade ruido (Auto-Sklearn, comunicación interauricular).
- `"neural networks"` es redundante con `"deep learning"`; `"computer vision"` trae detección por imagen.
- Mantener GPT, los agentes conversacionales, la simplificación de textos, el diseño inclusivo y universal y todo el bloque O.
- `"universal design"` trae el diseño universal para el aprendizaje: excluir las intervenciones pedagógicas sin artefacto de software evaluado.

**defensor-rsl**
- Los añadidos de P e I son los que más recall útil aportan; los agentes conversacionales y la simplificación de textos se nombran sin «artificial intelligence».
- `"computer vision"` cubre el reconocimiento de emociones y de mirada en autismo; el bloque P contiene su sesgo hacia la ceguera.
- `accessible` es el término más débil del paquete.
- Propone `"cognitive impairment"`, `"assistive technology"` y `"adaptive user interface"`.

**redaccion-rsl**
- Ocho ajustes de las justificaciones: definir MeSH y W3C, retirar un superlativo sin respaldo, desarrollar «estudios solo cognitivos» y completar las filas de MeSH. Se aplicaron literalmente, salvo el que describía `ASD`, que se retiró.

## Decisiones

| Punto | Decisión | Motivo |
|---|---|---|
| `accessible` | Se sustituye por `"accessible design"` y `"accessible interface"` | Ambos agentes lo ven débil; las frases cerradas conservan el enfoque sin comodín |
| `ASD` | Se retira | Recall casi nulo y ruido documentado |
| `"neural networks"` | Se retira y pasa a descriptores excluidos | Redundante con `"deep learning"` y `"machine learning"` |
| `"computer vision"` | Se mantiene | Descriptor IEEE; el criterio de exclusión de estudios de solo diagnóstico contiene el ruido |
| `"adaptive user interface"` | Se añade al bloque I | El tema incluye la personalización de interfaces |
| `"cognitive impairment"`, `"assistive technology"` | Se rechazan | El alcance ya los excluye (deterioro cognitivo y demencia; tecnología de apoyo ajena al proceso de software) |
| Diseño universal para el aprendizaje | Nuevo criterio de exclusión | Evita estudios pedagógicos sin artefacto de software |
| Comodines de IEEE Xplore | 10, el límite | Los nuevos comodines están solo en P |

Resultado: 71 términos (antes 52). La validación con las tres revisiones conocidas no cambia: Chemnad y Othman (2024) sigue sin el bloque O y Perry et al. (2024) sin el bloque C.

## Queda para el usuario

- Ejecutar la nueva query en Scopus y comparar el número de registros con los de la versión 5; si el aumento es excesivo, medir el aporte de `comprehension` y `"computer vision"` quitándolos uno a uno.
- Decidir si los bloques C y O, unidos con AND, deben pasar a ser opcionales, ya que la validación muestra que recortan revisiones afines.
- Formar el conjunto de control de 3 a 5 estudios primarios para la validación.
