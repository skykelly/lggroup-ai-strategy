import type { Metadata } from 'next'
import { Geist, Geist_Mono } from 'next/font/google'
import './globals.css'
import { auth } from '@/auth'
import Header from '@/components/Header'
import EmbeddedChrome from '@/components/EmbeddedChrome'
import ChatPopup from '@/components/ChatPopup'

const geistSans = Geist({ variable: '--font-geist-sans', subsets: ['latin'] })
const geistMono = Geist_Mono({ variable: '--font-geist-mono', subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Homestyle Wiki',
  description: '한국 리빙 시장 스타일·트렌드·카테고리 지식체계',
}

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const session = await auth()

  return (
    <html lang="ko">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased bg-neutral-950 text-neutral-100 min-h-screen`}>
        <EmbeddedChrome />
        <Header session={session} />
        <main>{children}</main>
        <ChatPopup session={session} />
      </body>
    </html>
  )
}
