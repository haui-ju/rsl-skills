---
name: rsl-polish-paper
description: >-
  Polishes the latest docs/[short-title]/paper/<fecha>/paper-borrador.md with
  critico-rsl, defensor-rsl (impacto-social-rsl when justificacion/objetivo-rsl are in
  the run), redaccion-rsl and citas-rsl, and writes paper-polish.md and paper-debate.md in that
  version, section by section according to paper/paper.yml (on = improve,
  rewrite = re-polish from scratch; frozen ones copied; stale ones reported). Use when the
  user says rsl-polish-paper.
---

# rsl-polish-paper

Polishes the latest `paper-borrador.md` into **`paper-polish.md`** (clean, ready to present) and **`paper-debate.md`** (trace), in the same version folder. Does not create from scratch (`rsl-make-paper`).

| State in `paper.yml` | What this skill does |
|---|---|
| `frozen` | Copy byte for byte; never edit. |
| `on` | Start from the current polished text; targeted fixes (grammar, continuity, precision, citations, trimming); keep thesis and structure. No polished text yet → polish from the borrador. **Re-polishing an already polished section = `on`.** |
| `rewrite` | Discard the polished text; re-polish from the borrador section; may reframe. |
| `off` | Absent. |

Invoke: `Usa rsl-polish-paper sobre docs/<slug>/`. Internal inputs (`topic.md`, informe, picoc) are never cited in the paper.

## Polish rules

Form: `playbooks/redaccion-academica.md` (siglas, one idea per sentence, 2–5 sentence paragraphs with real connectors, no work notation). On top of it, only for the polish:

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

- Metodología: tables and queries of the latest picoc as they are; `marco-pico` names the configured framework and its components in words; title from `paper:status`. PRISMA only from `RSL/seleccion/`.
- Resultados / Discusión / Conclusión: only from `RSL/extraccion/`, per `format.results_by`.
- Presentation (tables, figures, order) may imitate the recurring structure of `global/examples/` (one graph query); never their text.
- **Referencias** = every work cited, rebuilt every run, per `formato.citas` and `global/citation-style/<STYLE>.md`.

## Procedure

1. `pnpm -s paper:status docs/<slug>`. `ERROR` → stop and report. Nothing in **A mejorar** / **A reescribir** → only run `--cites` on the latest polish, report STALE / BLOCKED, stop (no version, no debate block). If the header says `etapas cerradas: …polish` (the latest version already has a finished polish) → `pnpm -s paper:status docs/<slug> --new-version`. Work only on A mejorar / A reescribir; STALE and BLOCKED are reported untouched (`WARN picoc …` → suggest `Usa rsl-picoc sobre docs/<slug>/`).
2. Read once: the worked sections of the borrador (and of the current polish for `on`), the frozen neighbors, the picoc general question and RQs. Evidence only via `graphify query … --graph docs/<slug>/graphify-out/graph.json` (no refresh, no full PDFs).
3. Agents in parallel (mode **sección**; prompt = the worked sections with their state, frozen neighbors as short context, the rules above; "no releer archivos completos"; at most 8 items each; web only to verify a claim):
   - `critico-rsl` and `defensor-rsl` always.
   - `impacto-social-rsl` only if `justificacion` or `objetivo-rsl` is being worked.
4. Brief synthesis in chat; write the polished sections (frozen copied unchanged; Referencias rebuilt).
5. `redaccion-rsl` on the worked sections with `pnpm -s redaccion:lint docs/<slug>/paper/<fecha>/paper-polish.md`; apply its fixes (form only) until those sections have 0 FAIL and every WARN fixed or justified. FAILs inside frozen sections are reported (suggest `on`); they do not block.
6. `citas-rsl` with `pnpm -s paper:status docs/<slug> --cites` until PASS or justified `PENDIENTE`.
7. Append a block to `paper-debate.md` (keep earlier blocks): date, worked sections, agents used, key decisions table, Redacción and Citas pass/fail.
8. `pnpm -s paper:status docs/<slug> --update polish` (no FAIL).
9. Chat: changes, stale / blocked and gaps, then the Cierre line.

## Cierre

The last message of the skill is exactly one line:

- Stop at the first failure (any `paper:status` step returns `ERROR:`, or `redaccion:lint` / `--cites` keep failing in the worked sections): `ERROR: <mensaje del script o sección que no pasó>. <cómo arreglarlo>`. Do not continue with later steps.
- Everything went well: `OK: polish paper/<versión>/paper-polish.md (secciones: …; agentes: …). Próximo paso: congela en paper/paper.yml las secciones validadas, o Usa rsl-make-paper sobre docs/<slug>/ para los grupos pendientes`.

## Forbidden

- Rewrite from scratch; editing previous versions, `paper-borrador.md`, informe, picoc or topic.
- Editing frozen sections (except re-rendering citations if `formato.citas` changed), states in `paper.yml`, `paper.shadow.yml` or `paper.state.jsonc`.
- Generating off or BLOCKED sections; inventing PRISMA counts, results or DOI.
- Deleting markers; `####` in the polish; raw debate inside `paper-polish.md`.
- Delivering with `redaccion:lint` FAIL in worked sections or `--cites` FAIL.
- Refreshing Graphify; copying from `global/examples/`.
