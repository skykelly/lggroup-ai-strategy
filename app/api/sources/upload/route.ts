import { auth } from '@/auth'
import { runIngest } from '@/lib/ingest'

export const runtime = 'nodejs'
export const maxDuration = 120

export async function POST(req: Request) {
  const session = await auth()
  if (!session) return Response.json({ error: 'Unauthorized' }, { status: 401 })

  const contentType = req.headers.get('content-type') ?? ''

  if (contentType.includes('multipart/form-data')) {
    const fd = await req.formData()
    const file = fd.get('file') as File | null
    const title = (fd.get('title') as string) || ''
    const url = (fd.get('url') as string) || undefined
    if (!file) return Response.json({ error: 'file required' }, { status: 400 })
    const content = await file.text()
    const sourceId = await runIngest({
      title: title || file.name.replace(/\.[^.]+$/, ''),
      raw_content: content,
      url,
      source_type: 'internal',
    })
    return Response.json({ source_id: sourceId })
  }

  const body = await req.json().catch(() => null)
  if (!body?.title || !body?.content) {
    return Response.json({ error: 'title and content required' }, { status: 400 })
  }

  const sourceId = await runIngest({
    title: body.title,
    raw_content: body.content,
    url: body.url,
    source_type: 'internal',
  })
  return Response.json({ source_id: sourceId })
}
