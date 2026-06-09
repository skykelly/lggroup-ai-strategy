import { and, eq } from 'drizzle-orm'
import { auth } from '@/auth'
import { db } from '@/lib/db'
import { sources, knowledge_embeddings } from '@/lib/db/schema'

export async function DELETE(req: Request) {
  const session = await auth()
  if (!session) return Response.json({ error: 'Unauthorized' }, { status: 401 })

  const id = new URL(req.url).searchParams.get('id')
  if (!id) return Response.json({ error: 'id required' }, { status: 400 })

  await db.delete(knowledge_embeddings).where(
    and(eq(knowledge_embeddings.ref_type, 'source'), eq(knowledge_embeddings.ref_id, id))
  )
  await db.delete(sources).where(eq(sources.id, id))

  return Response.json({ deleted: id })
}
