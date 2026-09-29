---
name: rsl-cribado-1
description: PRISMA screening 1 (title, abstract and keywords) of Scopus and Web of Science together. The user drops the Scopus CSV and the WoS export (Excel or tab-delimited) in the latest picoc/<fecha>-<MARCO>/ folder; a script converts WoS to CSV, merges both into resultados-<MARCO>.csv and removes duplicates first; defensor-rsl proposes SI/NO per unique record against the picoc criteria and critico-rsl attacks the proposal; writes cribado-1.md (report), cribado-1.shadow.jsonl (compact decisions) and cribado-1-sugerencia.md (keywords that worked, did not, or should be added, with Scopus and WoS queries). Never reads the exports and never edits them. Use when the user says rsl-cribado-1 or has just downloaded the Scopus and WoS results. The columns are added later by rsl-cribado-1-aplicar.
---

# rsl-cribado-1

First screening of PRISMA 2020 (records screened on **title, abstract and keywords only**) against the criteria of the latest picoc, over Scopus and Web of Science at once. The user runs the Scopus and WoS queries of the picoc and leaves both exports in that picoc folder; this skill analyses them and writes a report; the user reviews it; `rsl-cribado-1-aplicar` then writes the unified CSV with the two columns. Column mapping and dedup rules: `playbooks/columnas-scopus-wos.md`.

```text
docs/[titulo-breve]/picoc/<fecha>-<MARCO>/
  picoc.md                      (read) ## Criterios de inclusión y exclusión → CI1..CIn, CE1..CEn
  <scopus>.csv                  (user; read only by the script)
  <wos>.xls | <wos>.txt         (user; read only by the script)
  <wos>.csv                     (cribado:prepare: WoS converted, original headers)
  resultados-<MARCO>.csv        (cribado:prepare: unified, Id R001…, Fuente)
  cribado-1.md                  (cribado:report: the report for the user)
  cribado-1.shadow.jsonl        (cribado:report: one line per record, read by rsl-cribado-1-aplicar)
  cribado-1-sugerencia.md       (this skill, always)
  .cribado-1/
    estado.json, registros.jsonl, criterios.md   (cribado:prepare)
    propuestas/lote-NN.md       (the agents: defensor and critic tables)
    resoluciones.md, sintesis.json   (this skill)
    decisiones.jsonl, debate.md (cribado:merge)
    keywords.md                 (cribado:keywords)
    thesaurus.md, sugerencia-debate.md   (this skill and the agents)
```

Invoke: `Usa rsl-cribado-1 sobre docs/<slug>/`.

**Rule of screening 1: relevance, not compliance** (Kitchenham & Charters, 2007, p. 19: title and abstract first, full text later). A record is `NO` only when its title or abstract **shows** an exclusion criterion or **contradicts** an inclusion criterion (other population, no AI technique, a secondary study, sensory-only accessibility, AI that only diagnoses). What the abstract does **not** say (life-cycle phase, metric, instrument, evaluation design) is never a reason for `NO`: the record goes as `SI` with duda, and screening 2 decides on the full text. The prompts below carry this rule; say it again when you resolve disagreements.

## Procedure

**Token budget.** The agents write their tables to files and answer one line; never ask them to return the table, and never read `propuestas/`, `registros.jsonl`, `estado.json` or `decisiones.jsonl` yourself: `cribado:merge` consolidates and prints only what needs a decision. Use the prompt templates below verbatim (only `<…>` changes).

