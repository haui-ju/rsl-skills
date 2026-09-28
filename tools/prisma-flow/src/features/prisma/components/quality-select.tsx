import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

import { QUALITY_OPTIONS, isExportQuality } from '../constants/quality'
import { usePrismaStore } from '../store/use-prisma-store'

export function QualitySelect() {
  const quality = usePrismaStore((state) => state.quality)
  const setQuality = usePrismaStore((state) => state.setQuality)

  return (
    <Select
      value={quality}
      onValueChange={(value) => isExportQuality(value) && setQuality(value)}
    >
      <SelectTrigger
        size="sm"
        className="w-36"
        aria-label="Calidad de exportación"
      >
        <SelectValue />
      </SelectTrigger>
      <SelectContent position="popper" align="end">
        {QUALITY_OPTIONS.map((option) => (
          <SelectItem key={option.value} value={option.value}>
            {option.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  )
}
