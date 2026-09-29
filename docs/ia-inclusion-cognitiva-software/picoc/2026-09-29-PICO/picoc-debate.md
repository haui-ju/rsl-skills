# Debate del marco PICO — 2026-09-29

**Versión base:** `picoc/2026-09-28-7-PICO/picoc.md` · **Modo:** parcial (solo citas de vocabulario; sin agentes)

## Qué cambió y por qué

- La versión base usaba la ACM CCS y los MeSH en las justificaciones, pero la cabecera no los citaba con autor y año. `picoc:lint` fallaba por la nueva regla VOC (`playbooks/vocabulario-controlado.md`).
- La cabecera **Vocabulario** cita ahora los tres vocabularios usados: IEEE Thesaurus (IEEE, 2019), ACM Computing Classification System (ACM, 2012) y Medical Subject Headings (NLM, 2026). Las referencias están en `global/bibliography/bibliography.md` (`ieee-2019-thesaurus`, `acm-ccs-2012`, `nlm-2026-mesh`).
- La justificación de `user study` cita el concepto ACM CCS *User studies* (Human-centered computing → HCI design and evaluation methods), que sustenta ese término libre.

## Decisiones

| Decisión | Motivo |
|---|---|
| Sin cambios en términos, queries ni criterios | Solo cambian las citas, así que no cambia lo que recupera la búsqueda |
| Sin debate de agentes | No hay términos ni criterios nuevos que discutir |

## Para el usuario

- El paper debe re-sincronizar la nota de la Tabla III y sumar a Referencias las entradas de la ACM y de la NLM (`rsl-polish-paper`).
