# セットアップガイド
## Financial Intelligence System - 環境構築完全ガイド

このガイドでは、ローカル開発環境の構築から本番デプロイまでを順を追って説明します。

---

## 目次

1. [システム要件](#1-システム要件)
2. [事前準備](#2-事前準備)
3. [ローカル環境構築](#3-ローカル環境構築)
4. [APIキー取得](#4-apiキー取得)
5. [動作確認](#5-動作確認)
6. [よくある質問](#6-よくある質問)

---

## 1. システム要件

### ハードウェア要件
- **CPU**: 2コア以上
- **メモリ**: 8GB以上
- **ストレージ**: 10GB以上の空き容量

### ソフトウェア要件
- **OS**: macOS / Windows 10+ / Linux (Ubuntu 20.04+)
- **Node.js**: 20.x LTS
- **Python**: 3.11.x
- **Docker Desktop**: 最新版
- **Git**: 2.30+

---

## 2. 事前準備

### 2.1 Node.jsのインストール

#### macOS (Homebrew)
```bash
brew install node@20
```

#### Windows (Installer)
https://nodejs.org/ から LTS版をダウンロード

#### バージョン確認
```bash
node -v  # v20.x.x
npm -v   # 10.x.x
```

---

### 2.2 Pythonのインストール

#### macOS (Homebrew)
```bash
brew install python@3.11
```

#### Windows (Installer)
https://www.python.org/ から 3.11.x をダウンロード

#### バージョン確認
```bash
python --version  # Python 3.11.x
pip --version
```

---

### 2.3 Docker Desktopのインストール

https://www.docker.com/products/docker-desktop からダウンロードしてインストール

#### 動作確認
```bash
docker --version
docker-compose --version
```

---

## 3. ローカル環境構築

### 3.1 リポジトリのクローン

```bash
# HTTPSの場合
git clone --recurse-submodules https://github.com/asuka8888/02_seminar.git

# SSHの場合
git clone --recurse-submodules git@github.com:asuka8888/02_seminar.git

cd 02_seminar
```

---

### 3.2 データベースの起動

```bash
# PostgreSQL + Redis を起動
docker-compose up -d

# 起動確認
docker ps
# fin-intel-postgres, fin-intel-redis, fin-intel-pgadmin が表示されればOK

# ログ確認
docker logs fin-intel-postgres
```

**接続情報**:
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`
- pgAdmin: `http://localhost:5050`

---

### 3.3 フロントエンドのセットアップ

```bash
cd frontend

# 依存関係のインストール (初回のみ時間がかかります)
npm install

# 環境変数ファイルの作成
cp .env.example .env.local

# .env.local を編集
nano .env.local
# または VSCode: code .env.local
```

**`.env.local` の内容**:
```env
DATABASE_URL="postgresql://finuser:finpass123@localhost:5432/fin_intel"
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="your-secret-key-change-this"  # ← ランダムな文字列に変更
NEXT_PUBLIC_BACKEND_URL="http://localhost:8000"
```

#### Prisma のセットアップ

```bash
# Prisma Clientの生成
npx prisma generate

# データベースマイグレーション
npx prisma migrate dev --name init

# (オプション) Prisma Studio でDBを確認
npx prisma studio
# http://localhost:5555 で開く
```

#### 開発サーバーの起動

```bash
npm run dev
```

http://localhost:3000 でフロントエンドが起動します。

---

### 3.4 バックエンドのセットアップ

新しいターミナルを開いて:

```bash
cd backend

# 仮想環境の作成
python -m venv .venv

# 仮想環境の有効化
# macOS / Linux:
source .venv/bin/activate

# Windows (Command Prompt):
.venv\Scripts\activate.bat

# Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

#### 依存関係のインストール

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 環境変数の設定

```bash
cp .env.example .env
nano .env  # または code .env
```

**`.env` の最小構成** (まずはこれで起動確認):
```env
APP_NAME="Financial Intelligence System"
ENVIRONMENT="development"
DATABASE_URL="postgresql://finuser:finpass123@localhost:5432/fin_intel"
REDIS_URL="redis://localhost:6379"

# 以下は後で取得したAPIキーを設定
ANTHROPIC_API_KEY=""
TWITTER_BEARER_TOKEN=""
LINE_CHANNEL_ACCESS_TOKEN=""
```

#### 開発サーバーの起動

```bash
python src/main.py
```

http://localhost:8000 でバックエンドAPIが起動します。

APIドキュメント: http://localhost:8000/docs

---

## 4. APIキー取得

### 4.1 Anthropic API Key (必須)

1. https://console.anthropic.com/ にアクセス
2. アカウント作成 (GitHubまたはメールで登録)
3. "API Keys" → "Create Key"
4. 生成されたキーを `.env` の `ANTHROPIC_API_KEY` に設定

```env
ANTHROPIC_API_KEY="sk-ant-api03-xxxxxxxxxx..."
```

---

### 4.2 Twitter API v2 Bearer Token (必須)

1. https://developer.twitter.com/en/portal/dashboard にアクセス
2. アカウント作成・申請 (数時間〜1日で承認)
3. "Project & Apps" → "Create Project"
4. "Keys and Tokens" → "Bearer Token" を生成
5. `.env` に設定

```env
TWITTER_BEARER_TOKEN="AAAAAAAAAAAAAAAAAAAAAxxxxxxxx..."
```

**注意**: 無料プランでは月間制限があります。

---

### 4.3 LINE Messaging API (必須)

1. https://developers.line.biz/console/ にアクセス
2. "Create Provider" → "Create Channel" (Messaging API)
3. "Messaging API" タブ → "Channel access token (long-lived)"
4. `.env` に設定

```env
LINE_CHANNEL_ACCESS_TOKEN="xxxxxxxxxxxxxxxxxxxxxxxxx..."
```

---

### 4.4 Financial Modeling Prep (オプション)

1. https://financialmodelingprep.com/developer/docs/ にアクセス
2. "Get Free API Key"
3. `.env` に設定

```env
FMP_API_KEY="your-fmp-api-key"
```

---

### 4.5 Alpha Vantage (オプション)

1. https://www.alphavantage.co/support/#api-key にアクセス
2. "Get Your Free API Key Today"
3. `.env` に設定

```env
ALPHA_VANTAGE_API_KEY="your-alpha-vantage-key"
```

---

## 5. 動作確認

### 5.1 ヘルスチェック

#### フロントエンド
```bash
curl http://localhost:3000
# ページが表示されればOK
```

#### バックエンド
```bash
curl http://localhost:8000/health
# {"status":"healthy",...} が返ればOK
```

---

### 5.2 データベース接続確認

```bash
cd frontend
npx prisma studio
```

http://localhost:5555 でデータベースが確認できればOK

---

### 5.3 エンドツーエンドテスト

1. ブラウザで http://localhost:3000 を開く
2. ダッシュボードが表示される
3. バックエンドAPIとの通信が正常

---

## 6. よくある質問

### Q1: `npm install` が失敗する

**A**: Node.jsのバージョンを確認してください。
```bash
node -v  # v20.x.x であることを確認
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

---

### Q2: PostgreSQLに接続できない

**A**: Dockerが起動しているか確認してください。
```bash
docker ps
# fin-intel-postgres が表示されない場合:
docker-compose up -d postgres
```

---

### Q3: Prisma マイグレーションが失敗する

**A**: データベースをリセットしてみてください（開発環境のみ）。
```bash
npx prisma migrate reset
npx prisma migrate dev --name init
```

---

### Q4: Pythonパッケージのインストールが失敗する

**A**: 仮想環境を再作成してください。
```bash
deactivate  # 仮想環境を無効化
rm -rf .venv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Q5: ポートがすでに使用されている

**A**: 別のプロセスがポートを使用している可能性があります。

#### macOS / Linux
```bash
# ポート3000を使用しているプロセスを確認
lsof -i :3000
# プロセスを終了
kill -9 <PID>
```

#### Windows
```bash
# ポート3000を使用しているプロセスを確認
netstat -ano | findstr :3000
# プロセスを終了
taskkill /PID <PID> /F
```

---

## 次のステップ

セットアップが完了したら:

1. **機能開発**: `05_実行計画書.md` の Week 1 タスクを開始
2. **ドキュメント確認**: `06_技術要件書.md` で詳細な技術仕様を確認
3. **Issue確認**: GitHub Issue #190 で進捗を追跡

---

**作成日**: 2026年1月5日
**最終更新**: 2026年1月5日
