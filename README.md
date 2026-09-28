# FIS — Skills RSL + Graphify

Nomenclatura skills: `rsl-*` / `graphify-*` (inglés).

## Paso 0 — Preparar el entorno (recién clonado / máquina nueva)

```text
Usa rsl-bootstrap
```

El agente verifica/instala prerrequisitos (node + pnpm, pipx graphifyy, poppler), corre `pnpm install` y `pnpm run bootstrap` (grafo root + thesaurus IEEE + todos los temas) y reporta PASS/FAIL. A mano: ver [Clonar en otra máquina](#clonar-en-otra-máquina).

## Skills RSL

| Skill | Qué hace | Salida |
|-------|----------|--------|
| `rsl-bootstrap` | Paso 0: deja el entorno y todos los grafos Graphify listos | `graphify-out/` · `global/thesaurus/graphify-out/` · `docs/*/graphify-out/` |
| `rsl-topic-panel` | Estresa un tema (4 agentes + debate Mermaid + consenso) | `docs/[titulo-breve]/topic.md` |
| `rsl-make-report` | Genera el informe UTP (7 puntos) | `docs/[titulo-breve]/informe.md` |
| `rsl-polish-report` | Pule el informe (4 agentes) | `docs/[titulo-breve]/informe-polish.md` |
| `rsl-make-paper` | Genera la **Introducción** borrador (sin agentes; APA 7; puede ir larga con §1.1…) | `docs/[titulo-breve]/paper.md` |
| `rsl-polish-paper` | Pule la Introducción (4 agentes) → texto limpio + traza de debate | `paper-polish.md` + `paper-debate.md` |

## Skills Graphify (memoria — **tú** las ejecutas)

Los agentes `rsl-*` **no** regeneran Graphify solos. Tú invocas la skill cuando quieras actualizar la memoria. Las skills de paper **sí consultan** el grafo (`query`) para gastar menos tokens.

| Skill | Qué hace | Salida |
|-------|----------|--------|
| `graphify-root` | Crea/actualiza el grafo del **repo** | `graphify-out/` |
| `graphify-theme` | Crea/actualiza el grafo de **un tema** | `docs/[titulo-breve]/graphify-out/` |

Mismo tema → **misma carpeta**:

```text
docs/[titulo-breve]/
  topic.md
  informe.md
  informe-polish.md
  paper.md
  paper-polish.md        ← tema / problemática / objetivo + Intro fluida + 3 refs APA
  paper-debate.md        ← Mermaid + turnos (no va al documento)
  ficha.md               ← opcional (si la adjuntas; si no, se usa informe-polish/informe)
  RSL/
    PDF/                 ← originales
    MD/                  ← corpus indexable (RAG + headings + locators)
    index-manifest.json  ← traza (no re-lee lo indexado)
  graphify-out/          ← grafo del tema (gitignored)
```

Root (proyecto):

```text
graphify-out/     ← memoria Graphify del repo (skills, global/, playbooks/, README…)
global/           ← archivos generales que integra el usuario (líneas UTP, competencias, thesaurus)
playbooks/        ← protocolos compartidos que siguen varias skills (p. ej. vocabulario-controlado.md)
```

Agentes: `.cursor/agents/` (`critico-rsl`, `defensor-rsl`, `impacto-social-rsl`, `viabilidad-negocio-rsl`)

---

## Cómo ejecutar

### Estresar tema

```text
Usa rsl-topic-panel con este tema:

Título: ...
Problemática: ...
Objeto de estudio: ...
```

### Crear informe UTP

```text
Usa rsl-make-report sobre docs/[titulo-breve]/
```

### Pulir informe UTP

```text
Usa rsl-polish-report sobre docs/[titulo-breve]/informe.md
```

### Crear Introducción del paper (sin agentes)

Usa `topic.md` + ficha (`informe-polish.md` / `informe.md` / `ficha.md`) + Graphify + `RSL/MD/`.

```text
Usa rsl-make-paper sobre docs/ia-inclusion-cognitiva-software/
```

Salida: `paper.md` (borrador con Contexto…Organización numerados; **no** citar `topic.md` en el texto).

### Pulir Introducción del paper (4 agentes)

```text
Usa rsl-polish-paper sobre docs/[titulo-breve]/paper.md
```

Salidas:
- `paper-polish.md` — **Tema / Problemática (pregunta ¿…?) / Objetivo**; luego H2 en orden: **Contexto → El problema → Justificación → Objetivo de la RSL → Organización** (1–varios párrafos por bloque, sin 1.1/2.3); al final **Referencias** APA 7 de las **3 RSL ancla**.
- `paper-debate.md` — Mermaid + turnos del debate.

### Memoria Graphify — root

```text
Usa graphify-root
```

```bash
npm run graphify:refresh
```

### Memoria Graphify — tema (pipeline A→D)

```text
Usa graphify-theme sobre docs/ia-inclusion-cognitiva-software/
```

| Stage | Acción |
|-------|--------|
| **A prepare** | Diff `index-manifest.json` → `pdftotext` + MD estructurado (`##`/`###` + locators). Skip si ya indexado. |
| **B agent-RAG** | Solo si `needs_agent` (PDF ilegible / pocos headings). |
| **C build** | Grafo AST en `graphify-out/`. |
| **D verify** | Gates: ≥8 nodos/paper, queries smoke, informe/topic. |

```bash
npm run graphify:theme -- ia-inclusion-cognitiva-software
npm run graphify:theme:test -- ia-inclusion-cognitiva-software
```

Consulta (después de PASS):

```bash
graphify query "digital accessibility" --graph docs/ia-inclusion-cognitiva-software/graphify-out/graph.json
```

### Thesaurus IEEE (vocabulario controlado para PICO / keywords)

`global/thesaurus/IEEE.pdf` (IEEE Thesaurus 2019, 594 págs., ~10.4k términos) **no** se indexa en el root: tiene grafo propio con relaciones BT/NT/RT/USE. Parse local por fuentes del PDF (negrita = preferido, cursiva = no preferido); 0 tokens LLM.

```bash
npm run thesaurus:ieee                              # PDF → ieee-thesaurus.json + graphify-out/graph.json
pnpm -s thesaurus:check "machine learning" "autism" "large language models"   # tabla lista para PICOC
npm run thesaurus:lookup -- "Human computer interaction"
graphify explain "Assistive technology" --graph global/thesaurus/graphify-out/graph.json
graphify path "Machine learning" "Usability" --graph global/thesaurus/graphify-out/graph.json
```

Aristas: `broader` (BT) · `narrower` (NT) · `related` (RT) · `use` (no preferido → preferido). Cada nodo lleva `p.N` del PDF.
Si un concepto **no** aparece (p. ej. *Accessibility*, *Neurodiversity*, *LLM* en la edición 2019) se declara vacío de vocabulario y se usa término libre — no inventar descriptor IEEE.
Derivados gitignored (licencia CC BY-NC-ND).

**Protocolo en las skills:** `rsl-topic-panel` (tópicos), `rsl-make-report` (PICOC + keywords + query), `rsl-polish-report` (auditoría + crítico), `rsl-make-paper` (definiciones/método) siguen [`playbooks/vocabulario-controlado.md`](playbooks/vocabulario-controlado.md): descriptor IEEE preferido (USE si era no preferido) + UF al `OR` + términos libres marcados y justificados. Nunca un descriptor inventado.

---

## Orden sugerido

```text
rsl-bootstrap             ← paso 0 (una vez por clon / máquina)
  → rsl-topic-panel
  → rsl-make-report
  → PDFs en RSL/PDF/
  → graphify-theme (PASS)
  → rsl-polish-report
  → rsl-make-paper          ← Introducción borrador (APA 7; puede ser larga)
  → rsl-polish-paper        ← paper-polish.md limpio + paper-debate.md
```
(y de vez en cuando **`graphify-root`** si cambias skills / `global/`)

## Clonar en otra máquina

Los grafos (`graphify-out/`) y el JSON del thesaurus están gitignored; se regeneran desde lo versionado (`RSL/MD/*.md`, `index-manifest.json`, `global/thesaurus/IEEE.pdf`). Los PDFs ya indexados **no** se re-extraen (mismo sha en el manifest) → 0 tokens.

Requisitos (una vez por máquina):

```bash
# Node >= 18 + pnpm (corepack enable)
pipx install graphifyy && pipx ensurepath && hash -r
graphify install --platform cursor
sudo pacman -S poppler        # Debian/Ubuntu: poppler-utils · macOS: brew install poppler
```

Dejar todo listo:

```bash
pnpm install          # workspace: root + tools/* (prisma-flow)
pnpm run bootstrap    # root + thesaurus IEEE + todos los temas docs/* → resumen PASS/FAIL
```

Re-ejecutar `pnpm run bootstrap` solo cuando cambien skills/`global/`, temas o PDFs (o usar el comando puntual: `graphify:refresh`, `graphify:theme -- <slug>`, `thesaurus:ieee`).

## Tools (workspace pnpm)

`tools/*` son paquetes del mismo repo (sin `.git` propio). PRISMA flow diagram:

```bash
pnpm prisma:dev       # http://localhost:3000
pnpm prisma:build
```
