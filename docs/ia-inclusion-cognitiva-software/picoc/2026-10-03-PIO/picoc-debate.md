# Debate — picoc 2026-10-03-PIO (modo completo, cambio de marco)

**Fecha:** 2026-10-03 · **Base:** `picoc/2026-10-01-PICO/picoc.md` · **Cambio:** `formato.marco` → PIO (sin componente C de comparación); petición del usuario.

## Qué cambió

| Área | Acción |
|------|--------|
| Marco | PICO → PIO: tres bloques AND (P, I, O); RQ3 absorbe marcos COGA/WCAG y contraste cognitivo/sensorial en extracción |
| Query | Eliminado bloque C (discapacidad sensorial, lectores de pantalla); WCAG, `accessibility` y diseño inclusivo pasan al bloque O |
| Keywords paper | Sustituida keyword WCAG (comp. C) por *Machine learning* (I); se mantienen 6 filas KY |
| CI3 | Alineado con el bloque P (neurodiversidad, disgrafía, discalculia) |
| Cribado 1 sugerencia | No aplicada (cambio de marco prioriza versión PIO nueva; la sugerencia de `2026-10-01-PICO` queda obsoleta para esta ecuación) |

## Posiciones (resumen)

**critico-rsl:** `accessibility` y `metric*` en O amplían ruido (WCAG/GenAI sin P claro); COGA no tiene término en query; CI4/SDLC solo en cribado; Perry sigue sin cubrir O en resumen; opcional acotar chatbots en I.

**defensor-rsl:** PIO aumenta recall del núcleo P+I frente al AND sensorial del C; CE2 y RQ3 conservan el contraste; WCAG en O refleja outcomes normativos; fase SDLC en CI4 y extracción RQ2; no reintroducir C como AND.

**redaccion-rsl:** RQ3-O y justificación O reescritas (dos preguntas, COGA/WCAG expandidas, sin jerga «bloque AND»).

## Decisiones

| Tema | Decisión |
|------|----------|
| Bloque C | No reintroducido; contraste sensorial en CE2 + dato RQ3 |
| `accessibility` en O | Se mantiene (marco normativo dominante; coherente con validación Chemnad/Aljedaani) |
| `metric` / `metrics` | Se mantienen (versión PICO ya los justificaba; cribado 2 filtra) |
| Términos COGA en query | No se añade sigla `COGA`; `"cognitive accessibility"` permanece en P |
| SDLC en query | No se añade bloque Contexto; CI4 + extracción RQ2 |

## Pendiente para el usuario

- Ejecutar cribado 1 de nuevo con la ecuación PIO (conteos Scopus/WoS vs. PICO).
- Formar 3–5 estudios primarios de control para `## Validación de la búsqueda`.
- Actualizar enlace de § 2 del informe (`rsl-polish-report`) y secciones del paper en `frozen` que dependan del marco (`paper:status`).
