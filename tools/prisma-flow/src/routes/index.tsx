import { createFileRoute } from '@tanstack/react-router'
import { useRef } from 'react'

import { ExportToolbar } from '@/features/prisma/components/export-toolbar'
import { PrismaDiagram } from '@/features/prisma/components/prisma-diagram'
import { useHydrateStore } from '@/features/prisma/hooks/use-hydrate-store'

export const Route = createFileRoute('/')({ component: Home })

function Home() {
  const diagramRef = useRef<HTMLDivElement>(null)

  useHydrateStore()

  return (
    <div className="flex h-screen flex-col">
      <header className="flex h-14 shrink-0 items-center justify-between gap-6 border-b border-stone-300/70 bg-white px-5">
        <div className="flex items-baseline gap-3">
          <h1 className="text-sm font-semibold tracking-tight">
            Diagrama PRISMA
          </h1>
          <p className="hidden text-xs text-muted-foreground lg:block">
            Haz clic en cualquier cuadro para editar su texto
          </p>
        </div>
        <ExportToolbar targetRef={diagramRef} />
      </header>

      <main className="flex-1 overflow-auto">
        <div className="flex min-h-full min-w-fit items-center justify-center p-12">
          <div className="overflow-hidden rounded-sm shadow-[0_1px_2px_rgb(0_0_0/0.06),0_12px_32px_-12px_rgb(68_52_20/0.25)] ring-1 ring-stone-300/70">
            <PrismaDiagram ref={diagramRef} />
          </div>
        </div>
      </main>
    </div>
  )
}
