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
| `frozen` | Validated by the user: copy byte for byte, never edit. It is also the **quality reference**: its register, precision and prose are the bar for every `on`/`rewrite` section of the run, so read it before writing and match it. |
| `on` | **Base = this section in the previous version**; improve it (fix, fill gaps, add evidence, continuity, prose and sense per R9), keeping what works; never rewrite from scratch. No previous text → generated (`reescribir (nueva)`). |
| `rewrite` | Ignore the previous text; regenerate from the sources. First know **why it failed**: look for the reason in the latest `paper-debate.md` (decisions, Pendientes) or in the user's message; if it is not written, ask the user with AskQuestion (e.g. no tiene sentido · mal escrito o torpe · contenido incorrecto o incompleto · enfoque equivocado · otro) before writing. Record the reason in the debate; the new text must fix exactly that. |
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
3. For every `rewrite` section, get the reason it failed (see the state table). Inputs, read once: ficha, the latest picoc (path printed by `paper:status`), `topic.md`, and the frozen sections of the new version (coherence and quality reference: match their register and prose).
4. Evidence, graph first (no full PDFs, no refresh):
   - `graphify query "<tema de la sección>" --graph docs/<slug>/graphify-out/graph.json` + `RSL/MD/` locators `[PDF p.N]`.
   - One `graphify query "<sección>" --graph global/examples/graphify-out/graph.json` per section for structure and presentation only; never copy text, data or citations. Our writing must exceed them.
   - **Methodological sources** (Metodología in the run): read `global/bibliography/bibliography.md` first and cite what it lists (key, APA 7, citable passages with printed page); for more detail `pnpm graphify:bibliography:query "…"` and a pinpoint Read of the MD lines. Download only if the work is missing: open-access PDF with a verified DOI into `global/bibliography/<carpeta>/`, then `pnpm -s rsl:source <pdf>` (ERROR → stop), a row in the catalog and suggest `pnpm graphify:bibliography:refresh` to the user. No open PDF → cite from the verified record and mark `PENDIENTE` in the chat; never invent pages or DOI.
