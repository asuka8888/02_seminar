'use client'

import NewsCard from './NewsCard'

// Mock data (実際のデータは API から取得)
const mockNews = [
  {
    id: '1',
    source: '@elonmusk',
    platform: 'twitter',
    publishedAt: new Date(Date.now() - 3600000).toISOString(),
    originalText: 'Tesla stock is up 10% today!',
    translatedText: 'テスラ株が今日10%上昇！',
    summary: 'テスラの株価が10%急騰。電気自動車市場での優位性が評価された。',
    sentiment: 'positive',
    sentimentScore: 0.85,
    priority: 'high',
    keyTopics: ['Tesla', 'EV', '株価'],
    likes: 15000,
    retweets: 8000,
    category: 'us_tech_crypto',
    language: 'en',
    originalUrl: 'https://x.com/elonmusk/status/123456',
  },
  {
    id: '2',
    source: '@gold_locks_x',
    platform: 'twitter',
    publishedAt: new Date(Date.now() - 7200000).toISOString(),
    originalText: '日経平均が年初来高値を更新',
    summary: '日経平均株価が年初来高値を更新。半導体関連株が全面高となり、市場全体を牽引している。',
    sentiment: 'positive',
    sentimentScore: 0.75,
    priority: 'high',
    keyTopics: ['日経平均', '半導体', '株式'],
    likes: 3500,
    retweets: 1200,
    category: 'japanese_investors',
    language: 'ja',
    originalUrl: 'https://x.com/gold_locks_x/status/123457',
  },
  {
    id: '3',
    source: '@LizAnnSonders',
    platform: 'twitter',
    publishedAt: new Date(Date.now() - 10800000).toISOString(),
    originalText: 'Fed signals potential rate cuts in 2024',
    translatedText: 'FRBが2024年の利下げの可能性を示唆',
    summary: '連邦準備制度理事会が2024年の利下げの可能性を示唆。市場は好感を持って反応している。',
    sentiment: 'positive',
    sentimentScore: 0.65,
    priority: 'medium',
    keyTopics: ['FRB', '金利', '経済'],
    likes: 8500,
    retweets: 4200,
    category: 'us_macro_strategy',
    language: 'en',
    originalUrl: 'https://x.com/LizAnnSonders/status/123458',
  },
  {
    id: '4',
    source: '@HindenburgRes',
    platform: 'twitter',
    publishedAt: new Date(Date.now() - 14400000).toISOString(),
    originalText: 'New short report on XYZ Corp',
    translatedText: 'XYZ社に関する新たなショートレポート',
    summary: 'Hindenburg ResearchがXYZ社の不正会計疑惑を指摘。株価は急落している。',
    sentiment: 'negative',
    sentimentScore: -0.80,
    priority: 'high',
    keyTopics: ['ショート', '不正会計', 'リスク'],
    likes: 5500,
    retweets: 3100,
    category: 'us_short_sellers',
    language: 'en',
    originalUrl: 'https://x.com/HindenburgRes/status/123459',
  },
  {
    id: '5',
    source: '@bei_wayaku',
    platform: 'twitter',
    publishedAt: new Date(Date.now() - 18000000).toISOString(),
    originalText: 'AI関連株が全面高、NvidiaとMicrosoftが最高値更新',
    summary: 'AI関連株が全面高となり、NvidiaとMicrosoftが史上最高値を更新。AI投資ブームが加速。',
    sentiment: 'positive',
    sentimentScore: 0.90,
    priority: 'high',
    keyTopics: ['AI', 'Nvidia', 'Microsoft'],
    likes: 4200,
    retweets: 1800,
    category: 'japanese_analysts',
    language: 'ja',
    originalUrl: 'https://x.com/bei_wayaku/status/123460',
  },
  {
    id: '6',
    source: '@charliebilello',
    platform: 'twitter',
    publishedAt: new Date(Date.now() - 21600000).toISOString(),
    originalText: 'S&P 500 hits new all-time high',
    translatedText: 'S&P 500が史上最高値を更新',
    summary: 'S&P 500指数が史上最高値を更新。強い企業業績と経済指標が支援。',
    sentiment: 'positive',
    sentimentScore: 0.80,
    priority: 'medium',
    keyTopics: ['S&P500', '株式市場', '最高値'],
    likes: 9200,
    retweets: 5100,
    category: 'us_macro_strategy',
    language: 'en',
    originalUrl: 'https://x.com/charliebilello/status/123461',
  },
]

export default function NewsGrid() {
  return (
    <div>
      {/* Section Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-apple-gray-900">
          最新ニュース
        </h2>
        <button className="text-sm font-medium text-apple-blue hover:text-apple-purple transition-colors">
          すべて表示 →
        </button>
      </div>

      {/* News Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockNews.map((news, index) => (
          <div
            key={news.id}
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <NewsCard news={news} />
          </div>
        ))}
      </div>

      {/* Load More */}
      <div className="mt-8 text-center">
        <button className="
          px-8 py-3 bg-white/60 backdrop-blur-sm border border-apple-gray-200
          rounded-full text-sm font-medium text-apple-gray-700
          hover:bg-apple-gray-50 hover:border-apple-gray-300 hover:shadow-apple
          transition-all duration-300
        ">
          さらに読み込む
        </button>
      </div>
    </div>
  )
}
