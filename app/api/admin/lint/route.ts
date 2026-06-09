import { auth } from '@/auth'
import { lintWiki } from '@/lib/synthesize'

export async function POST() {
  const session = await auth()
  if (!session) return Response.json({ error: 'Unauthorized' }, { status: 401 })

  const issues = await lintWiki()
  return Response.json(issues)
}
