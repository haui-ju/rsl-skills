---
name: rsl-turnitin-arreglar
description: >-
  Simulación Turnitin RSL paso 2: lee *-informe-turnitin.md y genera
  paper-polish-turnitin.md o informe-polish-turnitin.md sin tocar el polish
  original. Requiere rsl-turnitin-informe previo. Use when user says
  rsl-turnitin-arreglar.
disable-model-invocation: true
---

# rsl-turnitin-arreglar

Aplica la remediación legítima del informe Turnitin y escribe la versión entregable **`*-turnitin.md`**.

SoT remediación: [`playbooks/deteccion-escritura-ia-turnitin.md`](playbooks/deteccion-escritura-ia-turnitin.md) §Remediación y §Contrato (§2 Tramos accionables).

## Invoke

```text
Usa rsl-turnitin-arreglar sobre docs/<slug>/paper/<fecha>/paper-polish.md
```

**Misma ruta** que usaste en `rsl-turnitin-informe`. Sin path → pedirla.

## Precondición

Existe `{dir}/{stem}-informe-turnitin.md` (stem del polish). Si no → `ERROR: ejecuta rsl-turnitin-informe primero sobre la misma ruta.`

## Salida

| Origen polish | Archivo generado |
|---------------|------------------|
| `paper-polish.md` | `paper-polish-turnitin.md` |
| `informe-polish.md` | `informe-polish-turnitin.md` |

El polish original **solo lectura**.

## Procedure

1. Leer polish (completo), `{stem}-informe-turnitin.md` (frontmatter + `## Tramos accionables` + `## Orden de aplicación`), y playbook §Remediación.
2. Copiar el polish íntegro como base del archivo `*-turnitin.md`.
3. Por cada `tramo_id` en orden de aplicación con `accion_tipo: reescritura`:
   - Aplicar los `pasos` del informe sobre las oraciones indicadas (mapear `S*` al texto vía informe/diagnóstico o re-ejecutar mentalmente el JSON qualified si hace falta).
   - Preservar citas, datos numéricos, DOI y referencias exactos.
   - Si el tramo cae en sección **frozen** del paper (`config.yml`), **avisar en chat** antes de cambiar; no cambiar sin confirmación implícita del usuario en el invoke.
4. Tramos `proceso`: no editar prosa; listar en chat checklist R1–R3 del informe.
5. Tramos `ninguna` o indicador `*%` sin reescritura: dejar prosa igual; OK con nota.
6. `pnpm -s redaccion:lint <archivo-turnitin>`; si FAIL → **`redaccion-rsl`** (solo forma) hasta 0 FAIL.
7. Si es paper: `pnpm -s paper:status docs/<slug> --cites <archivo-turnitin>`; si FAIL, corregir citas sin vaciar contenido.

## Cierre

- Fallo: `ERROR: <paso>. <arreglo>.`
- OK: `OK: <stem>-turnitin.md en <dir>. Revisa tramos fp_riesgo y confianza baja del informe antes de Turnitin institucional.`

## Forbidden

- R12–R13; humanizerai; parafraseadores anti-detector.
- Sobrescribir `paper-polish.md` / `informe-polish.md`.
- Informe de otro stem o carpeta.
- Borrar citas para bajar puntaje simulado.
