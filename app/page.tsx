import Link from 'next/link'
import { getEditorialContent, getConceptItems, getSources } from '@/lib/data'
import { renderMarkdown } from '@/lib/markdown'

export default async function HomePage() {
  const [editorialContent, allConcepts, allSources] = await Promise.all([
    getEditorialContent(),
    getConceptItems(),
    getSources(),
  ])

  const editorialHtml = editorialContent ? await renderMarkdown(editorialContent) : ''

  // source_count 높은 순, 동점이면 confidence 높은 순
  const topConcepts = [...allConcepts]
    .sort((a, b) => b.source_count - a.source_count || b.confidence - a.confidence)
    .slice(0, 6)

  const latestSources = allSources.slice(0, 4)

  // 마지막 업데이트: concepts 중 가장 최근 updated_at
  const lastUpdated = allConcepts.length > 0
    ? new Date(
        allConcepts.reduce((max, c) =>
          new Date(c.updated_at) > new Date(max) ? c.updated_at : max,
          allConcepts[0].updated_at
        )
      ).toLocaleDateString('ko-KR', { year: 'numeric', month: 'long', day: 'numeric' })
    : null

  return (
    <>
      {/* 통계 배너 */}
      <div className="border-b border-neutral-800 bg-neutral-900/40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-10 flex items-center gap-4 text-xs text-neutral-500">
          <span>Sources <strong className="text-neutral-300">{allSources.length}</strong>개</span>
          <span className="text-neutral-700">·</span>
          <span>Concepts <strong className="text-neutral-300">{allConcepts.length}</strong>개</span>
          {lastUpdated && (
            <>
              <span className="text-neutral-700">·</span>
              <span>업데이트 <strong className="text-neutral-300">{lastUpdated}</strong></span>
            </>
          )}
        </div>
      </div>

      {/* 메인 콘텐츠 */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-10">
        <div className="grid lg:grid-cols-[1fr_300px] gap-10">

          {/* 좌: 에디토리얼 */}
          <section>
            {editorialHtml ? (
              <div
                className="prose prose-invert prose-sm max-w-none
                  prose-headings:text-white prose-headings:font-semibold
                  prose-p:text-neutral-300 prose-p:leading-relaxed
                  prose-a:text-accent-400 prose-a:no-underline hover:prose-a:underline
                  prose-strong:text-white prose-code:text-accent-300
                  prose-hr:border-neutral-800"
                dangerouslySetInnerHTML={{ __html: editorialHtml }}
              />
            ) : (
              <div className="space-y-4">
                <h1 className="text-xl font-semibold text-white">Homestyle Wiki</h1>
                <p className="text-neutral-400 text-sm leading-relaxed">
                  브랜드·MD·마케터가 한국 리빙 시장의 스타일, 공간 트렌드, 카테고리 언어,
                  콘텐츠 키워드를 이해하고 활용하기 위한 지식체계입니다.
                </p>
                <p className="text-neutral-600 text-xs">
                  Admin → Editorial 탭에서 에디토리얼 콘텐츠를 작성하세요.
                </p>
              </div>
            )}
          </section>

          {/* 우: 사이드바 */}
          <aside className="space-y-8">

            {/* 핵심 개념 */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-xs font-semibold text-neutral-500 uppercase tracking-widest">핵심 개념</h2>
                <Link href="/concepts" className="text-xs text-neutral-600 hover:text-neutral-400 transition-colors">
                  전체 보기 →
                </Link>
              </div>
              <div className="flex flex-col gap-2">
                {topConcepts.map((concept) => (
                  <Link
                    key={concept.id}
                    href={`/concepts/${concept.slug}`}
                    className="group block bg-neutral-900 hover:bg-neutral-800/80 border border-neutral-800 hover:border-neutral-700 rounded-xl p-3 transition-all"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <span className="text-sm font-medium text-neutral-200 group-hover:text-white transition-colors leading-snug">
                        {concept.title}
                      </span>
                      {concept.source_count > 0 && (
                        <span className="text-xs text-neutral-600 shrink-0 mt-0.5">
                          {concept.source_count}
                        </span>
                      )}
                    </div>
                    {concept.brief && (
                      <p className="text-xs text-neutral-500 mt-1 line-clamp-2 leading-relaxed">
                        {concept.brief}
                      </p>
                    )}
                    <div className="flex items-center gap-1.5 mt-2">
                      {concept.concept_status === 'canonical' && (
                        <span className="text-xs bg-emerald-950/60 text-emerald-600 border border-emerald-900/50 px-1.5 py-0.5 rounded-md">
                          canonical
                        </span>
                      )}
                      {concept.concept_type && (
                        <span className="text-xs bg-neutral-800 text-neutral-500 px-1.5 py-0.5 rounded-md">
                          {concept.concept_type}
                        </span>
                      )}
                    </div>
                  </Link>
                ))}
              </div>
            </div>

            {/* 최신 소스 */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-xs font-semibold text-neutral-500 uppercase tracking-widest">최신 소스</h2>
                <Link href="/sources" className="text-xs text-neutral-600 hover:text-neutral-400 transition-colors">
                  전체 보기 →
                </Link>
              </div>
              {latestSources.length > 0 ? (
                <div className="flex flex-col gap-2">
                  {latestSources.map((source) => (
                    <Link
                      key={source.id}
                      href={`/sources/${source.id}`}
                      className="group block bg-neutral-900 hover:bg-neutral-800/80 border border-neutral-800 hover:border-neutral-700 rounded-xl p-3 transition-all"
                    >
                      <p className="text-sm font-medium text-neutral-200 group-hover:text-white transition-colors leading-snug line-clamp-2">
                        {source.title}
                      </p>
                      {source.one_line_summary && (
                        <p className="text-xs text-neutral-500 mt-1 line-clamp-2 leading-relaxed">
                          {source.one_line_summary}
                        </p>
                      )}
                      <div className="flex items-center gap-2 mt-2 text-xs text-neutral-600">
                        {source.publisher && <span>{source.publisher}</span>}
                        {source.published_at && (
                          <>
                            {source.publisher && <span>·</span>}
                            <span>{source.published_at}</span>
                          </>
                        )}
                      </div>
                    </Link>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-neutral-600 py-2">
                  Sources 탭에서 새 소스를 추가하세요.
                </p>
              )}
            </div>

          </aside>
        </div>
      </div>
    </>
  )
}
