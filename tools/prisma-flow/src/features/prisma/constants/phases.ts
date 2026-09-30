import type { PhaseDefinition } from '../types'

export const PHASES: PhaseDefinition[] = [
  {
    id: 'identification',
    label: 'Identification',
    theme: {
      label: 'bg-[#9cc2e5] text-black border-black',
      main: 'border-black bg-white',
      side: 'border-black bg-white',
      focus: 'focus-within:border-black focus-within:ring-2 focus-within:ring-black/20',
      arrow: 'text-black',
    },
    rows: [{ main: 'identified', side: 'removed' }],
  },
  {
    id: 'screening',
    label: 'Screening',
    theme: {
      label: 'bg-[#9cc2e5] text-black border-black',
      main: 'border-black bg-white',
      side: 'border-black bg-white',
      focus: 'focus-within:border-black focus-within:ring-2 focus-within:ring-black/20',
      arrow: 'text-black',
    },
    rows: [
      { main: 'screened', side: 'excluded' },
      { main: 'retrieved', side: 'notRetrieved' },
      { main: 'assessed', side: 'excludedReasons' },
    ],
  },
  {
    id: 'included',
    label: 'Included',
    theme: {
      label: 'bg-[#9cc2e5] text-black border-black',
      main: 'border-black bg-white',
      side: 'border-black bg-white',
      focus: 'focus-within:border-black focus-within:ring-2 focus-within:ring-black/20',
      arrow: 'text-black',
    },
    rows: [{ main: 'included' }],
  },
]
