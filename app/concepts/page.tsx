import { getConceptItems, getTopicsConfig } from '@/lib/data'
import ConceptGrid from './ConceptGrid'

export default async function ConceptsPage() {
  const [concepts, topics] = await Promise.all([
    getConceptItems(),
    getTopicsConfig(),
  ])

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <div className="mb-6">
        <h1 className="text-lg font-semibold text-white">Concepts</h1>
        <p className="text-xs text-neutral-500 mt-0.5">{concepts.length}개 개념</p>
      </div>

      <ConceptGrid concepts={concepts} topics={topics} />
    </div>
  )
}
