import { auth } from '@/auth'
import { synthesizeEditorial } from '@/lib/synthesize'

export const runtime = 'nodejs'
export const maxDuration = 60

export async function POST() {
  const session = await auth()
  if (!session) return Response.json({ error: 'Unauthorized' }, { status: 401 })

  const draft = await synthesizeEditorial()
  const draftLabel = `AI 초안 (${new Date().toLocaleDateString('ko-KR')})`

  return Response.json({
    draft_label: draftLabel,
    preview: draft.slice(0, 300),
  })
}