1. `pnpm -s cribado:prepare docs/<slug>`. It detects the exports by their headers (one per base; only Scopus or only WoS is fine), converts WoS to CSV, writes `resultados-<MARCO>.csv` and **removes duplicates first** (same DOI, same database id or same normalized title; the first occurrence stays, Scopus first, and gets `Fuente = Scopus; WoS`; the others are an automatic NO with the duplicates criterion). It prints the duplicates in one line and, per batch of 40 unique records, the line range of `.cribado-1/registros.jsonl`. ERROR → Cierre ERROR.
2. For each batch (up to 4 in parallel) `defensor-rsl`, then `critico-rsl` on the same batch (critics of different batches in parallel). `<dir>` is the absolute path of `picoc/<carpeta>/.cribado-1`:
   - Defensor: `Modo: **cribado** (propones). Tema: <alcance en una línea>. Lee solo las líneas <a> a <b> de <dir>/registros.jsonl y los criterios de <dir>/criterios.md; nada más, sin web. Escribe tu tabla en <dir>/propuestas/lote-<NN>.md bajo ## Defensor y responde una línea.`
   - Crítico: `Modo: **cribado** (criticas). Tema: <alcance en una línea>. Lee solo las líneas <a> a <b> de <dir>/registros.jsonl, <dir>/criterios.md y la sección ## Defensor de <dir>/propuestas/lote-<NN>.md; nada más, sin web. Añade tus desacuerdos al final de ese archivo bajo ## Crítico y responde una línea.`
3. `pnpm -s cribado:merge docs/<slug>`. Agreements are taken as they are; it prints only the disagreements (both positions and a trimmed abstract). Resolve each from that text with the rule of screening 1: `NO` only if the abstract shows a CE or contradicts a CI; a `NO` that rests on what the abstract does not say becomes `SI` with duda `sí` (the full text decides). A `NO` cites at least one code, main one first; motive of at most 25 words in Spanish, never data the abstract does not say. Write them in `.cribado-1/resoluciones.md` (`## Resoluciones` + `| Id | Decisión | Criterios | Duda | Motivo |`) and run `cribado:merge` again → OK. It writes `decisiones.jsonl` (keeping corrections of the user) and `debate.md`.
4. Write `.cribado-1/sintesis.json`: `{"aceptados": "…", "rechazados": "…", "dudas": "…"}`, each the general reason in Spanish (at most 120 words, no per-batch detail), from the merge output and the report counts.
5. `pnpm -s cribado:report docs/<slug>` → OK (fix and repeat on ERROR). `cribado-1.md` has, in this order: summary, duplicates (removed, kept, title, reason), accepted (why, then title and source), rejected (why, percentage by inclusion criterion not met and by exclusion criterion, then the list), doubts (why, list), the PRISMA line and the criteria. `cribado-1.shadow.jsonl` is written at the same time.
6. **Suggestion (always).** The goal is to **widen** the universe of candidates: add what the accepted records and the thesaurus show is missing, keep what works, and remove only what is proven to add nothing. The keyword analysis only sees the records the query already retrieved, so removals always shrink the search and additions from outside (thesaurus) are the only way to find what was missed.
   - `pnpm -s cribado:keywords docs/<slug>` → `.cribado-1/keywords.md`: hits of each query term in the unique records (SI and NO) and every author or index keyword of the accepted records that no query term covers.
   - Build the candidate list from three sources: (a) the keywords of the accepted records in `keywords.md`; (b) the UF and NT of every IEEE descriptor already in the picoc, plus related descriptors (`graphify query "<término>" --graph global/thesaurus/graphify-out/graph.json`); (c) the terms listed as retired in the picoc (`## Descriptores revisados y excluidos`) when the evidence came from an earlier screening, which may have used a stricter rule. Run `pnpm -s thesaurus:check "t1" "t2" …` on the current IEEE descriptors and all candidates in one call (`playbooks/vocabulario-controlado.md`).
   - **Removal rule:** a term is removed only if it has 0 SI (doubts count as SI) in total **and** at least 3 exclusive NO in this screening. Anything else stays, even with 0 records. Never remove on the evidence of an earlier screening.
   - **Cap: at most 100 keywords** in the whole query (all blocks together; `playbooks/vocabulario-controlado.md`, rule R2). If the additions go over, drop first the redundant variants the databases already retrieve (hyphen or plural forms), then the new terms with the least evidence; say which ones in `## Debate`. Count the terms of the suggested Scopus query before writing it.
   - Save the `thesaurus:check` output to `.cribado-1/thesaurus.md`. Then `defensor-rsl` (mode **sugerencia**): `Modo: **sugerencia** (propones). Objetivo: ampliar el universo de candidatos. Lee <dir>/keywords.md, <dir>/thesaurus.md y de <carpeta>/picoc.md solo la tabla de componentes, las queries de Scopus y Web of Science, los descriptores revisados y excluidos y los criterios. Propón agregar términos de las palabras clave de los aceptados, de los UF y NT del tesauro y de los retirados con evidencia de un cribado anterior. Quitar solo con 0 SI en total y al menos 3 NO exclusivos. Máximo 100 keywords en toda la query. Escribe en <dir>/sugerencia-debate.md bajo ## Defensor y responde una línea.` Then `critico-rsl` (mode **sugerencia**) with the same files plus that section, appending `## Crítico`.
   - Read `sugerencia-debate.md` once and settle the disagreements.
   - Write `cribado-1-sugerencia.md`:

     ```markdown
     # Sugerencia de búsqueda — cribado 1

     <!-- cribado:sugerencia picoc=<carpeta> -->

     Basada en <n> registros únicos de Scopus y Web of Science (SI <a>, NO <b>). No reemplaza la búsqueda: la amplía.

     **Efecto esperado:** <x> términos agregados, <y> quitados; los términos quitados dejan fuera <z> de los <n> registros actuales (<w> SI).

     ## Keywords

     | Comp. | Término | Estado | Evidencia | Vocabulario | Decisión |
     |---|---|---|---|---|---|
     (Estado: vale / no aporta / agregar / revisar; every current query term appears, plus the new ones)

     ## Query Scopus

     (code block, ready to run: the current query with the agreed changes)

     ## Query Web of Science

     (code block, ready to run)

     ## Debate

     (disagreements between defensor and critic and how each was settled, one line each)
     ```

     The IEEE Xplore query is not written here: `rsl-picoc` adjusts it when it applies the suggestion.