5. Write each section **between its markers** (create them if new; order of `paper.shadow.yml`). Headings follow the merged format printed by `paper:status`: groups as numbered H2 (`## I. Introducción`), sections as H3, H4 subsections allowed in the draft; `## Referencias` is derived.
6. Content per group:
   - **Introducción:** template below. For each anchor SLR: what it covers, n/DOI, what it does not cover (= gap). Every extra paragraph adds citation, delimitation, metric, ethics or SE-process detail; no stubs.
   - **Preguntas:** the picoc general question = problemática = § 1.2 (verbatim in the encabezado and in El problema 2.4, as an interrogative); its RQs give one specific objective each in Objetivo de la RSL and structure Organización. No new RQ.
   - **Metodología:** tables, RQs, keywords, queries and criteria of the latest picoc **as they are**; section by section in [Metodología template](#metodología-template-draft).
   - **Resultados / Discusión / Conclusión:** only from `RSL/extraccion/`, by RQ or theme (`format.results_by`).
   - **Abstract / Resumen:** only when content sections exist; keywords = the `## Keywords` table of the latest picoc as it is (EN column in the Abstract, ES column in the Resumen; never add or drop one).
7. `citas-rsl` on the worked sections only: `pnpm -s paper:status docs/<slug> --cites paper/<fecha>/paper-borrador.md` + its fixes until PASS or justified `PENDIENTE`.
8. `pnpm -s redaccion:lint docs/<slug>/paper/<fecha>/paper-borrador.md` and a self-check of R7 (one intention per paragraph, transitions) and R8 (important claims cited with verified sources; never "el lector") and R9 (prose with sense, precision, economy and elegance) → 0 FAIL in the worked sections (WARN allowed in the draft). FAILs inside frozen sections are reported (suggest `on`); they do not block.
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

## Metodología template (draft)

What each section must report (PRISMA 2020 item and Kitchenham y Charters page): [`playbooks/estandares-rsl.md`](../../../playbooks/estandares-rsl.md); this template gives the form. Order and letters (A., B., C.…) from `paper:status`; only the `on`/`rewrite` sections of the run. The group opens with one short paragraph (2–3 sentences), before the first marker, that states the method followed (Kitchenham y Charters, 2007) and why it is fixed in a prior protocol (reproducibility, less researcher bias, with the catalog page), then announces the order of the sections. It never opens by recapping the Introducción ("Los objetivos anteriores…"): the Metodología starts with what the review did.

Thread (R7 of `playbooks/redaccion-academica.md`): each section opens by picking up the previous one (framework → its components become keywords → keywords build one equation per base → the retrieved records are judged with the criteria → PRISMA documents that selection). Every method decision follows need → why the obvious alternative is not enough → decision → what the source says it adds (citation) → how it applies here. Never open a paragraph with the tool and its definition.

- **`marco-pico`**
  - One paragraph that names the framework of the latest picoc with its components in words (e.g. "Se adoptó el marco PICOC (población, intervención, comparación, resultado y contexto)…").
  - Justify it in two or three sentences with the catalog source: Kitchenham y Charters (2007, p. 11) adopt PICOC for software engineering from Petticrew y Roberts (never attribute the framework itself to Kitchenham). Say why each added component applies to this theme. With a framework other than PICOC, say what it drops or adds (e.g. PICO drops the context, PICOCT adds the time window) and why; without T, the time window is an inclusion criterion.
  - Then: the component table (`Tabla N — Marco <MARCO>`: one column per letter, the concept of each component), the general question (verbatim, as an interrogative) and the RQ table (`Componente | Código | Pregunta`).
- **`palabras-clave`**
  - The `## Palabras clave` table of the latest picoc as it is: `Componente | Palabras clave (ES) | Keywords (EN)`, grouped by component; IEEE descriptors in italics in the EN column.
  - One sentence says that the terms combine descriptors of the IEEE Thesaurus, cited as (Institute of Electrical and Electronics Engineers [IEEE], 2019), and free terms (Kitchenham y Charters, 2007, p. 14: indexing terms of the databases).
  - Under the table, one note: `*Nota.* En cursiva, descriptores del IEEE Thesaurus (IEEE, 2019); el resto son términos libres.` No per-term pages (they stay in the picoc). Reference entry from the catalog (`ieee-2019-thesaurus`).
- **`ecuacion-busqueda`**
  - Only Scopus and Web of Science, one code block each, copied from the picoc with their filters. Other bases of the picoc (IEEE Xplore, the auxiliary search) do not go into the paper.
  - One sentence on the Boolean logic (OR inside a component, AND between components). If the two bases search different fields (e.g. `TITLE-ABS-KEY` vs `ALL=`), justify it. One sentence says that the equations carry the limits of the inclusion criteria (period, document type, language, open access) so the search is documented and repeatable (Kitchenham y Charters, 2007, p. 16); a filter the base only offers in its interface (Web of Science open access) is named as such.
  - Close with `Tabla N — Búsqueda por base de datos`: `Base | Fecha de búsqueda | Años | Campos | Filtros | Registros`, one row per base (Scopus, Web of Science). Years, fields and filters from the equations; date and records are user markers (`X`, `n = X`), never filled in.
- **`criterios-seleccion`**
  - The criteria of the latest picoc, same text, coded `CI1…` (inclusion) and `CE1…` (exclusion) in two bullet lists.
  - Never add, merge or reword a criterion.
- **`seleccion-prisma`**
  - First paragraph: the selection is **reported** according to PRISMA 2020 (Page et al., 2021, p. 1), a reporting guideline with a 27-item checklist and a flow diagram; the execution follows Kitchenham y Charters. Say why it applies here, in one or two sentences, without overclaiming (it makes the searched corpus auditable; it does not prove gaps).
  - Second paragraph, the process (PRISMA item 8; Kitchenham y Charters, 2007, pp. 19–20): selection in stages (title and abstract, then full text); `[[ número de revisores y si trabajaron de forma independiente ]]`; `[[ cómo se resolvieron los desacuerdos ]]`; `[[ herramienta usada, p. ej. Rayyan o una hoja de cálculo ]]`; each exclusion recorded with its reason. With a single reviewer, say how the decisions were checked (discussion with the advisor or test-retest on a random sample, p. 20). The bracketed parts are user markers.
  - Steps as a numbered list. Counts come from `RSL/seleccion/` when it exists; otherwise every count is `n = X` for the user to replace:
    1. Registros identificados en Scopus (n = X) y en Web of Science (n = X) con la ecuación sin filtros.
    2. Registros excluidos por los filtros de la base de datos (periodo, tipo de documento, idioma y acceso abierto) (n = X).
    3. Duplicados eliminados (n = X).
    4. Registros cribados por título y resumen (n = X); excluidos (n = X).
    5. Informes buscados para recuperación (n = X); no recuperados (n = X).
    6. Informes evaluados a texto completo (n = X); excluidos por no cumplir un criterio de inclusión o por cumplir uno de exclusión (n = X).
    7. Estudios incluidos en la revisión (n = X).
  - Then the line `[[ AGREGAR DIAGRAMA ]]` alone and the caption `*Fig. 1. Diagrama de flujo PRISMA 2020 del proceso de selección.*` The user draws the diagram; never generate it.
- **`calidad`**
  - Only when it is `on` and `RSL/seleccion/` exists. The instrument as a short list of questions (e.g. objective stated, context described, method reproducible, results answer the question), the scale, who applied it (`[[ … ]]`) and how the score is used (it describes the corpus; it does not exclude unless the protocol says so) (Kitchenham y Charters, 2007, § 6.3).
- **`extraccion-datos`**
  - The extraction form as a table `Campo | RQ | Descripción`: bibliographic fields plus one field per RQ from the picoc column *Dato a extraer*. Say that it was piloted on a sample, who extracted and who checked (`[[ … ]]`), and what is done with missing data or duplicate publications (Kitchenham y Charters, 2007, § 6.4).
- **`sintesis`**
  - The synthesis method (descriptive and narrative, tabulated by RQ, thematic when the studies are heterogeneous) and how the results are presented (tables, figures) (Kitchenham y Charters, 2007, § 6.5). No meta-analysis unless the studies allow it.
- **`declaraciones`** (after Conclusión, PRISMA items 24–27)
  - Four short paragraphs, each a user marker unless the theme states it: registration and protocol (`[[ registro y número, o «La revisión no se registró» ]]`, where the protocol can be consulted, changes to the protocol); funding (`[[ … ]]`); conflicts of interest (`[[ … ]]`); availability of data and extraction forms (`[[ … ]]`). Never invent a registry, grant or repository.

Other sections, when `on` (content in `playbooks/estandares-rsl.md`):

- **`encabezado`**: the title identifies the work as a systematic review (R6: brief, no subtitle chains).
- **`resumen`**: structured per PRISMA 2020 Table 2 (Page et al., 2021, p. 5): objective; methods (databases and search date, criteria, quality, synthesis); results (studies included, main findings); limitations; conclusion; registration and funding. Counts and dates stay `X`.
- **`resultados-rq`**: add the studies that seemed to meet the criteria but were excluded, with the reason (PRISMA 16b), as a short table or appendix.
- **`amenazas`**: split the limitations of the **evidence** (quality of the primary studies, publication bias; Kitchenham y Charters, 2007, p. 15) from those of the **review process** (databases, languages, open access only, single reviewer). The open-access filter is always declared as a bias of the process.

`X` and `[[ … ]]` are user markers: they stay as they are through make and polish, and `redaccion:lint` counts them without failing.

## Cierre

The last message of the skill is exactly one line:

- Stop at the first failure (any `paper:status` step returns `ERROR:` (including `nada que generar`), `--cites` stays failing or `redaccion:lint` has FAIL in a worked section): `ERROR: <mensaje del script>. <cómo arreglarlo>`. Do not continue with later steps.
- Everything went well: `OK: borrador paper/<versión>/paper-borrador.md (mejoradas: …; reescritas: …; stale: …; blocked: …). Próximo paso: Usa rsl-polish-paper sobre docs/<slug>/`.

## Forbidden

- Polish agents (only `citas-rsl`).
- Editing previous versions, frozen/off sections, states in `config.yml`, `paper.shadow.yml` or `paper.state.jsonc`.
- Generating BLOCKED sections; inventing PRISMA counts (without `RSL/seleccion/` they are `X`), search dates, results, citations or DOI; replacing a user marker (`X`, `[[ … ]]`).
- Bases other than Scopus and Web of Science in `ecuacion-busqueda`.
- Deleting or renaming section markers; editing `informe*.md`, `picoc/` or `topic.md`.
- A framework in Metodología different from `formato.marco`.
- Internal traces in the text (`topic.md`, `informe`, panel, `GO_*`, skill names, repo paths).
- Copying from `global/examples/`; dumping full PDFs; refreshing Graphify.
