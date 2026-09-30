import { cn } from '@/lib/utils'

import type { PhaseTheme } from '../types'

interface PhaseLabelProps {
  label: string
  theme: PhaseTheme
}

export function PhaseLabel({ label, theme }: PhaseLabelProps) {
  return (
    <div
      className={cn(
        'flex w-10 shrink-0 items-center justify-center rounded-md border-[1.5px]',
        theme.label,
      )}
    >
      <span className="rotate-180 text-[15px] font-semibold tracking-wide [writing-mode:vertical-rl]">
        {label}
      </span>
    </div>
  )
}
