# Claude Code 開発プロンプト
## Financial Intelligence System 実装開始

---

## 📋 このプロンプトの使い方

このドキュメント全体を Claude Code に貼り付けて、システム実装を開始してください。

**コピー範囲**: この下の「=== ここからコピー ===」から「=== ここまでコピー ===」まで

---

# === ここからコピー ===

# Financial Intelligence System - 実装開始プロンプト

私は **女性起業家向け金融インテリジェンス配信システム** の開発を開始します。
以下の設計ドキュメントに基づいて、システムを実装してください。

---

## 🎯 プロジェクト概要

### システム名
**Financial Intelligence System（金融インテリジェンス配信システム）**

### 目的
- 海外の金融情報（50個のMust Follow Twitterアカウント）をリアルタイム監視
- Claude AIによる自動分析・翻訳
- LINE/メールで即座に配信
- 時価総額TOP10のリアルタイム追跡

---

## 📁 プロジェクト構造（既に構築済み）

プロジェクトは以下の構造で構築されています：

```
02_seminar_files/
├── frontend/                # Next.js 15 フロントエンド
│   ├── src/
│   │   ├── app/            # App Router
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/     # Reactコンポーネント
│   │   ├── lib/            # ユーティリティ
│   │   ├── server/         # tRPCサーバー
│   │   └── styles/
│   │       └── globals.css
│   ├── prisma/
│   │   └── schema.prisma   # データベーススキーマ
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── .env.example
│
├── backend/                # Python バックエンド
│   ├── src/
│   │   ├── main.py        # FastAPI エントリーポイント
│   │   ├── config/
│   │   │   └── settings.py
│   │   ├── api/           # APIエンドポイント
│   │   ├── agents/        # LangGraph AIエージェント
│   │   ├── scraper/       # Twitter/Web スクレイパー
│   │   ├── models/        # データモデル
│   │   ├── services/      # ビジネスロジック
│   │   └── utils/         # ユーティリティ
│   ├── requirements.txt
│   └── .env.example
│
├── docker-compose.yml      # PostgreSQL + Redis
├── scripts/
│   └── init-db.sql
│
└── ドキュメント/
    ├── 01_要件定義書_憲法.md
    ├── 02_要件定義書_全文_人間用.md
    ├── 03_仕様書_UI_API_DB.md
    ├── 04_ワークフロー.md
    ├── 05_実行計画書.md
    ├── 06_技術要件書.md
    ├── PROJECT_README.md
    └── SETUP_GUIDE.md
```

---

## 🛠️ 技術スタック

### フロントエンド
- **Next.js 15** (App Router)
- **TypeScript 5.3**
- **Tailwind CSS 3.4**
- **Prisma 5** (ORM)
- **tRPC 10** (型安全API)
- **NextAuth.js 5** (認証)
- **Zustand 4** (状態管理)
- **Recharts 2** (グラフ)

### バックエンド
- **Python 3.11**
- **FastAPI 0.109**
- **Claude Code** (Anthropic CLI)
- **LangChain / LangGraph** (AIエージェント)
- **Tweepy 4.14** (Twitter API)
- **Pandas / Polars** (データ処理)
- **Celery + Redis** (非同期タスク)

### データベース & インフラ
- **PostgreSQL 15**
- **Redis 7**
- **Docker**
- **Google Cloud** (本番環境)
  - Cloud Run
  - Cloud SQL
  - Secret Manager

---

## 📖 設計ドキュメント参照

プロジェクトには以下の設計ドキュメントが含まれています。
実装前に必ず参照してください：

### 1. 要件定義書（憲法） - `01_要件定義書_憲法.md`
システムの10の憲法的原則：
- 第1条: リアルタイム性の絶対保証
- 第2条: 情報の信頼性と透明性
- 第3条: AI翻訳の品質保証
- 第4条: ユーザー体験の最適化
- 第5条: セキュリティとプライバシー
- 第6条: スケーラビリティ
- 第7条: 可観測性と運用性
- 第8条: コスト効率性
- 第9条: オープンソース活用
- 第10条: 継続的改善

### 2. 要件定義書（全文・人間用） - `02_要件定義書_全文_人間用.md`
- ユーザーストーリー
- 機能要件
- 非機能要件
- KPI
- 開発スケジュール（8週間）

