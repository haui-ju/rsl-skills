---
name: rsl-polish-paper
description: >-
  Polishes the latest docs/[short-title]/paper/<fecha>/paper-borrador.md with
  critico-rsl, defensor-rsl (impacto-social-rsl when justificacion/objetivo-rsl are in
  the run), redaccion-rsl and citas-rsl, and writes paper-polish.md and paper-debate.md in that
  version, section by section according to config.yml (on = improve,
  rewrite = re-polish from scratch; frozen ones copied; stale ones reported). Use when the
  user says rsl-polish-paper.
---

# rsl-polish-paper

Polishes the latest `paper-borrador.md` into **`paper-polish.md`** (clean, ready to present) and **`paper-debate.md`** (trace), in the same version folder. Does not create from scratch (`rsl-make-paper`).

| State in `config.yml` | What this skill does |
|---|---|
| `frozen` | Validated by the user: copy byte for byte, never edit. It is also the **quality reference**: its register, precision and prose are the bar for every `on`/`rewrite` section of the run, so read it before writing and match it. |
| `on` | **Base = this section as it stands in the previous version** (the new version starts as its copy); improve it, never throw it away. Keep what works; fix what is wrong (errors, contradictions, missing citations); refine the prose, the sense and the coherence of the words (R9). **Minimal diff**: keep every sentence that has no problem; a fix replaces a word or a clause; a citation goes inside the sentence it supports. Keep thesis, structure and wording. No polished text yet → polish from the borrador. **Re-polishing an already polished section = `on`.** |
| `rewrite` | Discard the polished text and write the section again from the borrador and the sources; may reframe. First know **why it failed**: look for the reason in the latest `paper-debate.md` (decisions, Pendientes) or in the user's message; if it is not written, ask the user with AskQuestion (e.g. no tiene sentido · mal escrito o torpe · contenido incorrecto o incompleto · enfoque equivocado · otro) before writing. Record the reason in the debate; the new text must fix exactly that. |
| `off` | Absent. |

Invoke: `Usa rsl-polish-paper sobre docs/<slug>/`. Internal inputs (`topic.md`, informe, picoc) are never cited in the paper.

## Polish rules

