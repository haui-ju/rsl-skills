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
| `rsl-bootstrap` | Paso 0: deja el entorno y todos los grafos Graphify listos | `graphify-out/` · `global/thesaurus/graphify-out/` · `global/examples/graphify-out/` · `docs/*/graphify-out/` |
| `rsl-topic-panel` | Estresa un tema (4 agentes + debate Mermaid + consenso) | `docs/[titulo-breve]/topic.md` |
| `rsl-make-report` | Genera el informe UTP (7 puntos) y llama a `rsl-picoc` para el marco de búsqueda | `docs/[titulo-breve]/informe.md` + `picoc/<fecha>-<MARCO>/` |
| `rsl-polish-report` | Pule el informe (4 agentes); si el marco quedó desfasado llama a `rsl-picoc` (modo ligero si solo cambió la pregunta § 1.2) | `docs/[titulo-breve]/informe-polish.md` |
| `rsl-picoc` | Crea una versión nueva del marco de búsqueda con el marco de `paper.yml` (libre: PICO, PIO, PICOC, PICOCT, PICOS…; por defecto PICOCT): tabla por componente 1:1 con las queries, palabras clave IEEE (libres al final), modo completo (debate `critico-rsl` + `defensor-rsl` + `redaccion-rsl`) o ligero (solo actualiza la pregunta general, sin agentes), `picoc:lint` PASS | `docs/[titulo-breve]/picoc/<fecha>-<MARCO>/picoc.md` + `picoc-debate.md` |
| `rsl-make-paper` | Nueva versión del paper borrador, solo secciones `on` (mejorar) y `rewrite` (reescribir) de `paper.yml` (+ agente `citas-rsl` y `redaccion:lint`) | `docs/[titulo-breve]/paper/<fecha>/paper-borrador.md` |
| `rsl-polish-paper` | Pule esas secciones (`critico-rsl` + `defensor-rsl`; `impacto-social-rsl` si están Justificación u Objetivo; luego `redaccion-rsl` + `citas-rsl`) → texto limpio + traza de debate | `paper/<fecha>/paper-polish.md` + `paper-debate.md` |
| `rsl-qa-destroy` | Intenta romper el flujo a propósito (flujo positivo, orden mezclado, entradas destructivas, marco libre, revisión de skills y agentes) en un sandbox de `/tmp`; solo reporta | `qa/<fecha>/qa-report.md` + `qa-report.json` |
| `rsl-qa-fix` | Arregla los fallos del último reporte, deja cada uno como caso de regresión y repite `qa:destroy` hasta OK | código corregido + `qa/<fecha>/qa-fix.md` |

Todas las skills `rsl-*` terminan con una sola línea: `ERROR: <contexto>` si algo falló, u `OK: <qué se hizo>. Próximo paso: <skill>` si salió bien. Los scripts siguen el mismo contrato (última línea `OK:` o `ERROR:`; código de salida 0 o distinto de 0).

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
  informe.md             ← sección 2 solo enlaza al marco
  informe-polish.md
  picoc/                 ← marco de búsqueda versionado (solo rsl-picoc crea versiones; el paper lee la última)
    2026-09-28-PICOCT/   ← <fecha>-<MARCO> según formato.marco de paper.yml
      picoc.md           ← pregunta general, RQ por componente, tabla de componentes 1:1, palabras clave ES/EN, queries Scopus/WoS/IEEE Xplore
      picoc-debate.md    ← posturas de los agentes y decisiones
  paper/
    paper.yml            ← TÚ decides: cada sección frozen / on / rewrite / off + formato (romana, APA/IEEE, marco PICOCT…)
    paper.shadow.yml     ← detalle técnico: títulos, capítulos, depends_on (rara vez se edita)
    paper.state.jsonc    ← hashes y versiones (lo gestiona pnpm paper:status; no editar)
    2026-09-05/          ← una carpeta por corrida (trazabilidad; nunca se editan las anteriores)
      paper-borrador.md  ← versión rica (rsl-make-paper)
      paper-polish.md    ← versión limpia para presentar (rsl-polish-paper)
      paper-debate.md    ← debate por corrida (no va al documento)
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
  examples/       ← papers RSL reales de referencia (estructura/presentación; grafo propio)
  citation-style/ ← APA7.md · IEEE.md (reglas de citas; formato.citas de paper.yml)
