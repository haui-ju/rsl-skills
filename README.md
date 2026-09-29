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
| `rsl-bootstrap` | Paso 0: deja el entorno y todos los grafos Graphify listos | `graphify-out/` · `global/thesaurus/graphify-out/` · `global/examples/graphify-out/` · `global/bibliography/graphify-out/` · `docs/*/graphify-out/` |
| `rsl-topic-panel` | Estresa un tema (4 agentes + debate Mermaid + consenso) | `docs/[titulo-breve]/topic.md` |
| `rsl-make-report` | Genera el informe UTP (7 puntos) y llama a `rsl-picoc` para el marco de búsqueda | `docs/[titulo-breve]/informe.md` + `picoc/<fecha>-<MARCO>/` |
| `rsl-polish-report` | Pule el informe (4 agentes); si el marco quedó desfasado llama a `rsl-picoc` (modo ligero si solo cambió la pregunta § 1.2) | `docs/[titulo-breve]/informe-polish.md` |
| `rsl-picoc` | Crea una versión nueva del marco de búsqueda con el marco de `config.yml` (libre: PICO, PIO, PICOC, PICOCT, PICOS…; por defecto PICOCT): tabla por componente 1:1 con las queries, palabras clave IEEE (libres al final), 5–6 keywords del paper, criterios de inclusión y exclusión; modo completo (debate `critico-rsl` + `defensor-rsl` + `redaccion-rsl`), parcial (solo keywords o criterios) o ligero (solo la pregunta general, sin agentes); `picoc:lint` OK. **Solo lee** el informe, `config.yml` y el paper: nunca los modifica | `docs/[titulo-breve]/picoc/<fecha>-<MARCO>/picoc.md` + `picoc-debate.md` |
| `rsl-cribado-1` | Cribado 1 de PRISMA (título, resumen y palabras clave) de Scopus y Web of Science juntos: `cribado:prepare` pasa WoS a CSV, une ambas bases en `resultados-<MARCO>.csv` y elimina duplicados primero (el agente nunca lee las exportaciones); `defensor-rsl` propone SI/NO por registro con los criterios del picoc y `critico-rsl` lo critica; las dudas van como SI. Siempre deja una sugerencia de keywords (qué términos valen, cuáles no aportan y cuáles agregar) con las queries de Scopus y WoS. Correcciones con `cribado:set` | `picoc/<fecha>-<MARCO>/cribado-1.md` + `cribado-1.shadow.jsonl` + `cribado-1-sugerencia.md` |
| `rsl-cribado-1-aplicar` | Tras aprobar el reporte, copia el CSV unificado con dos columnas más al final: «¿Se acepta?» (SI o NO) y «Justificación cribado 1». No decide nada ni edita las exportaciones | `picoc/<fecha>-<MARCO>/resultados-<MARCO>-cribado-1.csv` |
| `rsl-make-paper` | Nueva versión del paper borrador, solo secciones `on` (mejorar) y `rewrite` (reescribir) de `config.yml` (+ agente `citas-rsl` y `redaccion:lint`) | `docs/[titulo-breve]/paper/<fecha>/paper-borrador.md` |
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
  config.yml             ← TÚ decides: cada sección del paper frozen / on / rewrite / off + formato (romana, APA/IEEE, marco PICOCT…)
  topic.md
  informe.md             ← sección 2 solo enlaza al marco
  informe-polish.md
  picoc/                 ← marco de búsqueda versionado (solo rsl-picoc crea versiones; el paper lee la última)
    2026-09-28-PICOCT/   ← <fecha>-<MARCO> según formato.marco de config.yml
      picoc.md           ← pregunta general, RQ por componente, tabla de componentes 1:1, palabras clave ES/EN, 5–6 keywords del paper, queries Scopus/WoS/IEEE Xplore, criterios de inclusión y exclusión
      picoc-debate.md    ← posturas de los agentes y decisiones
      scopus-result.csv  ← TÚ: la exportación de Scopus (CSV) con la query del picoc
      wos-resultados.xls ← TÚ: la exportación de Web of Science (Excel o Tab delimited .txt)
      wos-resultados.csv ← cribado:prepare: WoS pasado a CSV
      resultados-PICOCT.csv  ← cribado:prepare: Scopus + WoS unificados (columnas en playbooks/columnas-scopus-wos.md)
      cribado-1.md       ← rsl-cribado-1: duplicados, aceptados, rechazados (% por criterio), dudas y línea PRISMA
      cribado-1.shadow.jsonl  ← rsl-cribado-1: una línea por registro (id, fuente, decisión, motivo)
      cribado-1-sugerencia.md ← rsl-cribado-1: keywords que valen, no aportan o conviene agregar + queries Scopus y WoS
      .cribado-1/        ← trabajo interno (registros.jsonl, propuestas, decisiones, síntesis, keywords)
      resultados-PICOCT-cribado-1.csv  ← rsl-cribado-1-aplicar: el unificado con «¿Se acepta?» y «Justificación cribado 1»
  paper/
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
  bibliography/   ← fuentes metodológicas que citan todos los temas (Kitchenham 2007 · PRISMA 2020): PDF + MD + bibliography.md; grafo propio
  citation-style/ ← APA7.md · IEEE.md (reglas de citas; formato.citas de config.yml)
