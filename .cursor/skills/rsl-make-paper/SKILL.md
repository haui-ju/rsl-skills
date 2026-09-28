---
name: rsl-make-paper
description: >-
  Builds a new version docs/[short-title]/paper/<fecha>/paper-borrador.md — the
  rich draft of the RSL paper, section by section according to config.yml
  (on = improve, rewrite = regenerate from scratch; frozen/off ones are copied
  from the previous version). Uses topic.md, informe, the latest picoc/<fecha>-<MARCO>/picoc.md, Graphify theme memory,
  RSL/MD and global/examples. Use when the user says rsl-make-paper. Does NOT
  launch the 4-agent debate (that is rsl-polish-paper); only citas-rsl at the end.
---

# rsl-make-paper

Writes the **rich draft** as a new version `paper/<fecha>/paper-borrador.md`. Single proposer; the 4-agent debate belongs to `rsl-polish-paper`; here only `citas-rsl` runs at the end.

| State in `config.yml` | What this skill does |
|---|---|
| `frozen` | Copy byte for byte; never edit. |
| `on` | Improve the previous text (fix, fill gaps, add evidence, continuity); no rewrite from scratch. No previous text → generated (`reescribir (nueva)`). |
| `rewrite` | Ignore the previous text; regenerate from the sources. |
| `off` | Absent. |

```text
docs/[titulo-breve]/
  topic.md · informe-polish.md | informe.md · picoc/<último>/picoc.md   (internal inputs)
  RSL/MD/ (corpus) · RSL/seleccion/ + RSL/extraccion/ (user data, read only) · graphify-out/ (lookup only)
  config.yml (user) · paper/paper.shadow.yml (titles, groups, depends_on) · paper/paper.state.jsonc (script only)
  paper/<fecha>/paper-borrador.md (THIS skill) · paper-polish.md + paper-debate.md (rsl-polish-paper)
global/examples/ (structure reference) · global/citation-style/<STYLE>.md
```

Invoke: `Usa rsl-make-paper sobre docs/<slug>/`.

## Procedure

1. No `config.yml` → `pnpm -s paper:status docs/<slug> --init`; old `paper/paper.yml` or old format → `--migrate`. Any `ERROR` (e.g. unknown letter in `formato.marco`) → stop and report it.
2. `pnpm -s paper:status docs/<slug> --new-version`. It creates `paper/<fecha>/` (copy of the previous version) only if something is `on`/`rewrite`; otherwise it says so → report STALE / BLOCKED and stop. Work **only** on **A mejorar** and **A reescribir**. **STALE** frozen sections: do not touch (the user decides). **BLOCKED**: do not generate; say what is missing (`WARN picoc …` → suggest `Usa rsl-picoc sobre docs/<slug>/`; `RSL/extraccion` → user data).
3. Inputs, read once: ficha, the latest picoc (path printed by `paper:status`), `topic.md`, and the frozen sections of the new version (coherence only).
4. Evidence, graph first (no full PDFs, no refresh):
   - `graphify query "<tema de la sección>" --graph docs/<slug>/graphify-out/graph.json` + `RSL/MD/` locators `[PDF p.N]`.
   - One `graphify query "<sección>" --graph global/examples/graphify-out/graph.json` per section for structure and presentation only; never copy text, data or citations. Our writing must exceed them.
5. Write each section **between its markers** (create them if new; order of `paper.shadow.yml`). Headings follow the merged format printed by `paper:status`: groups as numbered H2 (`## I. Introducción`), sections as H3, H4 subsections allowed in the draft; `## Referencias` is derived.
6. Content per group:
   - **Introducción:** template below. For each anchor SLR: what it covers, n/DOI, what it does not cover (= gap). Every extra paragraph adds citation, delimitation, metric, ethics or SE-process detail; no stubs.
   - **Preguntas:** the picoc general question = problemática = § 1.2 (verbatim in the encabezado and in El problema 2.4, as an interrogative); its RQs give one specific objective each in Objetivo de la RSL and structure Organización. No new RQ.
   - **Metodología:** tables, RQs, keywords and queries of the latest picoc **as they are**. `marco-pico` names the configured framework with its components in words (e.g. "Se adoptó el marco PIO (población, intervención y resultado)…") and gives one row per component with its RQ; title from `paper:status`. States that the strings mix IEEE controlled vocabulary and free terms. `criterios-seleccion` = the inclusion and exclusion criteria of the latest picoc, as they are (two bullet lists or a two-column table). PRISMA counts only from `RSL/seleccion/`; never invent counts.
   - **Resultados / Discusión / Conclusión:** only from `RSL/extraccion/`, by RQ or theme (`format.results_by`).
   - **Abstract / Resumen:** only when content sections exist; keywords from the picoc.
7. `citas-rsl` on the worked sections only: `pnpm -s paper:status docs/<slug> --cites paper/<fecha>/paper-borrador.md` + its fixes until PASS or justified `PENDIENTE`.
8. `pnpm -s redaccion:lint docs/<slug>/paper/<fecha>/paper-borrador.md` → 0 FAIL (WARN allowed in the draft).
9. `pnpm -s paper:status docs/<slug> --update borrador`.
10. Chat: copied sections and the citas result, then the Cierre line.

## Writing

Language of `formato.idioma` (default Spanish académico-profesional, headings included); citations per `formato.citas` and `global/citation-style/<STYLE>.md`; form per `playbooks/redaccion-academica.md` (in the draft R1, R2 and R5 already apply; R3/R4 warnings are solved in the polish). New EN technical term → `pnpm -s thesaurus:check "…"`. Never invent DOI or findings.

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

## Cierre

The last message of the skill is exactly one line:

- Stop at the first failure (any `paper:status` step returns `ERROR:` (including `nada que generar`), `--cites` stays failing or `redaccion:lint` has FAIL): `ERROR: <mensaje del script>. <cómo arreglarlo>`. Do not continue with later steps.
- Everything went well: `OK: borrador paper/<versión>/paper-borrador.md (mejoradas: …; reescritas: …; stale: …; blocked: …). Próximo paso: Usa rsl-polish-paper sobre docs/<slug>/`.

## Forbidden

- Polish agents (only `citas-rsl`).
- Editing previous versions, frozen/off sections, states in `config.yml`, `paper.shadow.yml` or `paper.state.jsonc`.
- Generating BLOCKED sections; inventing PRISMA counts, results, citations or DOI.
- Deleting or renaming section markers; editing `informe*.md`, `picoc/` or `topic.md`.
- A framework in Metodología different from `formato.marco`.
- Internal traces in the text (`topic.md`, `informe`, panel, `GO_*`, skill names, repo paths).
- Copying from `global/examples/`; dumping full PDFs; refreshing Graphify.
