# qa-fix — ronda 1 sobre qa/2026-09-28

Reporte de partida: `qa/2026-09-28/qa-report.md` (8 casos en ERROR y 11 ataques propuestos). Reporte en verde: `qa/2026-09-28-2/qa-report.md` (60 casos, 0 fallos). Tema real `docs/ia-inclusion-cognitiva-software` intacto: `picoc:lint` en OK y `paper:status` sin versiones nuevas.

| id | causa | arreglo | archivos | caso de regresión |
|----|-------|---------|----------|-------------------|
| D01 | un `paper.yml` con YAML roto hacía caer `configured_marco` y el mensaje salía en varias líneas | `ConfigError` con su arreglo para YAML roto, contenido que no es un mapa o `formato` que no es un mapa; `rsl_out` junta el mensaje en una línea | `picoc_versions.py`, `rsl_out.py`, `paper-manifest.py` | D01 |
| D13 | `picoc:lint` daba OK con la § 1.2 sin pregunta o con varias | `ficha_questions()` exige exactamente una pregunta `¿…?` | `picoc-lint.py` | D13 |
| D14 | un filtro T con los años al revés pasaba | los años invertidos cuentan como error | `picoc-lint.py` | D14 |
| D15 | carpetas con fechas imposibles (`2026-13-45`, `2026-99-99`) se tomaban como versiones | `version_date()` valida la fecha; las carpetas con fechas inválidas se ignoran en picoc/ y paper/ | `picoc_versions.py`, `paper-manifest.py` | D15 |
| D17 | `thesaurus:check` sin términos dejaba el error de argparse en stderr, sin línea ERROR | `ap.error` lanza `Fail` con código 2 | `thesaurus-ieee.py` | D17 |
| K02 | un marco vacío o solo con `T` se aceptaba | `parse_marco` rechaza ambos | `picoc_versions.py` | K02 |
| S03 | el lint de skills leía `rsl-qa-*` como una skill inexistente `rsl-qa` | lookahead `(?!-?\*)` en la expresión regular | `qa-destroy.py` | S03 |
| S04 | 7 skills rsl-* no tenían la sección `## Cierre` con el contrato OK/ERROR | `## Cierre` con su próximo paso en cada skill; el último paso "Chat" ya no repite el próximo paso | `.cursor/skills/rsl-{bootstrap,topic-panel,make-report,polish-report,picoc,make-paper,polish-paper}/SKILL.md` | S04 |
| A3, A9 | con `paper.state.jsonc` de solo lectura o `paper/` sin escritura salía un traceback | `rsl_out.run()` convierte `PermissionError` y `OSError` en ERROR con la ruta y el arreglo | `rsl_out.py` | D21 |
| A4 | una versión con fecha futura quedaba como la última | fechas futuras dan ERROR en picoc/ y paper/ | `picoc_versions.py`, `paper-manifest.py` | D22 |
| A5 | `Frozen` o `' REWRITE '` en paper.yml daban estado desconocido | los estados se normalizan (`strip().lower()`) | `paper-manifest.py` | D23 |
| A8 | carpetas `-0`, `-1` y `-01` se tomaban como versiones | el sufijo exige `n ≥ 2` sin ceros a la izquierda | `picoc_versions.py`, `paper-manifest.py` | D24 |
| A11 | dos picoc con la misma fecha y número elegían uno al azar | ERROR "misma fecha y número" | `picoc_versions.py` | D25 |
| A1, A6, A10, A2, A7 | no rompían nada | se fijan como casos para que no se rompan más adelante | `qa-destroy.py` | D26, D27, D28, M16 |

Mejoras del arnés: los comandos del reporte muestran `python3` y citan las rutas con espacios; `--only` acepta ids (`D21,M16`); `--verbose` muestra todos los pasos.

OK: 13 bugs arreglados y 9 casos nuevos; qa:destroy en verde (qa/2026-09-28-2/). Próximo paso: rsl-qa-destroy para otra ronda, o seguir con el flujo RSL.
