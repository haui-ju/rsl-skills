import type { PhaseDefinition } from '../types'

export const PHASES: PhaseDefinition[] = [
  {
    id: 'identification',
    label: 'Identificación',
    theme: {
      label: 'bg-sky-100 text-sky-800 ring-sky-200',
      main: 'border-sky-300 bg-sky-50',
      side: 'border-sky-200 bg-white',
      focus: 'focus-within:border-sky-400 focus-within:ring-sky-200/70',
      arrow: 'text-sky-400',
    },
    rows: [{ main: 'identified', side: 'removed' }],
  },
  {
    id: 'screening',
    label: 'Cribado',
    theme: {
      label: 'bg-violet-100 text-violet-800 ring-violet-200',
      main: 'border-violet-300 bg-violet-50',
      side: 'border-violet-200 bg-white',
      focus: 'focus-within:border-violet-400 focus-within:ring-violet-200/70',
      arrow: 'text-violet-400',
    },
    rows: [
      { main: 'screened', side: 'excluded' },
      { main: 'retrieved', side: 'notRetrieved' },
      { main: 'assessed', side: 'excludedReasons' },
    ],
  },
  {
    id: 'included',
    label: 'Incluidos',
    theme: {
      label: 'bg-emerald-100 text-emerald-800 ring-emerald-200',
      main: 'border-emerald-300 bg-emerald-50',
      side: 'border-emerald-200 bg-white',
      focus: 'focus-within:border-emerald-400 focus-within:ring-emerald-200/70',
      arrow: 'text-emerald-400',
    },
    rows: [{ main: 'included' }],
  },
]
