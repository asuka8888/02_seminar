'use client'

export default function StatsOverview() {
  const stats = [
    {
      label: '総ニュース数',
      value: '1,247',
      change: '+12.5%',
      trend: 'up',
      icon: (
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      ),
      gradient: 'from-apple-blue to-apple-purple',
    },
    {
      label: '高インパクト',
      value: '47',
      change: '+8',
      trend: 'up',
      icon: (
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      ),
      gradient: 'from-apple-orange to-apple-red',
    },
    {
      label: 'ポジティブ',
      value: '68%',
      change: '+5.2%',
      trend: 'up',
      icon: (
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      gradient: 'from-apple-green to-emerald-500',
    },
    {
      label: 'アクティブソース',
      value: '91',
      change: '100%',
      trend: 'neutral',
      icon: (
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      ),
      gradient: 'from-apple-purple to-pink-500',
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 animate-fade-in">
      {stats.map((stat, index) => (
        <div
          key={stat.label}
          className="group relative bg-white/60 backdrop-blur-sm rounded-apple-lg p-6 border border-apple-gray-200/50 hover:border-apple-gray-300 hover:shadow-apple-lg transition-all duration-300 animate-slide-up"
          style={{ animationDelay: `${index * 100}ms` }}
        >
          {/* Gradient Background (on hover) */}
          <div className={`absolute inset-0 bg-gradient-to-br ${stat.gradient} opacity-0 group-hover:opacity-5 rounded-apple-lg transition-opacity duration-300`} />

          <div className="relative">
            {/* Icon */}
            <div className={`w-12 h-12 bg-gradient-to-br ${stat.gradient} rounded-apple flex items-center justify-center text-white shadow-apple mb-4`}>
              {stat.icon}
            </div>

            {/* Value */}
            <div className="text-3xl font-bold text-apple-gray-900 mb-1">
              {stat.value}
            </div>

            {/* Label */}
            <div className="text-sm text-apple-gray-600 mb-2">
              {stat.label}
            </div>

            {/* Change */}
            <div className="flex items-center space-x-1">
              {stat.trend === 'up' && (
                <svg className="w-4 h-4 text-apple-green" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              )}
              <span className={`text-xs font-medium ${stat.trend === 'up' ? 'text-apple-green' : 'text-apple-gray-500'}`}>
                {stat.change}
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
