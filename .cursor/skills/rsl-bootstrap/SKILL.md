---
name: rsl-bootstrap
description: >-
  Deja el entorno FIS listo tras clonar o en una máquina nueva: verifica e instala
  prerrequisitos (node/pnpm, pipx graphifyy, poppler), pnpm install del workspace
  y pnpm run bootstrap (grafo root + thesaurus IEEE + todos los temas docs/*).
  Use when the user says rsl-bootstrap, prepara el entorno, setup, o acaba de clonar el repo.
---

# rsl-bootstrap

Paso **0** del flujo: antes de `rsl-topic-panel` o cualquier skill que consulte Graphify.

Invocar esta skill **es** la autorización explícita para regenerar los tres grafos (root, thesaurus, temas).

## Procedure

1. Confirmar raíz del repo: `package.json` con script `bootstrap` y `pnpm-workspace.yaml`.
2. Prerrequisitos (comprobar cada uno con `command -v`; instalar solo lo que falte):

| Requisito | Check | Instalar |
|-----------|-------|----------|
| Node ≥ 18 | `node -v` | pedir al usuario (nvm / gestor del SO) |
| pnpm | `pnpm -v` | `corepack enable` (o `npm i -g pnpm`) |
| pipx | `pipx --version` | Arch `sudo pacman -S python-pipx` · Debian `sudo apt install pipx` · macOS `brew install pipx` |
| graphify | `graphify --help` y `~/.local/share/pipx/venvs/graphifyy/bin/python` | `pipx install graphifyy && pipx ensurepath` · luego `graphify install --platform cursor` |
| poppler | `pdftotext -v`, `pdftohtml -v`, `pdfinfo -v` | Arch `sudo pacman -S poppler` · Debian `sudo apt install poppler-utils` · macOS `brew install poppler` |

   Comandos con `sudo` o gestores del sistema: **pedir confirmación al usuario** antes de ejecutarlos (o que los corra él).
3. `pnpm install` (workspace root + `tools/*`).
4. `pnpm run bootstrap` → debe terminar con:

```text
PASS  root
PASS  thesaurus IEEE     (SKIP si falta global/thesaurus/IEEE.pdf)
PASS  temas docs/*
```

5. Si un tema falla con `needs_agent` (PDF sin texto legible): seguir la skill **graphify-theme** (etapa B agent-RAG) para ese tema y re-ejecutar `pnpm run bootstrap`.
6. Smoke opcional:

```bash
graphify query "skills rsl"
npm run thesaurus:lookup -- "Human computer interaction"
graphify query "cognitive accessibility" --graph docs/<slug>/graphify-out/graph.json
```

7. Chat: tabla requisito → ok/instalado/falta; resumen PASS/FAIL/SKIP; grafos generados; siguiente paso sugerido (`rsl-topic-panel` o el tema en curso).

## Notas

- No gasta tokens LLM: temas se reconstruyen desde `RSL/MD/*.md` + `index-manifest.json` (PDFs con mismo sha se saltan); thesaurus se parsea local.
- Idempotente: se puede re-ejecutar cuando cambien skills, `global/`, temas o PDFs.

## Forbidden

- `--force` en temas sin pedido explícito (re-extrae PDFs).
- Ejecutar `sudo` / instalar paquetes del sistema sin confirmación.
- Marcar el entorno como listo si el resumen tiene algún `FAIL`.
- Editar `topic.md`, `informe*`, `paper*` o PDFs.
