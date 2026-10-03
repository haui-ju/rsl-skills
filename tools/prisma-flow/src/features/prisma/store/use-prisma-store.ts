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
  loadFromJson: (data: any) => void
}

type PersistedPrismaState = Pick<PrismaState, 'texts' | 'quality'>

type IdentificationJson = {
  databases?: number | null
  registers?: number | null
  sources?: { name: string; n: number }[]
  scopus?: number | null
  wos?: number | null
}

function formatIdentificationText(
  id: IdentificationJson,
  formatN: (val: number | null | undefined) => string | number,
): string {
  const lines = [
    'Registros identificados de*:',
    `Bases de datos (n = ${formatN(id.databases)})`,
  ]

  const sources: { name: string; n: number }[] = [...(id.sources ?? [])]
  if (sources.length === 0) {
    if (id.scopus != null && id.scopus !== undefined) {
      sources.push({ name: 'Scopus', n: id.scopus })
    }
    if (id.wos != null && id.wos !== undefined) {
      sources.push({ name: 'Web of Science', n: id.wos })
    }
  }
  for (const s of sources) {
    lines.push(`${s.name} (n = ${formatN(s.n)})`)
  }

  const reg = id.registers
  if (reg != null && reg !== undefined && reg !== 0) {
    lines.push(`Registros (n = ${formatN(reg)})`)
  }

  return lines.join('\n')
}

export const usePrismaStore = create<PrismaState>()(
  persist(
    (set) => ({
      texts: DEFAULT_TEXTS,
      quality: DEFAULT_QUALITY,
      setText: (id, value) =>
        set((state) => ({ texts: { ...state.texts, [id]: value } })),
      setQuality: (quality) => set({ quality }),
      reset: () => set({ texts: DEFAULT_TEXTS }),
      loadFromJson: (data: any) => {
        set((state) => {
          const newTexts = { ...state.texts }

          const formatN = (val: number | null | undefined) =>
            val !== null && val !== undefined ? val : 'X'

          if (data.identification) {
            newTexts.identified = formatIdentificationText(
              data.identification,
              formatN,
            )
          }
          if (data.removed_before_screening) {
            newTexts.removed = `Registros eliminados antes del\ncribado:\nRegistros duplicados eliminados (n = ${formatN(data.removed_before_screening.duplicates)})\nRegistros marcados como inelegibles por herramientas automatizadas (n = ${formatN(data.removed_before_screening.ineligible_automation)})\nRegistros eliminados por otras razones (n = ${formatN(data.removed_before_screening.other_reasons)})`
          }
          if (data.screening) {
            newTexts.screened = `Registros cribados\n(n = ${formatN(data.screening.screened)})`
            newTexts.excluded = `Registros excluidos**\n(n = ${formatN(data.screening.excluded)})`
          }
          if (data.retrieval) {
            newTexts.retrieved = `Informes solicitados para recuperación\n(n = ${formatN(data.retrieval.sought)})`
            newTexts.notRetrieved = `Informes no recuperados\n(n = ${formatN(data.retrieval.not_retrieved)})`
          }
          if (data.eligibility) {
            newTexts.assessed = `Informes evaluados para elegibilidad\n(n = ${formatN(data.eligibility.assessed)})`
            if (data.eligibility.excluded_reasons && Object.keys(data.eligibility.excluded_reasons).length > 0) {
              const reasons = Object.entries(data.eligibility.excluded_reasons)
                .map(([reason, count]) => `${reason} (n = ${count})`)
                .join('\n')
              newTexts.excludedReasons = `Informes excluidos:\n${reasons}`
            } else {
              newTexts.excludedReasons = DEFAULT_TEXTS.excludedReasons
            }
          }
          if (data.included) {
            const ns = formatN(data.included.studies)
            const nr = formatN(data.included.reports)
            newTexts.included =
              ns === nr
                ? `Estudios incluidos en la revisión\n(n = ${ns})`
                : `Estudios incluidos en la revisión\n(n = ${ns})\nInformes de estudios incluidos\n(n = ${nr})`
          }

          return { texts: newTexts }
        })
      },
    }),
    {
      name: 'prisma-flow',
      version: 7,
      storage: createJSONStorage(() => localStorage),
      skipHydration: true,
      partialize: ({ texts, quality }): PersistedPrismaState => ({
        texts,
        quality,
      }),
      migrate: (persistedState: any, version: number) => {
        if (version < 7) {
          return {
            ...persistedState,
            texts: DEFAULT_TEXTS,
          }
        }
        return persistedState
      },
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
