---
name: rsl-make-paper
description: >-
  Builds docs/[short-title]/paper.md — full academic Introduction for the RSL
  (context, definitions, evidence state of the art, problem, justification,
  objective, organization). Uses topic.md, ficha/informe, Graphify theme memory
  and RSL/MD. Use when the user says rsl-make-paper. Does NOT launch the 4-agent
  debate (that is rsl-polish-paper).
---

# rsl-make-paper

## Goal

Write a complete **Introducción** of the RSL paper as `paper.md` in the theme folder. Single proposer flow (draft listo para pulir). Do **not** launch `critico-rsl` / `defensor-rsl` / `impacto-social-rsl` / `viabilidad-negocio-rsl` here — that is **`rsl-polish-paper`**.

## Output path (required)

```text
docs/[titulo-breve]/
  topic.md                 (from rsl-topic-panel — debate + consenso)
  ficha.md                 (optional alias; see Inputs)
  informe.md               (from rsl-make-report)
  informe-polish.md        (from rsl-polish-report — preferred ficha)
  paper.md                 (THIS skill)
  RSL/PDF/  RSL/MD/        (SLR corpus)
  graphify-out/            (theme memory — lookup only)
```

Same theme → **reuse** the existing folder. Slug: 3–6 words, lowercase, hyphenated.

## Inputs (required package)

Resolve in this order; **ask** if the theme folder is missing:

| Input | Role |
|-------|------|
| `topic.md` | Debate 4 agentes, veredicto, tema final, exclusiones |
| **Ficha** | Prefer `informe-polish.md` → else `informe.md` → else `ficha.md` (user may attach `ficha.md`) |
| Graphify | `graphify query … --graph docs/[tema]/graphify-out/graph.json` |
| `RSL/MD/*.md` | Locators + texto indexable (prefer over raw PDF) |
| User attachments | Extra PDF/MD of SLRs the user found — if PDF, place under `RSL/PDF/` (do not leave in theme root); suggest `graphify-theme` if new files need indexing |

Never invent DOI/findings. Cite only what topic/ficha/Graphify/MD support.

## Invoke

```text
Usa rsl-make-paper sobre docs/ia-inclusion-cognitiva-software/
```

## Writing style (required)

Spanish **académico-profesional**; connectors; cohesive paragraphs; **APA 7** in-text (`Autor, año`). No colloquial tone.

**Citas — hard rules:** never put `` `topic.md` ``, `informe.md`, “panel”, “GO_con_cambios”, skill names, or repo paths in the visible paper text. Those files are **internal inputs** only.

### Maximal useful expansion (required)

`paper.md` is the **rich draft** so `rsl-polish-paper` can compact with substance. **Explayarse al máximo útil:**

- Prefer **more** evidence paragraphs over a thin summary: for each anchor SLR, state *qué cubre*, *n/DOI*, *qué no cubre* (= hueco propio).
- Pull findings from Graphify / `RSL/MD` locators (`[PDF p.N]`); quote or paraphrase only what the source supports.
- Include frontiers (Xu, Paiva, Bi, normas, W3C) in-text when they delimit the topic.
- Fill every subsection of the template; do not leave stubs.
- Optional draft `## Referencias` (3 RSL ancla, APA 7) at the end.

**Do not:** invent findings, dump full PDFs, or pad with empty repetition. Every extra paragraph must add citation, delimitation, metric, ethic, or SE-process detail.

`paper.md` **may be long and numbered** (1.1, 2.3…). Camera-ready compact form = **`paper-polish.md`**.

### Problemática = pregunta (required)

Align the research problem with the ficha: the **problemática is an interrogative** (*¿Cómo…? / ¿En qué medida…?*). In §2 you may explain *why it arises* (trends, gaps, regulation), but the formulated problem itself remains a **question**. State that question explicitly in §2.4 (or §2 opening) so polish can lift it to the header.

## Procedure (required)

1. Resolve `docs/[titulo-breve]/`. Prefer folder of existing `topic.md` / `informe.md`.
2. Read **ficha** (`informe-polish.md` | `informe.md` | `ficha.md`) + `topic.md` (tema final, GO_*, exclusiones) — internal only.
3. **Graphify first** (if `graphify-out/graph.json` exists):
   ```bash
   graphify query "<pregunta>" --graph docs/[titulo-breve]/graphify-out/graph.json
   ```
   Prefer `RSL/MD/` chunks via locators; do **not** dump full PDFs. Do **not** refresh Graphify unless the user asks.
4. If Graphify missing/stale and user attached new RSL files → suggest `Usa graphify-theme sobre docs/[tema]/`; still write `paper.md` from available sources.
   **Términos técnicos (§1.1 Definiciones, §5 método):** reutilizar los descriptores de la sección 2 de la ficha; si aparece un término EN nuevo, validarlo con `pnpm -s thesaurus:check "…"` (`playbooks/vocabulario-controlado.md`). En el texto visible no citar el thesaurus como fuente de la definición; en §5 sí declarar que las cadenas usan vocabulario controlado IEEE + términos libres.
5. Write **`paper.md`** with the **exact section structure** below — **maximal useful expansion**.
6. Chat: path, sources, next step `Usa rsl-polish-paper sobre docs/[titulo-breve]/paper.md`

## File template (`paper.md`)

```markdown
# Introducción — [Título de la RSL]

## 1. Contexto
### 1.1 Definiciones generales
…

### 1.2 Lo que se sabe del tema hasta la fecha
(Basado en evidencias / citas de las RSL ancla y frontera — rico)

### 1.3 Situación actual y disputas
…

## 2. El problema
(Abrir o cerrar con la **problemática en forma de pregunta**)

### 2.1 Tendencias o nuevas perspectivas
…

### 2.2 Discrepancias existentes
…

### 2.3 Vacíos de conocimiento
…

### 2.4 Contraste: situación actual vs situación deseada
(Qué se propone estudiar; enfatizar contraste; **reformular la pregunta**)

## 3. Justificación
### 3.1 Justificación de la elección del tema
…

### 3.2 Utilidad de los resultados de la revisión
…

### 3.3 Necesidad de una RSL
…

## 4. Objetivo de la RSL
(Respuesta operativa a la pregunta; unión problema ↔ fronteras)

## 5. Organización del contenido de la revisión
…

## Referencias
(Opcional borrador: 3 RSL ancla APA 7)
```

## Forbidden

- Launching the 4 polish agents.
- Overwriting `informe.md` / `informe-polish.md` / `topic.md`.
- Inventing citations or DOI.
- Citing `topic.md`, panel verdicts, or repo paths in the paper body.
- Dumping full PDFs when Graphify / `RSL/MD` exists.
- Refreshing Graphify unless the user explicitly asks.
- Saving outside `docs/[titulo-breve]/`.
- Thin stub sections “to polish later”.
- Expecting `paper.md` to be camera-ready (`paper-polish.md`).
