'use client'

import { useState } from 'react'

export default function FilterBar() {
  const [activeFilter, setActiveFilter] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')

  const filters = [
    { id: 'all', label: 'すべて', count: 1247 },
    { id: 'high', label: '高インパクト', count: 47 },
    { id: 'positive', label: 'ポジティブ', count: 850 },
    { id: 'negative', label: 'ネガティブ', count: 197 },
    { id: 'today', label: '今日', count: 85 },
  ]

  return (
    <div className="bg-white/60 backdrop-blur-sm rounded-apple-lg p-4 border border-apple-gray-200/50 shadow-apple">
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
        {/* Filters */}
        <div className="flex flex-wrap gap-2">
          {filters.map((filter) => (
            <button
              key={filter.id}
              onClick={() => setActiveFilter(filter.id)}
              className={`
                px-4 py-2 rounded-full text-sm font-medium transition-all duration-300
                ${
                  activeFilter === filter.id
                    ? 'bg-apple-blue text-white shadow-apple'
                    : 'bg-apple-gray-100 text-apple-gray-700 hover:bg-apple-gray-200'
                }
              `}
            >
              {filter.label}
              <span className={`ml-2 ${activeFilter === filter.id ? 'text-white/80' : 'text-apple-gray-500'}`}>
                {filter.count}
              </span>
            </button>
          ))}
        </div>

        {/* Search */}
        <div className="relative">
          <input
            type="text"
            placeholder="ニュースを検索..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="
              w-full lg:w-80 px-4 py-2 pl-10
              bg-apple-gray-50 border border-apple-gray-200
              rounded-full text-sm
              focus:outline-none focus:ring-2 focus:ring-apple-blue focus:border-transparent
              transition-all duration-300
            "
          />
          <svg
            className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-apple-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </div>
      </div>
    </div>
  )
}
