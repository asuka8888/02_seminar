# データベースセットアップガイド

## 📋 目次

1. [概要](#概要)
2. [システム要件](#システム要件)
3. [PostgreSQL のセットアップ](#postgresql-のセットアップ)
4. [Prisma Client Python のセットアップ](#prisma-client-python-のセットアップ)
5. [データベーススキーマ](#データベーススキーマ)
6. [使用方法](#使用方法)
7. [トラブルシューティング](#トラブルシューティング)

---

## 概要

このガイドでは、Twitter/X スクレイピングシステムのデータベース（PostgreSQL）をセットアップし、Prisma Client Python を使用してデータを保存する方法を説明します。

### 技術スタック

- **データベース**: PostgreSQL 15
- **ORM**: Prisma Client Python
- **Python バージョン**: 3.11+

---

## システム要件

### 必須ソフトウェア

- PostgreSQL 15 以上
- Python 3.11 以上
- Node.js 20 以上（Prisma CLI 用）
- npm または yarn

---

## PostgreSQL のセットアップ

### macOS（Homebrew）

```bash
# PostgreSQL のインストール
brew install postgresql@15

# PostgreSQL の起動
brew services start postgresql@15

# データベースとユーザーの作成
createdb fin_intel
psql postgres -c "CREATE USER finuser WITH PASSWORD 'finpass123';"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE fin_intel TO finuser;"
```

### Docker（推奨）

```bash
# Docker Compose で起動
cd /path/to/02_seminar
docker-compose up -d postgres

# 接続確認
docker exec -it 02_seminar-postgres-1 psql -U finuser -d fin_intel
```

### Linux（Ubuntu/Debian）

```bash
# PostgreSQL のインストール
sudo apt update
sudo apt install postgresql postgresql-contrib

# PostgreSQL の起動
sudo systemctl start postgresql
sudo systemctl enable postgresql

# データベースとユーザーの作成
sudo -u postgres psql
  CREATE DATABASE fin_intel;
  CREATE USER finuser WITH PASSWORD 'finpass123';
  GRANT ALL PRIVILEGES ON DATABASE fin_intel TO finuser;
  \q
```

### Windows

1. [公式サイト](https://www.postgresql.org/download/windows/) からインストーラーをダウンロード
2. インストール時に以下を設定:
   - データベース名: `fin_intel`
   - ユーザー名: `finuser`
   - パスワード: `finpass123`
   - ポート: `5432`

---

## Prisma Client Python のセットアップ

### 1. 環境変数の設定

```bash
cd backend
cp .env.example .env
```

`.env` ファイルを編集:

```env
# Database
DATABASE_URL=postgresql://finuser:finpass123@localhost:5432/fin_intel

# Docker を使用する場合
# DATABASE_URL=postgresql://finuser:finpass123@localhost:5432/fin_intel

# リモートデータベースの場合
# DATABASE_URL=postgresql://user:password@hostname:5432/dbname
```

### 2. Prisma Client Python のインストール

```bash
# 依存関係をインストール
pip install -r requirements.txt

# または個別にインストール
pip install prisma
```

### 3. Prisma Client の生成

```bash
# schema.prisma から Python コードを生成
prisma generate --schema=schema.prisma
```

### 4. データベーススキーマの作成

```bash
# Prisma CLI (Node.js) を使用してスキーマをプッシュ
npx prisma db push --schema=schema.prisma --skip-generate
```

### 5. 自動セットアップスクリプト（推奨）

```bash
# ワンコマンドでセットアップ
chmod +x db_setup.sh
./db_setup.sh
```

このスクリプトは以下を自動実行します:
- 環境変数の確認
- Prisma Client Python のインストール
- Prisma Client の生成
- データベースマイグレーション
- 接続テスト

---

## データベーススキーマ

### News テーブル（ニュース）

| カラム名 | 型 | 説明 |
|---------|-----|------|
| id | String (UUID) | 主キー |
| source | String | ソースアカウント名（例: @elonmusk） |
| platform | String | プラットフォーム（twitter, news） |
| publishedAt | DateTime | 公開日時 |
| originalText | Text | 原文 |
| translatedText | Text | 翻訳文（英語→日本語） |
| summary | String | AI要約 |
| sentiment | String | センチメント（positive/negative/neutral） |
| sentimentScore | Float | センチメントスコア（-1.0〜1.0） |
| priority | String | 優先度（high/medium/low） |
| sector | String | セクター |
| tickers | String[] | 関連銘柄ティッカー |
| keyTopics | String[] | キートピック |
| likes | Int | いいね数 |
| retweets | Int | リツイート数 |
| replies | Int | 返信数 |
| originalUrl | String | 元URL |
| category | String | カテゴリ |
| language | String | 言語（ja/en） |
| processed | Boolean | 処理済みフラグ |
| createdAt | DateTime | 作成日時 |
| updatedAt | DateTime | 更新日時 |

### その他のテーブル

- **User**: ユーザー情報
- **UserSettings**: ユーザー設定
- **LineIntegration**: LINE連携情報
- **MarketCapRanking**: 時価総額ランキング
- **RankingChange**: ランキング変動
- **NotificationLog**: 通知ログ

詳細は `backend/schema.prisma` を参照してください。

---

## 使用方法

### 基本的な CRUD 操作

#### 1. データベース接続

```python
from database import db_manager
import asyncio

async def main():
    # 接続
    await db_manager.connect()

    # 処理...

    # 切断
    await db_manager.disconnect()

asyncio.run(main())
```

#### 2. ニュースの作成

```python
from datetime import datetime

news = await db_manager.client.news.create(
    data={
        'source': '@elonmusk',
        'platform': 'twitter',
        'publishedAt': datetime.now(),
        'originalText': 'Tesla stock is up 10% today!',
        'translatedText': 'テスラ株が今日10%上昇！',
        'summary': 'テスラ株の急騰に関するニュース',
        'sentiment': 'positive',
        'sentimentScore': 0.85,
        'priority': 'high',
        'sector': 'technology',
        'tickers': ['TSLA'],
        'keyTopics': ['Tesla', 'stocks', 'EV'],
        'likes': 1500,
        'retweets': 800,
        'replies': 200,
        'originalUrl': 'https://x.com/elonmusk/status/1234567890',
        'category': 'us_tech_crypto',
        'language': 'en',
        'processed': True
    }
)

print(f"Created news: {news.id}")
```

#### 3. ニュースの検索

```python
# 全件取得（最新10件）
recent_news = await db_manager.client.news.find_many(
    take=10,
    order={'publishedAt': 'desc'}
)

# 高インパクトニュースのみ
high_impact = await db_manager.client.news.find_many(
    where={'priority': 'high'},
    order={'publishedAt': 'desc'}
)

# 特定のソースのニュース
elon_tweets = await db_manager.client.news.find_many(
    where={'source': '@elonmusk'},
    take=20
)

# センチメントでフィルタ
positive_news = await db_manager.client.news.find_many(
    where={'sentiment': 'positive'},
    take=50
)
```

#### 4. ニュースの更新

```python
updated = await db_manager.client.news.update(
    where={'id': news_id},
    data={'processed': True}
)
```

#### 5. ニュースの削除

```python
# 1件削除
await db_manager.client.news.delete(
    where={'id': news_id}
)

# 複数削除
await db_manager.client.news.delete_many(
    where={'source': 'test_account'}
)
```

#### 6. 件数のカウント

```python
# 全件数
total = await db_manager.client.news.count()

# 条件付き
high_impact_count = await db_manager.client.news.count(
    where={'priority': 'high'}
)
```

### スクレイパーとの統合

スクレイパーシステムは自動的にデータベースに保存します:

```bash
# データベース保存を有効にして実行
cd backend/src
python main_scraper_pipeline.py
```

実装コード（`main_scraper_pipeline.py`）:

```python
async def _save_to_database(self, processed: ProcessedTweet):
    """処理済みツイートをデータベースに保存"""

    # 重複チェック
    existing = await db_manager.client.news.find_first(
        where={'originalUrl': tweet.url}
    )

    if existing:
        logger.debug(f"Tweet already exists, skipping")
        return

    # News レコードを作成
    news = await db_manager.client.news.create(data={...})

    logger.info(f"✓ Saved tweet to database")
```

---

## テスト

### データベース接続テスト

```bash
# 接続テスト
python src/database/db_manager.py

# 出力例:
# ================================================================================
# Database Connection Test
# ================================================================================
# DATABASE_URL: postgresql://finuser:finpass123@localhost:5432/fin_intel
# ✓ Connection successful
# ✓ Health check: OK
#
# Database Statistics:
#   - total_news: 0
#   - news_today: 0
#   - high_impact_news: 0
#   - processed_news: 0
#
# ✓ Test completed successfully
```

### CRUD テスト

```bash
# 完全なCRUDテスト
python src/database/test_database.py

# 出力例:
# ================================================================================
# Test 1: Create News Record
# ================================================================================
# ✓ Created news record:
#   ID: 550e8400-e29b-41d4-a716-446655440000
#   Source: test_account
#   Sentiment: positive (0.8)
#   Priority: medium
#   Key Topics: ['AI', 'stocks', 'market']
#
# ================================================================================
# Test 2: Find News Records
# ================================================================================
# ✓ Found 1 news records:
#   1. test_account (2026-01-08 15:30)
#      テスト用のニュースサマリー...
#      Sentiment: positive, Priority: medium
# ...
```

---

## Prisma Studio（データベースGUI）

Prisma Studio を使ってブラウザでデータベースを視覚的に管理できます:

```bash
# Prisma Studio を起動
npx prisma studio --schema=schema.prisma

# ブラウザで http://localhost:5555 が開きます
```

Prisma Studio でできること:
- テーブルのレコードを閲覧
- レコードの作成・編集・削除
- フィルタリング・ソート
- リレーションの表示

---

## トラブルシューティング

### 1. DATABASE_URL が設定されていない

**症状:**
```
❌ DATABASE_URL environment variable not set
```

**解決策:**
```bash
# .env ファイルを作成
cp .env.example .env

# .env を編集して DATABASE_URL を設定
DATABASE_URL=postgresql://finuser:finpass123@localhost:5432/fin_intel
```

### 2. データベースに接続できない

**症状:**
```
Failed to connect to database: connection refused
```

**解決策:**

**PostgreSQL が起動しているか確認:**
```bash
# macOS
brew services list | grep postgresql

# Linux
sudo systemctl status postgresql

# Docker
docker ps | grep postgres
```

**ポートが正しいか確認:**
```bash
# PostgreSQL のポートを確認
lsof -i :5432
```

### 3. Prisma Client が生成されていない

**症状:**
```
ImportError: cannot import name 'Prisma' from 'prisma'
```

**解決策:**
```bash
# Prisma Client を生成
prisma generate --schema=schema.prisma
```

### 4. データベーススキーマが存在しない

**症状:**
```
relation "news" does not exist
```

**解決策:**
```bash
# スキーマをプッシュ
npx prisma db push --schema=schema.prisma
```

### 5. マイグレーションエラー

**症状:**
```
Error: P3009: migrate found failed migrations
```

**解決策:**
```bash
# データベースをリセット（注意: 全データが削除されます）
npx prisma db push --schema=schema.prisma --force-reset

# または手動でテーブルを削除
psql -U finuser -d fin_intel -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

### 6. 接続プールの枯渇

**症状:**
```
Error: Too many connections
```

**解決策:**
```python
# 必ず disconnect() を呼ぶ
try:
    await db_manager.connect()
    # 処理...
finally:
    await db_manager.disconnect()

# または context manager を使用
async with db_manager.session():
    # 処理...
```

---

## パフォーマンス最適化

### 1. インデックスの活用

`schema.prisma` でインデックスが定義されています:

```prisma
model News {
  // ...

  @@index([publishedAt])
  @@index([sector])
  @@index([sentiment])
  @@index([priority])
  @@index([source])
}
```

### 2. バッチ挿入

大量のレコードを挿入する場合は `create_many` を使用:

```python
await db_manager.client.news.create_many(
    data=[
        {...},  # News 1
        {...},  # News 2
        {...},  # News 3
    ],
    skip_duplicates=True
)
```

### 3. 選択的フィールド取得

必要なフィールドのみを取得:

```python
news = await db_manager.client.news.find_many(
    select={
        'id': True,
        'source': True,
        'summary': True,
        'sentiment': True
    }
)
```

---

## 次のステップ

1. ✅ データベースセットアップ完了
2. ⏳ フロントエンド（Next.js）との連携
3. ⏳ LINE 通知システムの実装
4. ⏳ 本番環境へのデプロイ

---

## 関連ドキュメント

- [SCRAPING_SETUP_GUIDE.md](SCRAPING_SETUP_GUIDE.md) - スクレイピングシステムのセットアップ
- [backend/SCRAPER_README.md](backend/SCRAPER_README.md) - スクレイパーの詳細
- [backend/schema.prisma](backend/schema.prisma) - Prisma スキーマ定義

---

## サポート

問題が発生した場合:

1. GitHub Issues: https://github.com/asuka8888/02_seminar/issues
2. Prisma ドキュメント: https://prisma-client-py.readthedocs.io/
3. PostgreSQL ドキュメント: https://www.postgresql.org/docs/
