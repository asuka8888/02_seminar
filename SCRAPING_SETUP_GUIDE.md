# Twitter/X スクレイピングシステム セットアップガイド

## 📋 目次

1. [システム要件](#システム要件)
2. [セットアップ手順](#セットアップ手順)
3. [Ollama モデルのインストール](#ollama-モデルのインストール)
4. [プロキシ設定（オプション）](#プロキシ設定オプション)
5. [実行方法](#実行方法)
6. [トラブルシューティング](#トラブルシューティング)

---

## システム要件

### ハードウェア要件

**最小要件（Gemma 2 9B のみ使用）**
- CPU: 4コア以上
- RAM: 16GB
- ストレージ: 20GB 空き容量

**推奨要件（Qwen2.5 32B + Gemma 2 9B）**
- CPU: 8コア以上
- RAM: 32GB
- GPU: NVIDIA RTX 4080 (16GB VRAM) 以上
- ストレージ: 50GB 空き容量

**クラウド代替案**
- RunPod: RTX 4090 レンタル（$0.69/時間 = $500/月）
- Vast.ai: RTX 4080 レンタル（$0.30/時間 = $216/月）
- Google Cloud: A100 40GB（$300/月）

### ソフトウェア要件

- Python 3.11 以上
- Node.js 20 以上
- PostgreSQL 15
- Redis 7
- Docker & Docker Compose（推奨）
- Ollama（ローカルAIモデル実行）

---

## セットアップ手順

### 1. リポジトリのクローン

```bash
cd /path/to/your/workspace
git clone https://github.com/asuka8888/02_seminar.git
cd 02_seminar
```

### 2. バックエンド環境構築

```bash
cd backend

# Python 仮想環境を作成
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係をインストール
pip install -r requirements.txt

# Playwright ブラウザをインストール
playwright install chromium
```

### 3. Ollama のインストール

#### macOS / Linux

```bash
# Ollama インストール
curl -fsSL https://ollama.com/install.sh | sh

# Ollama サービス起動
ollama serve
```

#### Windows

1. https://ollama.com/download/windows からインストーラーをダウンロード
2. インストール後、自動的にサービスが起動

### 4. 必要なモデルをダウンロード

```bash
# メインモデル（翻訳・詳細分析用）- 20GB
ollama pull qwen2.5:32b

# 高速モデル（センチメント分析用）- 5.4GB
ollama pull gemma2:9b
```

ダウンロードには時間がかかる場合があります（回線速度による）。

### 5. データベースセットアップ

#### Docker Compose で起動（推奨）

```bash
cd ..  # プロジェクトルートに戻る
docker-compose up -d postgres redis
```

#### 手動セットアップ

**PostgreSQL**
```bash
# PostgreSQL インストール（macOS）
brew install postgresql@15
brew services start postgresql@15

# データベース作成
createdb fin_intel
```

**Redis**
```bash
# Redis インストール（macOS）
brew install redis
brew services start redis
```

### 6. 環境変数の設定

```bash
cd backend
cp .env.example .env
```

`.env` ファイルを編集：

```env
# Database
DATABASE_URL=postgresql://finuser:finpass123@localhost:5432/fin_intel
REDIS_URL=redis://localhost:6379

# Ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MAIN_MODEL=qwen2.5:32b
OLLAMA_FAST_MODEL=gemma2:9b

# Proxy (オプション)
ENABLE_PROXY=false
PROXY_SERVER=
PROXY_USERNAME=
PROXY_PASSWORD=

# Notification (オプション)
LINE_NOTIFY_TOKEN=
EMAIL_SMTP_HOST=
EMAIL_SMTP_PORT=587
EMAIL_FROM=
EMAIL_PASSWORD=

# Runtime
RUN_MODE=once  # once または continuous
```

---

## Ollama モデルのインストール

### 推奨モデル構成

| モデル | 用途 | サイズ | RAM要件 | 速度 | 精度 |
|--------|------|--------|---------|------|------|
| **Qwen2.5 32B** | メイン（翻訳・分析） | 20GB | 32GB | 遅い | 最高 |
| **Gemma 2 9B** | センチメント分析 | 5.4GB | 16GB | 高速 | 高い |

### インストール確認

```bash
# インストール済みモデルを確認
ollama list

# 出力例:
# NAME              ID              SIZE      MODIFIED
# qwen2.5:32b       abc123...       20 GB     2 hours ago
# gemma2:9b         def456...       5.4 GB    2 hours ago

# モデルのテスト実行
ollama run qwen2.5:32b "こんにちは"
```

### GPU 利用確認

```bash
# Ollama が GPU を使用しているか確認
ollama ps

# GPU使用状況を確認（NVIDIA）
nvidia-smi
```

---

## プロキシ設定（オプション）

アカウント凍結リスクをさらに低減するには、プロキシサービスの利用を推奨します。

### 推奨プロキシサービス

| サービス | タイプ | 料金 | 推奨度 |
|----------|--------|------|--------|
| **Smartproxy** | Residential | $75/月〜 | ⭐⭐⭐⭐⭐ |
| **Bright Data** | Residential | $500/月〜 | ⭐⭐⭐⭐ |
| **Oxylabs** | Mixed | $300/月〜 | ⭐⭐⭐⭐ |
| **ProxyMesh** | Datacenter | $10/月〜 | ⭐⭐⭐ |

### プロキシ設定方法

1. プロキシサービスに登録
2. `.env` ファイルを編集：

```env
ENABLE_PROXY=true
PROXY_SERVER=http://gate.smartproxy.com:7000
PROXY_USERNAME=your_username
PROXY_PASSWORD=your_password
```

3. 複数プロキシを設定する場合は、`proxy_configs.json` を作成：

```json
[
  {
    "server": "http://proxy1.example.com:8080",
    "username": "user1",
    "password": "pass1",
    "country": "JP",
    "residential": true
  },
  {
    "server": "http://proxy2.example.com:8080",
    "username": "user2",
    "password": "pass2",
    "country": "US",
    "residential": true
  }
]
```

---

## 実行方法

### 1. テスト実行（1アカウントのみ）

```bash
cd backend/src/scraper

# Playwright スクレイパーのテスト
python twitter_playwright.py
```

### 2. AI 分析のテスト

```bash
cd backend/src/agents

# Ollama 分析のテスト
python local_ai_analyzer.py
```

### 3. 1サイクル実行（24時間で91アカウント）

```bash
cd backend/src

# 環境変数設定
export RUN_MODE=once

# 実行
python main_scraper_pipeline.py
```

### 4. 連続実行（7日間）

```bash
cd backend/src

# 環境変数設定
export RUN_MODE=continuous

# 実行
python main_scraper_pipeline.py
```

### 5. バックグラウンド実行（推奨）

```bash
cd backend/src

# nohup で実行
nohup python main_scraper_pipeline.py > scraper.log 2>&1 &

# ログ確認
tail -f scraper.log
```

### 6. systemd サービスとして実行（Linux）

`/etc/systemd/system/twitter-scraper.service` を作成：

```ini
[Unit]
Description=Twitter Scraper Service
After=network.target postgresql.service redis.service ollama.service

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/02_seminar/backend/src
Environment="PATH=/path/to/venv/bin"
Environment="RUN_MODE=continuous"
ExecStart=/path/to/venv/bin/python main_scraper_pipeline.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

有効化：

```bash
sudo systemctl daemon-reload
sudo systemctl enable twitter-scraper
sudo systemctl start twitter-scraper
sudo systemctl status twitter-scraper
```

---

## トラブルシューティング

### 1. Ollama に接続できない

**症状:**
```
Failed to connect to Ollama server
```

**解決策:**
```bash
# Ollama サービスが起動しているか確認
ps aux | grep ollama

# 起動していない場合
ollama serve

# ポート確認
lsof -i :11434
```

### 2. モデルが見つからない

**症状:**
```
Main model 'qwen2.5:32b' not found
```

**解決策:**
```bash
# モデルを再ダウンロード
ollama pull qwen2.5:32b
ollama pull gemma2:9b

# インストール確認
ollama list
```

### 3. メモリ不足エラー

**症状:**
```
RuntimeError: CUDA out of memory
```

**解決策:**

**オプション1: 軽量モデルに変更**
```env
# .env ファイル
OLLAMA_MAIN_MODEL=qwen2.5:14b  # 32bの代わりに14b
```

**オプション2: GPU メモリを増やす**
```bash
# モデルの量子化（4bit）
ollama pull qwen2.5:32b-q4_0

# .env ファイル
OLLAMA_MAIN_MODEL=qwen2.5:32b-q4_0
```

### 4. Playwright ブラウザが起動しない

**症状:**
```
playwright._impl._api_types.Error: Executable doesn't exist
```

**解決策:**
```bash
# ブラウザを再インストール
playwright install chromium

# システム依存関係をインストール（Linux）
playwright install-deps chromium
```

### 5. Twitter でブロックされる

**症状:**
- アカウントが一時的にロックされる
- "Automated behavior detected" エラー

**解決策:**

1. **プロキシを有効化**
   ```env
   ENABLE_PROXY=true
   ```

2. **スクレイピング間隔を延長**
   - `scheduler.py` の `random_delay` を増やす：
   ```python
   random_delay = random.uniform(1200, 2400)  # 20-40分
   ```

3. **ヘッドレスモードを無効化（テスト時）**
   ```python
   scraper = TwitterPlaywrightScraper(headless=False)
   ```

4. **アカウントを分散**
   - 複数のXアカウントでスクレイピングを分散

### 6. データベース接続エラー

**症状:**
```
asyncpg.exceptions.InvalidCatalogNameError: database "fin_intel" does not exist
```

**解決策:**
```bash
# PostgreSQL に接続
psql postgres

# データベース作成
CREATE DATABASE fin_intel;
CREATE USER finuser WITH PASSWORD 'finpass123';
GRANT ALL PRIVILEGES ON DATABASE fin_intel TO finuser;
\q

# または Docker Compose を使用
docker-compose up -d postgres
```

---

## モニタリング & ログ

### ログファイル

```bash
# パイプラインログ
tail -f backend/src/scraper_pipeline.log

# スケジューラー状態
cat backend/src/scheduler_state.json
```

### 統計情報の確認

```python
# Python REPL から
from scraper.scheduler import TwitterScheduler

scheduler = TwitterScheduler(config_path='../config/twitter_accounts.json')
print(scheduler.stats)
```

---

## パフォーマンス最適化

### 1. GPU 高速化

```bash
# CUDA ツールキットのインストール（NVIDIA GPUのみ）
# https://developer.nvidia.com/cuda-downloads

# Ollama が GPU を使用していることを確認
ollama ps
```

### 2. マルチプロセス実行

複数のスクレイパーインスタンスを並列実行（要プロキシ）:

```bash
# 91アカウントを3つに分割
python main_scraper_pipeline.py --accounts 0-30 &
python main_scraper_pipeline.py --accounts 31-60 &
python main_scraper_pipeline.py --accounts 61-91 &
```

### 3. Redis キャッシュ

重複ツイートのスキップにRedisを活用（TODO: 実装予定）

---

## 次のステップ

1. ✅ システムセットアップ完了
2. ✅ テスト実行で動作確認
3. ⏳ 本番環境へデプロイ
4. ⏳ LINE 通知の設定
5. ⏳ ダッシュボード（フロントエンド）との連携

---

## サポート

問題が発生した場合:

1. GitHub Issues: https://github.com/asuka8888/02_seminar/issues
2. ドキュメント:
   - `SCRAPING_STRATEGY.md` - スクレイピング戦略
   - `OLLAMA_MODELS_GUIDE.md` - モデル選択ガイド
   - `FINAL_SYSTEM_SUMMARY.md` - システム全体像

---

## ライセンス

このシステムは教育・研究目的で作成されています。Twitter/X の利用規約を遵守してご使用ください。
