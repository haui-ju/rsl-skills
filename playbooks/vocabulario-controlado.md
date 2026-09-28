# Vocabulario controlado IEEE — PICO / PICOC / PICOCT / keywords / queries

Fuente de verdad para **cualquier** término de búsqueda que produzca una skill `rsl-*`: IEEE Thesaurus 2019 (`global/thesaurus/IEEE.pdf`, ~10.4k términos), indexado en `global/thesaurus/graphify-out/graph.json`.

Objetivo: términos **fieles al tema** (descriptor oficial + sinónimos oficiales) y **cero descriptores inventados**. Lo que IEEE no tiene se declara como término libre, al final y con justificación.

## Marco configurado y versiones

- El marco se configura en `docs/<slug>/paper/paper.yml` → `formato.marco: PICO | PICOC | PICOCT`. Si el usuario no dijo nada, es **PICOCT**.
- Cada generación es una versión trazable: `docs/<slug>/picoc/<AAAA-MM-DD>[-n]-<MARCO>/picoc.md` + `picoc-debate.md`. Solo la skill **`rsl-picoc`** crea versiones; las anteriores no se editan.
- Si el usuario cambia `formato.marco`, el último picoc queda **DESFASADO** y hay que correr `rsl-picoc` (crea `<hoy>-<MARCO>/`).
- El informe **no** contiene tablas ni queries: su sección 2 solo enlaza a la última versión. El paper siempre lee la última versión (`pnpm -s picoc:latest docs/<slug>`).
- El cribado (inclusión/exclusión, tipo de documento) y la extracción **no** van en el picoc: los define el usuario después.

## Herramientas

| Uso | Comando |
|-----|---------|
| Marco configurado + último picoc (OK · DESFASADO · FALTA) | `pnpm -s picoc:latest docs/<slug>` |
| Validar muchos términos en **una** llamada (preferido) | `pnpm -s thesaurus:check "term 1" "term 2" …` → tabla Markdown |
| Ficha completa de un término | `pnpm -s thesaurus:lookup "term"` |
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

## Reglas obligatorias

### Pregunta general

- Es la **misma** problemática (`¿…?`) de la ficha: copia literal de la § 1.2 de `informe-polish.md` (o `informe.md`). El paper también la copia. Si hay que cambiarla, se cambia en la ficha y se regenera el picoc.

### R1 — Relevancia: toda keyword nace del tema

- Cada componente se **traza a una frase concreta** del título, la problemática o el objeto de estudio → la columna `Justificación` cita esa frase entre comillas (“…”) y explica por qué entran sus keywords.
- Prohibido: términos genéricos que no salen del tema, NT/RT añadidos “porque existen” en el thesaurus, cercanos no equivalentes.
- Un descriptor IEEE solo entra si representa **ese** concepto del tema; si es más amplio o desviado, va a *Descriptores revisados y excluidos* con motivo.

### R2 — Tabla de componentes 1:1 con las queries

- La **tabla de componentes** tiene **exactamente una fila por componente del marco**, en su orden (PICOCT: P, I, C, O, Co, T). Todos entran; el usuario decide después cuál quitar.
- Columna `Keywords`: cada término **escrito exactamente como va en la query**, entre backticks, separados por ` · ` (p. ej. `` `autism` · `"autism spectrum"` · `neurodivers*` ``).
- Cada componente distinto de T es un bloque `( … OR … )` unido con `AND`, en el orden de la tabla, en **cada** query (Scopus, Web of Science, IEEE Xplore), con exactamente esos términos. Ni más ni menos.
- **T** no tiene términos: su fila indica el rango de años (`2020–2026`) y en las queries es el filtro de año (`PUBYEAR > 2019 AND PUBYEAR < 2027` · `PY=(2020-2026)` · IEEE Xplore: filtro de la interfaz anotado bajo la query). Sin filtros de tipo de documento (`DOCTYPE`, `DT`).
- Con PICO o PICOC no hay filtro de año.
- IEEE Xplore admite **10 comodines** por búsqueda: reservar `*` para las variantes morfológicas del bloque P y usar frases sin comodín en el resto (Scopus y Web of Science ya recuperan los plurales de las frases).

### R3 — Una pregunta por componente

- La pregunta general se descompone en **exactamente 1 RQ por componente** del marco, interrogativa, que reutiliza el concepto de su fila, con su **dato a extraer**. Se numeran RQ1…RQn en el orden del marco y la tabla de componentes enlaza su RQ.
- Juntas cubren toda la pregunta general; ninguna introduce conceptos fuera del marco.
- Códigos de componente: `P` Población · `I` Intervención · `C` Comparación · `O` Resultado · `Co` Contexto · `T` Tiempo.

### KW — Palabras clave ES / EN

