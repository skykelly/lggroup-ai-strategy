import { eq } from 'drizzle-orm'
import { db } from '@/lib/db'
import { sources } from '@/lib/db/schema'

export async function GET(req: Request) {
  const url = new URL(req.url).searchParams.get('url')
  if (!url) return Response.json({ exists: false })
  const [row] = await db.select({ id: sources.id }).from(sources).where(eq(sources.url, url)).limit(1)
  return Response.json({ exists: !!row })
}
