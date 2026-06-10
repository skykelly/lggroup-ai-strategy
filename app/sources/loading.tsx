export default function Loading() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 animate-pulse">
      <div className="flex items-center justify-between mb-6">
        <div>
          <div className="h-5 w-24 bg-neutral-800 rounded-md" />
          <div className="h-3 w-16 bg-neutral-900 rounded-md mt-2" />
        </div>
        <div className="h-9 w-24 bg-neutral-800 rounded-lg" />
      </div>
      <div className="space-y-2">
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} className="h-12 bg-neutral-900 border border-neutral-800 rounded-xl" />
        ))}
      </div>
    </div>
  )
}