- Cada fila: español · inglés · componente · tipo · página IEEE · justificación.
- El inglés es el **descriptor IEEE preferido** (con su página). Primero van todas las filas IEEE.
- Los términos **libres** solo pueden ir **al final** de la tabla, cada uno con una justificación breve (por qué no hay descriptor IEEE).
- Todo descriptor declarado en la tabla de componentes aparece en Palabras clave.

## Procedimiento (lo ejecuta `rsl-picoc`)

1. `pnpm -s picoc:latest docs/<slug>` → marco configurado (por defecto PICOCT).
2. Copiar la pregunta general de la § 1.2 de la ficha. Leer título y objeto (`topic.md`, ficha).

| Marco | Componentes |
|-------|-------------|
| PICO | P, I, C, O |
| PICOC | P, I, C, O, Co |
| PICOCT | P, I, C, O, Co, T |

   En Ingeniería de Software, P suele ser el perfil de usuario o el artefacto; I, la técnica; C, la alternativa o el sesgo a contrastar; O, métricas/calidad; Co, fases del ciclo de vida; T, la ventana temporal.
3. Conceptos por componente, cada uno con su frase de origen en el tema (R1).
4. Candidatos EN (2–4 por concepto: singular, guion, siglas) → **una** llamada `pnpm -s thesaurus:check …`.
5. Clasificar por estado; expandir con criterio: UF al `OR` si nacen del tema; NT solo si están en el alcance; RT nunca automático; BT nunca en la query.
6. Redactar las RQ por componente (R3).
7. Construir las 3 queries con los **mismos** bloques (R2). Truncamiento (`*`) solo en términos libres o plurales.
8. `pnpm -s picoc:lint docs/<slug>` → PASS antes de entregar.

## Plantilla `picoc/<fecha>-<MARCO>/picoc.md`

````markdown
# Marco de búsqueda — [título corto]

**Marco:** PICOCT · **Vocabulario:** IEEE Thesaurus 2019 + términos libres · **Tema:** [título completo]

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
| T | Ventana temporal | RQ6 | `2020–2026` | — | “…”; filtro de año en las 3 bases |

## Palabras clave

| Español | Inglés | Comp. | Tipo | Pág. IEEE | Justificación |
|---------|--------|-------|------|-----------|---------------|
| trastorno del espectro autista | Autism | P | IEEE | p.35 | — |
| … (todas las IEEE primero) | | | | | |
| neurodivergencia | neurodiversity | P | Libre | — | IEEE 2019 no tiene descriptor |

## Query Scopus

```text
TITLE-ABS-KEY (
  ( <bloque P> )
  AND ( <bloque I> )
  AND ( <bloque C> )
  AND ( <bloque O> )
  AND ( <bloque Co> )
)
AND PUBYEAR > 2019 AND PUBYEAR < 2027
```

## Query Web of Science

```text
ALL=( <bloque P> ) AND ALL=( <bloque I> ) AND ALL=( <bloque C> ) AND ALL=( <bloque O> ) AND ALL=( <bloque Co> )
AND PY=(2020-2026)
```

## Query IEEE Xplore

```text
( "IEEE Terms":"Autism" OR "autism spectrum" OR neurodivers* ) AND ( … ) AND ( … ) AND ( … ) AND ( … )
```

Filtro de año en la interfaz: 2020–2026.

## Búsqueda auxiliar — localizar revisiones afines (opcional; no es el corpus primario)

## Descriptores revisados y excluidos
````

- `Tipo` (palabras clave) ∈ `IEEE` · `IEEE (USE desde "…")` · `Libre`.
- IEEE Xplore: descriptores preferidos como `"IEEE Terms":"<Descriptor>"`; libres como texto. Mismos términos por bloque que Scopus y WoS.

## Prohibido

- Presentar como “descriptor IEEE” un término que `thesaurus:check` marcó LIBRE.
- Usar un término **no preferido** como descriptor principal cuando existe su USE.
- Justificación sin cita del tema, o sustituir un libre por un *cercano* no equivalente.
- Tabla y query con términos distintos (R2), en cualquiera de las 3 bases; componentes del marco sin fila.
- Secciones de cribado, extracción, “T — Filtros” o “Términos libres” aparte; filtros `DOCTYPE`/`DT`.
- Términos libres antes que los IEEE en Palabras clave, o sin justificación.
- Pregunta general distinta de la § 1.2 de la ficha; marco distinto del de `paper.yml`.
- Componentes sin RQ, o más de una por componente (R3).
- Tablas, keywords o queries dentro del informe (solo el enlace en la sección 2).
- Editar versiones anteriores de `picoc/`; entregar sin `picoc:lint` PASS; validar términos “de memoria”.
