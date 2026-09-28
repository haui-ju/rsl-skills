---
name: rsl-picoc
description: >-
  Builds or regenerates the search framework of an RSL theme as a traceable version
  docs/[short-title]/picoc/<fecha>-<MARCO>/picoc.md + picoc-debate.md, using the
  framework configured in paper/paper.yml (formato.marco: PICO | PICOC | PICOCT,
  default PICOCT). Component table 1:1 with the Scopus / Web of Science / IEEE Xplore
  queries, IEEE Thesaurus keywords (free terms last), debate with critico-rsl,
  defensor-rsl and redaccion-rsl, picoc:lint PASS. Use when the user says rsl-picoc,
  changes formato.marco, or when rsl-make-report / rsl-polish-report need the framework.
---

# rsl-picoc

## Goal

Create a **new version** of the search framework for one theme, following `playbooks/vocabulario-controlado.md` (source of truth for the template and rules). Previous versions are never edited.

## Paths

```text
docs/[titulo-breve]/
  topic.md · informe.md · informe-polish.md      (inputs; § 1.2 = pregunta general)
  paper/paper.yml                                 (formato.marco; created with --init if missing)
  picoc/
    2026-09-05-PICOCT/picoc.md                    (older version — read only)
    <hoy>[-n]-<MARCO>/picoc.md                    (output, this skill)
    <hoy>[-n]-<MARCO>/picoc-debate.md             (output, this skill)
```

## Invoke

```text
Usa rsl-picoc sobre docs/ia-inclusion-cognitiva-software/
Usa rsl-picoc sobre docs/ia-inclusion-cognitiva-software/ rewrite
```

If the folder is omitted → ask for it. `rewrite` = start from scratch, ignoring the previous version.

## Procedure (required)

1. **Marco.** `pnpm -s picoc:latest docs/[titulo-breve]`.
   - If there is no `paper/paper.yml` → `pnpm -s paper:status docs/[titulo-breve] --init` (creates it with `marco: PICOCT`).
   - Components: PICO = P, I, C, O · PICOC = + Co · PICOCT = + T.
2. **Pregunta general.** Copy literally the `¿…?` of § 1.2 of `informe-polish.md` (or `informe.md`). Never rephrase it here; if it must change, change the ficha first.
3. **Context.** Theme Graphify first (`graphify query "…" --graph docs/[titulo-breve]/graphify-out/graph.json`), plus `topic.md` and the ficha. Do **not** refresh Graphify.
   - If a previous version exists and no `rewrite`: start from it. If the marco changed, add or drop components (and the year filter when T comes or goes).
4. **Construcción.** One row per component, in marco order, with concept, linked RQ, keywords exactly as in the query, IEEE descriptor with page and a justification that quotes the theme (“…”).
   - All components enter the queries: every non-T component is an `AND` block; T is the year filter (`PUBYEAR > a-1 AND PUBYEAR < b+1` · `PY=(a-b)` · IEEE Xplore interface filter noted under its query). No `DOCTYPE`/`DT`.
   - Validate every EN candidate in **one** call: `pnpm -s thesaurus:check "t1" "t2" …`. Non-preferred → its USE. Free terms stay free.
   - Palabras clave ES / EN: IEEE preferred terms first with page; free terms only at the end, each with a brief justification.
   - One RQ per component (RQ1…RQn), with its *dato a extraer*.
5. **Debate** (in parallel). Shared prompt: draft picoc + `thesaurus:check` table + pregunta general + “Evalúa este marco de búsqueda según playbooks/vocabulario-controlado.md. Responde en español con el formato de tu rol.”
   - `critico-rsl`: terms without origin in the theme, recall vs. noise per block, blocks that would cut the evidence (e.g. C or O too narrow), invented descriptors.
   - `defensor-rsl`: why each term and each block is needed; evidence that the vocabulary matches the literature.
   - `redaccion-rsl`: prose of concepts, RQs and justifications (`playbooks/redaccion-academica.md`).
6. **Consolidar y escribir** in `docs/[titulo-breve]/picoc/<hoy>[-n]-<MARCO>/` (`-2`, `-3` if the folder of today already exists):
   - `picoc.md` with the playbook template;
   - `picoc-debate.md`: date, marco, base version, one block per agent (summary of the position), decisions taken (term added / removed / kept and why).
7. **Verificar:** `pnpm -s picoc:lint docs/[titulo-breve]` → **PASS** (fix and repeat until it passes). Then `pnpm -s picoc:latest docs/[titulo-breve]` → OK.
8. **Enlaces:** in `informe.md` and `informe-polish.md`, section 2 = only the link to the new version:
   `Las palabras clave, el marco <MARCO> (<componentes en palabras>) y las queries se encuentran en [picoc/<carpeta>/picoc.md](picoc/<carpeta>/picoc.md).`
   Componentes en palabras: PICO = población, intervención, comparación y resultado · PICOC = … y contexto · PICOCT = … contexto y tiempo (así la sigla queda definida).
9. **Chat:** path of the new version, lint result, main debate decisions, and paper sections that became stale (`pnpm -s paper:status docs/[titulo-breve]`). Next step (do not run here):

```text
Usa rsl-make-paper sobre docs/[titulo-breve]/
```

## Forbidden

- Editing previous versions under `picoc/`, `topic.md`, or the ficha (except the section 2 link).
- A marco different from `paper.yml` `formato.marco`.
- A pregunta general different from § 1.2 of the ficha.
- Screening / extraction sections, “T — Filtros”, document-type filters, or a separate “Términos libres” section.
- Free keywords before IEEE ones, or without justification; presenting a free term as an IEEE descriptor.
- Terms not validated with `thesaurus:check`; inventing descriptors or pages.
- Delivering without `picoc:lint` PASS.