playbooks/        ← protocolos compartidos que siguen varias skills (vocabulario-controlado.md, redaccion-academica.md)
```

Agentes: `.cursor/agents/` (`critico-rsl`, `defensor-rsl`, `impacto-social-rsl`, `viabilidad-negocio-rsl`, `citas-rsl`, `redaccion-rsl`)

---

## Comandos (`package.json`)

Todos con `pnpm <comando>` (`pnpm -s` oculta el eco de pnpm).

### Entorno

| Comando | Qué hace |
|---------|----------|
| `bootstrap` | Deja todo listo tras clonar: verifica prerrequisitos y construye los 5 grafos (root, thesaurus, ejemplos, bibliografía, temas). |
| `prisma:dev` | Levanta la herramienta del diagrama PRISMA en `http://localhost:3000`. |
| `prisma:build` | Compila esa herramienta. |

### Grafos Graphify — `graphify:<alcance>:<acción>`

| Alcance | Qué contiene |
|---------|--------------|
| `root` | Memoria del repo: skills, agentes, reglas, scripts, `global/` (sin thesaurus, ejemplos ni bibliografía), playbooks, README. |
| `theme` | Corpus de un tema `docs/<slug>/`: informe, topic, `picoc/`, última versión del paper y RSL en `RSL/MD`. |
| `thesaurus` | IEEE Thesaurus 2019 (10.4k términos con BT/NT/RT/USE), desde `global/thesaurus/IEEE.pdf`. |
| `examples` | Papers RSL de referencia en `global/examples/` (estructura por secciones). |
| `bibliography` | Fuentes metodológicas compartidas en `global/bibliography/` (una carpeta por tema metodológico, MD con `[PDF p.N]`). |

| Acción | Qué hace |
|--------|----------|
| `refresh` | Reconstruye el grafo (incremental: solo relee lo que cambió). |
| `status` | Valida sin reconstruir: OK si está al día; ERROR (exit 1) listando qué archivos son más nuevos o si falta el grafo. |
| `query "…"` | Consulta el grafo → nodos con archivo y línea (menos tokens que leer archivos). Acepta `--budget N`. |
| `open` | Abre `graph.html` en el navegador (thesaurus: vista agregada por comunidades). |

Ejemplos: `pnpm graphify:root:status` · `pnpm graphify:examples:query "estructura de Resultados"` · `pnpm graphify:theme:query <slug> "cognitive accessibility"`.
En `theme`, el `<slug>` se omite si solo hay un tema; `refresh`/`status` aceptan `--all`; `refresh` acepta `--force` y `--prepare-only`.

### Herramientas del flujo RSL

