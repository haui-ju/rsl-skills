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
  paper/paper.yml       (formato.marco; created with --init if missing — default PICOCT)
  picoc/<fecha>-<MARCO>/picoc.md   (via rsl-picoc — marco, palabras clave, RQ, queries)
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

Spanish **académico-profesional** following `playbooks/redaccion-academica.md` (R1 texto final sin notas de trabajo, R2 siglas definidas y dosificadas, R3 una idea por oración, R4 sin notación ×/+/-duro en la prosa, R5 citas ↔ tabla de la sección 3, R6 título breve). Tables only where the template requires them. The template's instructions are HTML comments: never copy them as visible text.

## Project sources

- `global/lineas-utp.md`
- `global/competencias.md`
- `playbooks/vocabulario-controlado.md` — **protocolo obligatorio** para PICOC y palabras clave (thesaurus IEEE)
- Optional prior verdict: `docs/[titulo-breve]/topic.md`

## Procedure (required)

1. Resolve folder `docs/[titulo-breve]/` (same theme as `topic.md` if it exists). Ensure `RSL/PDF/` exists.
2. Normalize título / problemática / objeto (may use afilado from `topic.md` if user agrees or verdict was GO_con_cambios).
3. **Marco configurado:** `pnpm -s picoc:latest docs/[titulo-breve]`. Si no existe `paper/paper.yml` → `pnpm -s paper:status docs/[titulo-breve] --init` (queda `marco: PICOCT`, salvo que el usuario haya pedido PICO o PICOC: entonces editar `formato.marco`).
4. **Up to 3 SLRs** (mínimo 2 revisiones; si no hay, mínimo 5 originales con antigüedad menor a 5 años). Download PDFs into `RSL/PDF/`. If fewer, add Scopus queries / placeholders. Never invent DOI/PDF.
5. Sections 4–7 (section 4 ≤ 300 words, citing the reviews of section 3; section 7 = título breve per R6).
6. Write `informe.md` with the **exact 7-point structure** below (sección 2 = solo el enlace al picoc).
7. **Marco de búsqueda:** ejecutar la skill **`rsl-picoc`** (lee y sigue `.cursor/skills/rsl-picoc/SKILL.md`): pregunta general = § 1.2 recién escrita, versión nueva en `picoc/<hoy>-<MARCO>/`, `picoc:lint` PASS y enlace de la sección 2 actualizado. Si falta el thesaurus → pedir `Usa rsl-bootstrap`; no inventar descriptores.
8. Chat: paths (`informe.md`, versión de `picoc/` + resultado del lint), SLRs found, queries pending, PDFs present/missing under `RSL/PDF/`.
9. Chat — **siguientes pasos** (no ejecutarlos aquí). Cerrar con:

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

Las palabras clave, el marco PICOCT (población, intervención, comparación, resultado, contexto y tiempo) y las queries se encuentran en [picoc/<carpeta>/picoc.md](picoc/<carpeta>/picoc.md).

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

## Forbidden

- Datetime folders; root `ficha_NNN.md`.
- Launching polish agents (only suggest the invoke command in chat).
- Leaving SLR PDFs outside `RSL/PDF/`.
- Omitting keywords/query when SLRs are missing.
- Keywords/PICOC sin `thesaurus:check`, o presentar como descriptor IEEE un término LIBRE / no preferido.
- Tablas PICOC, keywords o queries dentro de `informe.md` (van en `picoc/<fecha>-<MARCO>/picoc.md`; sección 2 solo enlaza).
- Escribir el picoc a mano en vez de usar `rsl-picoc`; entregar con `picoc:lint` en FAIL.
- Colloquial prose in narrative sections.
- Entregar con `pnpm -s redaccion:lint docs/[titulo-breve]/informe.md` en FAIL: marcas editoriales (`[citar]`, `TODO`, `PENDIENTE`…), huellas internas (`topic.md`, panel, veredicto, `GO_*`, skills, rutas, "Nota de artefacto") o siglas sin definir.
- Obras citadas en la prosa que no están en la tabla de la sección 3 (`pnpm -s paper:status docs/[titulo-breve] --cites docs/[titulo-breve]/informe.md` → PASS).
- Collapsing 1.1 / 1.2 / 1.3 into three top-level sections numbered 1–3.
