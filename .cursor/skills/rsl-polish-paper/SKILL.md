---
name: rsl-polish-paper
description: >-
  Polishes the latest docs/[short-title]/paper/<fecha>/paper-borrador.md with 4
  agents + citas-rsl and writes paper-polish.md and paper-debate.md in that
  version, section by section according to paper/paper.yml (only on
  sections; frozen ones copied; stale ones reported). Use when the
  user says rsl-polish-paper.
---

# rsl-polish-paper

## Goal

Polish the latest **`paper-borrador.md`** via 4-agent debate + `citas-rsl` → **`paper-polish.md`** (clean, ready to present) + **`paper-debate.md`** (trace), in the same version folder. Only sections marked **`on`** in `paper/paper.yml` are polished; **`frozen`** ones are copied byte for byte and **`off`** ones are omitted. Do not create from scratch (`rsl-make-paper`).

## Paths

```text
docs/[titulo-breve]/paper/
  paper.yml (on | frozen | off + formato) · paper.shadow.yml (títulos, depends_on) · paper.state.jsonc (no editar)
  <fecha>/paper-borrador.md → paper-polish.md + paper-debate.md
topic/informe*/picoc* = insumo interno (NUNCA citar en el paper)
global/examples/ (estructura) · global/citation-style/ (APA7 | IEEE)
```

If the latest version **already has** a finished polish (`paper:status` shows it in `paper.state.jsonc`), first run `pnpm -s paper:status docs/<slug> --new-version` (copies draft and polish) and work in the new version. Never edit previous versions.

## Division of labor

| | `paper-borrador.md` | `paper-polish.md` |
|---|---------------------|-------------------|
| Rol | Bodega rica (make se explaya) | Documento limpio, compacto |
| Sub-subsecciones (`#### 1.1`) | Permitidas | **Prohibidas** |
| Estructura | Grupos H2 numerados + secciones H3 | Igual (según `format`), solo H2/H3 |
| Extensión | Larga | **Masticado**: lo central; párrafos cortos |

## Fluidez y anti-"texto IA" (required — revisor de forma)

| Regla | Detalle |
|-------|---------|
| **Lo central primero** | Por bloque: 1 idea núcleo + evidencia mínima. Cortar listas de matices, acrónimos encadenados y relleno. |
| **Párrafos cortos** | Ideal **2–4 oraciones**; máx. ~5. |
| **Contexto** | ~4 párrafos **enlazados**: WCAG/COGA → acotar objeto → tejer las anclas en un hilo → tensiones que preparan El problema. |
| **Continuidad** | Cada párrafo abre con **conector real** (*En ese marco*, *A partir de*, *En consecuencia*, *Ese recorte exige*, *Así*, *De ahí que*, *A ello se suma*, *Por eso*, *El vacío, entonces*, *Con ese marco*…). |
| **Sin eco cíclico** | Anclas: una mención fuerte en Contexto; después solo si aportan avance. |
| **Prohibido "sabor IA"** | Enumeraciones disfrazadas, tríos forzados, guiones largos en serie, verbos genéricos, meta-comentarios. |

Coherence with frozen sections: read them as context; if a polished section contradicts a frozen one, report it in chat (do not edit the frozen one).

## Output structure (`paper-polish.md`)

Language per `formato.idioma` (default `es`; body and headings in that language, the Abstract/Resumen per `formato.resumen`). Headings per `formato` of `paper.yml` + `format` of `paper.shadow.yml` (defaults: roman numbering, letters A–E, APA 7). Every section between its markers, in the order of `paper.shadow.yml`:

