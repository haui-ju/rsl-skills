import type { BoxDefinition, BoxId } from '../types'

export const BOXES: Record<BoxId, BoxDefinition> = {
  identified: {
    label: 'Registros identificados',
    defaultText:
      'Registros identificados de*:\nBases de datos (n = )\nRegistros (n = )',
  },
  removed: {
    label: 'Registros eliminados antes del cribado',
    defaultText: 'Registros eliminados antes del\ncribado:\nRegistros duplicados eliminados (n = )\nRegistros marcados como inelegibles por herramientas automatizadas (n = )\nRegistros eliminados por otras razones (n = )',
  },
  screened: {
    label: 'Registros cribados',
    defaultText: 'Registros cribados\n(n = )',
  },
  excluded: {
    label: 'Registros excluidos',
    defaultText: 'Registros excluidos**\n(n = )',
  },
  retrieved: {
    label: 'Informes solicitados para recuperación',
    defaultText: 'Informes solicitados para recuperación\n(n = )',
  },
  notRetrieved: {
    label: 'Informes no recuperados',
    defaultText: 'Informes no recuperados\n(n = )',
  },
  assessed: {
    label: 'Informes evaluados para elegibilidad',
    defaultText: 'Informes evaluados para elegibilidad\n(n = )',
  },
  excludedReasons: {
    label: 'Informes excluidos',
    defaultText:
      'Informes excluidos:\nRazón 1 (n = )\nRazón 2 (n = )\nRazón 3 (n = )\netc.',
  },
  included: {
    label: 'Estudios incluidos',
    defaultText: 'Estudios incluidos en la revisión\n(n = )\nInformes de estudios incluidos\n(n = )',
  },
}

export const DEFAULT_TEXTS = Object.fromEntries(
  Object.entries(BOXES).map(([id, box]) => [id, box.defaultText]),
) as Record<BoxId, string>
