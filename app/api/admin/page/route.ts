import { eq, sql } from 'drizzle-orm'
import { auth } from '@/auth'
import { db } from '@/lib/db'
import { pages } from '@/lib/db/schema'
import { chunkText, rebuildEmbeddings } from '@/lib/embed'

export async function PUT(req: Request) {
  const session = await auth()
  if (!session) return Response.json({ error: 'Unauthorized' }, { status: 401 })

  const body = await req.json()
  const { id, title, slug, chapter_number, subsections, summary, topics, content } = body

  if (!id || !title || !slug) {
    return Response.json({ error: 'id, title, slug required' }, { status: 400 })
  }

  await db.update(pages).set({
    title,
    slug,
    chapter_number: chapter_number ?? null,
    subsections: Array.isArray(subsections) ? subsections : [],
    summary: summary ?? null,
    topics: Array.isArray(topics) ? topics : [],
    content: content ?? null,
    updated_at: sql`now()`,
  }).where(eq(pages.id, id))

  await rebuildEmbeddings('page', id, chunkText(content ?? ''))

  return Response.json({ ok: true })
}
