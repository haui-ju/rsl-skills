# Vocabulario controlado IEEE — marco de búsqueda (PICO, PIO, PICOC, PICOCT…), keywords y queries

Fuente de verdad para **cualquier** término de búsqueda que produzca una skill `rsl-*`: IEEE Thesaurus 2019 (`global/thesaurus/IEEE.pdf`, ~10.4k términos), indexado en `global/thesaurus/graphify-out/graph.json`.

Objetivo: términos **fieles al tema** (descriptor oficial + sinónimos oficiales) y **cero descriptores inventados**. Lo que IEEE no tiene se declara como término libre, al final y con justificación.

## Marco configurado y versiones

- El marco se configura en `docs/<slug>/config.yml` → `formato.marco`. Es **libre**: lo que decida el usuario (PICO, PIO, PICOC, PICOCT, PICOS… o una lista `[P, I, O]`). Si no dijo nada, es **PICOCT**.
- Letras válidas: `P` población · `I` intervención · `C` comparación · `O` resultado · `T` tiempo · `S` diseño de estudio. La **segunda** `C` es `Co` contexto (PICOC = P, I, C, O, Co). Una letra fuera de esta lista es **ERROR**: los scripts terminan con exit 1 y ninguna skill continúa hasta que el usuario la corrija.
- Cada generación es una versión trazable: `docs/<slug>/picoc/<AAAA-MM-DD>[-n]-<MARCO>/picoc.md` + `picoc-debate.md`. Solo la skill **`rsl-picoc`** crea versiones; las anteriores no se editan.
- Si el usuario cambia `formato.marco`, el último picoc queda **DESFASADO** y hay que correr `rsl-picoc` (crea `<hoy>-<MARCO>/`).
- `rsl-picoc` solo escribe la versión nueva de `picoc/`; lee el informe, `topic.md`, `config.yml` y el paper, pero nunca los modifica.
- El informe **no** contiene tablas ni queries: su sección 2 solo enlaza a la última versión; ese enlace lo escriben `rsl-make-report` y `rsl-polish-report`. El paper siempre lee la última versión (`pnpm -s picoc:latest docs/<slug>`).
- El picoc fija las **keywords del paper** (regla KY: 5 o 6, las más relevantes) y termina con los **criterios de inclusión y exclusión** (regla CR): qué debe cumplir un artículo para revisarse y qué lo descarta. La extracción de datos **no** va en el picoc.
- En las versiones nuevas, cada criterio se identifica de forma explícita y consecutiva: inclusión `CI1`, `CI2`, …, `CIn`; exclusión `CE1`, `CE2`, …, `CEn`. «Documentos duplicados», DOI/título repetido y cualquier otra deduplicación no son criterios `CE`: `cribado:prepare` los elimina como operación técnica y los informa por separado en PRISMA.

## Herramientas

| Uso | Comando |
|-----|---------|
| Marco configurado + último picoc (OK · DESFASADO · FALTA) | `pnpm -s picoc:latest docs/<slug>` |
| Validar muchos términos en **una** llamada (preferido) | `pnpm -s thesaurus:check "term 1" "term 2" …` → tabla Markdown |
| Ficha completa de un término | `pnpm -s thesaurus:lookup "term"` |
| Concepto ACM CCS 2012 (ruta, BT, NT) | `pnpm -s thesaurus:acm "term"` |
| Vecinos con relación + página | `graphify explain "Term" --graph global/thesaurus/graphify-out/graph.json` |
| Verificar el último picoc (marco, pregunta general, 1:1, RQ, IEEE) | `pnpm -s picoc:lint docs/<slug>` → debe dar PASS |

Si `global/thesaurus/ieee-thesaurus.json` o el grafo no existen → pedir `Usa rsl-bootstrap` (o `pnpm run bootstrap`). **No** continuar inventando descriptores.

## Estados que devuelve `thesaurus:check`

