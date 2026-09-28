---
name: rsl-make-report
description: >-
  Builds a UTP RSL report at docs/[short-title]/informe.md from a free topic
  (reuse the same folder as topic.md if the theme matches). Keywords, up to 3
  SLRs or Scopus queries, UTP sections 1–7, PDFs under RSL/PDF/. Use when
  the user says rsl-make-report. Does not run the 4-agent polish debate.
---

# rsl-make-report

Receive a research topic and write a UTP `informe.md` in the theme folder. Single proposer flow: no polish agents, no topic panel.

```text
docs/[titulo-breve]/
  topic.md              (optional, from rsl-topic-panel)
  informe.md            (this skill)
  paper/paper.yml       (formato.marco; --init if missing, default PICOCT)
  picoc/<fecha>-<MARCO>/picoc.md   (via rsl-picoc)
  RSL/PDF/              (SLR PDFs only, never next to .md)
```

Invoke with `Título / Problemática / Objeto de estudio / Carrera`, or `Usa rsl-make-report sobre docs/<slug>/` (reuses the folder and `topic.md`). No topic and no folder → ask; never invent a topic. Slug: 3–6 words, lowercase, hyphenated.

Writing: `playbooks/redaccion-academica.md` (Spanish académico-profesional). Template instructions are HTML comments: never copy them as visible text. Sources: `global/lineas-utp.md`, `global/competencias.md`, `topic.md` if present.

## Procedure

1. Resolve `docs/<slug>/` (same folder as `topic.md` for the same theme); create `RSL/PDF/`.
2. Normalize título / problemática / objeto (the sharpened version of `topic.md` if the verdict was GO_con_cambios or the user agrees).
3. `pnpm -s picoc:latest docs/<slug>`; no `paper.yml` → `pnpm -s paper:status docs/<slug> --init`, then set `formato.marco` if the user asked for another framework. ERROR (unknown letter) → stop and report it.
4. **Up to 3 SLRs** (at least 2 reviews; otherwise at least 5 primary studies from the last 5 years). PDFs into `RSL/PDF/`, referenced as `RSL/PDF/<file>.pdf`. Paywall → mark missing, keep DOI and Scopus query. Never invent DOI or PDF.
5. Write `informe.md` with the exact 7 points below (section 4 ≤ 300 words citing section 3; section 7 = short title; section 2 = only the picoc link).
6. Run **`rsl-picoc`** (full mode; general question = the new § 1.2). Missing thesaurus → ask for `Usa rsl-bootstrap`.
7. `pnpm -s redaccion:lint docs/<slug>/informe.md` (0 FAIL) and `pnpm -s paper:status docs/<slug> --cites docs/<slug>/informe.md` (PASS); fix and repeat.
8. Chat: SLRs found, pending queries and PDFs present or missing (do not run the next skills; no Graphify refresh here), then the Cierre line.

## File template (`informe.md`)

Exactly these 7 UTP points (do not invent a separate “paso 8” inside the file):

```markdown
# Informe RSL — [Título corto]

## 1. Tema de la investigación elegido para la RSL

### 1.1 Tema
...

### 1.2 Problemática
...

### 1.3 Objeto de estudio
...

## 2. Palabras clave

Las palabras clave, el marco <MARCO> (<componentes en palabras>) y las queries se encuentran en [picoc/<carpeta>/picoc.md](picoc/<carpeta>/picoc.md).

## 3. Artículos de revisión de literatura relacionados con el tema de investigación

<!-- Mínimo 2 artículos de revisión o, de no existir éstos, mínimo 5 artículos científicos originales con antigüedad menor a 5 años. Meta recomendada: 3 RSL. -->

| Referencia bibliográfica (APA) | DOI / URL | Razón | PDF |
|--------------------------------|-----------|-------|-----|
| ... o Pendiente | DOI | ... | `RSL/PDF/...` o Pendiente |

**Queries Scopus para completar RSL faltantes:**
\`\`\`
...
\`\`\`

## 4. Estado del conocimiento y necesidad de una nueva RSL

<!-- ≤ 300 palabras; prosa profesional; cita aquí (Autor, año) las revisiones de la sección 3 -->

## 5. Línea(s) de investigación de la UTP

<!-- Señale la(s) línea(s) a la que responde la investigación propuesta, con justificación: cómo el tema se asemeja y justifica con las líneas UTP. -->

## 6. Competencias de la carrera

<!-- Señale las competencias relacionadas con el tema, con justificación. -->

## 7. Título tentativo de la RSL

<!-- Título breve (≤ 20 palabras, sin subtítulo en cascada); será la base del título del paper. -->
...
```

## Cierre

The last message of the skill is exactly one line:

- Stop at the first failure (any script returns `ERROR:`, `rsl-picoc` ends in ERROR, or `redaccion:lint` / `--cites` keep failing): `ERROR: <paso y script que falló, con su mensaje>. <cómo arreglarlo>`. Do not continue with later steps.
- Everything went well: `OK: informe docs/<slug>/informe.md con <n> revisiones y marco <MARCO> en picoc/<carpeta>/. Próximo paso: Usa graphify-theme sobre docs/<slug>/ y luego Usa rsl-polish-report sobre docs/<slug>/informe.md`.

## Forbidden

- Datetime folders; root `ficha_NNN.md`; SLR PDFs outside `RSL/PDF/`.
- Launching polish agents (only suggest the command).
- Omitting queries when SLRs are missing.
- Framework tables, keywords or queries inside `informe.md`; writing the picoc by hand instead of `rsl-picoc`.
- Collapsing 1.1 / 1.2 / 1.3 into top-level sections.
- Delivering with `redaccion:lint` FAIL, `--cites` FAIL or `picoc:lint` FAIL.
