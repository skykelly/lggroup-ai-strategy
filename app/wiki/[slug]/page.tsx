import Link from 'next/link'
import { notFound } from 'next/navigation'
import { getPageBySlug, getWikiPages, getTopicsConfig } from '@/lib/data'
import { renderMarkdown } from '@/lib/markdown'
import MarkdownRenderer from '@/components/MarkdownRenderer'
import WikiChapterDrawer from '../WikiChapterDrawer'

export default async function WikiPageDetail({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  const [page, allPages, topics] = await Promise.all([
    getPageBySlug(slug),
    getWikiPages(),
    getTopicsConfig(),
  ])
  if (!page) notFound()

  const contentHtml = page.content ? await renderMarkdown(page.content) : ''

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <Link href="/wiki" className="text-xs text-neutral-600 hover:text-neutral-400 transition-colors mb-4 inline-block">
        ← Wiki
      </Link>

      <div className="grid lg:grid-cols-[240px_1fr] gap-10 mt-1 items-start">
        <WikiChapterDrawer pages={allPages} topics={topics} currentSlug={slug} />

        <div className="min-w-0">
          <h1 className="text-xl font-semibold text-white mb-2 leading-snug">{page.title}</h1>
          {page.summary && (
            <p className="text-sm text-neutral-400 leading-relaxed mb-6">{page.summary}</p>
          )}

          {contentHtml ? (
            <MarkdownRenderer html={contentHtml} />
          ) : (
            <p className="text-sm text-neutral-600">아직 작성된 내용이 없습니다.</p>
          )}
        </div>
      </div>
    </div>
  )
}