| Estado | Qué hacer |
|--------|-----------|
| **IEEE preferido** | Usar el descriptor tal cual. Sus **UF** son sinónimos oficiales → candidatos al mismo bloque `OR` (si nacen del tema). |
| **IEEE no preferido → USE** | Sustituir por el descriptor de la columna *Descriptor IEEE*; el término original queda como sinónimo. |
| **LIBRE (sin descriptor IEEE)** | Mantener como término libre, al final de Palabras clave y con justificación breve (concepto posterior a 2019, estándar W3C, término clínico…). |
| *Cercanos* | Pistas para explorar, **no** equivalentes. Solo reemplazan a un término libre si el significado es el mismo, y se justifica. |
| *ACM CCS 2012* | Concepto de la clasificación de ACM (`global/thesaurus/acm-ccs/`), con su ruta. Respalda un término **libre** de informática que IEEE 2019 no tiene (p. ej. *Accessibility*); el tipo sigue siendo `Libre` y la justificación cita «ACM CCS: <concepto>». Sus NT son candidatos a términos del bloque si nacen del tema. |

**Población clínica:** si IEEE no tiene el perfil (TDAH, dislexia, síndrome de Down…), verificarlo en MeSH (`https://id.nlm.nih.gov/mesh/lookup/descriptor?label=<término>&match=exact`) y citar en la justificación el descriptor y su identificador (p. ej. «MeSH *Dyslexia* (D004410)»); el tipo sigue siendo `Libre`.

### VOC — Vocabularios citados

- La línea `**Vocabulario:**` de la cabecera cita, con autor y año del catálogo `global/bibliography/bibliography.md`, **cada** vocabulario que el picoc usa, y solo esos: IEEE Thesaurus (IEEE, 2019) siempre; la ACM Computing Classification System (ACM, 2012) si alguna justificación cita «ACM CCS»; los Medical Subject Headings (NLM, 2026) si alguna cita «MeSH».
- Todo término libre de informática con concepto ACM CCS (exacto o de nombre casi idéntico, p. ej. *User studies* para `"user study"`, comprobado con `pnpm -s thesaurus:acm`) lo cita en su justificación.
- El paper hereda esta lista: la nota bajo la tabla de palabras clave cita los mismos vocabularios (`paper:status --picoc-sync` lo verifica).

## Reglas obligatorias

### Pregunta general

- Es la **misma** problemática (`¿…?`) de la ficha: copia literal de la § 1.2 de `informe-polish.md` (o `informe.md`). El paper también la copia. Si hay que cambiarla, se cambia en la ficha y se regenera el picoc.

### R1 — Relevancia: toda keyword nace del tema

- Cada componente se **traza a una frase concreta** del título, la problemática o el objeto de estudio → la columna `Justificación` cita esa frase entre comillas (“…”) y explica por qué entran sus keywords.
- Prohibido: términos genéricos que no salen del tema, NT/RT añadidos “porque existen” en el thesaurus, cercanos no equivalentes.
- Un descriptor IEEE solo entra si representa **ese** concepto del tema; si es más amplio o desviado, va a *Descriptores revisados y excluidos* con motivo.

### R2 — Tabla de componentes 1:1 con las queries

