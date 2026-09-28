---
name: rsl-picoc
description: >-
  Builds or regenerates the search framework of an RSL theme as a traceable version
  docs/[short-title]/picoc/<fecha>-<MARCO>/picoc.md + picoc-debate.md, using the free
  framework of paper/paper.yml (formato.marco, e.g. PICOCT default, PICO, PIO, PICOS).
  Full mode debates with critico-rsl, defensor-rsl and redaccion-rsl; light mode only
  refreshes the general question. Ends with picoc:lint PASS. Use when the user says
  rsl-picoc, changes formato.marco, or when rsl-make-report / rsl-polish-report call it.
---

# rsl-picoc

Creates a **new version** of the search framework. Template and rules: `playbooks/vocabulario-controlado.md` (source of truth; do not restate it). Previous versions are never edited.

```text
docs/[titulo-breve]/
  informe-polish.md | informe.md   § 1.2 = pregunta general (literal)
  paper/paper.yml                  formato.marco
  picoc/<fecha>[-n]-<MARCO>/picoc.md + picoc-debate.md   (output)
```

Invoke: `Usa rsl-picoc sobre docs/<slug>/` · add `rewrite` to ignore the previous version.

## Mode

| Mode | When | Agents |
|------|------|--------|
| **completo** | No previous version, `rewrite`, or the marco changed | Yes (on the changed rows only if the marco changed) |
| **ligero** | Only the § 1.2 question changed (called by `rsl-polish-report`) | No |

Nothing changed (`picoc:latest` OK, `picoc:lint` PASS, no `rewrite`) → report it and stop; no new version.

## Procedure

1. `pnpm -s picoc:latest docs/<slug>` → marco, latest version and the exact `siguiente versión` folder to create (never compute it by hand). No `paper.yml` → `pnpm -s paper:status docs/<slug> --init`. **ERROR** (unknown letter in the marco) → stop and tell the user which letter is invalid; do not guess.
2. Pregunta general = the `¿…?` of § 1.2 of the ficha, copied literally.
3. **Ligero:** copy the previous `picoc.md` into the `siguiente versión` folder, replace only the general question, write a 3-line `picoc-debate.md` (date, base version, "solo pregunta general"), go to step 7.
4. **Completo — build.** Context from the theme graph (`graphify query "…" --graph docs/<slug>/graphify-out/graph.json`) and the previous version if any; do not read PDFs or refresh Graphify. One row per component of the marco, in order; all non-T components are AND blocks; T = year filter; no screening or document-type filters. Validate every EN candidate in **one** `pnpm -s thesaurus:check "…" …` call. Run `picoc:lint` on the draft before the debate.
5. **Completo — debate** (parallel; prompt = only the component table, keywords, the `thesaurus:check` table and the lint output, not whole files; answers of at most 10 items; web only to verify a doubtful term):
   - `critico-rsl` (marco mode): origin in the theme, recall vs. noise per block, blocks that cut the evidence, IEEE Xplore wildcards.
   - `defensor-rsl` (marco mode): why each block and term is needed; terms the literature uses and are missing.
   - `redaccion-rsl`: prose of concepts, RQs and justifications only.
6. **Completo — consolidate:** validate new terms with `thesaurus:check`, write `picoc.md` and `picoc-debate.md` (positions in a few bullets per agent, a decisions table, what is left for the user).
7. `pnpm -s picoc:lint docs/<slug>` → **PASS** (fix and repeat).
8. Section 2 of `informe.md` / `informe-polish.md` = only the link: `Las palabras clave, el marco <MARCO> (<componentes en palabras>) y las queries se encuentran en [picoc/<carpeta>/picoc.md](picoc/<carpeta>/picoc.md).`
9. Chat: key decisions and the paper sections now stale or blocked (`pnpm -s paper:status docs/<slug>`), then the Cierre line.

## Cierre

The last message of the skill is exactly one line:

- Stop at the first failure (`picoc:latest` gives an ERROR other than FALTA/DESFASADO (e.g. unknown letter), `thesaurus:check` fails, or `picoc:lint` is not OK after fixing): `ERROR: <mensaje del script>. <cómo arreglarlo>`. Do not continue with later steps.
- Everything went well: `OK: marco <MARCO> en picoc/<carpeta>/ (modo <completo | ligero>), picoc:lint OK. Próximo paso: <la skill que la llamó | Usa rsl-make-paper sobre docs/<slug>/>`; nothing changed: `OK: el marco <MARCO> ya estaba al día; no se creó versión. Próximo paso: Usa rsl-make-paper sobre docs/<slug>/`.

## Forbidden

- Editing previous `picoc/` versions, `topic.md` or the ficha (except the section 2 link).
- Marco different from `formato.marco`; general question different from § 1.2.
- Inventing IEEE descriptors or pages; terms not validated with `thesaurus:check`.
- Delivering without `picoc:lint` PASS.