```markdown
<!-- paper:section id=encabezado -->
# [Título de la RSL]

**Tema.** … (enunciado corto)

**Problemática.** ¿…?

**Objetivo.** … (una o dos oraciones)
<!-- /paper:section -->

## I. Introducción

<!-- paper:section id=contexto -->
### Contexto
(3–5 párrafos cortos)
<!-- /paper:section -->

<!-- paper:section id=problema -->
### El problema
(3–4 párrafos: nace de lo anterior → pregunta → vacío → contraste)
<!-- /paper:section -->

<!-- paper:section id=justificacion -->
### Justificación
(2–4 párrafos)
<!-- /paper:section -->

<!-- paper:section id=objetivo-rsl -->
### Objetivo de la RSL
(2–3 párrafos)
<!-- /paper:section -->

<!-- paper:section id=organizacion -->
### Organización del contenido de la revisión
(1 párrafo, coherente con los grupos on de paper.yml)
<!-- /paper:section -->

## II. Metodología            ← solo si hay secciones on en el grupo
<!-- paper:section id=marco-pico -->
### A. Pregunta PICO y sus componentes
<!-- /paper:section -->
…

<!-- paper:section id=referencias -->
## Referencias
<!-- /paper:section -->
```

- Metodología: tables and queries from `picoc(-polish).md` as they are; PRISMA only from `RSL/seleccion/` (user data).
- Resultados / Discusión / Conclusión: only from `RSL/extraccion/` (user data), per `format.results_by`.
- Presentation (tables, figures, order within a group) imitating the recurring structure of `global/examples/` (`graphify query … --graph global/examples/graphify-out/graph.json`); never copy their text.

### Citas y referencias

- Style per `formato.citas` (paper.yml) → `global/citation-style/APA7.md` | `IEEE.md`.
- **Referencias = all works cited** in the paper (anchors, frontiers, W3C norms, laws), rebuilt every run; never frozen.
- **Prohibido:** `topic.md`, panel, GO_*, skills, paths.

### Problemática = pregunta

The **Problemática** header must be a research **question**.

## Procedure

1. `pnpm -s paper:status docs/<slug>` (create a new version if the latest is already polished). Work only on **A regenerar**; report **STALE** and **BLOCKED** without touching them.
2. Read the latest `paper-borrador.md` + ficha + `picoc(-polish).md` + `topic.md` (internal) + frozen sections (context).
3. Graphify lookup (theme + examples; no refresh).
4. Parallel on the sections to regenerate only: `critico-rsl`, `defensor-rsl`, `impacto-social-rsl`, `viabilidad-negocio-rsl`.
   Prompt: sections to polish + frozen neighbors as context + format; problemática-pregunta; masticado; continuidad; no sabor lista-IA / internal files.
5. Brief synthesis in chat.
6. Write the polished sections between their markers in `paper-polish.md` (copy frozen ones unchanged; rebuild Referencias).
7. **`citas-rsl`**: `pnpm -s paper:status docs/<slug> --cites` + agent fixes until PASS or justified `PENDIENTE`.
8. Append to `paper-debate.md` a block for this run: date, regenerated sections, Mermaid + turnos, **Forma/gramática pass-fail** (3–5 corrections; if fail → rewrite before delivering) and **Citas pass-fail** (citas-rsl table). Do not delete earlier blocks.
9. `pnpm -s paper:status docs/<slug> --update polish` (must end without FAIL).
10. List changes, stale / blocked sections, PDF/Graphify gaps. Suggest marking validated sections as `frozen` in `paper/paper.yml`.

## Forbidden

- Remake from scratch; editing previous versions, `paper-borrador.md`, informe, picoc or topic without request.
- Editing frozen sections (only citation re-render if `formato.citas` changed), changing the states in `paper.yml`, or editing `paper.shadow.yml` / `paper.state.jsonc`.
- Generating off or BLOCKED sections; inventing PRISMA counts or results.
- Deleting markers; `#### 1.1` subsections in the polish.
- Problemática afirmativa (debe ser ¿…?).
- Párrafos-pared o Contexto que vuelque todo el estado del arte.
- Raw debate inside paper-polish.md.
- Inventing DOI; refreshing Graphify without request; copying text from `global/examples/`.
