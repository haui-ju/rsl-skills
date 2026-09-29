---
name: rsl-picoc
description: >-
  Builds or regenerates the search framework of an RSL theme as a traceable version
  docs/[short-title]/picoc/<fecha>-<MARCO>/picoc.md + picoc-debate.md, using the free
  framework of config.yml (formato.marco, e.g. PICOCT default, PICO, PIO, PICOS).
  Full mode debates with critico-rsl, defensor-rsl and redaccion-rsl; light mode only
  refreshes the general question; sugerencia mode applies the keyword suggestion of
  rsl-cribado-1 (cribado-1-sugerencia.md) and only validates. Only writes picoc/; reads the informe, config.yml and
  paper but never edits them. Ends with picoc:lint PASS. Use when the user says
  rsl-picoc, changes formato.marco, or when rsl-make-report / rsl-polish-report call it.
---

# rsl-picoc

Creates a **new version** of the search framework. Template and rules: `playbooks/vocabulario-controlado.md` (source of truth; do not restate it). Previous versions are never edited.

**Read-only outside `picoc/`:** this skill only reads `topic.md`, the informe, `config.yml` and `paper/`; the only thing it writes is the new `picoc/<siguiente versión>/` folder (`picoc.md` + `picoc-debate.md`). The informe link and the paper are updated by their own skills.

```text
docs/[titulo-breve]/
  topic.md                         (read) Alcance y exclusiones → criterios de inclusión y exclusión
  informe-polish.md | informe.md   (read) § 1.2 = pregunta general (literal)
  config.yml                       (read) formato.marco
  paper/                           (read) only through paper:status
  picoc/<fecha>[-n]-<MARCO>/picoc.md + picoc-debate.md   (the only output)
```

Invoke: `Usa rsl-picoc sobre docs/<slug>/` · add `rewrite` to ignore the previous version.

## Mode

| Mode | When | Agents |
|------|------|--------|
| **completo** | No previous version, `rewrite`, or the marco changed | Yes (on the changed rows only if the marco changed) |
| **parcial** | Only the paper keywords or the inclusion/exclusion criteria change, or the previous version lacks them | `critico-rsl` and `defensor-rsl` on that part only |
| **ligero** | Only the § 1.2 question changed (called by `rsl-polish-report`) | No |
| **sugerencia** | `picoc:latest` prints a `sugerencia:` line (`cribado-1-sugerencia.md` of `rsl-cribado-1` in the latest version) | No (already debated in the screening) |

Nothing changed (`picoc:latest` OK without a `sugerencia:` line, `picoc:lint` PASS, no `rewrite`) → report it and stop; no new version.

## Procedure

1. `pnpm -s picoc:latest docs/<slug>` → marco, latest version and the exact `siguiente versión` folder to create (never compute it by hand). No `config.yml` → the script uses PICOCT; if the user wants another marco, they set `formato.marco` themselves (never create or edit `config.yml` here). **ERROR** (unknown letter in the marco) → stop and tell the user which letter is invalid; do not guess.
2. Pregunta general = the `¿…?` of § 1.2 of the ficha, copied literally.
3. **Ligero / parcial:** copy the previous `picoc.md` into the `siguiente versión` folder. Ligero replaces only the general question; if the previous version lacks `## Keywords` or the criteria, add them as in parcial mode. Parcial writes or rewrites only `## Keywords` (rule KY) and/or `## Criterios de inclusión y exclusión` (rule CR) and debates that part (`critico-rsl`: generic or redundant keywords, criteria that cut valid evidence or cannot be checked; `defensor-rsl`: what the theme needs and is missing). Write a short `picoc-debate.md` (date, base version, what changed and why), go to step 7.
   **Sugerencia:** copy the previous `picoc.md` into the `siguiente versión` folder and apply only what `cribado-1-sugerencia.md` decided: the terms marked *agregar* or *revisar* go to their component in the component table (keywords and justification) and to the three queries; *vale* terms stay; a term leaves only if the suggestion says so explicitly. The Scopus and Web of Science queries are the ones of the suggestion; adjust IEEE Xplore to the same terms (wildcard limit, rule of the playbook). Validate only the new terms with one `thesaurus:check` call (a term that fails as IEEE descriptor stays as a free term with justification); no agents. `## Keywords` changes only if a new term is clearly better for the paper. `picoc-debate.md`: date, base version, «modo sugerencia desde picoc/<carpeta>/cribado-1-sugerencia.md» and a table of the changes (term, component, action, evidence of the screening). Go to step 7.
