# Reporte qa:destroy — 2026-09-30

Casos: 80 · fallidos: 2 · grupos: destruir, marco, orden, positivo, skills

## Fallos

| Caso | Grupo | Qué se probó | Comando | Esperado | Obtenido | Problema | Sospechoso |
|---|---|---|---|---|---|---|---|
| S06 | skills | README lista todas las skills rsl-* | `(verificación)` | OK | README.md no menciona `rsl-cribado-2` | README.md no menciona `rsl-cribado-2` | .cursor/skills · .cursor/agents · README |
| S06 | skills | README lista todas las skills rsl-* | `(verificación)` | OK | README.md no menciona `rsl-cribado-2-memoria` | README.md no menciona `rsl-cribado-2-memoria` | .cursor/skills · .cursor/agents · README |
| P07 | positivo | rsl:source convierte un PDF real en MD junto al PDF y no lo rehace si está al día | `python3 scripts/rsl-source.py global/bibliography/prisma/page-2021-prisma-2020.pdf` | OK | ERROR: fallo interno (AttributeError): 'NoneType' object has no attribute '__dict__'. reporta el caso con rsl-qa-destroy. | se esperaba OK y salió ERROR; falta en la salida: «generado» | scripts/rsl-source.py |
| P07 | positivo | rsl:source convierte un PDF real en MD junto al PDF y no lo rehace si está al día | `(verificación)` | OK | rsl:source no escribió el MD junto al PDF | rsl:source no escribió el MD junto al PDF | .cursor/skills · .cursor/agents · README |
| P07 | positivo | rsl:source convierte un PDF real en MD junto al PDF y no lo rehace si está al día | `(verificación)` | OK | el MD global arrastra los ganchos de relevancia de un tema | el MD global arrastra los ganchos de relevancia de un tema | .cursor/skills · .cursor/agents · README |
| P07 | positivo | rsl:source convierte un PDF real en MD junto al PDF y no lo rehace si está al día | `(verificación)` | OK | rsl:source no dejó el texto por página en _raw/ | rsl:source no dejó el texto por página en _raw/ | .cursor/skills · .cursor/agents · README |
| P07 | positivo | rsl:source convierte un PDF real en MD junto al PDF y no lo rehace si está al día | `python3 scripts/rsl-source.py global/bibliography/prisma/page-2021-prisma-2020.pdf` | OK | ERROR: fallo interno (AttributeError): 'NoneType' object has no attribute '__dict__'. reporta el caso con rsl-qa-destroy. | se esperaba OK y salió ERROR; falta en la salida: «ya estaba al día» | scripts/rsl-source.py |
| P07 | positivo | rsl:source convierte un PDF real en MD junto al PDF y no lo rehace si está al día | `pnpm -s rsl:source global/bibliography/prisma/page-2021-prisma-2020.pdf --force` | OK | ERROR: fallo interno (AttributeError): 'NoneType' object has no attribute '__dict__'. reporta el caso con rsl-qa-destroy. | se esperaba OK y salió ERROR; falta en la salida: «generado» | package.json / scripts |

## Ataques propuestos

_(los agrega rsl-qa-destroy tras la corrida; rsl-qa-fix los convierte en casos)_
