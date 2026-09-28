---
name: rsl-topic-panel
description: >-
  Scopus-grade stress test of any RSL topic: 4 hard agents (critic, defender,
  social impact, business) with mandatory web evidence, cross-debate, and a
  final consensus topic written to docs/[short-title]/topic.md. Use when the
  user says rsl-topic-panel or pastes title/problem/object.
---

# rsl-topic-panel

## Goal

Stress-test a research topic at **Scopus / journal review** intensity. Four agents argue hard in their domain, grounded on **internet sources** (WebSearch/WebFetch). The orchestrator writes a full `topic.md` ending in a **Tema final propuesto** that all roles converge on.

## Output path (required)

```text
docs/[titulo-breve]/topic.md
```

Slug: 3–6 words, lowercase, hyphenated. Same folder reused by `rsl-make-report` / `rsl-polish-report`.

## Invoke

```text
Usa rsl-topic-panel con este tema:

Título: ...
Problemática: ...
Objeto de estudio: ...
Carrera: Ingeniería de Software
```

No topic → ask. Do not invent a topic.

## Rigor

Not a friendly brainstorm: an external reviewer from an indexed venue. The agents run in **modo panel** (their own files define it: mandatory WebSearch, real sources, question to the other role). Soft praise without evidence is failure.

## Procedure

### Round 1 — parallel

Launch `critico-rsl`, `defensor-rsl`, `impacto-social-rsl`, `viabilidad-negocio-rsl` in one response with:

```text
Modo panel. Evalúa solo este tema. Responde en español con el formato de tu rol.

## BLOQUE_TEMA
...
```

### Round 2 — cross-debate (orchestrator)

After all four return, the orchestrator (you):

1. Extract clashes (critic vs defender; social vs business trade-offs).
2. Only if a clash stays unresolved: **one** short follow-up to critic and defender with the other’s key points.
3. Build recommendations that agents would force on each other.
4. Force a **single converged topic** (not four alternatives). Prefer the sharpest version that survives the critic while keeping social/business value and SE alignment.
5. **Tópicos (3) finales con vocabulario IEEE** (`playbooks/vocabulario-controlado.md`): una llamada `pnpm -s thesaurus:check "…"` con las formulaciones EN de los 3 tópicos; en `### Tópicos (3) finales` anotar por tópico `IEEE: <descriptor> (p.N)` o `Libre: <término>` (+ motivo). Esto alimenta `rsl-picoc`; no construir queries aquí.

### Write `topic.md`

Use the full template below. **Never skip** `## Tema final propuesto` or `## Diagrama del debate`.

**Mermaid (required):** after the global verdict, include a **flowchart** of how the agents argued (ronda 1 → objeciones/preguntas → ronda 2 → consenso). Node IDs camelCase without spaces; edge labels = the real short objections or questions of this run, quoted if they have special characters.

In chat: path + one-line global verdict + pointer to Tema final.

## Output template (`topic.md`)

```markdown
# Veredicto del panel — [título corto]

## BLOQUE_TEMA (entrada)
- Título:
- Problemática:
- Objeto de estudio:
- Tópicos (3):
- Carrera/contexto:
- Notas:

## Veredicto global
GO | GO_con_cambios | NO_GO
Riesgo de rechazo (Scopus/revisor externo): alto | medio | bajo

## Diagrama del debate
*(Flujo breve: objeciones y preguntas cruzadas hasta el tema final.)*

\`\`\`mermaid
flowchart TD
  tema[TemaEntrada] --> r1[Ronda1_Paralelo]
  r1 --> crit[Critico]
  r1 --> def[Defensor]
  r1 --> soc[ImpactoSocial]
  r1 --> neg[ViabilidadNegocio]
  crit -->|"objecion_clave"| def
  def -->|"contraataque"| crit
  soc -->|"exigencia"| consenso
  neg -->|"exigencia"| consenso
  crit --> r2[Ronda2_Cruce]
  def --> r2
  r2 --> consenso[TemaFinalPropuesto]
\`\`\`

## Fuentes consultadas (panel)
- ...

## Ataques del crítico
- ...
### Fuentes del crítico
- ...

## Defensa
- ...
### Fuentes del defensor
- ...

## Impacto social
- ...
### Fuentes
- ...

## Viabilidad empresarial
- ...
### Fuentes
- ...

## Debate entre agentes
### Choques principales
- Crítico vs Defensor: ...
- Impacto vs Negocio (si aplica): ...
### Preguntas cruzadas
1. El crítico pregunta al defensor: ...
   - Respuesta / resolución: ...
2. El defensor reta al crítico: ...
   - Respuesta / resolución: ...
3. Impacto social exige: ...
4. Viabilidad empresarial exige: ...
### Recomendaciones cruzadas
- El crítico obliga a: ...
- El defensor propone conservar: ...
- Impacto social impone salvaguarda: ...
- Negocio impone salida accionable: ...

## 5 mejoras mínimas antes de presentar
1. ...

## Tema final propuesto
*(Consenso tras el debate. Un solo planteamiento. Listo para `rsl-make-report`.)*

### Título final
...

### Problemática final
...

### Objeto de estudio / objetivo final
...

### Tópicos (3) finales
1. ...
2. ...
3. ...

### Por qué se eligió este recorte
...

### Aporte científico defendible (una frase)
...

### Alcance y exclusiones
- Incluye: ...
- Excluye: ...

### Riesgos residuales y cómo mitigarlos
- ...

### Criterios de éxito ante un revisor Scopus
- ...

### Listo para siguiente skill
`rsl-make-report` sobre `docs/[titulo-breve]/`
```

## Forbidden

- Soft consensus without critic pressure; agents concluding without web search.
- Inventing DOI or papers.
- Skipping `## Tema final propuesto` or `## Diagrama del debate`, or leaving the Mermaid example generic.
- Writing `informe.md` here.
