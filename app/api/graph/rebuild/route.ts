import { auth } from '@/auth'
import { rebuildGraph } from '@/lib/graph'

export const runtime = 'nodejs'
export const maxDuration = 60

export async function POST() {
  const session = await auth()
  if (!session) return Response.json({ error: 'Unauthorized' }, { status: 401 })

  const data = await rebuildGraph()
  return Response.json({
    built_at: data.built_at,
    nodes: data.nodes.length,
    links: data.links.length,
  })
}