- La **tabla de componentes** tiene **exactamente una fila por componente del marco**, en su orden (p. ej. PICOCT: P, I, C, O, Co, T · PIO: P, I, O). Todos entran; el usuario decide después cuál quitar.
- Columna `Keywords`: cada término **escrito exactamente como va en la query**, entre backticks, separados por ` · ` (p. ej. `` `autism` · `"autism spectrum"` · `neurodivers*` ``).
- Cada componente distinto de T es un bloque `( … OR … )` unido con `AND`, en el orden de la tabla, en **cada** query (Scopus, Web of Science, IEEE Xplore), con exactamente esos términos. Ni más ni menos.
- **T** no tiene términos: su fila indica el rango de años (`2021–2026`), que es el mismo periodo de CR. `S` (diseño de estudio) es un bloque más de la query.
- **Filtros de inclusión en cada query**, haya o no T: los límites que fija CR (periodo, tipo de documento, idioma y acceso abierto) van después de los bloques y coinciden con CR. Ejemplo (artículos de revista, 2021–2026, inglés o español, acceso abierto):
  - Scopus: `PUBYEAR > 2020 AND PUBYEAR < 2027 AND (LIMIT-TO(DOCTYPE,"ar")) AND (LIMIT-TO(LANGUAGE,"English") OR LIMIT-TO(LANGUAGE,"Spanish")) AND (LIMIT-TO(OA,"all"))`.
  - Web of Science: `AND PY=(2021-2026) AND DT=(Article) AND LA=(English OR Spanish)`; el acceso abierto no tiene etiqueta de campo y va como filtro de la interfaz anotado bajo la query.
  - IEEE Xplore: todos los filtros de la interfaz, anotados bajo la query.
  Estos filtros son límites de la búsqueda: se reportan completos en el paper y, en PRISMA, los registros que quitan van en *registros eliminados antes del cribado* (`playbooks/estandares-rsl.md`).
- **Máximo 100 keywords** en total, sumando todos los bloques de la tabla (lo comprueba `picoc:lint`). Si una ampliación lo supera, primero se quitan las redundantes (variantes que la base ya recupera, como `"machine-learning"` frente a `"machine learning"`) y después las de menor evidencia en el cribado.
- IEEE Xplore admite **10 comodines** por búsqueda: reservar `*` para las variantes morfológicas del bloque P y usar frases sin comodín en el resto (Scopus y Web of Science ya recuperan los plurales de las frases).

### R3 — Una pregunta por componente

- La pregunta general se descompone en **exactamente 1 RQ por componente** del marco, interrogativa, que reutiliza el concepto de su fila, con su **dato a extraer**. Se numeran RQ1…RQn en el orden del marco y la tabla de componentes enlaza su RQ.
- Juntas cubren toda la pregunta general; ninguna introduce conceptos fuera del marco.

### KW — Palabras clave ES / EN

- Cada fila: español · inglés · componente · tipo · página IEEE · justificación.
- El inglés es el **descriptor IEEE preferido** (con su página). Primero van todas las filas IEEE.
- Los términos **libres** solo pueden ir **al final** de la tabla, cada uno con una justificación breve (por qué no hay descriptor IEEE).
- Todo descriptor declarado en la tabla de componentes aparece en Palabras clave.

### KY — Keywords del paper

- Sección `## Keywords` justo después de `## Palabras clave`: tabla `Keyword (EN) | Palabra clave (ES) | Comp.` con **5 o 6 filas, nunca más**. Son las que van tal cual al Abstract y al Resumen del paper; viven en el picoc porque cambian con él.
- Es la unión de los componentes, pero solo lo más relevante: al menos una keyword por componente del marco (salvo T) y ninguna repetida.
- Cada keyword es un término inglés de la tabla Palabras clave, con su mismo componente; el español es su traducción exacta.
- Preferir los términos que identifican el aporte y el vacío (lo que teclearía quien busca esta revisión) frente a los genéricos que ya dice el título.

### CR — Criterios de inclusión y exclusión

- Última sección del picoc: `## Criterios de inclusión y exclusión` con dos listas de viñetas, `### Inclusión` (qué se acepta para revisar un artículo) y `### Exclusión` (qué lo descarta).
- Criterios **breves**: uno por viñeta, verificable al leer título, resumen o texto completo, de 25 palabras como máximo. Al menos 2 por lista. Por ejemplo: «Artículos en inglés o español».
- La inclusión fija siempre el **periodo**, el **idioma**, el **tipo de documento** (p. ej. artículos de revista revisados por pares) y el **acceso abierto** (por defecto; solo se omite si el usuario lo pide). Si el marco tiene T, el periodo es el mismo que T. Sin indicación del usuario, el periodo son los 5 últimos años completos más el año en curso.
- Los criterios salen del tema: del alcance y las exclusiones de `topic.md` y de los componentes del marco. No se inventan restricciones que el tema no pide; tampoco se repite una query en forma de criterio.
- Una exclusión no es solo la negación de una inclusión: nombra el caso concreto que se descarta (duplicados, sin texto completo, literatura gris, estudios fuera del alcance del tema).

