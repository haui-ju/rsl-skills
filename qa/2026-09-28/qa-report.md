# Reporte qa:destroy — 2026-09-28

Casos: 51 · fallidos: 8 · grupos: destruir, marco, orden, positivo, skills

## Fallos

| Caso | Grupo | Qué se probó | Comando | Esperado | Obtenido | Problema | Sospechoso |
|---|---|---|---|---|---|---|---|
| D01 | destruir | paper.yml con YAML roto | `/usr/bin/python3 scripts/picoc-lint.py --latest docs/t021` | ERROR |             ^. reporta el caso con rsl-qa-destroy. | la última línea no empieza por OK: ni ERROR:; se esperaba ERROR y salió ?; falta en la salida: «YAML» | scripts/picoc-lint.py |
| D01 | destruir | paper.yml con YAML roto | `/usr/bin/python3 scripts/picoc-lint.py docs/t021` | ERROR |             ^. reporta el caso con rsl-qa-destroy. | la última línea no empieza por OK: ni ERROR:; se esperaba ERROR y salió ?; falta en la salida: «YAML» | scripts/picoc-lint.py |
| D13 | destruir | ficha sin pregunta en la § 1.2 y con dos preguntas | `/usr/bin/python3 scripts/picoc-lint.py docs/t040` | ERROR | OK: picoc docs/t040/picoc/2026-09-28-PICOCT/picoc.md (PICOCT) válido: 5 bloques, 73 términos, 6 RQ, T 2020–2026, 3 bases. | se esperaba ERROR y salió OK | scripts/picoc-lint.py |
| D13 | destruir | ficha sin pregunta en la § 1.2 y con dos preguntas | `/usr/bin/python3 scripts/picoc-lint.py docs/t040` | ERROR | OK: picoc docs/t040/picoc/2026-09-28-PICOCT/picoc.md (PICOCT) válido: 5 bloques, 73 términos, 6 RQ, T 2020–2026, 3 bases. | se esperaba ERROR y salió OK; falta en la salida: «1.2» | scripts/picoc-lint.py |
| D14 | destruir | picoc vacío, sin **Marco:**, sin queries, con DOCTYPE y con T invertido | `/usr/bin/python3 scripts/picoc-lint.py docs/t045` | ERROR | ERROR: el picoc docs/t045/picoc/2026-09-28-PICOCT/picoc.md (PICOCT) tiene 3 error(es) (ver detalle arriba). corrígelo regenerando una versión con rsl-picoc. | falta en la salida: «años» | scripts/picoc-lint.py |
| D15 | destruir | carpetas basura en picoc/ y paper/ se ignoran | `/usr/bin/python3 scripts/picoc-lint.py --latest docs/t046` | OK | OK: marco PICOCT al día (docs/t046/picoc/2026-13-45-PICOCT/picoc.md). | falta en la salida: «2026-09-28-PICOCT» | scripts/picoc-lint.py |
| D15 | destruir | carpetas basura en picoc/ y paper/ se ignoran | `/usr/bin/python3 scripts/picoc-lint.py docs/t046` | OK | ERROR: docs/t046/picoc/2026-13-45-PICOCT/picoc.md no declara '**Marco:** <letras>' (p. ej. PICOCT, PIO). regenera el marco con rsl-picoc. | se esperaba OK y salió ERROR | scripts/picoc-lint.py |
| D15 | destruir | carpetas basura en picoc/ y paper/ se ignoran | `/usr/bin/python3 scripts/paper-manifest.py docs/t046` | OK | OK: paper/2026-99-99: 0 a mejorar, 6 a reescribir. Próximo paso: rsl-make-paper. | no debería aparecer: «2026-99-99» | scripts/paper-manifest.py |
| D17 | destruir | argumentos inválidos en todos los scripts | `pnpm -s thesaurus:check` | ERROR | thesaurus-ieee.py: error: argument --check: expected at least one argument | la última línea no empieza por OK: ni ERROR:; se esperaba ERROR y salió ? | package.json / scripts |
| K02 | marco | variantes inválidas: PIX, PICCC, 123, vacío, P-I-O, PICoO, solo T | `/usr/bin/python3 scripts/picoc-lint.py --latest docs/t060` | ERROR | OK: marco PICOCT al día (docs/t060/picoc/2026-09-28-PICOCT/picoc.md). | se esperaba ERROR y salió OK; falta en la salida: «vacío» | scripts/picoc-lint.py |
| K02 | marco | variantes inválidas: PIX, PICCC, 123, vacío, P-I-O, PICoO, solo T | `/usr/bin/python3 scripts/paper-manifest.py docs/t063` | ERROR | OK: paper/—: 0 a mejorar, 3 a reescribir, 3 blocked. Próximo paso: Usa rsl-picoc sobre docs/t063/. | se esperaba ERROR y salió OK | scripts/paper-manifest.py |
| S03 | skills | agentes *-rsl y skills rsl-* citados existen; nombre del frontmatter = carpeta | `(verificación)` | OK | .cursor/skills/rsl-qa-destroy/SKILL.md: la skill rsl-qa no existe en .cursor/skills/ | .cursor/skills/rsl-qa-destroy/SKILL.md: la skill rsl-qa no existe en .cursor/skills/ | .cursor/skills · .cursor/agents · README |
| S04 | skills | cada skill rsl-* tiene la sección Cierre con el contrato OK/ERROR | `(verificación)` | OK | .cursor/skills/rsl-bootstrap/SKILL.md: falta '## Cierre' | .cursor/skills/rsl-bootstrap/SKILL.md: falta '## Cierre' | .cursor/skills · .cursor/agents · README |
| S04 | skills | cada skill rsl-* tiene la sección Cierre con el contrato OK/ERROR | `(verificación)` | OK | .cursor/skills/rsl-make-paper/SKILL.md: falta '## Cierre' | .cursor/skills/rsl-make-paper/SKILL.md: falta '## Cierre' | .cursor/skills · .cursor/agents · README |
| S04 | skills | cada skill rsl-* tiene la sección Cierre con el contrato OK/ERROR | `(verificación)` | OK | .cursor/skills/rsl-make-report/SKILL.md: falta '## Cierre' | .cursor/skills/rsl-make-report/SKILL.md: falta '## Cierre' | .cursor/skills · .cursor/agents · README |
| S04 | skills | cada skill rsl-* tiene la sección Cierre con el contrato OK/ERROR | `(verificación)` | OK | .cursor/skills/rsl-picoc/SKILL.md: falta '## Cierre' | .cursor/skills/rsl-picoc/SKILL.md: falta '## Cierre' | .cursor/skills · .cursor/agents · README |
| S04 | skills | cada skill rsl-* tiene la sección Cierre con el contrato OK/ERROR | `(verificación)` | OK | .cursor/skills/rsl-polish-paper/SKILL.md: falta '## Cierre' | .cursor/skills/rsl-polish-paper/SKILL.md: falta '## Cierre' | .cursor/skills · .cursor/agents · README |
| S04 | skills | cada skill rsl-* tiene la sección Cierre con el contrato OK/ERROR | `(verificación)` | OK | .cursor/skills/rsl-polish-report/SKILL.md: falta '## Cierre' | .cursor/skills/rsl-polish-report/SKILL.md: falta '## Cierre' | .cursor/skills · .cursor/agents · README |
| S04 | skills | cada skill rsl-* tiene la sección Cierre con el contrato OK/ERROR | `(verificación)` | OK | .cursor/skills/rsl-topic-panel/SKILL.md: falta '## Cierre' | .cursor/skills/rsl-topic-panel/SKILL.md: falta '## Cierre' | .cursor/skills · .cursor/agents · README |