playbooks/        ← protocolos compartidos que siguen varias skills (vocabulario-controlado.md, redaccion-academica.md)
```

Agentes: `.cursor/agents/` (`critico-rsl`, `defensor-rsl`, `impacto-social-rsl`, `viabilidad-negocio-rsl`, `citas-rsl`, `redaccion-rsl`)

---

## Comandos (`package.json`)

Todos con `pnpm <comando>` (`pnpm -s` oculta el eco de pnpm).

### Entorno

| Comando | Qué hace |
|---------|----------|
| `bootstrap` | Deja todo listo tras clonar: verifica prerrequisitos y construye los 4 grafos (root, thesaurus, ejemplos, temas). |
| `prisma:dev` | Levanta la herramienta del diagrama PRISMA en `http://localhost:3000`. |
| `prisma:build` | Compila esa herramienta. |

### Grafos Graphify — `graphify:<alcance>:<acción>`

| Alcance | Qué contiene |
|---------|--------------|
| `root` | Memoria del repo: skills, agentes, reglas, scripts, `global/` (sin thesaurus ni ejemplos), playbooks, README. |
| `theme` | Corpus de un tema `docs/<slug>/`: informe, topic, `picoc/`, última versión del paper y RSL en `RSL/MD`. |
| `thesaurus` | IEEE Thesaurus 2019 (10.4k términos con BT/NT/RT/USE), desde `global/thesaurus/IEEE.pdf`. |
| `examples` | Papers RSL de referencia en `global/examples/` (estructura por secciones). |

| Acción | Qué hace |
|--------|----------|
| `refresh` | Reconstruye el grafo (incremental: solo relee lo que cambió). |
| `status` | Valida sin reconstruir: PASS si está al día; STALE/FAIL (exit 1) listando qué archivos son más nuevos. |
| `query "…"` | Consulta el grafo → nodos con archivo y línea (menos tokens que leer archivos). Acepta `--budget N`. |
| `open` | Abre `graph.html` en el navegador (thesaurus: vista agregada por comunidades). |

Ejemplos: `pnpm graphify:root:status` · `pnpm graphify:examples:query "estructura de Resultados"` · `pnpm graphify:theme:query <slug> "cognitive accessibility"`.
En `theme`, el `<slug>` se omite si solo hay un tema; `refresh`/`status` aceptan `--all`; `refresh` acepta `--force` y `--prepare-only`.

### Herramientas del flujo RSL

| Comando | Qué hace |
|---------|----------|
| `thesaurus:check "t1" "t2" …` | Valida varios términos contra IEEE: preferido / no preferido (→ USE) / libre, con sinónimos (UF), específicos (NT) y página. |
| `thesaurus:lookup "término"` | Ficha completa de un término IEEE (todas sus relaciones y página). |
| `picoc:latest docs/<slug>` | Marco configurado en `paper.yml` + último `picoc/<fecha>-<MARCO>/picoc.md`: OK, DESFASADO (cambiaste el marco) o FALTA → correr `rsl-picoc`; también imprime la carpeta de la siguiente versión. |
| `picoc:lint docs/<slug>` | OK/ERROR del último picoc: marco = `paper.yml`, pregunta general = § 1.2 de la ficha, una fila por componente 1:1 con las queries Scopus/WoS/IEEE Xplore, T = filtro de año, 1 RQ por componente, descriptores IEEE preferidos, libres al final. |
| `redaccion:lint <archivo.md>` | Forma académica de informe o paper: FAIL por marcas pendientes (`[citar]`, TODO…), notas internas (panel, `topic.md`…) o siglas sin definir; avisos por frases largas, notación ×/+ y exceso de siglas. |
| `paper:status docs/<slug>` | Estado del paper según `paper/paper.yml`: qué se mejora (on) o reescribe (rewrite), stale, blocked; ERROR si se editó a mano una sección frozen; la línea OK indica el próximo paso. |
| `paper:status docs/<slug> --init` | Crea `paper/paper.yml` y `paper/paper.shadow.yml` por defecto. |
| `paper:status docs/<slug> --migrate` | Convierte un `paper.yml` del formato antiguo (enabled/frozen) al nuevo. |
| `paper:status docs/<slug> --new-version` | Crea `paper/<fecha>/` copiando la versión anterior. |
| `paper:status docs/<slug> --update borrador\|polish` | Registra hashes tras escribir el borrador o el polish. |
| `paper:status docs/<slug> --cites [archivo]` | Citas en texto vs Referencias (APA 7 o IEEE según `formato.citas`); con `informe-polish.md` compara contra la tabla de la sección 3. |
| `qa:destroy [--only grupo] [--keep] [--no-report]` | Arnés de `rsl-qa-destroy`: rompe el flujo en un sandbox y escribe `qa/<fecha>/qa-report.md`; nunca toca `docs/`. |

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

### Marco de búsqueda (libre: PICO, PIO, PICOC, PICOCT…)

```text
Usa rsl-picoc sobre docs/[titulo-breve]/
```

