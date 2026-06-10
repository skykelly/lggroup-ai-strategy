import { auth } from '@/auth'
import { db } from '@/lib/db'
import { concepts, pages } from '@/lib/db/schema'
import { chunkText, rebuildEmbeddings } from '@/lib/embed'

export const runtime = 'nodejs'
export const maxDuration = 300

export async function POST() {
  const session = await auth()
  if (!session) return Response.json({ error: 'Unauthorized' }, { status: 401 })

  const allConcepts = await db.select({ id: concepts.id, content: concepts.content }).from(concepts)
  const allPages = await db.select({ id: pages.id, content: pages.content }).from(pages)

  let rebuilt = 0
  for (const c of allConcepts) {
    await rebuildEmbeddings('concept', c.id, chunkText(c.content ?? ''))
    rebuilt++
  }
  for (const p of allPages) {
    await rebuildEmbeddings('page', p.id, chunkText(p.content ?? ''))
    rebuilt++
  }

  return Response.json({ rebuilt })
}