## Ataques propuestos

| Ataque | Comando | Esperado | Obtenido | ¿Rompe? | Por qué importa |
|---|---|---|---|---|---|
| A1 | paper:status / picoc:lint sobre 'docs/tema con ñ y espacios' | OK | OK | no | rutas reales con acentos y espacios |
| A2 | picoc:latest con picoc/<fecha>-PICOCT/picoc.md convertido en carpeta | ERROR claro | ERROR: picoc FALTA | no | no se cae; el mensaje podría nombrar la carpeta |
| A3 | chmod 444 paper.state.jsonc; paper:status --update borrador | ERROR: sin permiso de escritura en paper.state.jsonc | ERROR: fallo interno (PermissionError) | sí | el usuario no sabe qué arreglar |
| A4 | picoc/2099-01-01-PICOCT/picoc.md válido; picoc:latest | ERROR: versión con fecha futura | OK: marco PICOCT al día (2099-01-01-PICOCT) | sí | una carpeta con fecha futura queda como 'último' para siempre |
| A5 | paper.yml con 'contexto: Frozen' | OK (estado sin distinguir mayúsculas) | ERROR: valor inválido | sí | valor humano razonable rechazado |
| A6 | tema como symlink | OK | OK | no | clones con enlaces |
| A7 | borrar picoc/ con el paper ya generado; paper:status | OK con BLOCKED y próximo paso rsl-picoc | igual | no | recuperación del flujo |
| A8 | carpetas paper/2026-09-28-0 y 2026-09-28-01; --new-version | se ignoran o ERROR; la versión nueva es la última | crea 2026-09-28 que no queda como última (copia de -01) | sí | el orden de versiones se corrompe |
| A9 | chmod 555 paper/; --new-version | ERROR: sin permiso de escritura en paper/ | ERROR: fallo interno (PermissionError) | sí | mensaje no accionable |
| A10 | RQ con '\\|' escapado y '?' interna | OK | OK | no | tablas markdown reales |
| A11 | picoc/2026-09-28-PICOCT y 2026-09-28-PICO (misma fecha y n); picoc:latest | ERROR: dos versiones con la misma fecha y número | elige por fecha de modificación en silencio | sí | resultado depende del reloj del sistema de archivos |