Form: `playbooks/redaccion-academica.md` (siglas, one idea per sentence, 2–5 sentence paragraphs with real connectors, no work notation, R7: each paragraph has one intention and leads into the next; need before tool; R8: important claims are cited, only with verified sources; R9: sense, precision, economy and elegance; the voice is the review's, never "el lector"). On top of it, only for the polish:

- **`on` does not grow the text.** An agent proposal that adds a sentence is accepted only to fix a FAIL (factual error, contradiction, important claim without citation that cannot go inside an existing sentence, "el lector"); anything else (limits, nuances, extra safeguards) goes to Pendientes in `paper-debate.md`. Economy (R9) rules: a paragraph never gets longer just to add nuances, and a paragraph that already meets R9 is left as it is.
- **Write, do not bolt on:** agent input (a citation, a correction) is integrated by rewriting the sentence so it reads naturally (R9), never by appending clauses or sentences.
- **No redundancy:** an argument is said once in the worked sections (e.g. "una ausencia solo es creíble si…" lives in one place). A citation says what the cited authors state or recommend, not a vague "lo retoman".
- Compact document: only H2 groups and H3 sections (no `####`); per block one core idea plus minimal evidence; no wall paragraphs.
- Contexto: about 4 linked paragraphs (norm/framework → delimit the object → anchors woven into one thread → tensions that lead to El problema); it does not dump the whole state of the art.
- Anchors: one strong mention in Contexto; later only if they add progress.
- No "AI flavor": disguised enumerations, forced triads, series of long dashes, generic verbs, meta-comments.
- Problemática = the picoc general question (= § 1.2 of the ficha), as ¿…?.
- Coherence with frozen sections: read them as context; contradictions are reported in chat, not fixed in the frozen text.

## Output (`paper-polish.md`)

Language per `formato.idioma` (Abstract/Resumen per `formato.resumen`); headings per the merged format printed by `paper:status`. Every section between its markers, order of `paper.shadow.yml`. Section lengths and the encabezado:

```markdown
<!-- paper:section id=encabezado -->
# [Título ≤ 20 palabras, cercano al título tentativo de la ficha, sin subtítulo en cascada]

**Tema.** … · **Problemática.** ¿…? · **Objetivo.** … (una o dos oraciones; palabras completas, sin siglas)
<!-- /paper:section -->
```

Contexto 3–5 short paragraphs · El problema 3–4 (arises from the previous → question → gap → contrast) · Justificación 2–4 · Objetivo de la RSL 2–3 · Organización 1 (coherent with the `on` groups).

- Metodología: same content rules as the [Metodología template of rsl-make-paper](../rsl-make-paper/SKILL.md#metodología-template-draft); the polish only tightens the prose. What each section must report: `playbooks/estandares-rsl.md` (PRISMA 2020 item and Kitchenham y Charters page); a missing item in an `on` section is a finding for the critic.
  - Tables, keywords, Scopus and Web of Science queries (with their filters) and CI/CE criteria stay as in the latest picoc.
  - The framework justification cites Kitchenham y Charters (2007), the PRISMA paragraph cites Page et al. (2021) and the keywords cite the IEEE Thesaurus (IEEE, 2019) with the note under the table, all from `global/bibliography/bibliography.md` with the printed page of the catalog.
  - User markers (`X`, `n = X`, `[[ … ]]`) are kept exactly; PRISMA counts only from `RSL/seleccion/`.
  - Length: framework justification 1–2 paragraphs; the PRISMA paragraphs (guideline, then process with the reviewer markers) plus the numbered steps.
- Resultados / Discusión / Conclusión: only from `RSL/extraccion/`, per `format.results_by`.
- Presentation (tables, figures, order) may imitate the recurring structure of `global/examples/` (one graph query); never their text.
- **Referencias** = every work cited, rebuilt every run, per `formato.citas` and `global/citation-style/<STYLE>.md`.

## Procedure

1. `pnpm -s paper:status docs/<slug>`. `ERROR` → stop and report. Nothing in **A mejorar** / **A reescribir** → only run `--cites` on the latest polish, report STALE / BLOCKED, stop (no version, no debate block). If the header says `etapas cerradas: …polish` (the latest version already has a finished polish) → `pnpm -s paper:status docs/<slug> --new-version`. Work only on A mejorar / A reescribir; STALE and BLOCKED are reported untouched (`WARN picoc …` → suggest `Usa rsl-picoc sobre docs/<slug>/`).
2. For every `rewrite` section, get the reason it failed (see the state table) before anything else. Read once: the frozen sections first, as the quality reference, then the worked sections of the borrador (and of the current polish for `on`), the frozen neighbors, the picoc general question and RQs; with Metodología in the run, also `global/bibliography/bibliography.md`. Evidence only via `graphify query … --graph docs/<slug>/graphify-out/graph.json` or `pnpm graphify:bibliography:query "…"` (no refresh, no full PDFs).
3. Agents in parallel (mode **sección**; prompt = the worked sections with their state, frozen neighbors as short context, the rules above; "no releer archivos completos"; at most 8 items each; web only to verify a claim):
   - Every prompt includes the state of each section, the reason for each `rewrite` and the frozen sections as the quality reference.
   - `critico-rsl` and `defensor-rsl` always. `critico-rsl` must return the **Sustento** table (R8); each row is resolved with a verified source (theme corpus, `global/bibliography/bibliography.md`, existing references) or by rephrasing the claim as the review's own decision. Never invent a source.
   - `impacto-social-rsl` only if `justificacion` or `objetivo-rsl` is being worked.
4. Brief synthesis in chat; write the polished sections (frozen copied unchanged; Referencias rebuilt).
5. `redaccion-rsl` on the worked sections (its **Calidad de prosa** table, R9: sense, precision, economy, elegance, judged on the text itself), with `pnpm -s redaccion:lint docs/<slug>/paper/<fecha>/paper-polish.md`; apply its fixes (form only) until its verdict is PASS: every paragraph OK in the **Hilo** table (R7: one intention, transition from the previous paragraph, need before tool) and in **Calidad de prosa** (R9), 0 FAIL and every WARN fixed or justified. Its answer must include the Hilo table and the rewritten paragraphs; if they are missing, relaunch it (never apply its summary by hand). After applying, run it again on the changed paragraphs. FAILs inside frozen sections are reported (suggest `on`); they do not block.
6. `citas-rsl` with `pnpm -s paper:status docs/<slug> --cites` until PASS or justified `PENDIENTE`.
7. Append a block to `paper-debate.md` (keep earlier blocks): date, worked sections, agents used, key decisions table, Redacción and Citas pass/fail.
8. `pnpm -s paper:status docs/<slug> --update polish` (no FAIL).
9. Chat: changes, stale / blocked and gaps, then the Cierre line.

## Cierre

The last message of the skill is exactly one line:

- Stop at the first failure (any `paper:status` step returns `ERROR:`, or `redaccion:lint` / `--cites` keep failing in the worked sections): `ERROR: <mensaje del script o sección que no pasó>. <cómo arreglarlo>`. Do not continue with later steps.
- Everything went well: `OK: polish paper/<versión>/paper-polish.md (secciones: …; agentes: …). Próximo paso: congela en config.yml las secciones validadas, o Usa rsl-make-paper sobre docs/<slug>/ para los grupos pendientes`.

## Forbidden

- Rewrite from scratch; editing previous versions, `paper-borrador.md`, informe, picoc or topic.
- Editing frozen sections (except re-rendering citations if `formato.citas` changed), states in `config.yml`, `paper.shadow.yml` or `paper.state.jsonc`.
- Generating off or BLOCKED sections; inventing PRISMA counts, search dates, results or DOI; replacing a user marker (`X`, `[[ … ]]`).
- Deleting markers; `####` in the polish; raw debate inside `paper-polish.md`.
- Delivering with `redaccion:lint` FAIL in worked sections or `--cites` FAIL.
- Refreshing Graphify; copying from `global/examples/`.
