import { useEffect } from 'react'

import { usePrismaStore } from '../store/use-prisma-store'

export function useHydrateStore() {
  useEffect(() => {
    void usePrismaStore.persist.rehydrate()
  }, [])
}
