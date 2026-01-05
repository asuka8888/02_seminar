# 仕様書（UI / API / DB）
## 女性起業家向け金融インテリジェンス配信システム

**作成日**: 2026年1月5日
**バージョン**: 1.0
**対象読者**: 開発エンジニア
**プロジェクトコード**: FIN-INTEL-001

---

## 目次

1. [UI仕様](#1-ui仕様)
2. [API仕様](#2-api仕様)
3. [データベース仕様](#3-データベース仕様)
4. [外部API連携仕様](#4-外部api連携仕様)
5. [認証・認可仕様](#5-認証認可仕様)
6. [エラーハンドリング仕様](#6-エラーハンドリング仕様)

---

## 1. UI仕様

### 1.1 画面一覧

| 画面ID | 画面名 | URL | 認証 | 優先度 |
|---|---|---|---|---|
| UI-001 | ランディングページ | / | 不要 | 中 |
| UI-002 | ログイン | /auth/signin | 不要 | 高 |
| UI-003 | サインアップ | /auth/signup | 不要 | 高 |
| UI-004 | ダッシュボード | /dashboard | 必須 | 高 |
| UI-005 | 時価総額ランキング | /dashboard/marketcap | 必須 | 高 |
| UI-006 | ニュースフィード | /dashboard/news | 必須 | 高 |
| UI-007 | 設定 | /dashboard/settings | 必須 | 中 |
| UI-008 | プロフィール | /dashboard/profile | 必須 | 低 |

---

### 1.2 UI-004: ダッシュボード（メイン画面）

#### レイアウト
```
┌─────────────────────────────────────────────────────────┐
│ Header: ロゴ | ナビゲーション | 通知 | ユーザーアイコン  │
├─────────────────────────────────────────────────────────┤
│ Sidebar (左)                │ Main Content (右)        │
│ ┌─────────────────────┐   │ ┌──────────────────────┐ │
│ │ - ダッシュボード      │   │ │ 最新ニュース（5件）  │ │
│ │ - ランキング         │   │ │ [Card] [Card] [Card]  │ │
│ │ - ニュースフィード    │   │ └──────────────────────┘ │
│ │ - 設定               │   │ ┌──────────────────────┐ │
│ └─────────────────────┘   │ │ 時価総額TOP10         │ │
│                             │ │ [Table]               │ │
│                             │ └──────────────────────┘ │
│                             │ ┌──────────────────────┐ │
│                             │ │ セクター別ヒートマップ│ │
│                             │ │ [Heatmap]             │ │
│                             │ └──────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

#### コンポーネント詳細

##### 1. Header
- **ロゴ**: クリックでダッシュボードに戻る
- **ナビゲーション**: ダッシュボード / ランキング / ニュース
- **通知アイコン**: 未読通知数をバッジ表示
- **ユーザーアイコン**: ドロップダウンメニュー（プロフィール / ログアウト）

##### 2. 最新ニュースカード
```typescript
interface NewsCard {
  id: string;
  title: string;          // 要約（日本語、50文字以内）
  source: string;         // 情報源アカウント名
  sentiment: 'positive' | 'negative' | 'neutral';
  priority: 'high' | 'medium' | 'low';
  sector: string;         // セクター
  publishedAt: Date;
  originalUrl: string;    // 原文へのリンク
  notionUrl?: string;     // Notion詳細ページ
}
```

**デザイン**:
- 優先度「高」: 赤枠、左に🔴アイコン
- センチメント「positive」: 背景色を薄い赤
- センチメント「negative」: 背景色を薄い青
- ホバー時: 影を表示、カーソルをポインターに

**表示データ**:
- タイトル（太字）
- ソース名（小文字、灰色）
- 時刻（相対時刻: "5分前"）
- センチメントアイコン（🚀強気 / 📉弱気 / ➖中立）

##### 3. 時価総額TOP10テーブル
```typescript
interface MarketCapRanking {
  rank: number;
  companyName: string;
  ticker: string;
  marketCap: number;     // USD
  change: number;        // 前日比（%）
  sector: string;
  country: string;
  logo?: string;         // 企業ロゴURL
}
```

**カラム**:
| カラム名 | 幅 | ソート | 備考 |
|---|---|---|---|
| 順位 | 50px | ✓ | 変動矢印付き（↑↓） |
| 企業名 | 200px | ✓ | ロゴ+名前 |
| ティッカー | 80px | ✓ | クリックでTradingView表示 |
| 時価総額 | 150px | ✓ | 「$2.5T」形式 |
| 変動率 | 100px | ✓ | 色付き（赤/青） |
| セクター | 120px | ✓ | バッジ表示 |

**インタラクション**:
- 行クリック: 企業詳細モーダル表示
- ティッカークリック: TradingViewチャート埋め込み表示
- ヘッダークリック: ソート切り替え

##### 4. セクター別ヒートマップ
- **ライブラリ**: Recharts（Treemap）
- **データ**: 各セクターの時価総額合計と変動率
- **色**: 変動率に応じてグラデーション（赤=上昇、青=下落）
- **表示**: セクター名 + 変動率%

---

### 1.3 UI-005: 時価総額ランキング詳細画面

#### タブ構成
```
[ 世界 ] [ 米国 ] [ 欧州 ] [ 日本 ]
```

#### 各タブ内容
- TOP10テーブル（拡張版）
- 推移グラフ（過去7日間の順位変動）
- 変動理由の説明（AI分析結果）

#### 推移グラフ
- **ライブラリ**: Recharts（LineChart）
- **X軸**: 日付
- **Y軸**: 順位（逆順: 1位が上）
- **線**: 各企業ごとに色分け

---

### 1.4 UI-006: ニュースフィード

#### レイアウト
```
┌──────────────────────────────┐
│ フィルター                    │
│ [セクター▼] [センチメント▼]   │
└──────────────────────────────┘
┌──────────────────────────────┐
│ ニュースカード（無限スクロール） │
│ [Card] [Card] [Card] ...      │
└──────────────────────────────┘
```

#### 無限スクロール実装
- **ライブラリ**: `react-infinite-scroll-component`
- **初期読み込み**: 20件
- **追加読み込み**: スクロール末尾で10件ずつ

---

### 1.5 UI-007: 設定画面

#### セクション

##### 1. 通知設定
```typescript
interface NotificationSettings {
  channels: {
    line: boolean;
    email: boolean;
    slack: boolean;
  };
  frequency: 'immediate' | 'hourly' | 'daily';
  sectors: string[];      // 関心セクター
  mutedKeywords: string[]; // ミュートキーワード
  mutedAccounts: string[]; // ミュートアカウント
}
```

**UI要素**:
- トグルスイッチ（LINE / メール / Slack）
- ラジオボタン（配信頻度）
- マルチセレクト（セクター選択）
- タグ入力（キーワード・アカウント）

##### 2. LINE連携設定
- **LINE連携ボタン**: LINE Login OAuth 2.0
- **連携状態表示**: 「連携済み」 / 「未連携」
- **解除ボタン**: 連携解除

---

### 1.6 レスポンシブデザイン

#### ブレークポイント
```typescript
const breakpoints = {
  mobile: '640px',   // スマホ
  tablet: '768px',   // タブレット
  desktop: '1024px', // PC
};
```

#### モバイル対応
- **Sidebar**: ハンバーガーメニューで折りたたみ
- **テーブル**: カード表示に切り替え
- **グラフ**: 縦向きに最適化

---

### 1.7 ダークモード対応

```typescript
// Tailwind CSS設定
// tailwind.config.ts
darkMode: 'class', // クラスベース

// カラースキーム
colors: {
  background: 'hsl(var(--background))',
  foreground: 'hsl(var(--foreground))',
  // ... shadcn/ui標準カラー
}
```

---

## 2. API仕様

### 2.1 API設計方針

- **プロトコル**: tRPC（型安全なRPC）
- **認証**: JWT（HTTPヘッダー: `Authorization: Bearer <token>`）
- **エラー形式**: JSON
- **日時形式**: ISO 8601（例: `2026-01-05T10:30:00Z`）
- **通貨**: USD（米ドル）

---

### 2.2 エンドポイント一覧

#### 認証API

##### POST /api/auth/signup
**説明**: 新規ユーザー登録

**リクエスト**:
```typescript
interface SignUpRequest {
  email: string;      // メールアドレス
  password: string;   // パスワード（8文字以上）
  name: string;       // 表示名
}
```

**レスポンス**:
```typescript
interface SignUpResponse {
  user: {
    id: string;
    email: string;
    name: string;
  };
  token: string; // JWT
}
```

**エラー**:
- `400`: バリデーションエラー
- `409`: メールアドレス既に登録済み

---

##### POST /api/auth/signin
**説明**: ログイン

**リクエスト**:
```typescript
interface SignInRequest {
  email: string;
  password: string;
}
```

**レスポンス**:
```typescript
interface SignInResponse {
  user: {
    id: string;
    email: string;
    name: string;
  };
  token: string;
}
```

---

#### ニュースAPI

##### GET /api/news
**説明**: ニュースフィード取得

**クエリパラメータ**:
```typescript
interface NewsQuery {
  sector?: string;         // セクターフィルター
  sentiment?: 'positive' | 'negative' | 'neutral';
  priority?: 'high' | 'medium' | 'low';
  limit?: number;          // デフォルト: 20
  offset?: number;         // ページネーション
}
```

**レスポンス**:
```typescript
interface NewsResponse {
  news: NewsItem[];
  total: number;
  hasMore: boolean;
}

interface NewsItem {
  id: string;
  title: string;
  summary: string;         // AI要約（日本語）
  originalText: string;    // 原文（英語）
  source: {
    account: string;       // Twitterアカウント名
    platform: 'twitter' | 'news';
  };
  sentiment: 'positive' | 'negative' | 'neutral';
  priority: 'high' | 'medium' | 'low';
  sector: string;
  tickers: string[];       // 関連ティッカー
  publishedAt: string;     // ISO 8601
  originalUrl: string;
  notionUrl?: string;
}
```

---

##### GET /api/news/:id
**説明**: ニュース詳細取得

**レスポンス**:
```typescript
interface NewsDetailResponse {
  news: NewsItem;
  relatedNews: NewsItem[]; // 関連ニュース
  analysis: {
    reason: string;         // AI分析結果
    impact: string;         // 市場への影響
  };
}
```

---

#### 時価総額ランキングAPI

##### GET /api/marketcap/ranking
**説明**: 時価総額ランキング取得

**クエリパラメータ**:
```typescript
interface RankingQuery {
  region: 'global' | 'us' | 'europe' | 'japan';
  limit?: number; // デフォルト: 10
}
```

**レスポンス**:
```typescript
interface RankingResponse {
  rankings: MarketCapItem[];
  updatedAt: string;
}

interface MarketCapItem {
  rank: number;
  previousRank?: number;  // 前回順位（変動矢印用）
  company: {
    name: string;
    ticker: string;
    sector: string;
    country: string;
    logo?: string;
  };
  marketCap: number;      // USD
  marketCapLocal: number; // 現地通貨
  currency: string;       // 通貨コード
  change: {
    amount: number;       // 変動額
    percentage: number;   // 変動率
  };
  price: number;          // 株価
}
```

---

##### GET /api/marketcap/history
**説明**: ランキング推移取得

**クエリパラメータ**:
```typescript
interface HistoryQuery {
  region: 'global' | 'us' | 'europe' | 'japan';
  days?: number; // デフォルト: 7
}
```

**レスポンス**:
```typescript
interface HistoryResponse {
  history: {
    date: string;
    rankings: MarketCapItem[];
  }[];
}
```

---

#### 設定API

##### GET /api/settings
**説明**: ユーザー設定取得

**レスポンス**:
```typescript
interface SettingsResponse {
  notifications: {
    channels: {
      line: boolean;
      email: boolean;
      slack: boolean;
    };
    frequency: 'immediate' | 'hourly' | 'daily';
  };
  preferences: {
    sectors: string[];
    mutedKeywords: string[];
    mutedAccounts: string[];
  };
  integrations: {
    line?: {
      connected: boolean;
      userId?: string;
    };
    slack?: {
      connected: boolean;
      webhookUrl?: string;
    };
  };
}
```

---

##### PUT /api/settings
**説明**: ユーザー設定更新

**リクエスト**:
```typescript
interface UpdateSettingsRequest {
  notifications?: {
    channels?: {
      line?: boolean;
      email?: boolean;
      slack?: boolean;
    };
    frequency?: 'immediate' | 'hourly' | 'daily';
  };
  preferences?: {
    sectors?: string[];
    mutedKeywords?: string[];
    mutedAccounts?: string[];
  };
}
```

**レスポンス**:
```typescript
interface UpdateSettingsResponse {
  success: boolean;
  settings: SettingsResponse;
}
```

---

#### リアルタイム更新API

##### GET /api/sse/news
**説明**: Server-Sent Eventsによるニュースのリアルタイム配信

**レスポンス（ストリーム）**:
```
event: news
data: {"id":"123","title":"...","sentiment":"positive"}

event: news
data: {"id":"124","title":"...","sentiment":"negative"}
```

---

### 2.3 tRPC ルーター定義例

```typescript
// src/server/api/routers/news.ts
import { z } from 'zod';
import { createTRPCRouter, protectedProcedure } from '../trpc';

export const newsRouter = createTRPCRouter({
  getAll: protectedProcedure
    .input(
      z.object({
        sector: z.string().optional(),
        sentiment: z.enum(['positive', 'negative', 'neutral']).optional(),
        limit: z.number().min(1).max(100).default(20),
        offset: z.number().min(0).default(0),
      })
    )
    .query(async ({ ctx, input }) => {
      const news = await ctx.db.news.findMany({
        where: {
          sector: input.sector,
          sentiment: input.sentiment,
        },
        take: input.limit,
        skip: input.offset,
        orderBy: { publishedAt: 'desc' },
      });

      return {
        news,
        total: await ctx.db.news.count(),
        hasMore: (input.offset + input.limit) < total,
      };
    }),

  getById: protectedProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ ctx, input }) => {
      const news = await ctx.db.news.findUnique({
        where: { id: input.id },
        include: { relatedNews: true },
      });
      return news;
    }),
});
```

---

## 3. データベース仕様

### 3.1 データベース設計方針

- **RDBMS**: PostgreSQL 15
- **ORM**: Prisma 5.x
- **命名規則**: スネークケース（例: `user_id`）
- **主キー**: UUID v4
- **タイムスタンプ**: UTC

---

### 3.2 Prismaスキーマ

```prisma
// prisma/schema.prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// ユーザーテーブル
model User {
  id            String    @id @default(uuid())
  email         String    @unique
  name          String
  passwordHash  String
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt

  settings      UserSettings?
  lineIntegration LineIntegration?

  @@map("users")
}

// ユーザー設定テーブル
model UserSettings {
  id                String   @id @default(uuid())
  userId            String   @unique
  user              User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  // 通知設定
  notifyLine        Boolean  @default(false)
  notifyEmail       Boolean  @default(true)
  notifySlack       Boolean  @default(false)
  notifyFrequency   String   @default("hourly") // immediate, hourly, daily

  // 優先設定
  preferredSectors  String[] // JSON配列
  mutedKeywords     String[]
  mutedAccounts     String[]

  createdAt         DateTime @default(now())
  updatedAt         DateTime @updatedAt

  @@map("user_settings")
}

// LINE連携テーブル
model LineIntegration {
  id          String   @id @default(uuid())
  userId      String   @unique
  user        User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  lineUserId  String   @unique
  accessToken String   // 暗号化推奨
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  @@map("line_integrations")
}

// ニューステーブル
model News {
  id            String   @id @default(uuid())

  // メタデータ
  source        String   // Twitterアカウント名
  platform      String   // twitter, news
  publishedAt   DateTime

  // コンテンツ
  originalText  String   @db.Text  // 原文（英語）
  translatedText String  @db.Text  // 翻訳文（日本語）
  summary       String   // AI要約（3行程度）

  // 分析結果
  sentiment     String   // positive, negative, neutral
  priority      String   // high, medium, low
  sector        String
  tickers       String[] // 関連銘柄ティッカー

  // リンク
  originalUrl   String
  notionUrl     String?

  // 管理
  processed     Boolean  @default(false)
  createdAt     DateTime @default(now())
  updatedAt     DateTime @updatedAt

  @@index([publishedAt])
  @@index([sector])
  @@index([sentiment])
  @@map("news")
}

// 時価総額ランキングテーブル
model MarketCapRanking {
  id              String   @id @default(uuid())

  // 地域・時間
  region          String   // global, us, europe, japan
  snapshotAt      DateTime // スナップショット取得時刻

  // 企業情報
  rank            Int
  ticker          String
  companyName     String
  sector          String
  country         String

  // 時価総額
  marketCapUsd    Decimal  @db.Decimal(20, 2) // USD
  marketCapLocal  Decimal  @db.Decimal(20, 2) // 現地通貨
  currency        String   // USD, JPY, EUR

  // 株価・変動
  price           Decimal  @db.Decimal(10, 2)
  changeAmount    Decimal  @db.Decimal(10, 2)
  changePercent   Decimal  @db.Decimal(5, 2)

  // 前回順位（変動検出用）
  previousRank    Int?

  // 管理
  createdAt       DateTime @default(now())

  @@index([region, snapshotAt])
  @@index([ticker])
  @@map("market_cap_rankings")
}

// ランキング変動分析テーブル
model RankingChange {
  id            String   @id @default(uuid())

  ticker        String
  region        String
  oldRank       Int
  newRank       Int
  changeDate    DateTime

  // AI分析結果
  reason        String   @db.Text  // 変動理由
  newsReferences String[] // 参考ニュースID

  createdAt     DateTime @default(now())

  @@index([ticker, changeDate])
  @@map("ranking_changes")
}

// 配信ログテーブル
model NotificationLog {
  id          String   @id @default(uuid())
  userId      String
  newsId      String?
  channel     String   // line, email, slack
  status      String   // sent, failed
  sentAt      DateTime @default(now())
  errorMessage String?

  @@index([userId, sentAt])
  @@map("notification_logs")
}

// システムログテーブル
model SystemLog {
  id          String   @id @default(uuid())
  level       String   // info, warn, error
  service     String   // frontend, backend-python
  message     String   @db.Text
  metadata    Json?    // 追加情報（JSON）
  createdAt   DateTime @default(now())

  @@index([level, createdAt])
  @@map("system_logs")
}
```

---

### 3.3 インデックス戦略

| テーブル | カラム | 理由 |
|---|---|---|
| `news` | `publishedAt` | 時系列ソートの高速化 |
| `news` | `sector` | セクターフィルタの高速化 |
| `news` | `sentiment` | センチメントフィルタの高速化 |
| `market_cap_rankings` | `region, snapshotAt` | 地域別・時刻別取得の最適化 |
| `market_cap_rankings` | `ticker` | 銘柄検索の高速化 |
| `ranking_changes` | `ticker, changeDate` | 変動履歴検索の最適化 |

---

### 3.4 データ保持ポリシー

| テーブル | 保持期間 | 削除方法 |
|---|---|---|
| `news` | 90日間 | バッチ処理で自動削除 |
| `market_cap_rankings` | 1年間 | 月次で古いデータをアーカイブ |
| `ranking_changes` | 無期限 | - |
| `notification_logs` | 30日間 | バッチ処理で自動削除 |
| `system_logs` | 7日間 | バッチ処理で自動削除 |

---

## 4. 外部API連携仕様

### 4.1 Twitter API（X API）

**利用プラン**: Basic（月$100）
**レート制限**:
- ツイート取得: 300リクエスト/15分
- ユーザータイムライン: 500リクエスト/15分

**使用エンドポイント**:
```
GET /2/tweets/search/recent
GET /2/users/:id/tweets
```

**実装ライブラリ**: `tweepy`

**リトライロジック**:
- 429（レート制限）: 15分待機後リトライ
- 503（サーバーエラー）: exponential backoff（1秒、2秒、4秒）

---

### 4.2 Financial Modeling Prep API

**利用プラン**: Professional（月$249）
**レート制限**: 500リクエスト/分

**使用エンドポイント**:
```
GET /api/v3/stock-screener
GET /api/v3/quote/{ticker}
GET /api/v3/historical-market-capitalization/{ticker}
```

**認証**: APIキーをクエリパラメータに付与
```
https://financialmodelingprep.com/api/v3/quote/AAPL?apikey=YOUR_API_KEY
```

---

### 4.3 Alpha Vantage API

**利用プラン**: Premium（月$49.99）
**レート制限**: 75リクエスト/分

**使用エンドポイント**:
```
GET /query?function=CURRENCY_EXCHANGE_RATE
GET /query?function=GLOBAL_QUOTE
```

**MCP統合**: Alpha Vantage公式MCPサーバー利用

---

### 4.4 LINE Messaging API

**認証**: Channel Access Token（長期トークン）

**使用API**:
```
POST https://api.line.me/v2/bot/message/push
```

**Flex Message例**:
```json
{
  "type": "flex",
  "altText": "重要なニュース",
  "contents": {
    "type": "bubble",
    "header": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "🚀 強気ニュース",
          "color": "#FF0000",
          "weight": "bold"
        }
      ]
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "エヌビディアが史上最高値を更新",
          "weight": "bold",
          "size": "lg"
        },
        {
          "type": "text",
          "text": "AI需要の急増により...",
          "size": "sm",
          "color": "#999999",
          "wrap": true
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "詳細を見る",
            "uri": "https://notion.so/abc123"
          }
        }
      ]
    }
  }
}
```

---

## 5. 認証・認可仕様

### 5.1 認証フロー

#### サインアップ
```
1. ユーザーがメールアドレス・パスワード入力
2. バックエンドがパスワードをbcryptでハッシュ化
3. DBにユーザー登録
4. JWTトークン生成・返却
5. フロントエンドがトークンをlocalStorageに保存
```

#### ログイン
```
1. ユーザーがメールアドレス・パスワード入力
2. バックエンドがパスワードを検証
3. JWTトークン生成・返却
4. フロントエンドがトークンをlocalStorageに保存
```

### 5.2 JWT構造

```typescript
interface JWTPayload {
  sub: string;      // ユーザーID
  email: string;
  iat: number;      // 発行時刻
  exp: number;      // 有効期限（24時間）
}
```

**署名アルゴリズム**: HS256
**秘密鍵**: 環境変数 `JWT_SECRET` から取得

### 5.3 認可制御

- **公開ページ**: `/`, `/auth/*`
- **認証必須**: `/dashboard/*`, `/api/*`（一部を除く）

**Next.js Middleware**:
```typescript
// src/middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { verifyJWT } from '@/lib/auth';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value;

  if (!token) {
    return NextResponse.redirect(new URL('/auth/signin', request.url));
  }

  try {
    verifyJWT(token);
    return NextResponse.next();
  } catch {
    return NextResponse.redirect(new URL('/auth/signin', request.url));
  }
}

export const config = {
  matcher: ['/dashboard/:path*'],
};
```

---

## 6. エラーハンドリング仕様

### 6.1 エラーレスポンス形式

```typescript
interface ErrorResponse {
  error: {
    code: string;      // エラーコード
    message: string;   // ユーザー向けメッセージ
    details?: any;     // 詳細情報（開発時のみ）
  };
}
```

### 6.2 エラーコード一覧

| コード | HTTPステータス | 説明 |
|---|---|---|
| `AUTH_INVALID_CREDENTIALS` | 401 | メールアドレスまたはパスワードが間違っています |
| `AUTH_TOKEN_EXPIRED` | 401 | トークンの有効期限が切れました |
| `AUTH_UNAUTHORIZED` | 403 | 権限がありません |
| `VALIDATION_ERROR` | 400 | 入力値が不正です |
| `RESOURCE_NOT_FOUND` | 404 | リソースが見つかりません |
| `RATE_LIMIT_EXCEEDED` | 429 | リクエスト制限を超えました |
| `EXTERNAL_API_ERROR` | 502 | 外部APIとの通信に失敗しました |
| `INTERNAL_SERVER_ERROR` | 500 | サーバーエラーが発生しました |

### 6.3 エラーハンドリング実装例

```typescript
// tRPC エラーハンドリング
import { TRPCError } from '@trpc/server';

export const exampleProcedure = protectedProcedure
  .input(z.object({ id: z.string() }))
  .query(async ({ ctx, input }) => {
    try {
      const data = await ctx.db.news.findUnique({
        where: { id: input.id },
      });

      if (!data) {
        throw new TRPCError({
          code: 'NOT_FOUND',
          message: '指定されたニュースが見つかりません',
        });
      }

      return data;
    } catch (error) {
      if (error instanceof TRPCError) throw error;

      // 予期しないエラー
      throw new TRPCError({
        code: 'INTERNAL_SERVER_ERROR',
        message: 'サーバーエラーが発生しました',
        cause: error,
      });
    }
  });
```

---

**作成日**: 2026年1月5日
**次回更新予定**: 実装開始時に詳細を追記
