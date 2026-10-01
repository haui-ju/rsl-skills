import { createServerFn } from '@tanstack/react-start'
import fs from 'node:fs'
import path from 'node:path'

function findLatestPrismaJson(dir: string): { path: string; mtime: number } | null {
  let latest: { path: string; mtime: number } | null = null

  function search(currentPath: string, depth: number) {
    if (depth > 5) return // Limit depth to avoid searching too much
    
    let entries;
    try {
      entries = fs.readdirSync(currentPath, { withFileTypes: true })
    } catch {
      return
    }

    for (const entry of entries) {
      const fullPath = path.join(currentPath, entry.name)
      
      if (entry.isDirectory()) {
        // Skip node_modules and other hidden folders to be fast
        if (!entry.name.startsWith('.') && entry.name !== 'node_modules') {
          search(fullPath, depth + 1)
        }
      } else if (entry.isFile() && entry.name === 'prisma.json') {
        // Check if it's inside a picoc folder
        if (fullPath.includes('/picoc/')) {
          const stats = fs.statSync(fullPath)
          if (!latest || stats.mtimeMs > latest.mtime) {
            latest = { path: fullPath, mtime: stats.mtimeMs }
          }
        }
      }
    }
  }

  search(dir, 0)
  return latest
}

export const getLatestPrismaData = createServerFn({ method: 'GET' }).handler(
  async () => {
    try {
      // Root of the workspace (assuming tools/prisma-flow is the cwd or we can go up)
      const workspaceRoot = path.resolve(process.cwd(), '../../docs')
      
      const latest = findLatestPrismaJson(workspaceRoot)
      
      if (latest) {
        const content = fs.readFileSync(latest.path, 'utf-8')
        return JSON.parse(content)
      }
      
      return null
    } catch (e) {
      console.error('Error finding latest prisma.json:', e)
      return null
    }
  }
)
