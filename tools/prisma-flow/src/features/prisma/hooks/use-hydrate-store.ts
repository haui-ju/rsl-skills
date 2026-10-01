import { useEffect } from 'react'
import { toast } from 'sonner'

import { getLatestPrismaData } from '../server/get-latest-prisma'
import { usePrismaStore } from '../store/use-prisma-store'

export function useHydrateStore() {
  const loadFromJson = usePrismaStore((state) => state.loadFromJson)

  useEffect(() => {
    void usePrismaStore.persist.rehydrate()

    // Intentar cargar los datos más recientes automáticamente
    getLatestPrismaData().then((data) => {
      if (data) {
        loadFromJson(data)
        toast.success('Datos cargados automáticamente desde el último prisma.json')
      }
    }).catch(console.error)
  }, [loadFromJson])
}
