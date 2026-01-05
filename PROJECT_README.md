# Financial Intelligence System
## 女性起業家向け金融インテリジェンス配信システム

[![Next.js](https://img.shields.io/badge/Next.js-15.1-black)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> Twitter監視 × AI分析 × リアルタイム配信で、世界の金融インテリジェンスを日本語で届けるシステム

---

## 📋 プロジェクト概要

このシステムは、海外の金融情報（50個のMust Follow Twitterアカウント + 時価総額TOP10）をリアルタイムで監視し、Claude AIによる分析・翻訳を経て、LINE/メールで即座に配信する金融インテリジェンスプラットフォームです。

### 主な機能

- **Twitter監視**: 50個の厳選された金融アカウントをリアルタイム監視
- **AI分析**: Claude Code + LangGraphによるインテリジェント分析
- **自動翻訳**: 英語→日本語の高品質翻訳
- **市場データ**: 時価総額TOP10のリアルタイム追跡
- **即時配信**: LINE Messaging API / SendGridによる通知
- **ダッシュボード**: Next.js 15 + Tailwind CSSの洗練されたUI

---

## 🏗️ アーキテクチャ

### ハイブリッド構成

```
┌─────────────────────────────────────────────────────────┐
│  Frontend (Next.js 15)                                  │
│  - App Router + React Server Components                │
│  - Tailwind CSS + shadcn/ui                            │
│  - tRPC + Prisma                                       │
└────────────────┬────────────────────────────────────────┘
                 │ API (tRPC)
┌────────────────▼────────────────────────────────────────┐
│  Intelligence Engine (Python + FastAPI)                 │
│  - Claude Code + LangGraph                             │
│  - Twitter Scraping (crawl4ai + tweepy)                │
│  - Financial APIs (FMP + Alpha Vantage)                │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│  Infrastructure (Google Cloud + Docker)                 │
│  - Cloud SQL (PostgreSQL 15)                           │
│  - Cloud Run (Container deployment)                    │
│  - Redis (Cache + Message Broker)                      │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 プロジェクト構造

```
02_seminar_files/
├── frontend/                # Next.js 15 フロントエンド
│   ├── src/
│   │   ├── app/            # App Router
│   │   ├── components/     # React コンポーネント
│   │   ├── lib/            # ユーティリティ
│   │   ├── server/         # tRPC サーバー
│   │   └── styles/         # グローバルCSS
│   ├── prisma/
│   │   └── schema.prisma   # Prisma スキーマ
│   └── package.json
│
├── backend/                # Python バックエンド
│   ├── src/
│   │   ├── api/           # FastAPI エンドポイント
│   │   ├── agents/        # LangGraph AIエージェント
│   │   ├── scraper/       # Twitter/Web スクレイパー
│   │   ├── models/        # データモデル
│   │   ├── services/      # ビジネスロジック
│   │   └── config/        # 設定管理
│   └── requirements.txt
│
├── taisun_agent/           # Git Submodule (既存エージェント)
├── docker-compose.yml      # Docker構成
├── scripts/                # ユーティリティスクリプト
│   └── init-db.sql
│
└── ドキュメント/
    ├── 01_要件定義書_憲法.md
    ├── 02_要件定義書_全文_人間用.md
    ├── 03_仕様書_UI_API_DB.md
    ├── 04_ワークフロー.md
    ├── 05_実行計画書.md
    └── 06_技術要件書.md
```

---

## 🚀 クイックスタート

### 前提条件

- Node.js 20.x
- Python 3.11
- Docker Desktop
- Git

### 1. リポジトリのクローン

```bash
git clone --recurse-submodules https://github.com/asuka8888/02_seminar.git
cd 02_seminar
```

### 2. データベースの起動

```bash
docker-compose up -d postgres redis
```

### 3. フロントエンドのセットアップ

```bash
cd frontend

# 依存関係のインストール
npm install

# 環境変数の設定
cp .env.example .env.local
# .env.local を編集してAPIキーを設定

# Prismaマイグレーション
npx prisma generate
npx prisma migrate dev --name init

# 開発サーバー起動
npm run dev
```

フロントエンドは http://localhost:3000 で起動します。

### 4. バックエンドのセットアップ

```bash
cd ../backend

# 仮想環境の作成
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
cp .env.example .env
# .env を編集してAPIキーを設定

# 開発サーバー起動
python src/main.py
```

バックエンドAPIは http://localhost:8000 で起動します。

---

## 🔑 APIキーの取得

### 必須APIキー

1. **Anthropic API Key** (Claude)
   - https://console.anthropic.com/
   - `ANTHROPIC_API_KEY`

2. **Twitter API v2 Bearer Token**
   - https://developer.twitter.com/
   - `TWITTER_BEARER_TOKEN`

3. **LINE Messaging API**
   - https://developers.line.biz/
   - `LINE_CHANNEL_ACCESS_TOKEN`

### オプションAPIキー

4. **Financial Modeling Prep** (市場データ)
   - https://financialmodelingprep.com/
   - `FMP_API_KEY`

5. **Alpha Vantage** (株価データ)
   - https://www.alphavantage.co/
   - `ALPHA_VANTAGE_API_KEY`

6. **OpenAI API** (フォールバック用)
   - https://platform.openai.com/
   - `OPENAI_API_KEY`

---

## 📊 技術スタック

### フロントエンド
- **Next.js 15** - React フレームワーク (App Router)
- **TypeScript 5.3** - 型安全な開発
- **Tailwind CSS 3.4** - ユーティリティファーストCSS
- **Prisma 5** - TypeScript ORM
- **tRPC 10** - 型安全なAPI通信
- **Zustand 4** - 状態管理
- **NextAuth.js 5** - 認証
- **Recharts 2** - データ可視化

### バックエンド
- **Python 3.11** - メイン言語
- **FastAPI 0.109** - Web フレームワーク
- **Claude Code** - Anthropic CLI
- **LangChain / LangGraph** - AIエージェント
- **Tweepy 4.14** - Twitter API
- **Pandas / Polars** - データ処理
- **Celery + Redis** - 非同期タスク

### インフラ
- **PostgreSQL 15** - メインDB
- **Redis 7** - キャッシュ/メッセージブローカー
- **Docker** - コンテナ化
- **Google Cloud** - 本番環境 (Cloud Run, Cloud SQL)

---

## 🧪 テスト

### フロントエンド

```bash
cd frontend
npm run test
npm run type-check
npm run lint
```

### バックエンド

```bash
cd backend
pytest
black . --check
ruff check .
mypy src/
```

---

## 📦 デプロイ

### Google Cloud Run へのデプロイ

```bash
# フロントエンド
cd frontend
gcloud run deploy fin-intel-frontend \
  --source . \
  --region asia-northeast1 \
  --allow-unauthenticated

# バックエンド
cd ../backend
gcloud run deploy fin-intel-backend \
  --source . \
  --region asia-northeast1 \
  --set-env-vars="DATABASE_URL=postgresql://..."
```

詳細は `05_実行計画書.md` の「デプロイ計画」セクションを参照してください。

---

## 📖 ドキュメント

| ドキュメント | 説明 |
|---|---|
| [01_要件定義書_憲法.md](01_要件定義書_憲法.md) | システムの10の憲法的原則 |
| [02_要件定義書_全文_人間用.md](02_要件定義書_全文_人間用.md) | 完全な要件定義 |
| [03_仕様書_UI_API_DB.md](03_仕様書_UI_API_DB.md) | UI/API/DB仕様 |
| [04_ワークフロー.md](04_ワークフロー.md) | システムワークフロー |
| [05_実行計画書.md](05_実行計画書.md) | 8週間開発計画 |
| [06_技術要件書.md](06_技術要件書.md) | 技術詳細仕様 |

---

## 🐛 トラブルシューティング

### PostgreSQLに接続できない

```bash
# Dockerコンテナの状態確認
docker ps

# ログ確認
docker logs fin-intel-postgres

# 再起動
docker-compose restart postgres
```

### Prismaマイグレーションエラー

```bash
# Prisma Clientの再生成
npx prisma generate

# データベースのリセット（開発環境のみ）
npx prisma migrate reset
```

### Pythonパッケージのインストールエラー

```bash
# pip のアップグレード
pip install --upgrade pip

# 仮想環境の再作成
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🤝 コントリビューション

Issue #190 で開発状況を追跡しています:
https://github.com/taiyousan15/taisun_agent/issues/190

---

## 📄 ライセンス

MIT License

---

## 📧 お問い合わせ

プロジェクトに関する質問は、GitHub Issueまたはリポジトリオーナーまでお願いします。

---

**作成日**: 2026年1月5日
**バージョン**: 1.0.0
**開発開始予定**: 2026年1月6日
