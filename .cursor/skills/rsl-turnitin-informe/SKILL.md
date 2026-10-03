---
name: rsl-turnitin-informe
description: >-
  Simulación Turnitin RSL paso 1: turnitin:qualified + agente turnitin-rsl →
  *-informe-turnitin.md (contrato playbook). El usuario debe indicar la ruta del
  paper-polish.md o informe-polish.md. Use when user says rsl-turnitin-informe.
disable-model-invocation: true
---

# rsl-turnitin-informe

Genera el informe detallado **`{stem}-informe-turnitin.md`** junto al archivo que indiques (p. ej. `paper-polish.md`). No modifica el polish.

SoT: [`playbooks/deteccion-escritura-ia-turnitin.md`](playbooks/deteccion-escritura-ia-turnitin.md).

## Invoke

```text
Usa rsl-turnitin-informe sobre docs/<slug>/paper/<fecha>/paper-polish.md
```

**Sin path** → pedir la ruta completa; no inferir el polish más reciente.

## Salida

| Origen | Informe |
|--------|---------|
| `paper-polish.md` | `paper-polish-informe-turnitin.md` |
| `informe-polish.md` | `informe-polish-informe-turnitin.md` |

Misma carpeta que el origen. `{stem}` = nombre del archivo sin `.md`.

## Procedure

1. Comprobar que existe el archivo indicado por el usuario.
2. Ejecutar `pnpm -s turnitin:qualified <ruta>`. Si exit ≠ 0, escribir informe mínimo `NO_PROCESABLE` si aplica y cerrar **ERROR** con el mensaje del script.
3. Lanzar subagente **`turnitin-rsl`** con: ruta fuente, JSON íntegro de qualified, idioma (`languageHint` del JSON, default `es`).
4. Escribir `{dir}/{stem}-informe-turnitin.md` con la respuesta del agente.
5. Validar: frontmatter YAML con `turnitin_rsl_informe: "1"`, sección `## Tramos accionables` con tabla, `## Orden de aplicación`. Si falta → relanzar agente una vez; si sigue fallando → **ERROR**.

## Cierre

Una sola línea en chat:

- Fallo: `ERROR: <paso>. <arreglo>.`
- OK: `OK: <stem>-informe-turnitin.md en <dir>; indicador simulado <valor>; <n> tramos reescritura. Próximo paso: Usa rsl-turnitin-arreglar sobre <misma ruta del polish>.`

## Forbidden

- Inferir paper o informe sin path del usuario.
- Editar `paper-polish.md` / `informe-polish.md`.
- Humanizers, bypassers, R12–R13.
- Formato libre distinto al contrato del playbook.
