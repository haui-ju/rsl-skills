---
name: rsl-qa-destroy
description: >-
  Tries to break the RSL flow on purpose and writes a bug report: runs the qa:destroy
  harness (positive flow, mixed order, destructive inputs, free marco, static checks of
  skills and agents) in a /tmp sandbox, then tries at least 5 new attacks by hand.
  Writes qa/<fecha>[-n]/qa-report.md + qa-report.json. Never edits code. Use when the
  user says rsl-qa-destroy, wants to find bugs, or before trusting a change to the flow.
---

# rsl-qa-destroy

Destroy to build: find every way the flow breaks and report it. **Only reports**; fixing belongs to `rsl-qa-fix`.

```text
scripts/qa-destroy.py   harness (cases grouped: positivo · orden · destruir · marco · skills)
qa/fixtures/            fixed inputs copied to the sandbox (never edited here)
qa/<fecha>[-n]/         qa-report.md (human) + qa-report.json (for rsl-qa-fix)   ← output, committed to git
```

Invoke: `Usa rsl-qa-destroy` (optionally `--only <grupo>` to focus).

## Procedure

1. `pnpm -s qa:destroy` (whole run, about 30 s). It builds the sandbox in `/tmp`, runs every case and writes the report. Each step must end with `OK:` or `ERROR:`, with a coherent exit code, no traceback, and the expected keyword.
2. Read `qa/<carpeta>/qa-report.md`. For each failure, confirm it is a real bug and not a bad case (a wrong case is also reported, with suspect `scripts/qa-destroy.py`).
3. **New attacks** (at least 5, by hand, in your own sandbox: `pnpm -s qa:destroy --keep --no-report --only positivo` gives a ready `/tmp/rsl-qa-*` with themes). Pick attacks the harness does not cover yet; ideas:
   - inputs: very long or odd names, spaces or accents in paths, symlinks, read-only files, files that are directories;
   - content: huge files, markdown tables with `|` inside cells, questions with `?` inside, repeated headings;
   - flow: running a skill step twice, interrupting between two commands, dates in the future, deleting a picoc that the paper already used;
   - text rules: a skill or agent that contradicts another, or a step that can loop forever.
   Run each one and write it under `## Ataques propuestos` in `qa-report.md` and in `proposed` of `qa-report.json`, with `{id, comando, esperado, obtenido, por qué importa}`. Mark whether it broke something.
4. Do not change code, skills or fixtures, and never touch `docs/`.

## Cierre

- Failures or broken attacks: `ERROR: k de N casos fallaron (<ids>) y m ataques nuevos rompieron algo; reporte en qa/<carpeta>/. Próximo paso: rsl-qa-fix`.
- All green: `OK: N casos y m ataques nuevos sin fallos; reporte en qa/<carpeta>/. Próximo paso: rsl-qa-fix para convertir los ataques en casos, o seguir con el flujo RSL`.

## Forbidden

- Editing any file other than the new report; touching `docs/`; refreshing Graphify.
- Hiding a failure or softening the report.
