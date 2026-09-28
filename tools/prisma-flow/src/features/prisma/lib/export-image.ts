import { toBlob } from 'html-to-image'

import { pixelRatioOf } from '../constants/quality'
import type { ExportQuality } from '../types'

const FILE_NAME = 'prisma-flow'

async function renderBlob(node: HTMLElement, quality: ExportQuality) {
  if (document.activeElement instanceof HTMLElement) {
    document.activeElement.blur()
  }
  node.dataset.exporting = 'true'
  try {
    const blob = await toBlob(node, {
      pixelRatio: pixelRatioOf(quality),
      backgroundColor: '#ffffff',
      cacheBust: true,
    })
    if (!blob) throw new Error('No se pudo generar la imagen')
    return blob
  } finally {
    delete node.dataset.exporting
  }
}

export async function downloadImage(node: HTMLElement, quality: ExportQuality) {
  const blob = await renderBlob(node, quality)
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${FILE_NAME}-${quality}.png`
  link.click()
  URL.revokeObjectURL(url)
}

export async function copyImage(node: HTMLElement, quality: ExportQuality) {
  await navigator.clipboard.write([
    new ClipboardItem({ 'image/png': renderBlob(node, quality) }),
  ])
}
