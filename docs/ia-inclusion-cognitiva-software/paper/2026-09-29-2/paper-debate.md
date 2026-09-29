# Debate del paper — 2026-09-29-2

**Versión base:** `paper/2026-09-29/paper-polish.md` · **Picoc:** `picoc/2026-09-29-PICO/picoc.md`

## Qué cambió y por qué

- El picoc nuevo cita en su cabecera los tres vocabularios que usa: IEEE Thesaurus (IEEE, 2019), ACM Computing Classification System (ACM, 2012) y Medical Subject Headings (NLM, 2026). La versión anterior del paper solo citaba el IEEE Thesaurus.
- **palabras-clave** (frozen, re-sincronizada): la _Nota._ de la Tabla III cita ahora los tres vocabularios. La prosa frozen no se tocó.
- **Referencias**: se añadieron las entradas de la Association for Computing Machinery (2012) y de la National Library of Medicine (2026), tomadas del catálogo `global/bibliography/bibliography.md` (`acm-ccs-2012`, `nlm-2026-mesh`).
- **marco-pico** y **ecuacion-busqueda**: sin cambios de contenido; el picoc nuevo no cambia términos ni queries.

## Verificación

| Comprobación | Resultado |
|---|---|
| `paper:status --picoc-sync` | OK (marco-pico, palabras-clave, ecuacion-busqueda, criterios-seleccion) |
| `redaccion:lint` | OK, 0 errores (20 avisos, todos en texto frozen o en la pregunta literal) |
| `paper:status --cites` | OK, 13 referencias coherentes |

## Para el usuario

- El párrafo frozen que presenta la Tabla III menciona solo el IEEE Thesaurus. Si quieres que la prosa también nombre la ACM CCS y los MeSH, pon `palabras-clave: on` en `config.yml` y vuelve a correr `rsl-polish-paper`.
