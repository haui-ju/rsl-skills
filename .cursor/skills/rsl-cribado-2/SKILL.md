---
name: rsl-cribado-2
description: PRISMA screening 2 step 1 — retrieval only. Reads resultados-<MARCO>-cribado-1.csv of the latest picoc, creates RSL/picoc/<fecha>-cribado-2-<MARCO>/ with documentos.json and documentos.md, downloads open-access PDFs by DOI into docs/pdf/<Id>-<titulo-slug>.pdf, updates prisma.json retrieval. Manual PDFs go in docs/pdf-draft/ (title-like filename) then rsl-cribado-2-alineamiento-pdfs. No MD or graph. Use when the user says rsl-cribado-2.
---

# rsl-cribado-2

Retrieval of reports for PRISMA 2020 screening 2 (full text). Subset of SI from `docs/<slug>/config.yml` → `cribado_2.use`: `all` (default, every SI including doubts), `solo_si` (SI without `duda` in `cribado-1.shadow.jsonl`), `solo_dudas` (SI with duda). The cribado-1 CSV is unchanged; only retrieval is filtered.

```text
docs/[titulo-breve]/
  config.yml                         (cribado_2.use — set before init/download; re-run init if you change it)
  picoc/<fecha>-<MARCO>/
    resultados-<MARCO>-cribado-1.csv   (read)
    prisma.json                        (retrieval.sought / not_retrieved)
  RSL/picoc/<fecha-base>-cribado-2-<MARCO>/
    documentos.json / documentos.md    (# = CSV order; enlaces DOI+descarga; descargado si|no; porque)
    docs/pdf/                          canonical PDFs
    docs/pdf-draft/                    user drops PDFs named ≈ article title
    docs/md/                           (empty until rsl-cribado-2-memoria)
```

Invoke: `Usa rsl-cribado-2 sobre docs/<slug>/`.

## Procedure

0. Read `cribado_2.use` in `config.yml` (or assume `all`). If the user wants only accepted-without-doubt or only doubts, they edit it **before** step 1.
1. `pnpm -s cribado2:init docs/<slug>` if `documentos.json` is missing (creates folders and the retrieval table for the filtered SI subset; `documentos.json` stores `cribado_2_use`, `si_total`, `si_retrieval`).
2. `pnpm -s cribado2:download docs/<slug>`. Requires `resultados-<MARCO>-cribado-1.csv` (else run `rsl-cribado-1-aplicar`). Open-access chain: Unpaywall, OpenAlex, Semantic Scholar, `citation_pdf_url`. Valid PDF only if `%PDF` and > 10 KB. E-mail: `UNPAYWALL_EMAIL` or `git config user.email`.
3. `documentos.md` lists each SI with **enlaces** (`[DOI](https://doi.org/…)` and `[PDF]` or `[descargar]` with the best open URL from the download attempt). For rows still `descargado: no`, the script fills `porque` (short, Spanish) — do not invent reasons in chat. To refresh the table from `documentos.json` without re-downloading: `pnpm -s cribado2:documentos docs/<slug>`.
4. Manual retrieval: user saves PDFs in `docs/pdf-draft/` with a filename close to the **title** (not the canonical `Id-slug` name), then `Usa rsl-cribado-2-alineamiento-pdfs` (or `pnpm -s cribado2:align`).
5. Chat: `cribado_2.use`, SI for retrieval vs SI in CSV, downloaded count, not retrieved, link to `documentos.md`, PRISMA retrieval line. If `download` warns that `use` changed, tell the user to run `cribado2:init` again. If pending, summarise `porque` patterns in one or two sentences. Then Cierre.

## Cierre

- Failure: `ERROR: <mensaje del script>. <cómo arreglarlo>`.
- Success: `OK: <d> de <n> PDF en RSL/picoc/<carpeta-cribado-2>/docs/pdf/ (<m> manuales/alineados, <x> no recuperados). Próximo paso: Usa rsl-cribado-2-memoria sobre docs/<slug>/` (or alineamiento if they only added drafts).

## Forbidden

- Paywalled bypass (Sci-Hub, shared credentials, captcha solvers).
- Editing `resultados-*-cribado-1.csv`, `picoc.md`, `documentos.json` or `documentos.md` by hand.
- MD conversion or Graphify (rsl-cribado-2-memoria).
- Saving cribado-2 PDFs under `RSL/PDF/` (informe corpus).
