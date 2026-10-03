import { useEffect } from 'react'
import { toast } from 'sonner'

import { getLatestPrismaData } from '../server/get-latest-prisma'
import { getPrismaFromPath } from '../server/get-prisma-from-path'
import { usePrismaStore } from '../store/use-prisma-store'

/** Ruta relativa al root del repo; si se indica, tiene prioridad sobre «último prisma.json». */
export function useHydrateStore(prismaRelPath?: string) {
  const loadFromJson = usePrismaStore((state) => state.loadFromJson)

  useEffect(() => {
    void usePrismaStore.persist.rehydrate()

    const load = prismaRelPath
      ? getPrismaFromPath({ data: prismaRelPath })
      : getLatestPrismaData()

    void load
      .then((data) => {
        if (data) {
          loadFromJson(data)
          toast.success(
            prismaRelPath
              ? `PRISMA cargado desde ${prismaRelPath}`
              : 'Datos cargados desde el último prisma.json',
          )
        }
      })
      .catch(console.error)
  }, [loadFromJson, prismaRelPath])
}
