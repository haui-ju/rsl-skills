---
name: graphify-theme
description: >-
  Create or refresh Graphify memory for one docs/[titulo-breve] theme.
  Pipeline: prepare → agent-RAG if needed → build → verify. Tracks
  RSL/index-manifest.json. Use when user says graphify-theme.
---

# graphify-theme

Memoria **por tema** para que agentes consulten papers sin reabrir PDFs.

## Flujo (obligatorio)

```text
┌─────────────┐    needs_agent?     ┌──────────────┐
│ A  PREPARE  │ ────── yes ───────► │ B  AGENT RAG │
│  pdftotext  │                     │  MD detallado│
│  + structure│ ◄──── stamp ────────│  + headings  │
└──────┬──────┘                     └──────────────┘
       │ no pending
       ▼
┌─────────────┐     fail      ┌─────────────┐
│ C  BUILD    │ ────────────► │  stop/fix │
│  graphify   │               │  MD/heading │
└──────┬──────┘               └─────────────┘
       ▼
┌─────────────┐
│ D  VERIFY   │  ← tests de calidad (nodos, queries)
│  gates      │
└─────────────┘
```

| Stage | Comando | Qué hace |
|-------|---------|----------|
| **A** | `pnpm graphify:theme:refresh <slug> --prepare-only` | Diff vs `RSL/index-manifest.json`. Nuevos/cambiados PDF → texto + **MD con muchos `##`/`###`** (Graphify solo indexa headings). Skip si hash igual y ya indexado. Exit `2` si queda `needs_agent`. |
| **B** | Solo si `needs_agent` | Leer PDF, escribir `RSL/MD/<stem>.md` rico (≥8 headings), luego `--stamp-agent`. **No** re-leer lo `graphify_indexed` con mismo hash. |
| **C+D** | `pnpm graphify:theme:refresh <slug>` | Build grafo + **verify** (falla si papers quedan con <8 nodos o queries vacías). |
| Status | `pnpm graphify:theme:status <slug>` | Valida sin reconstruir: grafo al día (ningún MD/PDF/paper más nuevo) + gates de verify. |

## Layout

```text
docs/<slug>/
  informe.md / topic.md
  RSL/
    PDF/                  originales
    MD/                   corpus indexable (RAG)
    MD/_raw/              pdftotext crudo (debug)
    index-manifest.json   traza (no re-leer)
  graphify-out/           graph.json (gitignored)
```

## Procedure (cuando invocan la skill)

1. Resolver `docs/<slug>/` (preguntar si falta).
2. **A** — `pnpm graphify:theme:refresh <slug> --prepare-only`
3. Si exit 2 / `needs_agent`:
   - Para cada PDF pendiente: extraer texto, escribir MD con Metadata, Abstract, Keywords, Concept/Finding hooks (`###`), secciones `##`, cuerpo.
   - Stamp:
     ```bash
     # usar el mismo python del pipeline (pipx graphifyy)
     ~/.local/share/pipx/venvs/graphifyy/bin/python \
       scripts/graphify-theme-offline.py docs/<slug> \
       --stamp-agent "RSL/PDF/<file>.pdf" \
       --stamp-notes "agent-rag"
     ```
4. **C+D** — `pnpm graphify:theme:refresh <slug>` (debe exit 0).
5. Opcional — `pnpm graphify:theme:status <slug>` (debe dar PASS).
6. Chat: slug, nodos, manifest, skipped vs nuevos, `needs_agent` restantes, path del grafo.

`--force` solo si el usuario pide rebuild total.

## Lookup (después de PASS)

```bash
graphify query "<q>" --graph docs/<slug>/graphify-out/graph.json
graphify explain "<concept>" --graph docs/<slug>/graphify-out/graph.json
```

Preferir grafo / `RSL/MD/*` sobre `RSL/PDF/*`.

## Por qué locators (página + ancla)

Graphify AST **solo crea nodos desde headings**. Por eso el prepare no deja el PDF como muro de texto:

1. `RSL/MD/_raw/<stem>.txt` — texto crudo **con `===== PDF PAGE N =====`**
2. `RSL/MD/<stem>.md` — técnica **locator index**:
   - tabla `Kind | Label | PDF page | MD anchor`
   - chunks `### [PDF p.N] …` (nodo Graphify + página del PDF)
   - concepts/findings/sections con la misma forma
3. El agente consulta el grafo; si necesita el original, abre `RSL/PDF/…` en la **página** del locator (sin releer todo).

## Forbidden

- Refresh root (`graphify-root`).
- Skip verify.
- Re-leer PDF ya `graphify_indexed` (mismo sha) sin `--force`.
- Marcar `graphify_indexed` si verify falla.