El marco sale de `formato.marco` en `paper/paper.yml` (por defecto PICOCT) y es libre: `P` población, `I` intervención, `C` comparación, `O` resultado, `T` tiempo, `S` diseño de estudio; la segunda `C` es contexto. Una letra fuera de esa lista es ERROR y nada continúa. Si lo cambias (p. ej. `marco: PIO`), `picoc:latest` marca DESFASADO, las secciones del paper que dependen del marco quedan BLOCKED y `rsl-picoc` crea `picoc/<fecha>-PIO/`. El cribado (inclusión/exclusión, tipo de documento) no va en el picoc: lo defines tú.

### Crear el paper (borrador rico)

Usa `topic.md` + ficha (`informe-polish.md` / `informe.md`) + último `picoc/<fecha>-<MARCO>/picoc.md` + Graphify + `RSL/MD/` + `global/examples/`.

```text
Usa rsl-make-paper sobre docs/ia-inclusion-cognitiva-software/
```

Salida: nueva carpeta `paper/<fecha>/paper-borrador.md`. La primera vez crea `paper/paper.yml` con solo la **Introducción** activada.

### Pulir el paper (agentes + redacción + citas)

```text
Usa rsl-polish-paper sobre docs/[titulo-breve]/
```

Salidas en la misma versión:
- `paper-polish.md` — encabezado (**Tema / Problemática ¿…? / Objetivo**), `## I. Introducción` (Contexto → El problema → Justificación → Objetivo de la RSL → Organización), los grupos que actives y **Referencias** con todas las obras citadas.
- `paper-debate.md` — un bloque por corrida: agentes usados, decisiones y veredictos de forma y de citas.

Para volver a pulir un texto ya pulido, deja la sección en `on` (mejoras puntuales); `rewrite` la replantea desde el borrador. Si nada está en `on`/`rewrite`, `--new-version` no crea versión.

### Regenerar solo algunas secciones (`paper/paper.yml`)

Solo editas una palabra por sección, agrupadas por capítulo:

```yaml
Introducción:
  contexto:      frozen
  problema:      on
  objetivo-rsl:  rewrite
```

| Estado | Qué le dices | Efecto en la próxima corrida (borrador y polish) |
|--------|--------------|--------------------------------------------------|
| `frozen` | Está bien, no lo toques | Se copia tal cual; si cambia una fuente de `depends_on` (p. ej. un picoc nuevo) queda **stale** y se avisa |
| `on` | Revísalo y mejóralo | Conserva el texto actual como base y lo corrige, completa y pule; no lo reescribe |
| `rewrite` | Reescríbelo / replantéalo | Descarta el texto actual y lo vuelve a escribir desde las fuentes; puede cambiar estructura y argumento |
| `off` | No está activo | No se genera ni aparece (por defecto todo lo posterior a la Introducción) |

Una sección en `on` que aún no tiene texto se escribe desde cero (sale como `reescribir (nueva)` en `paper:status`).

```bash
pnpm -s paper:status docs/<slug>            # tabla: qué se mejora o reescribe, stale, blocked; FAIL si editaste a mano una frozen
pnpm -s paper:status docs/<slug> --cites    # citas en texto vs Referencias (APA7 | IEEE según formato.citas)
```

- `formato` en `paper.yml`: `idioma` (es por defecto; en, pt, fr, de… cualquier código ISO 639-1), `numeracion` (romana | arabiga | ninguna), `citas` (apa7 | ieee), `resumen` (idiomas), `resultados_por` (rq | tema), `marco` (libre, letras P I C O T S, la segunda C = contexto; por defecto PICOCT; letra desconocida = ERROR).
- `paper.shadow.yml`: títulos, capítulo y `depends_on` de cada sección, más formato avanzado (letras A–E, ejemplos). Solo si quieres cambiar dependencias o títulos.
- Metodología sale del último picoc y dice explícitamente qué marco se usa (el de `formato.marco`). Resultados/Discusión/Conclusión necesitan `RSL/seleccion/` y `RSL/extraccion/` (**los preparas tú**: correr las queries, validar artículos, PRISMA); mientras no existan quedan **blocked**, nunca se inventan.
- Añadir un paper de ejemplo: copiar el `.md` en `global/examples/` (convertido con `global/to-md.md`) y correr `pnpm graphify:examples:refresh`.

### Memoria Graphify — root

```text
Usa graphify-root
```

```bash
pnpm graphify:root:refresh
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
pnpm graphify:theme:refresh ia-inclusion-cognitiva-software
pnpm graphify:theme:status ia-inclusion-cognitiva-software
```

Consulta (después de PASS):

