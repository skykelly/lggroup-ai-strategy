import { auth } from '@/auth'
import { getChatSessions } from '@/lib/data'
import ChatInterface from './ChatInterface'

export default async function ChatPage() {
  const session = await auth()
  const sessions = session?.user?.email ? await getChatSessions(session.user.email) : []

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <h1 className="text-lg font-semibold text-white mb-4">Chat</h1>
      <ChatInterface initialSessions={sessions} />
    </div>
  )
}
