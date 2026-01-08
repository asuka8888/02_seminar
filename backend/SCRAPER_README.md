# Twitter/X スクレイピングシステム

> スクレイピング + Ollama ローカルAI による完全自動化された金融インテリジェンス収集システム

## 🎯 概要

このシステムは、Twitter/X から91の金融インテリジェンスアカウントを監視し、Ollama（ローカルAI）で自動翻訳・分析を行い、高インパクトな情報をリアルタイムで配信します。

**コスト削減**: $7,880/月 → $130/月（98%削減）

## ✨ 主な機能

### 1. アカウント凍結回避型スクレイピング
- ✅ Playwright ステルスモード（ヘッドレス検出回避）
- ✅ User-Agent ローテーション（6種類）
- ✅ ランダム遅延（10-20分間隔）
- ✅ プロキシローテーション対応
- ✅ 人間的な動作シミュレーション（スクロール、マウス移動）
- ✅ セッション管理（Cookie 保存・再利用）

### 2. Ollama ローカルAI分析
- ✅ Qwen2.5 32B: 英語→日本語翻訳、詳細市場分析
- ✅ Gemma 2 9B: 高速センチメント分析
- ✅ 完全オフライン動作（外部API不要）
- ✅ Claude API の約100倍のコスト削減

### 3. インテリジェントスケジューリング
- ✅ 91アカウントを24時間で均等分散
- ✅ 自動リトライ・エラーハンドリング
- ✅ 進捗状態の保存・復元
- ✅ 複数サイクル連続実行対応

### 4. データパイプライン
- ✅ スクレイピング → AI分析 → データベース保存 → 通知
- ✅ PostgreSQL への自動保存
- ✅ 高インパクト情報の LINE/Email 通知
- ✅ リアルタイムログ・統計情報

## 📊 システムアーキテクチャ

```
┌─────────────────────────────────────────────────────────────┐
│                     Scheduler                                │
│                  (91 accounts / 24h)                         │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Playwright Scraper                              │
│  - Stealth Mode                                              │
│  - Proxy Rotation                                            │
│  - User-Agent Rotation                                       │
│  - Human-like Behavior                                       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
                    [ Raw Tweets ]
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  Ollama AI Analyzer                          │
│  ┌──────────────────┐     ┌──────────────────┐             │
│  │  Qwen2.5 32B     │     │   Gemma 2 9B     │             │
│  │  ─────────────   │     │  ──────────────  │             │
│  │  - Translation   │     │  - Sentiment     │             │
│  │  - Analysis      │     │    (fast)        │             │
│  │  - Summary       │     │                  │             │
│  └──────────────────┘     └──────────────────┘             │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
                [ Analyzed Results ]
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
    ┌─────────┐      ┌─────────┐     ┌─────────┐
    │  PostgreSQL │      │  LINE   │     │  Email  │
    │  Database   │      │  Notify │     │         │
    └─────────┘      └─────────┘     └─────────┘
```

## 🗂 ディレクトリ構造

```
backend/
├── src/
│   ├── scraper/
│   │   ├── twitter_playwright.py    # メインスクレイパー（Playwright）
│   │   ├── scheduler.py              # 91アカウント スケジューラー
│   │   ├── proxy_manager.py          # プロキシローテーション管理
│   │   └── __init__.py
│   ├── agents/
│   │   ├── local_ai_analyzer.py      # Ollama AI 分析（翻訳・センチメント）
│   │   └── __init__.py
│   ├── main_scraper_pipeline.py      # 統合パイプライン
│   ├── quick_start.sh                # クイックスタート スクリプト
│   └── scheduler_state.json          # スケジューラー状態（自動生成）
├── requirements.txt
├── .env.example
└── SCRAPER_README.md                 # このファイル
```

## 🚀 クイックスタート

### 前提条件

- Python 3.11+
- Ollama がインストール済み
- PostgreSQL & Redis（Docker 推奨）

### 1. 自動セットアップ

```bash
cd backend/src
./quick_start.sh
```

このスクリプトは以下を自動実行します:
- Python 仮想環境の作成
- 依存関係のインストール
- Playwright ブラウザのインストール
- Ollama モデルの確認
- データベースの起動（Docker）
- 設定ファイルの作成

### 2. Ollama モデルのインストール

```bash
# メインモデル（20GB）
ollama pull qwen2.5:32b

# 高速モデル（5.4GB）
ollama pull gemma2:9b

# Ollama サービス起動
ollama serve
```

### 3. テスト実行

```bash
# スクレイパーのテスト
cd scraper
python twitter_playwright.py

# AI 分析のテスト
cd ../agents
python local_ai_analyzer.py
```

### 4. 本番実行

```bash
cd ..

# 1サイクル（24時間で91アカウント）
python main_scraper_pipeline.py

# 連続実行（7日間）
export RUN_MODE=continuous
python main_scraper_pipeline.py

# バックグラウンド実行
nohup python main_scraper_pipeline.py > scraper.log 2>&1 &
tail -f scraper.log
```

## ⚙️ 設定

### 環境変数（.env）

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
PROXY_SERVER=http://gate.smartproxy.com:7000
PROXY_USERNAME=your_username
PROXY_PASSWORD=your_password

# Notification
LINE_NOTIFY_TOKEN=your_line_token