| Comando | Qué hace |
|---------|----------|
| `thesaurus:check "t1" "t2" …` | Valida varios términos contra IEEE: preferido / no preferido (→ USE) / libre, con sinónimos (UF), específicos (NT) y página. |
| `thesaurus:lookup "término"` | Ficha completa de un término IEEE (todas sus relaciones y página). |
| `picoc:latest docs/<slug>` | Marco configurado en `config.yml` + último `picoc/<fecha>-<MARCO>/picoc.md`: OK, DESFASADO (cambiaste el marco) o FALTA → correr `rsl-picoc`; también imprime la carpeta de la siguiente versión. |
| `picoc:lint docs/<slug>` | OK/ERROR del último picoc: marco = `config.yml`, pregunta general = § 1.2 de la ficha, una fila por componente 1:1 con las queries Scopus/WoS/IEEE Xplore, T = filtro de año, 1 RQ por componente, descriptores IEEE preferidos, libres al final, 5 o 6 keywords del paper (una por componente como mínimo) y al final criterios de inclusión y exclusión breves (idioma, tipo de documento y años de T). |
| `redaccion:lint <archivo.md>` | Forma académica de informe o paper: FAIL por marcas pendientes (`[citar]`, TODO…), notas internas (panel, `topic.md`…) o siglas sin definir; avisos por frases largas, notación ×/+ y exceso de siglas. Los marcadores del usuario (`n = X`, `[[ AGREGAR DIAGRAMA ]]`) no fallan: se cuentan en la línea OK. |
| `rsl:source <pdf>` | Convierte un PDF de `global/bibliography/<carpeta>/` en MD junto al PDF (índice con página del PDF) y deja el texto por página en `_raw/`; ERROR si no es un PDF real. |
| `paper:status docs/<slug>` | Estado del paper según `config.yml`: qué se mejora (on) o reescribe (rewrite), stale, blocked; ERROR si se editó a mano una sección frozen; la línea OK indica el próximo paso. |
| `paper:status docs/<slug> --init` | Crea `config.yml` y `paper/paper.shadow.yml` por defecto. |
| `paper:status docs/<slug> --migrate` | Mueve el antiguo `config.yml` a `config.yml` y convierte el formato antiguo (enabled/frozen) al nuevo. |
| `paper:status docs/<slug> --new-version` | Crea `paper/<fecha>/` copiando la versión anterior. |
| `paper:status docs/<slug> --update borrador\|polish` | Registra hashes tras escribir el borrador o el polish. |
| `paper:status docs/<slug> --cites [archivo]` | Citas en texto vs Referencias (APA 7 o IEEE según `formato.citas`); con `informe-polish.md` compara contra la tabla de la sección 3. |
| `cribado:prepare docs/<slug>` | Detecta las exportaciones de Scopus y WoS de la última carpeta del picoc, pasa WoS a CSV, las une en `resultados-<MARCO>.csv`, elimina duplicados (DOI, id de la base o título), numera los criterios CI y CE y escribe `.cribado-1/registros.jsonl` con el rango de líneas de cada lote de 40. |
| `cribado:merge docs/<slug>` | Consolida las tablas de los agentes (`.cribado-1/propuestas/lote-NN.md`): toma los acuerdos, imprime solo los desacuerdos y, con `resoluciones.md`, escribe `decisiones.jsonl` y `debate.md`. |
| `cribado:report docs/<slug>` | Valida `.cribado-1/decisiones.jsonl` y `sintesis.json` y escribe `cribado-1.md` y `cribado-1.shadow.jsonl`. |
| `cribado:keywords docs/<slug>` | Cuenta cuántos registros (SI y NO) recupera cada término de la query y lista palabras clave de los aceptados que ninguna query cubre (`.cribado-1/keywords.md`). |
| `cribado:set docs/<slug> <id> SI\|DUDA\|NO "motivo" [criterios]` | Corrige la decisión de un registro (`DUDA` = SI con duda) y regenera el reporte y el shadow. |
| `cribado:apply docs/<slug>` | Escribe `resultados-<MARCO>-cribado-1.csv` con las dos columnas; ERROR si el reporte no está al día o las exportaciones cambiaron. |
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

El marco sale de `formato.marco` en `config.yml` (por defecto PICOCT) y es libre: `P` población, `I` intervención, `C` comparación, `O` resultado, `T` tiempo, `S` diseño de estudio; la segunda `C` es contexto. Una letra fuera de esa lista es ERROR y nada continúa. Si lo cambias (p. ej. `marco: PIO`), `picoc:latest` marca DESFASADO, las secciones del paper que dependen del marco quedan BLOCKED y `rsl-picoc` crea `picoc/<fecha>-PIO/`. Los criterios de inclusión y exclusión del picoc son los que usa `rsl-cribado-1`.

### Cribado 1 (título, resumen y palabras clave)

Corre las queries de Scopus y Web of Science del último picoc y deja en esa carpeta las exportaciones con resumen y palabras clave: Scopus en CSV y WoS en Excel (o Tab delimited `.txt`). Luego:

