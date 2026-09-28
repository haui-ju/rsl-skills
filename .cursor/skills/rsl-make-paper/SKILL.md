---
name: rsl-make-paper
description: >-
  Builds a new version docs/[short-title]/paper/<fecha>/paper-borrador.md — the
  rich draft of the RSL paper, section by section according to paper/paper.yml
  (on = improve, rewrite = regenerate from scratch; frozen/off ones are copied
  from the previous version). Uses topic.md, informe, picoc.md, Graphify theme memory,
  RSL/MD and global/examples. Use when the user says rsl-make-paper. Does NOT
  launch the 4-agent debate (that is rsl-polish-paper); only citas-rsl at the end.
---

# rsl-make-paper

## Goal

Write the **rich draft** of the RSL paper as a new version `paper/<fecha>/paper-borrador.md`. Single proposer flow (maximal useful expansion). The 4-agent debate belongs to **`rsl-polish-paper`**; here only **`citas-rsl`** runs at the end.

Each section of `paper/paper.yml` has one state:

| State | Meaning (user) | What this skill does on `paper-borrador.md` |
|---|---|---|
| `frozen` | "Está bien, no lo toques" | Copy byte for byte; never edit. |
| `on` | "Revísalo y mejóralo" | Keep the previous text as the base (structure, argument, voice). Fix errors, fill gaps, add evidence, improve continuity. Do **not** rewrite from scratch. |
| `rewrite` | "Reescríbelo / replantéalo" | Ignore the previous text; regenerate from the sources (topic, informe, picoc, RSL/MD, graph). Structure and argument may change. |
| `off` | "No está activo" | Do nothing; the section does not appear. |

An `on` section with no previous text is shown as `reescribir (nueva)` and is generated from the sources. Titles, groups and `depends_on` live in `paper/paper.shadow.yml`.

## Paths (required)

```text
docs/[titulo-breve]/
  topic.md · informe-polish.md · picoc(-polish).md     (insumos internos)
  RSL/PDF/  RSL/MD/                                     (corpus)
  RSL/seleccion/  RSL/extraccion/                       (los prepara el USUARIO: queries, validación, PRISMA; solo lectura)
  graphify-out/                                         (memoria del tema — solo lookup)
  paper/
    paper.yml            (lo edita el usuario: frozen / on / rewrite / off + formato)
    paper.shadow.yml     (títulos, grupos, depends_on, formato avanzado)
    paper.state.jsonc    (hashes y versiones — lo gestiona paper:status; no editar)
    <fecha>/
      paper-borrador.md  (THIS skill)
      paper-polish.md    (rsl-polish-paper)
      paper-debate.md    (rsl-polish-paper)
global/examples/*.md       (papers reales de referencia — estructura/presentación)
global/citation-style/     (APA7.md · IEEE.md)
```

Same theme → **reuse** the existing folder. Never edit previous version folders.

## Invoke

```text
Usa rsl-make-paper sobre docs/ia-inclusion-cognitiva-software/
```

## Procedure (required)

1. Resolve `docs/[titulo-breve]/`. If `paper/paper.yml` is missing → `pnpm -s paper:status docs/<slug> --init` (crea `paper.yml` + `paper.shadow.yml`; Introducción on, resto off). If `paper:status` says the old format → `--migrate`.
2. Run `pnpm -s paper:status docs/<slug>` first: if **A mejorar** and **A reescribir** are both empty (everything frozen/off), do not create a version; report STALE / BLOCKED and stop. Otherwise `pnpm -s paper:status docs/<slug> --new-version` → creates `paper/<fecha>/` copying the previous version and prints the table. Work **only** on the sections listed in **A mejorar (on)** — improve — and **A reescribir (rewrite)** — regenerate. Report **STALE** (frozen whose sources changed: do not touch, the user decides) and **BLOCKED** (missing data, e.g. `RSL/extraccion`: do not generate, say what is missing).
3. Read internal inputs: ficha (`informe-polish.md` | `informe.md`), marco (`picoc-polish.md` | `picoc.md`), `topic.md`; and the **frozen** sections of the new version as context (coherence; never edit them).
4. **Graphify first:**
   ```bash
   graphify query "<pregunta>" --graph docs/[titulo-breve]/graphify-out/graph.json
   graphify query "<sección a escribir>" --graph global/examples/graphify-out/graph.json
   rg "^#" global/examples/*.md
   ```
   Theme graph + `RSL/MD/` locators for evidence (no full PDFs). Examples: only headings and a short passage per section to imitate **structure and presentation**; never copy their text, data or citations. Our writing must exceed their quality. Do not refresh Graphify.
