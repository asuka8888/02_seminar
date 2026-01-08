'use client'

import { useState, useEffect } from 'react'

export default function Header() {
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10)
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <header
      className={`sticky top-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-white/80 backdrop-blur-xl shadow-apple border-b border-apple-gray-200'
          : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-apple-blue to-apple-purple rounded-apple flex items-center justify-center shadow-apple-lg">
              <svg
                className="w-6 h-6 text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
                />
              </svg>
            </div>
            <div>
              <h1 className="text-xl font-semibold text-apple-gray-900">
                Financial Intelligence
              </h1>
              <p className="text-xs text-apple-gray-500">
                女性起業家のための金融インテリジェンス
              </p>
            </div>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <a
              href="#"
              className="text-sm font-medium text-apple-gray-900 hover:text-apple-blue transition-colors"
            >
              ダッシュボード
            </a>
            <a
              href="#"
              className="text-sm font-medium text-apple-gray-600 hover:text-apple-blue transition-colors"
            >
              ニュース
            </a>
            <a
              href="#"
              className="text-sm font-medium text-apple-gray-600 hover:text-apple-blue transition-colors"
            >
              市場データ
            </a>
            <a
              href="#"
              className="text-sm font-medium text-apple-gray-600 hover:text-apple-blue transition-colors"
            >
              設定
            </a>
          </nav>

          {/* User Menu */}
          <div className="flex items-center space-x-4">
            {/* Live Indicator */}
            <div className="hidden sm:flex items-center space-x-2 px-3 py-1.5 bg-apple-green/10 rounded-full">
              <div className="w-2 h-2 bg-apple-green rounded-full animate-pulse" />
              <span className="text-xs font-medium text-apple-green">Live</span>
            </div>

            {/* Profile */}
            <button className="w-9 h-9 rounded-full bg-gradient-to-br from-apple-gray-200 to-apple-gray-300 flex items-center justify-center hover:shadow-apple-lg transition-shadow">
              <span className="text-sm font-semibold text-apple-gray-700">A</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}
