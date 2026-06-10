import { auth } from '@/auth'
import { upsertSetting } from '@/lib/settings'

export async function PUT(req: Request) {
  const session = await auth()
  if (!session) return Response.json({ error: 'Unauthorized' }, { status: 401 })

  const { metrics } = await req.json()
  if (!Array.isArray(metrics)) {
    return Response.json({ error: 'metrics array required' }, { status: 400 })
  }

  await upsertSetting('metrics_content', JSON.stringify(metrics))

  return Response.json({ ok: true })
}
