'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { signOut } from 'next-auth/react'
import type { Session } from 'next-auth'
import { useState } from 'react'
import SearchBox from './SearchBox'
import WikiIndexDrawer from './WikiIndexDrawer'
import type { WikiPageItem, TopicNode, ConceptItem } from '@/lib/types'

interface Props {
  session: Session | null
  wikiPages: WikiPageItem[]
  wikiTopics: TopicNode[]
  concepts: ConceptItem[]
}

const KNOWLEDGE_ITEMS = [
  { href: '/knowledge', label: '그래프' },
  { href: '/concepts',  label: '개념'   },
  { href: '/wiki',      label: '위키'   },
]

export default function Header({ session, wikiPages, wikiTopics, concepts }: Props) {
  const [mobileOpen, setMobileOpen] = useState(false)
  const [indexOpen, setIndexOpen] = useState(false)
  const pathname = usePathname()
  const currentSlug = pathname.startsWith('/wiki/') ? pathname.slice('/wiki/'.length) : undefined

  const linkClass = (href: string) =>
    `text-sm transition-colors ${
      pathname === href || pathname.startsWith(href + '/')
        ? 'text-white'
        : 'text-neutral-400 hover:text-white'
    }`

  const closeMobile = () => setMobileOpen(false)

  return (
    <header className="bg-neutral-950 border-b border-neutral-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 flex items-center justify-between h-14">

        {/* 좌측: 전체 위키 목록 + 로고 */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setIndexOpen(true)}
            aria-label="전체 위키 목록 열기"
            className="text-neutral-400 hover:text-white text-lg w-8 text-center"
          >
            ☰
          </button>
          <Link href="/" className="text-white font-semibold tracking-tight">
            Homestyle Wiki
          </Link>
        </div>

        {/* 데스크탑 nav */}
        <nav className="hidden md:flex items-center gap-6">
          <Link href="/"        className={linkClass('/')}>Home</Link>
          <Link href="/sources" className={linkClass('/sources')}>Sources</Link>

          {/* Knowledge 드롭다운 */}
          <div className="group relative">
            <button className="flex items-center gap-1 text-sm text-neutral-400 hover:text-white transition-colors">
              Knowledge <span className="text-xs opacity-70">▾</span>
            </button>
            <div className="hidden group-hover:block absolute top-full left-0 pt-2 min-w-[9rem]">
              <div className="bg-neutral-900 border border-neutral-700 rounded-lg py-1 shadow-xl">
                {KNOWLEDGE_ITEMS.map(({ href, label }) => (
                  <Link
                    key={href}
                    href={href}
                    className="block px-4 py-2 text-sm text-neutral-300 hover:text-white hover:bg-neutral-800 transition-colors"
                  >
                    {label}
                  </Link>
                ))}
              </div>
            </div>
          </div>

          <Link href="/metrics" className={linkClass('/metrics')}>Metrics</Link>
          <Link href="/chat"    className={linkClass('/chat')}>Chat</Link>
          {session && (
            <Link href="/admin" className={linkClass('/admin')}>Admin</Link>
          )}
        </nav>

        {/* 데스크탑 검색 + 로그인/로그아웃 */}
        <div className="hidden md:flex items-center gap-4">
          <SearchBox className="w-40" />
          {session ? (
            <button
              onClick={() => signOut({ callbackUrl: '/' })}
              className="text-sm text-neutral-400 hover:text-white transition-colors"
            >
              로그아웃
            </button>
          ) : (
            <Link href="/auth/signin" className="text-sm text-neutral-400 hover:text-white transition-colors">
              로그인
            </Link>
          )}
        </div>

        {/* 모바일 햄버거 */}
        <button
          className="md:hidden text-neutral-400 hover:text-white text-lg w-8 text-center"
          onClick={() => setMobileOpen((v) => !v)}
          aria-label="메뉴 열기"
        >
          {mobileOpen ? '✕' : '☰'}
        </button>
      </div>

      {/* 모바일 메뉴 */}
      {mobileOpen && (
        <nav className="md:hidden border-t border-neutral-800 px-4 py-4 flex flex-col gap-4">
          <SearchBox />
          <Link href="/"          className="text-sm text-neutral-300 hover:text-white" onClick={closeMobile}>Home</Link>
          <Link href="/sources"   className="text-sm text-neutral-300 hover:text-white" onClick={closeMobile}>Sources</Link>
          <div className="border-t border-neutral-800 pt-3 flex flex-col gap-3">
            <span className="text-xs text-neutral-600 uppercase tracking-widest">Knowledge</span>
            {KNOWLEDGE_ITEMS.map(({ href, label }) => (
              <Link key={href} href={href} className="text-sm text-neutral-300 hover:text-white pl-2" onClick={closeMobile}>
                {label}
              </Link>
            ))}
          </div>
          <Link href="/metrics"   className="text-sm text-neutral-300 hover:text-white" onClick={closeMobile}>Metrics</Link>
          <Link href="/chat"      className="text-sm text-neutral-300 hover:text-white" onClick={closeMobile}>Chat</Link>
          {session && (
            <Link href="/admin"   className="text-sm text-neutral-300 hover:text-white" onClick={closeMobile}>Admin</Link>
          )}
          <div className="border-t border-neutral-800 pt-3">
            {session ? (
              <button
                onClick={() => { signOut({ callbackUrl: '/' }); closeMobile() }}
                className="text-sm text-neutral-400 hover:text-white"
              >
                로그아웃
              </button>
            ) : (
              <Link href="/auth/signin" className="text-sm text-neutral-300 hover:text-white" onClick={closeMobile}>
                로그인
              </Link>
            )}
          </div>
        </nav>
      )}

      <WikiIndexDrawer
        open={indexOpen}
        onClose={() => setIndexOpen(false)}
        pages={wikiPages}
        topics={wikiTopics}
        concepts={concepts}
        currentSlug={currentSlug}
      />
    </header>
  )
}