```text
Usa rsl-cribado-1 sobre docs/[titulo-breve]/
```

Revisa `picoc/<fecha>-<MARCO>/cribado-1.md` (duplicados, aceptados, rechazados con el porcentaje por criterio, dudas y la línea PRISMA). Pide las correcciones que quieras y, cuando lo apruebes:

```text
Usa rsl-cribado-1-aplicar sobre docs/[titulo-breve]/
```

`cribado-1-sugerencia.md` propone cómo mejorar la búsqueda (sin tirar lo que funciona). Para llevarla a una versión nueva del picoc, `Usa rsl-picoc sobre docs/[titulo-breve]/`: `picoc:latest` avisa la sugerencia y la skill entra en modo sugerencia (solo valida, sin debate).

### Crear el paper (borrador rico)

Usa `topic.md` + ficha (`informe-polish.md` / `informe.md`) + último `picoc/<fecha>-<MARCO>/picoc.md` + Graphify + `RSL/MD/` + `global/examples/`.

```text
Usa rsl-make-paper sobre docs/ia-inclusion-cognitiva-software/
```

Salida: nueva carpeta `paper/<fecha>/paper-borrador.md`. La primera vez crea `config.yml` con solo la **Introducción** activada.

### Pulir el paper (agentes + redacción + citas)

```text
Usa rsl-polish-paper sobre docs/[titulo-breve]/
```

Salidas en la misma versión:
- `paper-polish.md` — encabezado (**Tema / Problemática ¿…? / Objetivo**), `## I. Introducción` (Contexto → El problema → Justificación → Objetivo de la RSL → Organización), los grupos que actives y **Referencias** con todas las obras citadas.
- `paper-debate.md` — un bloque por corrida: agentes usados, decisiones y veredictos de forma y de citas.

Para volver a pulir un texto ya pulido, deja la sección en `on` (mejoras puntuales); `rewrite` la replantea desde el borrador. Si nada está en `on`/`rewrite`, `--new-version` no crea versión.

### Regenerar solo algunas secciones (`config.yml`)

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

- `formato` en `config.yml`: `idioma` (es por defecto; en, pt, fr, de… cualquier código ISO 639-1), `numeracion` (romana | arabiga | ninguna), `citas` (apa7 | ieee), `resumen` (idiomas), `resultados_por` (rq | tema), `marco` (libre, letras P I C O T S, la segunda C = contexto; por defecto PICOCT; letra desconocida = ERROR).
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

### Bibliografía compartida (`global/bibliography/`)

Obras metodológicas que cualquier tema cita sin volver a buscarlas: `picoc/` (Kitchenham y Charters, 2007) y `prisma/` (Page et al., 2021). El catálogo [`global/bibliography/bibliography.md`](global/bibliography/bibliography.md) trae la referencia APA 7, el DOI o enlace, la licencia y los pasajes citables con su página. El PDF solo se versiona si su licencia es abierta; si no, queda en `.gitignore` y el catálogo guarda el enlace.

```bash
pnpm -s rsl:source global/bibliography/<carpeta>/<archivo>.pdf   # PDF → MD junto al PDF
pnpm graphify:bibliography:refresh                               # tras agregar una obra
pnpm graphify:bibliography:query "PICOC"
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
  → (tú: queries de Scopus y WoS, exportaciones en picoc/<fecha>-<MARCO>/) → rsl-cribado-1 → (tú: revisar) → rsl-cribado-1-aplicar
  → rsl-make-paper          ← paper/<fecha>/paper-borrador.md (secciones on de config.yml)
  → rsl-polish-paper        ← paper-polish.md limpio + paper-debate.md
  → marcar frozen en config.yml lo validado · activar Metodología · (tú: selección PRISMA) · activar Resultados…
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
pnpm run bootstrap    # root + thesaurus IEEE + ejemplos + bibliografía + todos los temas docs/* → resumen PASS/FAIL
```

Re-ejecutar `pnpm run bootstrap` solo cuando cambien skills/`global/`, temas o PDFs (o usar el comando puntual: `graphify:root:refresh`, `graphify:theme:refresh <slug>`, `graphify:thesaurus:refresh`).

## Tools (workspace pnpm)

`tools/*` son paquetes del mismo repo (sin `.git` propio). PRISMA flow diagram:

```bash
pnpm prisma:dev       # http://localhost:3000
pnpm prisma:build
```
