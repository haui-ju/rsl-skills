---
name: rsl-cribado-1-aplicar
description: After the user approves the report of rsl-cribado-1, writes resultados-<MARCO>-cribado-1.csv — the unified Scopus and Web of Science CSV with two more columns at the end, «¿Se acepta?» (SI or NO) and «Justificación cribado 1» — from cribado-1.shadow.jsonl, and closes PRISMA screening 1. Decides nothing and never edits the exports or the unified CSV. Use when the user says rsl-cribado-1-aplicar or approves the screening.
---

# rsl-cribado-1-aplicar

Closes the first screening (title, abstract and keywords). Only after the user has read `picoc/<carpeta>/cribado-1.md` and approved it; corrections belong to `rsl-cribado-1` (`cribado:set`), not here.

```text
docs/[titulo-breve]/picoc/<fecha>-<MARCO>/
  resultados-<MARCO>.csv             (read; never edited)
  cribado-1.shadow.jsonl + cribado-1.md   (read)
  resultados-<MARCO>-cribado-1.csv   (the only output)
```

Invoke: `Usa rsl-cribado-1-aplicar sobre docs/<slug>/`.

## Procedure

1. `pnpm -s cribado:apply docs/<slug>`. It checks that the exports and the unified CSV did not change since `cribado:prepare` and that `cribado-1.md` and the shadow are up to date with the decisions; then it writes `resultados-<MARCO>-cribado-1.csv`: the unified columns and rows in the same order, plus `¿Se acepta?` (SI or NO) and `Justificación cribado 1` (motive and criteria only — never a `Duda:` prefix; SI with duda stays `SI` and the doubt is in `cribado-1.md` / `cribado-1.shadow.jsonl`; duplicates say which record and base they repeat).
2. ERROR «no están al día» → `pnpm -s cribado:report docs/<slug>`, tell the user the report changed and ask them to review it again; do not apply until they approve.
3. Chat: SI and NO counts, the path of the new CSV and the PRISMA line of the report (for the paper's selection section). Then the Cierre line.

## Cierre

The last message of the skill is exactly one line:

- Failure: `ERROR: <mensaje del script>. <cómo arreglarlo>`.
- Everything went well: `OK: picoc/<carpeta>/resultados-<MARCO>-cribado-1.csv con <n> registros (SI <a>, NO <b>). Próximo paso: Usa rsl-cribado-2 sobre docs/<slug>/ (descarga los PDF de los SI)`.

## Forbidden

- Applying without the user's approval of the current report.
- Changing any decision (that is `rsl-cribado-1` with `cribado:set`), editing the exports or the unified CSV, or writing the columns by hand.
