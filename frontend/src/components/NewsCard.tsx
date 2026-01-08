'use client'

interface NewsCardProps {
  news: {
    id: string
    source: string
    platform: string
    publishedAt: string
    originalText: string
    translatedText?: string
    summary: string
    sentiment: string
    sentimentScore: number
    priority: string
    keyTopics: string[]
    likes: number
    retweets: number
    category: string
    language: string
    originalUrl: string
  }
}

export default function NewsCard({ news }: NewsCardProps) {
  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return 'text-apple-green bg-apple-green/10 border-apple-green/20'
      case 'negative':
        return 'text-apple-red bg-apple-red/10 border-apple-red/20'
      default:
        return 'text-apple-gray-600 bg-apple-gray-100 border-apple-gray-200'
    }
  }

  const getPriorityBadge = (priority: string) => {
    switch (priority) {
      case 'high':
        return (
          <span className="px-2 py-1 text-xs font-semibold bg-gradient-to-r from-apple-orange to-apple-red text-white rounded-full">
            HIGH
          </span>
        )
      case 'medium':
        return (
          <span className="px-2 py-1 text-xs font-semibold bg-apple-blue/10 text-apple-blue border border-apple-blue/20 rounded-full">
            MEDIUM
          </span>
        )
      default:
        return null
    }
  }

  const formatTime = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMs / 3600000)
    const diffDays = Math.floor(diffMs / 86400000)

    if (diffMins < 60) return `${diffMins}分前`
    if (diffHours < 24) return `${diffHours}時間前`
    if (diffDays < 7) return `${diffDays}日前`
    return date.toLocaleDateString('ja-JP')
  }

  return (
    <div className="group relative animate-scale-in">
      {/* Card */}
      <div className="
        h-full bg-white/60 backdrop-blur-sm rounded-apple-lg p-6
        border border-apple-gray-200/50
        hover:border-apple-gray-300 hover:shadow-apple-xl
        transition-all duration-300
        cursor-pointer
      ">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center space-x-3">
            {/* Source Avatar */}
            <div className="w-10 h-10 bg-gradient-to-br from-apple-blue to-apple-purple rounded-full flex items-center justify-center text-white font-semibold shadow-apple">
              {news.source.charAt(0).toUpperCase()}
            </div>
            <div>
              <div className="font-semibold text-apple-gray-900">
                {news.source}
              </div>
              <div className="text-xs text-apple-gray-500">
                {formatTime(news.publishedAt)}
              </div>
            </div>
          </div>

          {/* Priority Badge */}
          {getPriorityBadge(news.priority)}
        </div>

        {/* Summary */}
        <div className="mb-4">
          <p className="text-apple-gray-800 leading-relaxed line-clamp-3">
            {news.summary}
          </p>
        </div>

        {/* Topics */}
        {news.keyTopics && news.keyTopics.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-4">
            {news.keyTopics.slice(0, 3).map((topic, index) => (
              <span
                key={index}
                className="px-2 py-1 text-xs font-medium bg-apple-gray-100 text-apple-gray-700 rounded-full"
              >
                {topic}
              </span>
            ))}
          </div>
        )}

        {/* Footer */}
        <div className="flex items-center justify-between pt-4 border-t border-apple-gray-200/50">
          {/* Sentiment */}
          <div className={`flex items-center space-x-2 px-3 py-1.5 rounded-full border ${getSentimentColor(news.sentiment)}`}>
            {news.sentiment === 'positive' && (
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            )}
            {news.sentiment === 'negative' && (
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            )}
            <span className="text-xs font-semibold capitalize">
              {news.sentiment}
            </span>
          </div>

          {/* Engagement */}
          <div className="flex items-center space-x-4 text-apple-gray-500">
            <div className="flex items-center space-x-1">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
              <span className="text-xs">{news.likes}</span>
            </div>
            <div className="flex items-center space-x-1">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
              </svg>
              <span className="text-xs">{news.retweets}</span>
            </div>
          </div>
        </div>

        {/* Hover Effect - Read More */}
        <div className="absolute inset-0 bg-gradient-to-br from-apple-blue/5 to-apple-purple/5 rounded-apple-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
      </div>
    </div>
  )
}
