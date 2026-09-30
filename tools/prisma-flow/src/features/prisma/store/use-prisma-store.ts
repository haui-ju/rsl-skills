import { create } from 'zustand'
import { createJSONStorage, persist } from 'zustand/middleware'

import { DEFAULT_TEXTS } from '../constants/boxes'
import { DEFAULT_QUALITY, isExportQuality } from '../constants/quality'
import type { BoxId, ExportQuality } from '../types'

interface PrismaState {
  texts: Record<BoxId, string>
  quality: ExportQuality
  setText: (id: BoxId, value: string) => void
  setQuality: (quality: ExportQuality) => void
  reset: () => void
}

type PersistedPrismaState = Pick<PrismaState, 'texts' | 'quality'>

export const usePrismaStore = create<PrismaState>()(
  persist(
    (set) => ({
      texts: DEFAULT_TEXTS,
      quality: DEFAULT_QUALITY,
      setText: (id, value) =>
        set((state) => ({ texts: { ...state.texts, [id]: value } })),
      setQuality: (quality) => set({ quality }),
      reset: () => set({ texts: DEFAULT_TEXTS }),
    }),
    {
      name: 'prisma-flow',
      version: 2,
      storage: createJSONStorage(() => localStorage),
      skipHydration: true,
      partialize: ({ texts, quality }): PersistedPrismaState => ({
        texts,
        quality,
      }),
      merge: (persisted, current) => {
        const saved = persisted as Partial<PersistedPrismaState> | undefined
        return {
          ...current,
          quality: isExportQuality(saved?.quality)
            ? saved.quality
            : current.quality,
          texts: { ...current.texts, ...saved?.texts },
        }
      },
    },
  ),
)
