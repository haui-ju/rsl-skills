import type { ExportQuality } from '../types'

export const QUALITY_OPTIONS: {
  value: ExportQuality
  label: string
  pixelRatio: number
}[] = [
  { value: '1x', label: '1x · Estándar', pixelRatio: 1 },
  { value: '2x', label: '2x · Alta', pixelRatio: 2 },
  { value: '3x', label: '3x · Máxima', pixelRatio: 3 },
]

export const DEFAULT_QUALITY: ExportQuality = '2x'

export const isExportQuality = (value: unknown): value is ExportQuality =>
  QUALITY_OPTIONS.some((option) => option.value === value)

export const pixelRatioOf = (quality: ExportQuality) =>
  QUALITY_OPTIONS.find((option) => option.value === quality)?.pixelRatio ?? 1
