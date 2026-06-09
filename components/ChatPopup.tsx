'use client'
import type { Session } from 'next-auth'

// Phase 12에서 구현 예정
export default function ChatPopup({ session }: { session: Session | null }) {
  if (!session) return null
  return null
}