## Procedimiento (lo ejecuta `rsl-picoc`)

1. `pnpm -s picoc:latest docs/<slug>` → marco configurado (por defecto PICOCT) y sus componentes.
2. Copiar la pregunta general de la § 1.2 de la ficha. Leer título y objeto (`topic.md`, ficha).
   En Ingeniería de Software, P suele ser el perfil de usuario o el artefacto; I, la técnica; C, la alternativa o el sesgo a contrastar; O, métricas/calidad; Co, fases del ciclo de vida; T, la ventana temporal; S, el tipo de estudio.
3. Conceptos por componente, cada uno con su frase de origen en el tema (R1).
4. Candidatos EN (2–4 por concepto: singular, guion, siglas) → **una** llamada `pnpm -s thesaurus:check …`.
5. Clasificar por estado; expandir con criterio: UF al `OR` si nacen del tema; NT solo si están en el alcance; RT nunca automático; BT nunca en la query.
6. Redactar las RQ por componente (R3).
7. Construir las 3 queries con los **mismos** bloques y los filtros de CR (R2). Truncamiento (`*`) solo en términos libres o plurales.
   Validar la búsqueda (Kitchenham y Charters, 2007, p. 14): listar en `## Validación de la búsqueda` 3–5 estudios relevantes ya conocidos (de `RSL/`, del informe o del tema) con su DOI, y marcar si la query de Scopus debería recuperarlos (sus términos aparecen en título, resumen o palabras clave). El usuario confirma la recuperación real en la base; si un estudio no se recuperaría, revisar los bloques.
8. Elegir las 5 o 6 keywords del paper (KY) y redactar los criterios de inclusión y exclusión (CR) desde el alcance y las exclusiones de `topic.md` y el marco.
9. `pnpm -s picoc:lint docs/<slug>` → OK antes de entregar.

## Plantilla `picoc/<fecha>-<MARCO>/picoc.md`

````markdown
# Marco de búsqueda — [título corto]

**Marco:** PICOCT · **Vocabulario:** IEEE Thesaurus (IEEE, 2019) y términos libres; los de informática se contrastan con la ACM Computing Classification System (ACM, 2012) y los perfiles clínicos con los Medical Subject Headings (NLM, 2026) — solo los que se usen (regla VOC) · **Tema:** [título completo]

## Pregunta general (problemática)

¿… (copia literal de la § 1.2 de la ficha) …?

## Preguntas por componente

| RQ | Comp. | Pregunta (RQ) | Dato a extraer |
|----|-------|---------------|----------------|
| RQ1 | P | ¿…? | … |
| RQ2 | I | ¿…? | … |
| RQ3 | C | ¿…? | … |
| RQ4 | O | ¿…? | … |
| RQ5 | Co | ¿…? | … |
| RQ6 | T | ¿…? | … |

## Tabla de componentes (1:1 con las queries)

| Comp. | Concepto | RQ | Keywords | Descriptor IEEE (pág.) | Justificación |
|-------|----------|----|----------|------------------------|---------------|
| P | … | RQ1 | `autism` · `"autism spectrum"` · `neurodivers*` | Autism (p.35) | Nace de “usuarios con … neurodivergencia”; `neurodivers*` sin descriptor IEEE |
| … | … | … | … | … | … |
| T | Ventana temporal | RQ6 | `2021–2026` | — | “…”; filtro de año en las 3 bases |

## Palabras clave

| Español | Inglés | Comp. | Tipo | Pág. IEEE | Justificación |
|---------|--------|-------|------|-----------|---------------|
| trastorno del espectro autista | Autism | P | IEEE | p.35 | — |
| … (todas las IEEE primero) | | | | | |
| neurodivergencia | neurodiversity | P | Libre | — | IEEE 2019 no tiene descriptor |

