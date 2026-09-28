import { useState } from 'react'
import type { ReactNode, RefObject } from 'react'
import { Copy, Download, Loader2, RotateCcw } from 'lucide-react'
import { toast } from 'sonner'

import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from '@/components/ui/tooltip'

import { copyImage, downloadImage } from '../lib/export-image'
import { usePrismaStore } from '../store/use-prisma-store'
import { QualitySelect } from './quality-select'

type Action = 'download' | 'copy'

interface ExportToolbarProps {
  targetRef: RefObject<HTMLDivElement | null>
}

export function ExportToolbar({ targetRef }: ExportToolbarProps) {
  const [pending, setPending] = useState<Action | null>(null)
  const quality = usePrismaStore((state) => state.quality)
  const reset = usePrismaStore((state) => state.reset)

  const run = async (action: Action) => {
    const node = targetRef.current
    if (!node || pending) return
    setPending(action)
    try {
      if (action === 'download') {
        await downloadImage(node, quality)
        toast.success('Imagen descargada')
      } else {
        await copyImage(node, quality)
        toast.success('Imagen copiada al portapapeles')
      }
    } catch {
      toast.error('No se pudo exportar la imagen')
    } finally {
      setPending(null)
    }
  }

  const handleReset = () => {
    reset()
    toast.success('Textos restablecidos')
  }

  return (
    <div className="flex items-center gap-3">
      <ToolbarButton tooltip="Restablecer textos originales">
        <Button size="sm" variant="ghost" onClick={handleReset}>
          <RotateCcw />
          Restablecer
        </Button>
      </ToolbarButton>

      <Separator orientation="vertical" className="h-6" />

      <div className="flex items-center gap-2">
        <span className="text-xs font-medium text-muted-foreground">
          Calidad
        </span>
        <QualitySelect />
      </div>

      <div className="flex items-center gap-2">
        <ToolbarButton tooltip="Copiar imagen al portapapeles">
          <Button
            size="sm"
            variant="outline"
            onClick={() => run('copy')}
            disabled={!!pending}
          >
            {pending === 'copy' ? (
              <Loader2 className="animate-spin" />
            ) : (
              <Copy />
            )}
            Copiar
          </Button>
        </ToolbarButton>

        <ToolbarButton tooltip="Descargar como PNG">
          <Button
            size="sm"
            onClick={() => run('download')}
            disabled={!!pending}
          >
            {pending === 'download' ? (
              <Loader2 className="animate-spin" />
            ) : (
              <Download />
            )}
            Descargar PNG
          </Button>
        </ToolbarButton>
      </div>
    </div>
  )
}

function ToolbarButton({
  tooltip,
  children,
}: {
  tooltip: string
  children: ReactNode
}) {
  return (
    <Tooltip>
      <TooltipTrigger asChild>{children}</TooltipTrigger>
      <TooltipContent>{tooltip}</TooltipContent>
    </Tooltip>
  )
}