4. **Completo — build.** Context from the theme graph (`graphify query "…" --graph docs/<slug>/graphify-out/graph.json`) and the previous version if any; do not read PDFs or refresh Graphify. One row per component of the marco, in order; all non-T components are AND blocks; every query carries the inclusion filters of CR (years, document type, language, open access) after the blocks, with or without T (rule R2; WoS open access and IEEE Xplore filters are interface filters noted under the query). After Palabras clave, `## Keywords` (rule KY): 5 or 6 of its terms, at least one per component except T, the ones the paper will use. After the queries, `## Validación de la búsqueda`: 3–5 known relevant studies (from `RSL/`, the informe or the theme) with DOI and whether the Scopus query should retrieve them (Kitchenham & Charters, 2007, p. 14); never invent a study or DOI. Close with `## Criterios de inclusión y exclusión` (rule CR): short bullets from the scope and exclusions of `topic.md` and the marco; inclusion always fixes years (with T, the same), language, document type and **open access** (default; drop it only if the user asks). Validate every EN candidate in **one** `pnpm -s thesaurus:check "…" …` call. Its ACM CCS 2012 column backs free computing terms (also try `pnpm -s thesaurus:acm "…"` for near-identical names, e.g. *User studies*), and clinical population terms are checked in MeSH (both rules in the playbook). The `**Vocabulario:**` header cites, with author and year from `global/bibliography/bibliography.md`, every vocabulary the justifications use and only those (rule VOC: IEEE, 2019 · ACM, 2012 · NLM, 2026). Run `picoc:lint` on the draft before the debate.
5. **Completo — debate** (parallel; prompt = only the component table, keywords, the `thesaurus:check` table and the lint output, not whole files; answers of at most 10 items; web only to verify a doubtful term):
   - `critico-rsl` (marco mode): origin in the theme, recall vs. noise per block, blocks that cut the evidence, IEEE Xplore wildcards, generic paper keywords, criteria that exclude valid evidence or cannot be checked.
   - `defensor-rsl` (marco mode): why each block, term and criterion is needed; terms or criteria the literature uses and are missing.
   - `redaccion-rsl`: prose of concepts, RQs, justifications and criteria only.
6. **Completo — consolidate:** validate new terms with `thesaurus:check`, write `picoc.md` and `picoc-debate.md` (positions in a few bullets per agent, a decisions table, what is left for the user).
7. `pnpm -s picoc:lint docs/<slug>` → **PASS** (fix and repeat).
8. Chat: key decisions; whether section 2 of the informe still links an older version (do not edit it: `rsl-polish-report` refreshes the link); the paper sections now stale or blocked (`pnpm -s paper:status docs/<slug>`, read only); then the Cierre line.

## Cierre

The last message of the skill is exactly one line:

- Stop at the first failure (`picoc:latest` gives an ERROR other than FALTA/DESFASADO (e.g. unknown letter), `thesaurus:check` fails, or `picoc:lint` is not OK after fixing): `ERROR: <mensaje del script>. <cómo arreglarlo>`. Do not continue with later steps.
- Everything went well: `OK: marco <MARCO> en picoc/<carpeta>/ (modo <completo | parcial | ligero | sugerencia>), picoc:lint OK. Próximo paso: <la skill que la llamó | Usa rsl-polish-report sobre docs/<slug>/informe.md si el enlace de la sección 2 quedó viejo, y luego Usa rsl-make-paper sobre docs/<slug>/>`; nothing changed: `OK: el marco <MARCO> ya estaba al día; no se creó versión. Próximo paso: Usa rsl-make-paper sobre docs/<slug>/`.

## Forbidden

- Writing anything outside the new `picoc/<carpeta>/`: no edits to `informe.md`, `informe-polish.md` (not even the section 2 link), `paper/`, `config.yml` or `topic.md`; no `paper:status --init`, `--new-version` or `--update`.
- Editing previous `picoc/` versions.
- Marco different from `formato.marco`; general question different from § 1.2.
- Inventing IEEE descriptors or pages; terms not validated with `thesaurus:check`.
- Using ACM CCS or MeSH in a justification without citing it in the header, or citing an unused vocabulary (VOC).
- Delivering without `picoc:lint` PASS.
