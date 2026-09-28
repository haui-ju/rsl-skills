# Fixtures de qa:destroy

Material fijo que `scripts/qa-destroy.py` copia a un sandbox en /tmp para romper el flujo sin tocar `docs/`.

- `informe.md`: ficha mínima y limpia (pasa `redaccion:lint`); su § 1.2 es la pregunta general de los picoc.
- `picoc-PICOCT.md`: marco PICOCT válido (pasa `picoc:lint`).
- `picoc-PIO.md`: el mismo marco reducido a P, I, O, sin filtro de año.
- `paper-borrador.md`: borrador limpio con las secciones que `--init` deja en on.

Si cambian las reglas de un lint, actualiza aquí el fixture afectado; no relajes el caso.
