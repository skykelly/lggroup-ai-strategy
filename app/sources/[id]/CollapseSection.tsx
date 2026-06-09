'use client'
import { useState } from 'react'
import MarkdownRenderer from '@/components/MarkdownRenderer'

export default function CollapseSection({ html }: { html: string }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="border border-neutral-800 rounded-xl overflow-hidden">
      <button
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-center justify-between px-5 py-3.5 text-sm text-neutral-400 hover:text-neutral-200 hover:bg-neutral-900/50 transition-colors"
      >
        <span>{open ? '원문 접기' : '원문 펼치기'}</span>
        <span className="text-xs opacity-60">{open ? '▲' : '▼'}</span>
      </button>
      {open && (
        <div className="px-5 pb-5 pt-2 border-t border-neutral-800">
          <MarkdownRenderer html={html} />
        </div>
      )}
    </div>
  )
}