### 3. 仕様書（UI / API / DB） - `03_仕様書_UI_API_DB.md`
- UIレイアウト詳細
- tRPC APIエンドポイント仕様
- Prismaスキーマ定義
- データモデル

### 4. ワークフロー - `04_ワークフロー.md`
- データ収集→分析→配信の全フロー
- LangGraphステートマシン
- Mermaidダイアグラム

### 5. 実行計画書 - `05_実行計画書.md`
- 8週間の詳細開発計画
- フェーズ別タスク
- マイルストーン

### 6. 技術要件書 - `06_技術要件書.md`
- パッケージバージョン詳細
- 環境変数一覧
- デプロイ設定

---

## 🚀 実装タスク（優先順位順）

### Phase 1: コア機能実装（Week 2-3）

#### 1. Twitterスクレイパー実装
**ファイル**: `backend/src/scraper/twitter_scraper.py`

**要件**:
- 50個の監視対象アカウントから過去24時間の投稿を取得
- crawl4ai または tweepy を使用
- レート制限対応
- エラーハンドリング

**監視対象アカウント例** (全50件は `株情報収集・配信システム開発.md` 参照):
```python
TWITTER_ACCOUNTS = [
    "LizAnnSonders",      # Charles Schwab
    "elerianm",           # Mohamed El-Erian
    "Schuldensuehner",    # Holger Zschaepitz
    "lisaabramowicz1",    # Lisa Abramowicz
    "charliebilello",     # Charlie Bilello
    # ... 残り45件
]
```

#### 2. Claude AI分析エージェント実装
**ファイル**: `backend/src/agents/intelligence_agent.py`

**要件**:
- LangGraph でステートフルエージェント構築
- 入力: Twitter投稿（英語）
- 出力:
  - 日本語翻訳
  - 3行要約
  - センチメント分析 (positive/negative/neutral)
  - 優先度 (high/medium/low)
  - 関連セクター
  - 関連銘柄ティッカー

#### 3. Prismaマイグレーション実行
**ファイル**: `frontend/prisma/schema.prisma`

**タスク**:
```bash
cd frontend
npx prisma generate
npx prisma migrate dev --name initial_schema
```

#### 4. tRPC APIルーター実装
**ファイル**: `frontend/src/server/api/routers/news.ts`

**エンドポイント**:
- `news.getAll` - ニュース一覧取得
- `news.getById` - ニュース詳細取得
- `news.getBySector` - セクター別取得
- `news.getBySentiment` - センチメント別取得

#### 5. ダッシュボードUI実装
**ファイル**: `frontend/src/app/dashboard/page.tsx`

**コンポーネント**:
- ニュースフィード（リアルタイム更新）
- センチメント分析グラフ
- セクター別フィルター
- 優先度別ソート

---

### Phase 2: データ配信機能（Week 4）

#### 6. LINE配信機能実装
**ファイル**: `backend/src/services/line_notifier.py`

**要件**:
- LINE Messaging APIでFlex Message送信
- 優先度の高いニュースを即時配信
- ユーザー設定に基づく配信頻度制御

#### 7. メール配信機能実装
**ファイル**: `backend/src/services/email_notifier.py`

**要件**:
- SendGrid API使用
- HTMLメールテンプレート
- 日次サマリーメール

---

### Phase 3: 時価総額ランキング機能（Week 5）

#### 8. 市場データ取得実装
**ファイル**: `backend/src/services/market_data_fetcher.py`

**要件**:
- Financial Modeling Prep API使用
- 時価総額TOP10を定期取得（1時間ごと）
- 順位変動検出

#### 9. ランキング変動分析
**ファイル**: `backend/src/agents/ranking_analyzer.py`

**要件**:
- Claude AIで順位変動理由を分析
- 関連ニュースとの紐付け

---

## 🔑 環境変数設定

### フロントエンド `.env.local`
```env
DATABASE_URL="postgresql://finuser:finpass123@localhost:5432/fin_intel"
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="your-secret-key-here"
NEXT_PUBLIC_BACKEND_URL="http://localhost:8000"
```

### バックエンド `.env`
```env
# AI APIs
ANTHROPIC_API_KEY="sk-ant-api03-xxxxx"
OPENAI_API_KEY="sk-xxxxx"

# Data Collection
TWITTER_BEARER_TOKEN="AAAAAAAAAxxxxxxxxx"
FMP_API_KEY="your-fmp-key"
ALPHA_VANTAGE_API_KEY="your-alpha-vantage-key"

# Notification
LINE_CHANNEL_ACCESS_TOKEN="your-line-token"
SENDGRID_API_KEY="SG.xxxxx"

# Database
DATABASE_URL="postgresql://finuser:finpass123@localhost:5432/fin_intel"
REDIS_URL="redis://localhost:6379"
```