## Keywords

| Keyword (EN) | Palabra clave (ES) | Comp. |
|--------------|--------------------|-------|
| Autism | trastorno del espectro autista | P |
| … (5 o 6 filas, al menos una por componente salvo T) | | |

## Query Scopus

```text
TITLE-ABS-KEY (
  ( <bloque P> )
  AND ( <bloque I> )
  AND ( <bloque C> )
  AND ( <bloque O> )
  AND ( <bloque Co> )
)
AND PUBYEAR > 2020 AND PUBYEAR < 2027
AND ( LIMIT-TO ( DOCTYPE , "ar" ) )
AND ( LIMIT-TO ( LANGUAGE , "English" ) OR LIMIT-TO ( LANGUAGE , "Spanish" ) )
AND ( LIMIT-TO ( OA , "all" ) )
```

## Query Web of Science

```text
ALL=( <bloque P> ) AND ALL=( <bloque I> ) AND ALL=( <bloque C> ) AND ALL=( <bloque O> ) AND ALL=( <bloque Co> )
AND PY=(2021-2026) AND DT=(Article) AND LA=(English OR Spanish)
```

Filtro de la interfaz: Open Access.

## Query IEEE Xplore

```text
( "IEEE Terms":"Autism" OR "autism spectrum" OR neurodivers* ) AND ( … ) AND ( … ) AND ( … ) AND ( … )
```

Filtros de la interfaz: 2021–2026 · Journals · Open Access; el filtro que la interfaz no ofrezca se aplica en el cribado.

## Validación de la búsqueda

| Estudio conocido | DOI | Fuente | ¿Lo recupera la query de Scopus? |
|---|---|---|---|
| Autor et al. (año) | 10.… | `RSL/…` o informe | Sí: “…” en el título / No: falta el término … |

## Búsqueda auxiliar — localizar revisiones afines (opcional; no es el corpus primario)

## Descriptores revisados y excluidos

## Criterios de inclusión y exclusión

### Inclusión

- Artículos publicados entre 2021 y 2026 (T).
- Artículos en inglés o español.
- Artículos de revista revisados por pares.
- Artículos de acceso abierto.
- … (un criterio breve por viñeta, salido del tema)

### Exclusión

- Duplicados entre bases de datos.
- Estudios sin texto completo disponible.
- … (casos concretos que el tema deja fuera)
````

- `Tipo` (palabras clave) ∈ `IEEE` · `IEEE (USE desde "…")` · `Libre`.
- IEEE Xplore: descriptores preferidos como `"IEEE Terms":"<Descriptor>"`; libres como texto. Mismos términos por bloque que Scopus y WoS.

## Prohibido

- Presentar como “descriptor IEEE” un término que `thesaurus:check` marcó LIBRE.
- Usar la ACM CCS o MeSH en las justificaciones sin citarlos en la cabecera, o citar en la cabecera un vocabulario que no se usa (VOC).
- Usar un término **no preferido** como descriptor principal cuando existe su USE.
- Justificación sin cita del tema, o sustituir un libre por un *cercano* no equivalente.
- Tabla y query con términos distintos (R2), en cualquiera de las 3 bases; componentes del marco sin fila.
- Secciones de extracción, “Cribado”, “T — Filtros” o “Términos libres” aparte (el cribado son los criterios de CR); filtros de la query distintos de CR, o CR sin acceso abierto (salvo que el usuario lo pida).
- Términos libres antes que los IEEE en Palabras clave, o sin justificación.
- Pregunta general distinta de la § 1.2 de la ficha; marco distinto del de `config.yml`.
- Componentes sin RQ, o más de una por componente (R3).
- Tablas, keywords o queries dentro del informe (solo el enlace en la sección 2).
- Editar versiones anteriores de `picoc/`; entregar sin `picoc:lint` PASS; validar términos “de memoria”.