5. Write each section to improve or rewrite **between its markers** (create them if the section is new; keep the order of `paper.shadow.yml`):
   ```markdown
   <!-- paper:section id=contexto -->
   ### Contexto
   …
   <!-- /paper:section -->
   ```
   Headings follow the merged format (`formato` of `paper.yml` + `format` of `paper.shadow.yml`, as printed by `paper:status`): groups as H2 numbered per `format.numbering` (`## I. Introducción`, `## II. Metodología`…; letters A–E for sections if `subsection_letters`), sections as H3, deeper numbered subsections as H4 (`#### 1.1 …`) allowed in the draft. `## Referencias` is derived (all works cited in any section).
6. Content rules per group:
   - **Introducción:** template below (maximal useful expansion).
   - **Metodología:** from `picoc(-polish).md` — its RQs, keywords, tables and the 3 queries **as they are** (no new terms or RQ). PRISMA / selection only from `RSL/seleccion/` (user data); never invent counts.
   - **Resultados / Discusión / Conclusión:** only from `RSL/extraccion/` (user data), by RQ or by theme per `format.results_by`.
   - **Abstract / Resumen:** only when the content sections exist; keywords from `picoc` (`format.keywords_from`).
7. **`citas-rsl`** (single agent) on the improved and rewritten sections: `pnpm -s paper:status docs/<slug> --cites paper/<fecha>/paper-borrador.md` + agent fixes until PASS or justified `PENDIENTE`.
8. `pnpm -s paper:status docs/<slug> --update borrador`.
9. Chat: version path, improved / rewritten / copied / stale / blocked sections, sources, citas result, next step `Usa rsl-polish-paper sobre docs/[titulo-breve]/`.

## Writing style (required)

Write in the language of `formato.idioma` (default `es`: Spanish **académico-profesional**); headings (Introducción/Introduction, Referencias/References…) in that language too; connectors; cohesive paragraphs. Citations per `formato.citas` (paper.yml) following `global/citation-style/<STYLE>.md`.

**Hard rules:** never put `topic.md`, `informe.md`, "panel", "GO_con_cambios", skill names or repo paths in the visible text. Never invent DOI/findings. Cite only what topic/ficha/Graphify/MD support.

**Términos técnicos:** reuse the descriptors of the search table of `picoc(-polish).md`; a new EN term → `pnpm -s thesaurus:check "…"` (`playbooks/vocabulario-controlado.md`). In Metodología declare that the strings use IEEE controlled vocabulary + free terms.

**Preguntas:** the general question of `picoc(-polish).md` is the problemática (§ El problema); its per-component sub-questions structure Objetivo de la RSL (one specific objective per RQ) and Organización. Do not invent RQ.

### Maximal useful expansion (draft)

For each anchor SLR: *qué cubre*, *n/DOI*, *qué no cubre* (= own gap). Pull findings from Graphify / `RSL/MD` locators (`[PDF p.N]`). Frontiers (Xu, Paiva, norms, W3C) in-text when they delimit the topic. No stubs; every extra paragraph adds citation, delimitation, metric, ethic or SE-process detail.

### Problemática = pregunta

The problemática is an **interrogative** and is stated explicitly in El problema (subsection 2.4 in the draft).

## Introducción template (draft)

```markdown
<!-- paper:section id=encabezado -->
# [Título de la RSL]
<!-- /paper:section -->

## I. Introducción

<!-- paper:section id=contexto -->
### Contexto
#### 1.1 Definiciones generales
#### 1.2 Lo que se sabe del tema hasta la fecha
#### 1.3 Situación actual y disputas
<!-- /paper:section -->

<!-- paper:section id=problema -->
### El problema
#### 2.1 Tendencias o nuevas perspectivas
#### 2.2 Discrepancias existentes
#### 2.3 Vacíos de conocimiento
#### 2.4 Contraste: situación actual vs situación deseada (pregunta reformulada)
<!-- /paper:section -->

<!-- paper:section id=justificacion -->
### Justificación
#### 3.1 Justificación de la elección del tema
#### 3.2 Utilidad de los resultados de la revisión
#### 3.3 Necesidad de una RSL
<!-- /paper:section -->

<!-- paper:section id=objetivo-rsl -->
### Objetivo de la RSL
<!-- /paper:section -->

<!-- paper:section id=organizacion -->
### Organización del contenido de la revisión
<!-- /paper:section -->

<!-- paper:section id=referencias -->
## Referencias
<!-- /paper:section -->
```

## Forbidden

- Launching the 4 polish agents (only `citas-rsl`).
- Editing previous versions, frozen or off sections, the states in `paper.yml`, or `paper.shadow.yml` / `paper.state.jsonc` by hand.
- Generating BLOCKED sections or inventing PRISMA counts / results (the selection is the user's work).
- Deleting or renaming section markers.
- Overwriting `informe*.md` / `picoc*.md` / `topic.md`.
- Inventing citations or DOI; citing internal files in the paper body.
- Copying text, data or citations from `global/examples/`.
- Dumping full PDFs when Graphify / `RSL/MD` exists; refreshing Graphify.
- Thin stub sections "to polish later".