```bash
pnpm graphify:theme:query ia-inclusion-cognitiva-software "digital accessibility"
```

### Thesaurus IEEE (vocabulario controlado para PICO / keywords)

`global/thesaurus/IEEE.pdf` (IEEE Thesaurus 2019, 594 págs., ~10.4k términos) **no** se indexa en el root: tiene grafo propio con relaciones BT/NT/RT/USE. Parse local por fuentes del PDF (negrita = preferido, cursiva = no preferido); 0 tokens LLM.

```bash
pnpm graphify:thesaurus:refresh                     # PDF → ieee-thesaurus.json + graphify-out/graph.json
pnpm -s thesaurus:check "machine learning" "autism" "large language models"   # tabla lista para PICOC
pnpm -s thesaurus:lookup "Human computer interaction"
pnpm graphify:thesaurus:query "machine learning"
graphify explain "Assistive technology" --graph global/thesaurus/graphify-out/graph.json
graphify path "Machine learning" "Usability" --graph global/thesaurus/graphify-out/graph.json
```

Aristas: `broader` (BT) · `narrower` (NT) · `related` (RT) · `use` (no preferido → preferido). Cada nodo lleva `p.N` del PDF.
Si un concepto **no** aparece (p. ej. *Accessibility*, *Neurodiversity*, *LLM* en la edición 2019) se declara vacío de vocabulario y se usa término libre — no inventar descriptor IEEE.
Derivados gitignored (licencia CC BY-NC-ND).

**Protocolo en las skills:** `rsl-topic-panel` (tópicos), `rsl-picoc` (marco versionado; lo llaman `rsl-make-report` y `rsl-polish-report`), `rsl-make-paper` (definiciones, RQ en §4/§5) siguen [`playbooks/vocabulario-controlado.md`](playbooks/vocabulario-controlado.md): descriptor IEEE preferido (USE si era no preferido) + términos libres marcados y justificados; cada componente justificado con una frase del tema; tabla de componentes y queries (Scopus, Web of Science, IEEE Xplore) **1:1**; una pregunta por componente; palabras clave libres solo al final. Nunca un descriptor inventado.

```bash
pnpm -s picoc:latest docs/[titulo-breve]   # marco configurado + último picoc (OK | DESFASADO | FALTA)
pnpm -s picoc:lint docs/[titulo-breve]     # PASS/FAIL del último picoc
```

**Redacción:** informe y paper siguen [`playbooks/redaccion-academica.md`](playbooks/redaccion-academica.md): texto final sin notas de trabajo ni marcas como `[citar]`; siglas definidas en su primera aparición y dosificadas; una idea por oración; sin notación ×/+ ni jerga interna en la prosa; citas coherentes con las referencias; título breve y cercano al título tentativo de la ficha. Las skills cierran con `redaccion:lint` (0 FAIL) y el agente `redaccion-rsl`.

```bash
pnpm -s redaccion:lint docs/[titulo-breve]/paper/<fecha>/paper-polish.md
```

### Papers de ejemplo (`global/examples/`)

Grafo propio (no entra al root) con la estructura de papers RSL reales; las skills del paper lo consultan para imitar la presentación, nunca el texto.

```bash
pnpm graphify:examples:refresh                      # incremental (solo si cambió algún ejemplo)
pnpm graphify:examples:query "estructura de Resultados"
```

---

## Orden sugerido

```text
rsl-bootstrap             ← paso 0 (una vez por clon / máquina)
  → rsl-topic-panel
  → rsl-make-report
  → PDFs en RSL/PDF/
  → graphify-theme (PASS)
  → rsl-polish-report
  → rsl-make-paper          ← paper/<fecha>/paper-borrador.md (secciones on de paper.yml)
  → rsl-polish-paper        ← paper-polish.md limpio + paper-debate.md
  → marcar frozen en paper.yml lo validado · activar Metodología · (tú: selección PRISMA) · activar Resultados…
```
(y de vez en cuando **`graphify-root`** si cambias skills / `global/`; tras tocar scripts o skills: **`rsl-qa-destroy`** → **`rsl-qa-fix`**)

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
pnpm run bootstrap    # root + thesaurus IEEE + ejemplos + todos los temas docs/* → resumen PASS/FAIL
```

Re-ejecutar `pnpm run bootstrap` solo cuando cambien skills/`global/`, temas o PDFs (o usar el comando puntual: `graphify:root:refresh`, `graphify:theme:refresh <slug>`, `graphify:thesaurus:refresh`).

## Tools (workspace pnpm)

`tools/*` son paquetes del mismo repo (sin `.git` propio). PRISMA flow diagram:

```bash
pnpm prisma:dev       # http://localhost:3000
pnpm prisma:build
```
