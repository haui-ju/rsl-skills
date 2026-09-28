# Estándares RSL — Kitchenham y Charters (2007) y PRISMA 2020

Fuente de verdad de **qué debe reportar** el paper de una RSL y en qué sección. La forma (cómo se escribe) está en `playbooks/redaccion-academica.md`; el marco de búsqueda, en `playbooks/vocabulario-controlado.md`. Las obras están en `global/bibliography/` (catálogo `bibliography.md`); las páginas son las impresas, las que van en la cita.

- Kitchenham, B., & Charters, S. (2007). *Guidelines for performing systematic literature reviews in software engineering* (EBSE-2007-01). Tabla 8, estructura del reporte: pp. 42–43.
- Page, M. J., et al. (2021). The PRISMA 2020 statement. *BMJ, 372*, n71. Lista de 27 ítems: p. 4 (Tabla 1); resumen: p. 5 (Tabla 2); diagrama de flujo: p. 5 (Fig. 1).

Las skills citan este playbook y no repiten su contenido. Una sección en `off` no se genera, pero su ítem sigue aquí: al activarla, se escribe según esta tabla.

## Correspondencia ítem → sección del paper

| Sección del paper (`id`) | PRISMA 2020 (ítem) | Kitchenham y Charters (2007) | Qué debe decir |
|---|---|---|---|
| `encabezado` (título) | 1 | Tabla 8, p. 42 | El título identifica el trabajo como revisión sistemática; breve y basado en la pregunta. |
| `resumen` | 2 (Tabla 2, p. 5) | Tabla 8, p. 42 | Resumen estructurado: objetivo; criterios; fuentes y fecha de búsqueda; evaluación de calidad; síntesis; estudios incluidos; resultados principales; limitaciones de la evidencia; interpretación; financiamiento y registro. |
| `contexto`, `problema`, `justificacion` | 3 | Tabla 8, p. 42 | Por qué hace falta la revisión y qué dicen las revisiones previas. |
| `objetivo-rsl` | 4 | § 5.3, pp. 9–11 | Objetivo explícito y preguntas de investigación (RQ). |
| `marco-pico` | 4 | § 5.3.2, pp. 10–11 | Marco de la pregunta y una RQ por componente. |
| `criterios-seleccion` | 5 | § 6.2.1, p. 18 | Criterios de inclusión y exclusión fijados en el protocolo, incluidos los filtros (años, tipo, idioma, acceso abierto). |
| `ecuacion-busqueda` | 6, 7 | § 6.1.1, p. 14; § 6.1.4, p. 16 | Todas las bases con su **fecha de búsqueda**, años cubiertos y la **ecuación completa con sus filtros y límites**. Tabla por base: base, fecha, años, campos, filtros, registros. |
| `palabras-clave` | 7 | § 6.1.1, p. 14 | Componentes de la pregunta, sinónimos y términos de indexación (tesauro). |
| `seleccion-prisma` | 8, 16a | § 6.2.2–6.2.3, pp. 19–20 | Cuántos revisores cribaron cada registro, si trabajaron de forma independiente, cómo se resolvieron los desacuerdos y qué herramientas se usaron. Con un solo revisor: verificación por un supervisor o test-retest sobre una muestra (p. 20). Diagrama de flujo con n por etapa. |
| `calidad` | 11 | § 6.3, pp. 20–29 | Instrumento de calidad (lista de preguntas), quién lo aplicó y cómo se usa el resultado (no excluir por calidad salvo que el protocolo lo diga). |
| `extraccion-datos` | 9, 10a, 10b | § 6.4, pp. 29–34 | Formulario de extracción definido en el protocolo y probado en una muestra piloto; campos por RQ; quién extrae y quién verifica; qué se hace con datos faltantes o publicaciones duplicadas. |
| `sintesis` | 13a–13d | § 6.5, pp. 34–39 | Método de síntesis (descriptiva o narrativa, tabulación por RQ, síntesis temática) y cómo se presentan los resultados (tablas, gráficos). |
| `distribucion`, `hallazgos-generales` | 16a, 17 | Tabla 8, p. 43 | Resultado de la selección y características de cada estudio incluido, en tabla. |
| `resultados-rq` | 19, 20 | Tabla 8, p. 43 | Resultados por pregunta, con resúmenes en tabla. |
| `resultados-rq` o anexo | 16b | Tabla 8, p. 42 | Estudios que parecían cumplir los criterios pero se excluyeron, con el motivo. |
| `discusion-temas`, `discusion-rq` | 23a, 23d | Tabla 8, p. 43 | Interpretación frente a otras revisiones; implicaciones para la práctica y la investigación. |
| `amenazas` | 23b, 23c, 14 | § 6.1.2, p. 15; Tabla 8, p. 43 | Limitaciones de la **evidencia** (calidad de los estudios, sesgo de publicación) separadas de las del **proceso** de revisión (bases, idioma, acceso abierto, un solo revisor). |
| `conclusion` | 23d | Tabla 8, p. 43 | Implicaciones para la práctica del desarrollo y preguntas abiertas. |
| `declaraciones` | 24a–24c, 25, 26, 27 | Tabla 8, p. 43 | Registro y protocolo (dónde consultarlo o que no se registró) y **cambios al protocolo**; financiamiento; conflicto de intereses; disponibilidad de datos, formularios y materiales. |

## Reglas que siguen de las fuentes

- **Protocolo antes de buscar** (Kitchenham y Charters, 2007, p. 12): pregunta, búsqueda, criterios, calidad y extracción se fijan antes; los cambios se reportan en `declaraciones`.
- **Validar la búsqueda** (p. 14): la ecuación debe recuperar estudios relevantes ya conocidos; el picoc los lista.
- **Documentar la búsqueda** (p. 16): por base, fecha, años cubiertos y ecuación; se guardan los resultados sin filtrar.
- **Selección en varias etapas** (p. 19): título y resumen, luego texto completo; se registra el motivo de cada exclusión (p. 20).
- **Filtros como límites** (PRISMA ítem 7): si la ecuación usa filtros (años, tipo, idioma, acceso abierto), se reportan completos; en el diagrama, los registros que quitan los filtros van en *registros eliminados antes del cribado*.
- **Datos del usuario**: número de revisores, fechas, n por etapa y registro se dejan con marcadores (`X`, `n = X`, `[[ … ]]`); nunca se inventan.
