# Vocabulario controlado IEEE — PICO / PICOC / PICOCT / keywords / queries

Fuente de verdad para **cualquier** término de búsqueda que produzca una skill `rsl-*`: IEEE Thesaurus 2019 (`global/thesaurus/IEEE.pdf`, ~10.4k términos), indexado en `global/thesaurus/graphify-out/graph.json`.

Objetivo: términos **fieles al tema** (descriptor oficial + sinónimos oficiales) y **cero descriptores inventados**. Lo que IEEE no tiene se declara como término libre, con justificación.

Salida: archivo **aparte** `docs/[titulo-breve]/picoc.md` (borrador, `rsl-make-report`) → `picoc-polish.md` (pulido, `rsl-polish-report`). El informe **no** contiene tablas ni queries: su sección 2 solo enlaza a este archivo.

## Herramientas

| Uso | Comando |
|-----|---------|
| Validar muchos términos en **una** llamada (preferido) | `pnpm -s thesaurus:check "term 1" "term 2" …` → tabla Markdown |
| Ficha completa de un término | `pnpm -s thesaurus:lookup "term"` |
| Vecinos con relación + página | `graphify explain "Term" --graph global/thesaurus/graphify-out/graph.json` |
| Verificar el archivo del marco (reglas 1:1, RQ, IEEE) | `pnpm -s picoc:lint docs/<slug>/picoc.md` → debe dar PASS |

Si `global/thesaurus/ieee-thesaurus.json` o el grafo no existen → pedir `Usa rsl-bootstrap` (o `pnpm run bootstrap`). **No** continuar inventando descriptores.

## Estados que devuelve `thesaurus:check`

| Estado | Qué hacer |
|--------|-----------|
| **IEEE preferido** | Usar el descriptor tal cual. Sus **UF** son sinónimos oficiales → candidatos al mismo bloque `OR` (si nacen del tema). |
| **IEEE no preferido → USE** | Sustituir por el descriptor de la columna *Descriptor IEEE*; el término original queda como sinónimo. |
| **LIBRE (sin descriptor IEEE)** | Mantener como término libre **marcado** y justificado (concepto posterior a 2019, estándar W3C, término clínico…). |
| *Cercanos* | Pistas para explorar, **no** equivalentes. Solo reemplazan a un término libre si el significado es el mismo, y se justifica. |

## Reglas obligatorias

### R1 — Relevancia: toda keyword nace del tema

- Cada término de búsqueda se **traza a una frase concreta** del título, la problemática o el objeto de estudio (`topic.md` / informe) → columna `Origen en el tema` (cita corta en cursiva).
- Prohibido: términos genéricos que no salen del tema, NT/RT añadidos “porque existen” en el thesaurus, cercanos no equivalentes.
- Un descriptor IEEE solo entra si representa **ese** concepto del tema; si es más amplio o desviado, va a *Descriptores revisados y excluidos* con motivo.

### R2 — 1:1 tabla ↔ query

- La **tabla de búsqueda** contiene solo los componentes que van a la query. Columna `Términos en la query`: cada término **escrito exactamente como va en la query**, entre backticks, separados por ` · ` (p. ej. `` `autism` · `"autism spectrum"` · `neurodivers*` ``). Columna `N` = número de términos.
- Cada bloque `( … OR … )` de **cada** query (Scopus, Web of Science, IEEE Xplore) tiene **exactamente** esos N términos, con el mismo orden de bloques que las filas. En la query no puede haber un término que no esté en la tabla, ni al revés.
- Los componentes que **no** van a la query (típicamente C y O) van en una tabla aparte **Cribado / extracción**. T = filtros (año, tipo de documento), no términos.

### R3 — Una pregunta por componente

- La **pregunta general** es la problemática (`¿…?`) del tema/informe.
- Se descompone en **exactamente 1 sub-pregunta por componente** del marco (P, I, C, O, Co, T según corresponda), interrogativa, que reutiliza el concepto y las palabras de su fila.
- Juntas cubren toda la pregunta general; ninguna introduce conceptos fuera del marco. Cada una indica el **dato a extraer** para responderla.
- Códigos de componente: `P` Población · `I` Intervención · `C` Comparación · `O` Resultado · `Co` Contexto · `T` Tiempo / tipo de estudio.

## Procedimiento

1. Leer título, problemática y objeto (`topic.md`, informe). Elegir marco:

