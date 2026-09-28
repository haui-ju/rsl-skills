import { useRef } from 'react'

import { Textarea } from '@/components/ui/textarea'
import { cn } from '@/lib/utils'

import { BOXES } from '../constants/boxes'
import { useAutoResize } from '../hooks/use-auto-resize'
import { usePrismaStore } from '../store/use-prisma-store'
import type { BoxId, BoxVariant, PhaseTheme } from '../types'

interface PrismaBoxProps {
  id: BoxId
  variant: BoxVariant
  theme: PhaseTheme
}

export function PrismaBox({ id, variant, theme }: PrismaBoxProps) {
  const ref = useRef<HTMLTextAreaElement>(null)
  const value = usePrismaStore((state) => state.texts[id])
  const setText = usePrismaStore((state) => state.setText)

  useAutoResize(ref, value)

  return (
    <div
      className={cn(
        'flex h-full shrink-0 rounded-[3px] border-[1.5px] p-1 transition-[border-color,box-shadow] focus-within:ring-3',
        variant === 'main' ? 'w-80' : 'w-72',
        variant === 'main' ? theme.main : theme.side,
        theme.focus,
      )}
    >
      <Textarea
        ref={ref}
        value={value}
        onChange={(event) => setText(id, event.target.value)}
        aria-label={BOXES[id].label}
        spellCheck={false}
        rows={2}
        className={cn(
          'max-h-72 min-h-24 resize-none overflow-y-auto rounded-none border-0 bg-transparent px-4 py-3 text-base leading-relaxed text-slate-800 shadow-none focus-visible:ring-0 md:text-base dark:bg-transparent',
          'group-data-[exporting=true]/diagram:max-h-none group-data-[exporting=true]/diagram:overflow-hidden',
          variant === 'main' ? 'font-medium' : 'text-slate-700',
        )}
      />
    </div>
  )
}
