# Sugerencia de ampliación de query (cribado 1)

## Defensor

La query actual suma **100** keywords (tope). Tras cribado 1 solo **3** términos cumplen retirada (0 SI y ≥3 NO exclusivos). Se liberan 3 huecos para incorporar evidencia de palabras clave aceptadas no cubiertas y descriptores IEEE del ciclo de vida (CI4), sin reintroducir el bloque AND de ingeniería de software ni `cognitive impairment*` (demencia/diagnóstico, excluido en picoc).

### Tabla de propuesta

| Comp. | Término | Estado | Evidencia | Propuesta |
|---|---|---|---|---|
| P | `learning difficult*` | quitar | 0 SI, 4 NO exclusivos | Sustituido por `learning disabilit*` y variantes MeSH |
| I | `context-aware` | quitar | 0 SI, 3 NO exclusivos | Mantener `context awareness` (IEEE p.106) |
| O | `metrics` | quitar | 0 SI, 12 NO exclusivos; plural de `metric` (2 NO, 0 SI) | Conservar `metric` y métricas nombradas (`readability`, `usability`, etc.) |
| I | `software design` | agregar | 2 SI en aceptados; keyword sin cubrir; IEEE p.497; NT Usability | OR en bloque I; refuerza CI4 sin bloque AND de ingeniería |
| I | `mobile applications` | agregar | 2 SI (`mobile applications`, `mobile web applications`); IEEE p.336 | OR en bloque I; artefactos móviles en el resumen |
| I | `user profile` | agregar | 3 SI, 0 NO; thesaurus:check → libre (perfil de personalización) | OR en bloque I; alinea personalización en tiempo de ejecución (RQ2) |
| I | `software prototyping` | reserva | 2 SI; IEEE p.498; sin hueco tras 3+3 | Añadir solo si una futura retirada libera slot |
| I | `accessible content generation` | reserva | 1 SI; libre; COGA/GenAI | Misma condición |
| C | `web sites` | reserva | 2 SI (`websites`); IEEE p.584 UF de consulta `websites` | Preferir descriptor IEEE frente a forma libre |
| I | `natural language generation` | mantener | 0 registros en cribado 1 | Ya en query; ACM CCS; no cumple retirada |
| P | `autistic` | mantener | 0 SI, 0 NO exclusivos | Regla: no retirable |
| P | `attention deficit` | mantener | 0 SI, 2 NO exclusivos | Por debajo del umbral de retirada |
| I | `chatbot` | mantener | 0 SI, 1 NO exclusivo | Puede aportar en nueva búsqueda |
| O | `easy read` | mantener | 0 SI, 2 NO exclusivos | Variante británica de lectura fácil |
| P | `cognitive impairment` | no agregar | 1 SI en aceptados | Picoc excluye por ruido demencia/diagnóstico; usar perfiles P existentes |
| — | `COGA` | no agregar | — | Ruido genético; frase `coga guideline*` solo como reserva |

### Bloques OR propuestos (cambios respecto a `picoc.md`)

**P** — eliminar: `"learning difficult*"`.

**I** — eliminar: `"context-aware"`. Añadir: `"software design"` · `"mobile applications"` · `"user profile"`.

**O** — eliminar: `metrics`.

**C** — sin cambio en esta ronda (huecos absorbidos por I).

### Fragmentos para Scopus / WoS (bloques I y P, O)

```text
# P (extracto)
... OR dyslexi* OR "cognitive accessibility" OR Asperger
  OR "intellectual developmental disorder" OR "learning disorder*"
  OR dyscalculia OR dysgraphia OR "reading disabilit*" )
# (sin "learning difficult*")

# I (extracto)
... OR "ambient intelligence" OR "context awareness"
  OR "reinforcement learning" OR "contrastive learning"
  OR "software design" OR "mobile applications" OR "user profile" )

# O (extracto)
( usability OR "user experience" OR metric OR "accessibility metric"
# (sin metrics)
  OR "readability metrics" OR readability ...
```

**Conteo:** 100 − 3 + 3 = **100** keywords.

### Términos que no aportan en cribado 1 pero se conservan

`autistic`, `attention deficit`, `learning disorder*`, `dysgraphia`, `reading disabilit*`, `chatbot`, `conversational agents`, `intelligent agents`, `virtual agent`, `context-aware` (si no se aplica aún el parche), `reinforcement learning`, `deafness`, `visual impairment`, `visually impaired`, `metric`, `metrics`, `readability metrics`, `easy read`, `user satisfaction`, `user acceptance`, más los **16** sin registros (`asperger`, `dyscalculia`, `text mining`, `adaptive user interface`, etc.): ninguno alcanza 0 SI con ≥3 NO exclusivos salvo los tres propuestos a quitar.

## Crítico

| Comp. | Término | Propuesta | Tu posición | Motivo |
|---|---|---|---|---|
| O | `metrics` | quitar | no quitar | keywords.md: 1 SI y 16 registros; incumple la regla (0 SI y ≥3 NO exclusivos) |
| I | `software design` | agregar | no agregar | IEEE *Software design* (p.497) es fase SDLC, no técnica de IA; el bloque I no sustituye el contexto retirado |
| I | `mobile applications` | agregar | no agregar | Plataforma (IEEE p.336), no familia de IA; en el cribado previo del tema se descartó por bloque |
| I | `user profile` | agregar | no agregar | 3 SI pero indizador genérico de personalización; no es técnica de IA y amplía software sin ML |
| I | `software prototyping` | reserva | agregar en lugar de `software design` | 2 SI, IEEE p.498; prototipo evaluado encaja mejor con CI4 que el diseño genérico |
