# Reporte qa:destroy — 2026-09-30-3

Casos: 80 · fallidos: 1 · grupos: destruir, marco, orden, positivo, skills

## Fallos

| Caso | Grupo | Qué se probó | Comando | Esperado | Obtenido | Problema | Sospechoso |
|---|---|---|---|---|---|---|---|
| C01 | orden | cribado 1: prepare pasa WoS a CSV, une Scopus y WoS en resultados-<MARCO>.csv y deduplica (DOI y título, dentro y entre bases) antes de los lotes; report escrib | `(verificación)` | OK | criterios.md convirtió la deduplicación técnica en un criterio científico | criterios.md convirtió la deduplicación técnica en un criterio científico | .cursor/skills · .cursor/agents · README |

## Ataques propuestos

_(los agrega rsl-qa-destroy tras la corrida; rsl-qa-fix los convierte en casos)_
