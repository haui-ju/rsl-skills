import type { BoxDefinition, BoxId } from '../types'

export const BOXES: Record<BoxId, BoxDefinition> = {
  identified: {
    label: 'Registros identificados',
    defaultText:
      'Registros identificados desde*:\nBases de Datos (n=2)\nRegistros/Archivos (n=53)',
  },
  removed: {
    label: 'Registros eliminados antes del cribado',
    defaultText: 'Registros eliminados antes del cribado:\nDuplicados (n=2)',
  },
  screened: {
    label: 'Registros cribados',
    defaultText: 'Registros cribados\n(n=51)',
  },
  excluded: {
    label: 'Registros excluidos',
    defaultText: 'Registros excluidos**\n(n=25)',
  },
  retrieved: {
    label: 'Publicaciones recuperadas',
    defaultText: 'Publicaciones recuperadas para evaluación\n(n=26)',
  },
  notRetrieved: {
    label: 'Publicaciones no recuperadas',
    defaultText: 'Publicaciones no recuperadas\n(n=4)',
  },
  assessed: {
    label: 'Publicaciones evaluadas para elegibilidad',
    defaultText: 'Publicaciones evaluadas para elegibilidad\n(n=22)',
  },
  excludedReasons: {
    label: 'Publicaciones excluidas',
    defaultText:
      'Publicaciones excluidas:\nRazón 1 (n=2)\nRazón 2 (n=1)\nRazón 3 (n=1)\netc.',
  },
  included: {
    label: 'Estudios incluidos',
    defaultText: 'Nuevos estudios incluidos en la revisión\n(n=18)',
  },
}

export const DEFAULT_TEXTS = Object.fromEntries(
  Object.entries(BOXES).map(([id, box]) => [id, box.defaultText]),
) as Record<BoxId, string>
