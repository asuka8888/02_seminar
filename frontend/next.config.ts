import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
  // 環境変数の設定
  env: {
    NEXT_PUBLIC_APP_NAME: 'Financial Intelligence System',
  },
}

export default nextConfig
