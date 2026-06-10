export default function Loading() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 animate-pulse">
      <div className="mb-6">
        <div className="h-5 w-28 bg-neutral-800 rounded-md" />
        <div className="h-3 w-48 bg-neutral-900 rounded-md mt-2" />
      </div>
      <div className="h-[600px] bg-neutral-900 border border-neutral-800 rounded-xl" />
    </div>
  )
}
