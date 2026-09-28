import { cn } from '@/lib/utils'

interface FlowArrowProps {
  direction: 'down' | 'right'
  className?: string
}

export function FlowArrow({ direction, className }: FlowArrowProps) {
  const isDown = direction === 'down'

  return (
    <div
      aria-hidden
      className={cn(
        'flex items-center justify-center',
        isDown ? 'h-12 w-80 flex-col' : 'w-20 self-center px-2.5',
        className,
      )}
    >
      <span
        className={cn('bg-current', isDown ? 'w-0.5 flex-1' : 'h-0.5 flex-1')}
      />
      <svg
        viewBox={isDown ? '0 0 12 10' : '0 0 10 12'}
        className={cn(
          'shrink-0 fill-current',
          isDown ? '-mt-px h-2.5 w-3' : '-ml-px h-3 w-2.5',
        )}
      >
        <path d={isDown ? 'M0 0 H12 L6 10 Z' : 'M0 0 V12 L10 6 Z'} />
      </svg>
    </div>
  )
}
