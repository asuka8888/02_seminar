import { Suspense } from 'react'
import Header from '@/components/Header'
import NewsGrid from '@/components/NewsGrid'
import FilterBar from '@/components/FilterBar'
import StatsOverview from '@/components/StatsOverview'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-apple-gray-50 via-white to-apple-gray-100">
      {/* Header */}
      <Header />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Overview */}
        <Suspense fallback={<StatsOverviewSkeleton />}>
          <StatsOverview />
        </Suspense>

        {/* Filter Bar */}
        <div className="mt-8">
          <FilterBar />
        </div>

        {/* News Grid */}
        <div className="mt-8">
          <Suspense fallback={<NewsGridSkeleton />}>
            <NewsGrid />
          </Suspense>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-24 border-t border-apple-gray-200 bg-white/50 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center text-apple-gray-500 text-sm">
            <p>© 2026 Financial Intelligence System</p>
            <p className="mt-2">女性起業家向け金融インテリジェンス配信システム</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

// Loading Skeletons
function StatsOverviewSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-6 animate-pulse">
      {[...Array(4)].map((_, i) => (
        <div key={i} className="bg-white/60 backdrop-blur-sm rounded-apple-lg p-6 h-32" />
      ))}
    </div>
  )
}

function NewsGridSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse">
      {[...Array(9)].map((_, i) => (
        <div key={i} className="bg-white/60 backdrop-blur-sm rounded-apple-lg p-6 h-64" />
      ))}
    </div>
  )
}