7. Chat: counts (records per base, duplicates, SI, NO, doubts, disagreements), links to `cribado-1.md` and `cribado-1-sugerencia.md`, and that the user should review the report. Then the Cierre line.
8. **Corrections** (in this or a later turn): one `pnpm -s cribado:set docs/<slug> <id> SI|DUDA|NO "<motivo>" [CI3,CE5]` per record (`DUDA` = `SI` with duda) (it regenerates the report and the shadow); no new debate. If the general reasons no longer fit, update `sintesis.json` and run `cribado:report`. Then the Cierre line again.

## Cierre

The last message of the skill is exactly one line:

- Stop at the first failure (`cribado:prepare` or `cribado:report` still ERROR after fixing): `ERROR: <mensaje del script>. <cómo arreglarlo>`.
- Everything went well: `OK: cribado 1 de <n> registros (<d> duplicados, SI <a>, NO <b>, dudas <c>) en picoc/<carpeta>/cribado-1.md, con sugerencia de keywords en cribado-1-sugerencia.md. Próximo paso: revisa el reporte y, si lo apruebas, Usa rsl-cribado-1-aplicar sobre docs/<slug>/ (para la sugerencia: Usa rsl-picoc sobre docs/<slug>/)`.

## Forbidden

- Reading the exports or `resultados-<MARCO>.csv` (Read, cat, head, grep) or passing them to an agent: only line ranges of `registros.jsonl`.
- Editing the exports, `resultados-<MARCO>.csv`, `picoc.md`, `estado.json`, `registros.jsonl`, `decisiones.jsonl` or the shadow by hand (decisions go through `resoluciones.md` + `cribado:merge`, or `cribado:set`).
- Asking an agent to return its table in the reply, or reading the batch files yourself.
- Criteria that are not in the picoc; screening with the full text, PDFs or the web.
- A suggestion that empties or replaces the query instead of improving it; a suggestion that only removes terms; removing a term outside the removal rule; descriptors that did not pass `thesaurus:check` presented as IEEE.
- Editing `picoc.md` with the suggestion (that is `rsl-picoc`, mode sugerencia).
- Writing `resultados-<MARCO>-cribado-1.csv` (that is `rsl-cribado-1-aplicar`, after the user approves).
- Delivering without `cribado:report` OK.