| Marco | Cuándo | Componentes |
|-------|--------|-------------|
| PICO | base (intervención sobre población) | P, I, C, O |
| PICOC | el contexto (p. ej. fases SE) delimita el corpus | + Co |
| PICOCT | además se declara ventana temporal / tipo de documento | + T |

   En Ingeniería de Software, P suele ser el perfil de usuario o el artefacto; I, la técnica; O, métricas/calidad; Co, fases del ciclo de vida.
2. Conceptos por componente, cada uno con su **origen en el tema** (R1).
3. Candidatos EN (2–4 por concepto: singular, guion, siglas) → **una** llamada `pnpm -s thesaurus:check …`.
4. Clasificar por estado; expandir con criterio: UF al `OR` si nacen del tema; NT solo si están en el alcance; RT nunca automático; BT nunca en la query.
5. Decidir qué componentes van a la query (normalmente P, I, Co) y cuáles a cribado/extracción (normalmente C, O).
6. Redactar la pregunta general y las sub-preguntas por componente (R3).
7. Construir las 3 queries con los **mismos** bloques (R2). Truncamiento (`*`) solo en términos libres o plurales.
8. `pnpm -s picoc:lint docs/<slug>/picoc.md` → PASS antes de entregar.

## Plantilla `picoc.md` / `picoc-polish.md`

````markdown
# Marco de búsqueda — [título corto]

**Marco:** PICOCT · **Vocabulario:** IEEE Thesaurus 2019 + términos libres · **Tema:** [título completo]

## Pregunta general (problemática)

¿…?

## Preguntas por componente

| Comp. | Pregunta (RQ) | Dato a extraer |
|-------|---------------|----------------|
| P | ¿…? | … |
| I | ¿…? | … |
| C | ¿…? | … |
| O | ¿…? | … |
| Co | ¿…? | … |
| T | ¿…? | … |

## Tabla de búsqueda (1:1 con las queries)

| Comp. | Concepto (ES) | Origen en el tema | Términos en la query | N | Descriptor IEEE (pág.) | Libres (justificación) |
|-------|---------------|-------------------|----------------------|---|------------------------|------------------------|
| P | … | *…* | `autism` · `"autism spectrum"` · `neurodivers*` | 3 | Autism (p.35) | `neurodivers*`: sin descriptor IEEE |

## Cribado / extracción (no entran a la query)

| Comp. | Concepto (ES) | Origen en el tema | Descriptores / términos | Uso |
|-------|---------------|-------------------|-------------------------|-----|

## T — Filtros

| Base | Filtro |
|------|--------|

## Palabras clave

| Español | Inglés | Tipo | Pág. IEEE |
|---------|--------|------|-----------|

## Query Scopus

```text
TITLE-ABS-KEY (
  ( <bloque 1> )
  AND
  ( <bloque 2> )
)
AND PUBYEAR > 2019
AND ( LIMIT-TO ( DOCTYPE , "ar" ) OR LIMIT-TO ( DOCTYPE , "cp" ) )
```

## Query Web of Science

```text
(ALL=( <bloque 1> )) AND ALL=( <bloque 2> )
AND PY=(2020-2026) AND DT=(Article OR Proceedings Paper)
```

## Query IEEE Xplore

```text
( "IEEE Terms":"Autism" OR "autism spectrum" OR neurodivers* ) AND ( … )
```

## Descriptores revisados y excluidos

## Términos libres (sin descriptor IEEE)
````

- `Tipo` (palabras clave) ∈ `IEEE` · `IEEE (USE desde "…")` · `Libre`. Toda palabra clave debe aparecer en la tabla de búsqueda o en la de cribado.
- IEEE Xplore: descriptores preferidos como `"IEEE Terms":"<Descriptor>"`; libres como texto. Mismo N por bloque que Scopus y WoS.
- Filtros de IEEE Xplore (año, Journals/Conferences) se aplican en la interfaz y se anotan en *T — Filtros*.

## Prohibido

- Presentar como “descriptor IEEE” un término que `thesaurus:check` marcó LIBRE.
- Usar un término **no preferido** como descriptor principal cuando existe su USE.
- Términos sin `Origen en el tema`, o sustituir un libre por un *cercano* no equivalente.
- Tabla y query con términos distintos o distinto N (R2), en cualquiera de las 3 bases.
- Componentes sin sub-pregunta, o más de una por componente (R3).
- Tablas PICOC, keywords o queries dentro del informe (solo el enlace en la sección 2).
- Entregar sin `picoc:lint` PASS; validar términos “de memoria”.
