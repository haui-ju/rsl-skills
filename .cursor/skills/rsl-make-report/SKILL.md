---
name: rsl-make-report
description: >-
  Builds a UTP RSL report at docs/[short-title]/informe.md from a free topic
  (reuse the same folder as topic.md if the theme matches). Keywords, up to 3
  SLRs or Scopus queries, UTP sections 1–7, PDFs under RSL/PDF/. Use when
  the user says rsl-make-report. Does not run the 4-agent polish debate.
---

# rsl-make-report

## Goal

Receive a research topic and write a polished UTP `informe.md` in the theme folder. Single proposer flow. Do **not** call `rsl-polish-report` agents here. Do **not** mix with `rsl-topic-panel` logic beyond reusing the folder.

## Output path (required)

```text
docs/[titulo-breve]/
  topic.md              (optional, from rsl-topic-panel)
  informe.md            (this skill)
  picoc.md              (this skill — marco PICO/PICOC/PICOCT, palabras clave, RQ, queries)
  RSL/
    PDF/                (SLR PDFs only — never next to .md)
```

Same theme as an existing panel → **reuse** that folder (where `topic.md` already lives).

Slug: 3–6 words, lowercase, hyphenated. If the user points to an existing `docs/.../topic.md`, use that folder.

### PDFs (required)

- Store every downloaded SLR PDF under `docs/[titulo-breve]/RSL/PDF/`.
- Create the folder if missing. Do **not** leave PDFs in the theme root (keeps token-heavy binaries out of the markdown workspace; the user may later convert PDF → MD with another tool under `RSL/`).
- In `informe.md`, reference PDFs as `RSL/PDF/<filename>.pdf`.
- Never invent DOI/PDF. If a PDF cannot be downloaded (paywall), note it as missing and keep the DOI + Scopus query.

## Invoke

```text
Usa rsl-make-report

Título: ...
Problemática: ...
Objeto de estudio: ...
Carrera: Ingeniería de Software
```

Or: `Usa rsl-make-report sobre docs/ia-pipelines-amenazas/` (reuse folder + read `topic.md` if present).

No topic and no folder → ask. Do not invent a topic.

## Writing style (required)

Spanish **académico-profesional** with connectors; cohesive paragraphs; no colloquial tone. Tables only where the template requires them.

## Project sources

- `global/lineas-utp.md`
- `global/competencias.md`
- `playbooks/vocabulario-controlado.md` — **protocolo obligatorio** para PICOC y palabras clave (thesaurus IEEE)
- Optional prior verdict: `docs/[titulo-breve]/topic.md`

## Procedure (required)

1. Resolve folder `docs/[titulo-breve]/` (same theme as `topic.md` if it exists). Ensure `RSL/PDF/` exists.
2. Normalize título / problemática / objeto (may use afilado from `topic.md` if user agrees or verdict was GO_con_cambios).
3. **`picoc.md` (always)** — archivo aparte, con la plantilla y las reglas R1–R3 de `playbooks/vocabulario-controlado.md`:
   - Marco según el tema (PICO / PICOC / PICOCT; ver tabla del playbook).
   - Pregunta general = problemática; **1 sub-pregunta por componente** (T incluido) con su dato a extraer.
   - Cada término con `Origen en el tema` (título / problemática / objeto); nada genérico ni “porque existe en IEEE”.
   - **Una** llamada `pnpm -s thesaurus:check "…" "…"`; descriptor preferido (USE si era no preferido); LIBRE marcado y justificado.
   - Tabla de búsqueda **1:1** con los bloques de las queries **Scopus, Web of Science e IEEE Xplore** (mismos términos, mismo N). C/O fuera de la query → tabla de cribado.
   - `pnpm -s picoc:lint docs/[titulo-breve]/picoc.md` → **PASS** antes de seguir.
   - Si falta el grafo del thesaurus → pedir `Usa rsl-bootstrap`; no inventar descriptores.
4. **Up to 3 SLRs** (mínimo 2 revisiones; si no hay, mínimo 5 originales con antigüedad menor a 5 años). Download PDFs into `RSL/PDF/`. If fewer, add Scopus queries / placeholders. Never invent DOI/PDF.
5. Sections 4–7 (section 4 ≤ 300 words; **citar las RSL de la sección 3**).
6. Write `informe.md` with the **exact 7-point structure** below (sección 2 = solo el enlace a `picoc.md`).
7. Chat: paths (`informe.md`, `picoc.md` + resultado del lint), SLRs found, queries pending, PDFs present/missing under `RSL/PDF/`.
8. Chat — **siguientes pasos** (no ejecutarlos aquí). Cerrar con:

```text
Usa graphify-theme sobre docs/[titulo-breve]/
```

```text
Usa rsl-polish-report sobre docs/[titulo-breve]/informe.md
```

Do **not** run Graphify refresh from this skill (user owns **graphify-theme** / **graphify-root**).

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

Las palabras clave, el marco PICOCT y las queries se encuentran en [picoc.md](picoc.md).

## 3. Artículos de revisión de literatura relacionados con el tema de investigación

*(Mínimo 2 artículos de revisión o, de no existir éstos, mínimo 5 artículos científicos originales con antigüedad menor a 5 años. Meta recomendada: 3 RSL.)*

| Referencia bibliográfica (APA) | DOI / URL | Razón | PDF |
|--------------------------------|-----------|-------|-----|
| ... o Pendiente | DOI | ... | `RSL/PDF/...` o Pendiente |

**Queries Scopus para completar RSL faltantes:**
\`\`\`
...
\`\`\`

## 4. Estado del conocimiento y necesidad de una nueva RSL

(≤ 300 palabras; prosa profesional; **citar aquí las revisiones de la sección 3**)

## 5. Línea(s) de investigación de la UTP

(Señale la(s) línea(s) a la que responde la investigación propuesta, **con justificación**: cómo el tema se asemeja y justifica con las líneas UTP.)

## 6. Competencias de la carrera

(Señale las competencias relacionadas con el tema, **con justificación**.)

## 7. Título tentativo de la RSL

(Será ajustado a medida que se desarrolle la investigación.)
...
```

## Forbidden

- Datetime folders; root `ficha_NNN.md`.
- Launching polish agents (only suggest the invoke command in chat).
- Leaving SLR PDFs outside `RSL/PDF/`.
- Omitting keywords/query when SLRs are missing.
- Keywords/PICOC sin `thesaurus:check`, o presentar como descriptor IEEE un término LIBRE / no preferido.
- Tablas PICOC, keywords o queries dentro de `informe.md` (van en `picoc.md`; sección 2 solo enlaza).
- Tabla y query con términos distintos o distinto N; términos sin origen en el tema; componentes sin sub-pregunta.
- Entregar `picoc.md` sin `picoc:lint` PASS.
- Colloquial prose in narrative sections.
- Collapsing 1.1 / 1.2 / 1.3 into three top-level sections numbered 1–3.
