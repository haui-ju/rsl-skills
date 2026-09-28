# Vocabulario controlado IEEE — PICO / PICOC / PICOCT / keywords / queries

Fuente de verdad para **cualquier** término de búsqueda que produzca una skill `rsl-*`: IEEE Thesaurus 2019 (`global/thesaurus/IEEE.pdf`, ~10.4k términos), indexado en `global/thesaurus/graphify-out/graph.json`.

Objetivo: términos **fieles** (descriptor oficial + sinónimos oficiales) y **cero descriptores inventados**. Lo que IEEE no tiene se declara como término libre, con justificación.

## Herramientas

| Uso | Comando |
|-----|---------|
| Validar muchos términos en **una** llamada (preferido) | `pnpm -s thesaurus:check "term 1" "term 2" …` → tabla Markdown |
| Ficha completa de un término | `pnpm -s thesaurus:lookup "term"` |
| Vecinos con relación + página | `graphify explain "Term" --graph global/thesaurus/graphify-out/graph.json` |
| Explorar un concepto (amplio, con ruido) | `graphify query "concepto" --graph global/thesaurus/graphify-out/graph.json` |

Si `global/thesaurus/ieee-thesaurus.json` o el grafo no existen → pedir `Usa rsl-bootstrap` (o `pnpm run bootstrap`). **No** continuar inventando descriptores.

## Estados que devuelve `thesaurus:check`

| Estado | Qué hacer |
|--------|-----------|
| **IEEE preferido** | Usar el descriptor tal cual. Sus **UF** son sinónimos oficiales → van en el mismo bloque `OR`. |
| **IEEE no preferido → USE** | Sustituir por el descriptor de la columna *Descriptor IEEE*; el término original queda como sinónimo. |
| **LIBRE (sin descriptor IEEE)** | Mantener como término libre **marcado** y justificado (p. ej. concepto posterior a 2019, estándar W3C, término clínico). Opcional: fuente externa (W3C COGA, MeSH). |
| *Cercanos* | Pistas para explorar, **no** equivalentes. Solo reemplazan a un término libre si el significado es el mismo, y se justifica. |

## Procedimiento (obligatorio)

1. **Conceptos por componente** del marco elegido (tabla abajo), en español.
2. **Candidatos EN**: 2–4 formulaciones por concepto (singular, variantes con guion, siglas).
3. **Una sola** llamada `pnpm -s thesaurus:check …` con todos los candidatos (no gastar tokens término a término).
4. **Clasificar** según la tabla de estados.
5. **Expandir con criterio**:
   - UF → siempre al `OR` del concepto.
   - NT → solo los que caen dentro del alcance/exclusiones del tema (no volcar todos).
   - RT → nunca automático; solo si el alcance lo pide y se justifica.
   - BT → no se usa en la query (amplía demasiado); sirve para ubicar el concepto.
6. **Query por bloques**: `(descriptor OR UF OR libres del concepto) AND (…) AND (…)`; truncamiento (`*`) solo sobre términos libres o plurales, no para deformar descriptores.
7. **Trazabilidad**: debajo de la query, lista de términos libres con su justificación y el número de página IEEE de cada descriptor usado.

## Marcos

| Marco | Componentes | Validación IEEE |
|-------|-------------|-----------------|
| PICO | Población · Intervención · Comparación · Outcome (resultado) | P, I, C, O |
| PICOC | PICO + **C**ontexto | P, I, C, O, Contexto |
| PICOCT | PICOC + **T** (tiempo / tipo de estudio) | T **no** se valida: es filtro (`PUBYEAR`, `DOCTYPE`) |
| SPIDER / otros | según el marco | todo concepto de búsqueda |

En Ingeniería de Software, “Población” suele ser el artefacto/sistema o el perfil de usuario; “Intervención”, la técnica (p. ej. IA); “Outcome”, métricas/calidad.

## Formato de salida

### Tabla del marco

```markdown
| Componente | Concepto (ES) | Descriptor IEEE | Sinónimos (UF / variantes) | Términos libres (justificación) | Pág. IEEE |
|------------|---------------|-----------------|----------------------------|----------------------------------|-----------|
| P | … | Autism | — | "autism spectrum disorder" (forma clínica usada en títulos) | p.35 |
| I | … | Machine learning | Machine-learning | "large language model*" (LIBRE: posterior a 2019) | p.294 |
```

### Tabla de palabras clave

```markdown
| Español | Inglés | Tipo | Pág. IEEE |
|---------|--------|------|-----------|
| aprendizaje automático | machine learning | IEEE | p.294 |
| interacción humano-computador | human computer interaction | IEEE (USE desde "human-computer interaction") | p.232 |
| accesibilidad cognitiva | cognitive accessibility | Libre | — |
```

`Tipo` ∈ `IEEE` · `IEEE (USE desde "…")` · `Libre`.

## Prohibido

- Presentar como “descriptor IEEE” un término que `thesaurus:check` marcó LIBRE.
- Usar un término **no preferido** como descriptor principal cuando existe su USE.
- Sustituir un término libre por un *cercano* no equivalente para “parecer controlado”.
- Añadir RT o todos los NT sin justificar alcance.
- Validar términos “de memoria” sin ejecutar `thesaurus:check` / `lookup`.
