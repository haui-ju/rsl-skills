import { createServerFn } from '@tanstack/react-start'
import fs from 'node:fs'
import path from 'node:path'

/** Ruta relativa al root del repo (rsl-skills), p. ej. docs/.../picoc/.../prisma.json */
export const getPrismaFromPath = createServerFn({ method: 'GET' })
  .inputValidator((rel: string) => rel)
  .handler(async ({ data: relPath }) => {
    const repoRoot = path.resolve(process.cwd(), '../..')
    const full = path.join(repoRoot, relPath)
    if (!fs.existsSync(full)) {
      throw new Error(`No existe ${full}`)
    }
    return JSON.parse(fs.readFileSync(full, 'utf-8'))
  })