---

## 📝 実装時の注意事項

### 1. Prismaスキーマに従う
`frontend/prisma/schema.prisma` に定義されたモデルを厳密に使用してください：
- User
- UserSettings
- LineIntegration
- News
- MarketCapRanking
- RankingChange
- NotificationLog

### 2. TypeScript型安全性
tRPCを使用して、フロントエンド⇔バックエンド間の型安全性を確保してください。

### 3. エラーハンドリング
- Twitter API のレート制限
- Claude API のトークン制限
- データベース接続エラー
すべてに適切なエラーハンドリングとリトライロジックを実装してください。

### 4. ログ出力
`backend/src/main.py` で設定されたロギングを使用してください。

---

## 🧪 テストについて

実装後は以下のテストを実行してください：

### フロントエンド
```bash
cd frontend
npm run type-check
npm run lint
```

### バックエンド
```bash
cd backend
pytest
black . --check
mypy src/
```

---

## 📊 開発の進め方

### ステップ1: 設計ドキュメントを読む
まず、以下のドキュメントを読んで全体像を把握してください：
- `PROJECT_README.md` - プロジェクト概要
- `02_要件定義書_全文_人間用.md` - 詳細要件
- `03_仕様書_UI_API_DB.md` - 技術仕様

### ステップ2: 環境確認
```bash
# データベース起動確認
docker ps
# fin-intel-postgres が起動していることを確認

# フロントエンド起動確認
cd frontend
npm run dev
# http://localhost:3000 で起動

# バックエンド起動確認
cd backend
python src/main.py
# http://localhost:8000 で起動
```

### ステップ3: Phase 1から順次実装
上記の「実装タスク」を Phase 1 → Phase 2 → Phase 3 の順に実装してください。

### ステップ4: Git コミット
機能ごとにコミットしてください：
```bash
git add .
git commit -m "feat: Twitter scraper implementation"
git push origin main
```

---

## 🎯 最初に実装すべき機能

**今すぐ始めるべきタスク**:

1. **Twitterスクレイパー** (`backend/src/scraper/twitter_scraper.py`)
   - まず10個のアカウントで動作確認
   - その後50個に拡張

2. **Claude分析エージェント** (`backend/src/agents/intelligence_agent.py`)
   - 1つのツイートを分析するプロトタイプから開始
   - 翻訳→要約→分析のパイプライン構築

3. **データベース保存** (`backend/src/models/news.py`)
   - Prismaで解析結果をDBに保存
   - フロントエンドで表示

---

## 📞 質問・不明点がある場合

実装中に不明点があれば、以下のドキュメントを参照してください：
- 技術的な詳細: `06_技術要件書.md`
- ワークフロー: `04_ワークフロー.md`
- セットアップ: `SETUP_GUIDE.md`

---

## 🚀 さあ、実装を始めましょう！

上記の情報を基に、**Phase 1: Twitterスクレイパー実装**から開始してください。

実装方針：
1. まず動くプロトタイプを作る
2. 段階的に機能を追加
3. 各機能ごとにテスト
4. ドキュメント化

**最初の目標**: 1つのTwitterアカウントから投稿を取得し、Claudeで分析し、データベースに保存する最小限のパイプラインを構築してください。

実装開始をお願いします！

# === ここまでコピー ===

---

## 補足情報

### すでに完了していること
✅ プロジェクトディレクトリ構造作成
✅ Next.js 15 フロントエンド基本セットアップ
✅ Python バックエンド基本セットアップ
✅ Docker Compose (PostgreSQL + Redis)
✅ Prisma スキーマ定義
✅ 環境変数テンプレート
✅ 設計ドキュメント (6ファイル)

### これから実装すべきこと
⏳ Twitterスクレイパー
⏳ Claude AI分析エージェント
⏳ tRPC APIエンドポイント
⏳ ダッシュボードUI
⏳ LINE/メール配信機能
⏳ 時価総額ランキング機能

---

**使用方法**:
上記の「=== ここからコピー ===」から「=== ここまでコピー ===」までを
新しいClaude Codeセッションに貼り付けて実装を開始してください。