# Runtime
RUN_MODE=once  # once または continuous
```

### 監視アカウント（config/twitter_accounts.json）

```json
{
  "version": "2.0",
  "totalAccounts": 91,
  "globalSettings": {
    "priority": "high",
    "checkInterval": "5m",
    "aiAnalysisDepth": "deep"
  },
  "categories": {
    "japanese_investors": { ... },
    "us_macro_strategy": { ... },
    ...
  }
}
```

## 📈 パフォーマンス

### スクレイピング速度

| 設定 | 時間 | アカウント/時間 |
|------|------|----------------|
| 1サイクル（91アカウント） | 24時間 | ~3.8 |
| プロキシなし（安全間隔） | 15-20分/アカウント | - |
| プロキシあり（並列実行） | 5-10分/アカウント | - |

### AI 分析速度

| モデル | 用途 | 速度（RTX 4080） |
|--------|------|-----------------|
| Qwen2.5 32B | 翻訳・分析 | ~15秒/ツイート |
| Gemma 2 9B | センチメント | ~3秒/ツイート |

### リソース使用量

| コンポーネント | CPU | RAM | GPU VRAM |
|----------------|-----|-----|----------|
| Playwright | 10-20% | 500MB | - |
| Qwen2.5 32B | 5% | 8GB | 14GB |
| Gemma 2 9B | 5% | 4GB | 6GB |
| PostgreSQL | 5% | 1GB | - |
| **合計** | **25-35%** | **13GB** | **14GB** |

## 🛡️ アカウント凍結回避戦略

### 実装済み対策（10個）

1. ✅ **ヘッドレス検出回避**: Playwright ステルスモード
2. ✅ **User-Agent ローテーション**: 6種類の実在ブラウザUA
3. ✅ **ランダム遅延**: 10-20分（人間的な間隔）
4. ✅ **プロキシローテーション**: IP分散
5. ✅ **セッション管理**: Cookie 保存・再利用
6. ✅ **人間的動作**: スクロール、マウス移動
7. ✅ **リクエスト量制限**: 91アカウント/24時間
8. ✅ **エラーハンドリング**: 失敗時の自動リトライ（指数バックオフ）
9. ✅ **時間帯分散**: 24時間で均等分散
10. ✅ **WebDriver プロパティ削除**: 自動化検出回避

### プロキシ推奨設定

| サービス | タイプ | 料金 | 凍結リスク |
|----------|--------|------|-----------|
| なし | - | $0 | 中〜高 |
| Smartproxy | Residential | $75/月 | 低 |
| Bright Data | Residential | $500/月 | 非常に低 |

## 📊 統計情報とログ

### リアルタイムログ

```bash
# パイプラインログ
tail -f backend/src/scraper_pipeline.log

# スケジューラー状態
cat backend/src/scheduler_state.json
```

### 統計情報の例

```json
{
  "total_accounts": 91,
  "scraped_accounts": 45,
  "total_tweets": 850,
  "total_errors": 3,
  "start_time": "2026-01-08T10:00:00",
  "end_time": null
}
```

### プロキシ統計

```python
from scraper.proxy_manager import ProxyManager

manager = ProxyManager(proxies=proxy_configs)
stats = manager.get_statistics()

# {
#   'total_proxies': 3,
#   'healthy_proxies': 3,
#   'total_success': 125,
#   'total_errors': 2,
#   'avg_response_time': 0.85
# }
```

## 🔧 トラブルシューティング

### Ollama 接続エラー

```bash
# Ollama サービスを起動
ollama serve

# モデルが存在するか確認
ollama list
```

### メモリ不足

```env
# 軽量モデルに変更
OLLAMA_MAIN_MODEL=qwen2.5:14b  # 32b → 14b
OLLAMA_FAST_MODEL=gemma2:2b    # 9b → 2b
```

### Twitter ブロック

```env
# プロキシを有効化
ENABLE_PROXY=true
PROXY_SERVER=http://your.proxy.com:8080
```

### データベース接続エラー

```bash
# Docker で起動
docker-compose up -d postgres redis

# 手動で作成
createdb fin_intel
```

## 📚 ドキュメント

- **SCRAPING_STRATEGY.md**: 詳細なスクレイピング戦略
- **OLLAMA_MODELS_GUIDE.md**: モデル選択ガイド
- **SCRAPING_SETUP_GUIDE.md**: 完全セットアップガイド
- **FINAL_SYSTEM_SUMMARY.md**: システム全体像

## 🔄 更新履歴

### v2.0.0 (2026-01-08)
- ✅ Playwright スクレイパー実装
- ✅ Ollama AI 分析統合
- ✅ プロキシローテーション対応
- ✅ 91アカウント対応スケジューラー
- ✅ 凍結回避戦略（10個）実装
- ✅ コスト98%削減達成

### v1.0.0 (2026-01-05)
- API ベースシステム（非推奨）

## 📄 ライセンス

このシステムは教育・研究目的で作成されています。

**重要**: Twitter/X の利用規約を遵守してください:
- 過度なスクレイピングは避ける
- レート制限を守る
- アカウント凍結リスクを理解する

## 🤝 サポート

問題・質問は GitHub Issues へ:
https://github.com/asuka8888/02_seminar/issues

---

**Made with ❤️ for Female Entrepreneurs**
