---
name: rsl-qa-fix
description: >-
  Fixes the bugs of the latest qa:destroy report (qa/<fecha>[-n]/qa-report.json): root
  cause in scripts, skills or agents, a minimal fix, and a regression case in
  scripts/qa-destroy.py; proposed attacks become new cases. Re-runs qa:destroy until OK
  and writes qa-fix.md in the report folder. Use when the user says rsl-qa-fix or after
  rsl-qa-destroy reports ERROR.
---

# rsl-qa-fix

Repairs what `rsl-qa-destroy` found. Every fix leaves a case that would have caught it.

Invoke: `Usa rsl-qa-fix` (latest report) or `Usa rsl-qa-fix sobre qa/<carpeta>/`.

## Procedure

1. Read the latest `qa/<carpeta>/qa-report.json`. No report, or no failures and no proposed attacks → stop with ERROR (see Cierre).
2. Group failures by suspect file. For each one:
   - reproduce it (the step's `cmd` runs as is inside `pnpm -s qa:destroy --keep --no-report --verbose --only <grupo | ids como D21,M16>`);
   - find the root cause and apply the minimal fix in the script, skill or agent (respect the OK/ERROR contract of `scripts/rsl_out.py`: one final line, coherent exit code, no traceback);
   - if the case itself was wrong, fix the case and say so; never weaken an assertion only to make it pass.
3. Turn each proposed attack into a case in `scripts/qa-destroy.py` (right group, next free id), then fix what it breaks.
4. `pnpm -s qa:destroy` (writes a new report) until `OK:`. At most 3 rounds; if something still fails, stop and report it.
5. Check that the real themes are untouched: `pnpm -s picoc:lint docs/<slug>` and `pnpm -s paper:status docs/<slug>` for each theme in `docs/` (no new versions).
6. Write `qa-fix.md` in the report folder you started from: one row per bug `| id | causa | arreglo | archivos | caso de regresión |` and the id of the new green report.

## Cierre

- Everything fixed: `OK: k bugs arreglados y m casos nuevos; qa:destroy en verde (qa/<nuevo>/). Próximo paso: rsl-qa-destroy para otra ronda, o seguir con el flujo RSL`.
- Something left or no input: `ERROR: <ids> siguen fallando (<motivo>) | no hay reporte con fallos; corre rsl-qa-destroy`.

## Forbidden

- Deleting or relaxing cases to turn the run green; editing fixtures to hide a bug (update them only when a rule changed on purpose, and say so).
- Touching `docs/`; refreshing Graphify; changing behavior not related to a reported bug.
