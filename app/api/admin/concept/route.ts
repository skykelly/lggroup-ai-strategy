import { eq, sql } from 'drizzle-orm'
import { auth } from '@/auth'
import { db } from '@/lib/db'
import { concepts } from '@/lib/db/schema'
import { chunkText, rebuildEmbeddings } from '@/lib/embed'

export async function PUT(req: Request) {
  const session = await auth()
  if (!session) return Response.json({ error: 'Unauthorized' }, { status: 401 })

  const body = await req.json()
  const {
    id, title, slug, brief, concept_type, concept_status, confidence,
    aliases, topics, related_concepts, content,
  } = body

  if (!id || !title || !slug) {
    return Response.json({ error: 'id, title, slug required' }, { status: 400 })
  }

  await db.update(concepts).set({
    title,
    slug,
    brief: brief ?? null,
    concept_type: concept_type ?? null,
    concept_status: concept_status ?? 'candidate',
    confidence: Number(confidence) || 0,
    aliases: Array.isArray(aliases) ? aliases : [],
    topics: Array.isArray(topics) ? topics : [],
    related_concepts: Array.isArray(related_concepts) ? related_concepts : [],
    content: content ?? null,
    updated_at: sql`now()`,
  }).where(eq(concepts.id, id))

  await rebuildEmbeddings('concept', id, chunkText(content ?? ''))

  return Response.json({ ok: true })
}
