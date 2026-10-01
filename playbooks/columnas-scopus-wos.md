# Columnas de Scopus y Web of Science (cribado 1)

Fuente de verdad para `scripts/cribado.py` y la skill `rsl-cribado-1`: qué cabecera trae cada exportación y cómo se unifican. El usuario deja los archivos en la carpeta del último picoc (`docs/<slug>/picoc/<fecha>-<MARCO>/`).

## Exportaciones que se aceptan

| Base | Archivo | Cómo exportar |
|---|---|---|
| Scopus | `*.csv` (UTF-8, cabecera en la fila 1) | Export → CSV, con *Citation information* y *Abstract & keywords* |
| Web of Science | `*.xls` (Excel, hoja 1, cabecera en la fila 1) | Export → Excel, *Full Record* |
| Web of Science | `*.txt` (texto delimitado por tabulaciones, etiquetas de dos letras) | Export → Tab delimited file, *Full Record* |

El `.xls` se lee con `xlrd` (entorno de graphify: `pipx inject graphifyy xlrd`) y se convierte a `wos-resultados.csv` con las mismas cabeceras del Excel. El `.txt` usa las etiquetas y se convierte igual.

## Mapeo a las columnas del unificado

| Columna unificada | Scopus CSV | WoS Excel | WoS tabulado |
|---|---|---|---|
| Título | `Title` | `Article Title` | `TI` |
| Autores | `Authors` | `Authors` | `AU` |
| Año | `Year` | `Publication Year` | `PY` |
| Revista | `Source title` | `Source Title` | `SO` |
| DOI | `DOI` | `DOI` | `DI` |
| Id base | `EID` | `UT (Unique WOS ID)` | `UT` |
| Tipo de documento | `Document Type` | `Document Type` | `DT` |
| Idioma | `Language of Original Document` | `Language` | `LA` |
| Acceso abierto | `Open Access` | `Open Access Designations` | `OA` |
| Palabras clave autor | `Author Keywords` | `Author Keywords` | `DE` |
| Palabras clave índice | `Index Keywords` | `Keywords Plus` | `ID` |
| Resumen | `Abstract` | `Abstract` | `AB` |
| Enlace | `Link` | `DOI Link` | `DL` |

En exportaciones WoS (Excel), `DOI Link` a veces sale como `0` aunque `DOI`/`DI` traiga el identificador: `cribado:prepare` ignora ese cero y, si hay DOI, escribe `https://doi.org/<doi>` en la columna unificada `Enlace`.

El unificado `resultados-<MARCO>.csv` tiene, en este orden: `Id`, `Fuente`, las columnas de la tabla y `Fila origen` (fila del archivo de la base, contando la cabecera como 1). `Id` es `R001…` en el orden Scopus y luego WoS. Obligatorias: Título y Resumen (ERROR si una exportación no las trae); las demás pueden faltar (quedan vacías). En WoS el año llega como número (`2024.0`) y se guarda como `2024`.

## Duplicados (antes del análisis)

- Mismo DOI (minúsculas, sin `https://doi.org/` ni `doi:`), mismo título normalizado (sin tildes, minúsculas, solo letras y números) o mismo Id base.
- Se conserva la primera aparición (Scopus va primero); el conservado pasa a `Fuente = Scopus; WoS` y completa con WoS los campos vacíos (p. ej., resumen o palabras clave).
- El duplicado queda en el unificado con NO automático y el criterio de exclusión de duplicados del picoc; no entra en los lotes de los agentes.
