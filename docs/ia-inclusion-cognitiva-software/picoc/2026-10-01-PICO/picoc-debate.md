# Debate — picoc 2026-10-01-PICO (modo parcial, CR)

**Fecha:** 2026-10-01 · **Base:** `picoc/2026-09-29-2-PICO/picoc.md` · **Cambio:** criterios de inclusión y exclusión (petición del usuario) y alineación R2 de Scopus, Web of Science e IEEE Xplore con el tipo documental.

## Qué cambió

| Área | Acción |
|------|--------|
| CI empírico (métrica/instrumento obligatorio) | Eliminado (petición explícita; RQ4 sigue extrayendo métricas en cribado 2) |
| CE duplicados, sin texto completo, SLR para delimitar vacío | Eliminados (deduplicación = PRISMA técnico; acceso al texto = gestión de recuperación, no CE) |
| CE preprints/tesis/editoriales/congreso | Sustituido por CI2 (revista + congreso) y CE1 (artículos de revisión y secundarios) |
| Queries Scopus/WoS/IEEE | `ar`+`cp` / Article+Proceedings Paper / nota de Conference Proceedings |

## Posiciones (resumen)

**critico-rsl:** CI2 (solo OA) y CI3 («dirigidos a») pueden recortar recall en cribado 1; CI4 en inclusión repite el riesgo de exigir fase en el resumen; sin criterio empírico aumenta ruido protocolo/opinión; CE1 sigue excluyendo SLR del corpus primario (coherente con síntesis primaria).

**defensor-rsl:** CI1–CI4 y CE2–CE5 anclan PICO y los falsos positivos del cribado 1; congreso en CI2 recupera prototipos SE/GenAI; recomendó reintroducir CI empírico y CE de duplicados/texto (rechazado por el usuario en esta versión).

## Decisiones

| Tema | Decisión |
|------|----------|
| Tipos documentales | CI2: artículos de revista **o** artículos de congreso revisados por pares, OA, EN/ES; CE1: artículos de revisión y secundarios sin empírico primario |
| Empírico obligatorio en CI | No en esta versión |
| Duplicados / texto completo como CE | No (playbook CR + `cribado:prepare`) |
| Queries | Actualizadas para coincidir con CI2 (`ar`+`cp`) |

## Pendiente para el usuario

- Cribado 1: regla de duda cuando falte población o fase en el resumen pero haya IA + software + perfil cognitivo implícito.
- Modo **sugerencia** del cribado 1 (`cribado-1-sugerencia.md`) sigue pendiente en otra versión picoc si se desea aplicar keywords.
