import { getKnowledgeItems } from '@/lib/data'
import SearchResults from './SearchResults'

export default async function SearchPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>
}) {
  const { q } = await searchParams
  const items = await getKnowledgeItems()

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <h1 className="text-lg font-semibold text-white mb-4">검색</h1>
      <SearchResults items={items} initialQuery={q ?? ''} />
    </div>
  )
}
