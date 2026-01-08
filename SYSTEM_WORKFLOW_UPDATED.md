# システムワークフロー詳細解説（全アカウント同一優先度版）
## Financial Intelligence System - 完全動作フロー

**作成日**: 2026年1月5日
**バージョン**: 2.0（全アカウント平等監視）
**最終更新**: 2026年1月5日

---

## ✅ 修正内容サマリー

### 変更前（v1.0）
- ❌ 優先度別に3段階（Critical/High/Medium）
- ❌ チェック間隔が3分〜30分とバラバラ
- ❌ 通知タイミングも優先度で差別化

### 変更後（v2.0）
- ✅ **全91アカウント完全平等**
- ✅ **全て5分間隔で監視**
- ✅ **全て深層AI分析（Deep）**
- ✅ **全て10分以内に通知**

---

## 📊 統一された設定内容

### グローバル設定

| 項目 | 設定値 | 説明 |
|------|--------|------|
| **監視対象アカウント数** | **91件** | 日本41件 + 米国50件 |
| **優先度** | **High（全て）** | 全アカウント同一優先度 |
| **チェック間隔** | **5分** | 全アカウント統一 |
| **AI分析深度** | **Deep（深層）** | 全アカウント最高品質分析 |
| **通知遅延** | **10分** | 分析完了後10分以内に通知 |
| **通知チャネル** | **LINE/Email/Dashboard** | 全て有効 |

---

## 📍 監視対象アカウント一覧（91件）

### 日本語アカウント（41件）

#### 個人投資家・トレーダー（35件）
1. gold_locks_x
2. monkswagger1
3. paristexas2009
4. yasutaketin
5. pyon
6. 4th_skywalker
7. dawin1958
8. takechans1
9. hakureifarm
10. utbuffett
11. markminervini
12. enu_beat
13. spinspin1978
14. senjouinrenshu3
15. senjouinrenshu
16. 2okutameo
17. 225sakimonoaiko
18. sumitomo_yuu
19. iketeruyuyu
20. yaslovestech
21. harusmile
22. sen_axis
23. money_tweet1118
24. pontamaru_1028
25. kabutrader_nori
26. tradetool1
27. kanti990
28. heihachiro888
29. investor__x
30. raise_grave
31. coinspace_
32. capitalnvest
33. shenmacro
34. goviex
35. to1210shi

#### 市場アナリスト（3件）
36. bei_wayaku（米国市場翻訳・解説）
37. fukuri41（複利運用情報）
38. market_letter_（マーケットレター）

#### 重要アカウント（3件）
39. keith_market 🔑
40. utdanaher 🔑
41. roe_roe_roe 🔑

---

### 英語アカウント（50件）

#### 米国マクロ経済・市場戦略（15件）
42. LizAnnSonders（Charles Schwab）
43. elerianm（Mohamed El-Erian）
44. Schuldensuehner（Holger Zschaepitz）
45. lisaabramowicz1（Lisa Abramowicz）
46. charliebilello（Charlie Bilello）
47. jsblokland（Jeroen Blokland）
48. NorthmanTrader（Sven Henrich）
49. DiMartinoBooth（元FRB顧問）
50. LynAldenContact（Lyn Alden）
51. RaoulGMI（Raoul Pal）
52. GRDecter（Genevieve Roch-Decter）
53. jessefelder（Jesse Felder）
54. biancoresearch（Jim Bianco）
55. MacroAlf（Alf）
56. yardeni（Yardeni Research）

#### 米国テクニカル分析（10件）
57. WilliamONeil（CAN SLIM）
58. IBDinvestors（IBD）
59. TrendSpider（AI分析）
60. PeterLBrandt（古典的チャート）
61. alphatrends（Brian Shannon）
62. allstarcharts（JC Parets）
63. Stocktwits（センチメント）
64. InvestorsLive（Nathan Michaud）
65. OptionsHawk（オプション監視）
66. RedDogT3（Scott Redler）

#### 米国ショートセラー（3件）
67. HindenburgRes（Hindenburg Research）
68. muddywatersre（Muddy Waters）
69. CitronResearch（Citron Research）

#### 米国ファンダメンタルズ分析（10件）
70. AswathDamodaran（NYU教授）
71. BrianFeroldi（財務解説）
72. AppEconomyIns（決算ビジュアル）
73. 10kdiver（10-K分析）
74. awealthofcs（Ben Carlson）
75. morganhousel（Morgan Housel）
76. iancassel（MicroCap）
77. SahilBloom（メンタルモデル）
78. bespokeinvest（Bespoke）
79. ValueStockGeek（バリュー投資）

#### 米国テック・暗号資産（4件）
80. paulg（Paul Graham）
81. balajis（Balaji）
82. VitalikButerin（Vitalik）
83. 100trillionUSD（PlanB）

#### 米国速報・オルタナティブ（7件）
84. DeItaone（Walter Bloomberg）
85. zerohedge（ZeroHedge）
86. unusual_whales（政治家取引追跡）
87. VCBrags（VC風刺）
88. TrungTPhan（ビジネス歴史）
89. gurgavin（チャート速報）
90. Benzinga（Benzinga）

---

## 🔄 システム全体ワークフロー（統一版）

### Phase 1: データ収集（Twitter監視）

```
┌─────────────────────────────┐
│ Celeryスケジューラー起動     │
│ - 5分ごとに実行              │
│ - 全91アカウント対象         │
└────────┬────────────────────┘
         ▼
┌─────────────────────────────┐
│ Twitter API 並列呼び出し     │
│ - 91アカウントを並列処理     │
│ - 各アカウント最新25件取得   │
│ - レート制限対応（900req/15m）│
└────────┬────────────────────┘
         ▼
┌─────────────────────────────┐
│ 重複排除 & データ抽出        │
│ - 前回取得時刻との差分のみ   │
│ - 投稿ID、テキスト、日時     │
│ - メディアURL、著者情報      │
└────────┬────────────────────┘
         ▼
    Phase 2へ（全投稿）
```

**具体的な動作例**:
```
5:00 PM - 91アカウント全てチェック開始
5:00-5:02 PM - 並列で投稿取得（平均120秒）
5:02 PM - 新規投稿45件検知
5:02 PM - Phase 2のAI分析へ

5:05 PM - 91アカウント再チェック
5:07 PM - 新規投稿12件検知
5:07 PM - Phase 2のAI分析へ
```

---

### Phase 2: AI分析パイプライン（統一深層分析）

```
┌──────────────────────────┐
│ 新規投稿受信              │
│ - 日本語: 41アカウント    │
│ - 英語: 50アカウント      │
└────────┬─────────────────┘
         ▼
┌──────────────────────────┐
│ 言語判定                  │
│ - 日本語 → 分析へ         │
│ - 英語 → 翻訳へ           │
└────┬─────────────────────┘
     │
  ┌──┴──┐
  ▼     ▼
日本語  英語
  │     │
  │  ┌──▼────────────────┐
  │  │ Claude翻訳         │
  │  │ - モデル: Sonnet 4.5│
  │  │ - 金融用語対応     │
  │  │ - 処理時間: 5秒    │
  │  └────┬───────────────┘
  │       │
  └───┬───┘
      ▼
┌────────────────────────────┐
│ LangGraph深層分析          │
│ 【全アカウント統一処理】    │
│                            │
│ ① センチメント分析         │
│    - Positive/Negative/    │
│      Neutral判定           │
│                            │
│ ② セクター判定             │
│    - Tech/Finance/Energy/  │
│      Healthcare等          │
│                            │
│ ③ 関連銘柄抽出             │
│    - ティッカーシンボル    │
│    - 企業名抽出            │
│                            │
│ ④ 影響度分析               │
│    - 市場への影響度評価    │
│    - High/Medium/Low       │
│                            │
│ ⑤ 3行要約生成              │
│    - 投資家向けサマリー    │
│    - 読みやすく整形        │
│                            │
│ ⑥ 過去投稿との関連性       │
│    - 同一著者の過去発言    │
│    - トレンド分析          │
│                            │
│ 処理時間: 平均30秒/投稿    │
└────────┬───────────────────┘
         ▼
    Phase 3へ
```

**分析結果の例**:

```json
{
  "id": "tweet_abc123",
  "source": "keith_market",
  "category": "japanese_vip",
  "publishedAt": "2026-01-05T17:05:00Z",

  "originalText": "NVIDIA決算、予想上回るも株価下落。AIバブル懸念か。テック株全体に波及の可能性。",
  "translatedText": null,

  "analysis": {
    "sentiment": "negative",
    "sentimentScore": -0.65,
    "sector": "tech",
    "tickers": ["NVDA", "MSFT", "GOOGL"],
    "impact": "high",
    "summary": "NVIDIA好決算も株価下落。市場はAI期待の過熱を警戒。テック株全体への波及リスクあり。",
    "relatedPastTweets": ["tweet_xyz789"],
    "marketImplication": "テクノロジーセクター全体の調整局面入りの可能性"
  },

  "processingTime": 28.5,
  "analysisDepth": "deep"
}
```

---

### Phase 3: データベース保存（全投稿統一処理）

```
┌──────────────────────────┐
│ 分析結果受信              │
│ - 全91アカウント同一処理  │
└────────┬─────────────────┘
         ▼
┌──────────────────────────┐
│ Prisma ORM                │
│ - データ検証              │
│ - 重複チェック            │
│ - トランザクション処理    │
└────────┬─────────────────┘
         ▼
┌──────────────────────────┐
│ PostgreSQL保存            │
│                           │
│ News テーブル:            │
│ - id (UUID)               │
│ - source (著者)           │
│ - originalText            │
│ - translatedText          │
│ - sentiment               │
│ - sector                  │
│ - tickers[]               │
│ - summary                 │
│ - publishedAt             │
│ - createdAt               │
│                           │
│ インデックス:             │
│ - publishedAt (降順)      │
│ - sentiment               │
│ - sector                  │
└────────┬─────────────────┘
         ▼
    Phase 4へ
```

---

### Phase 4: 通知配信（10分バッチ統一）

```
┌──────────────────────────┐
│ DB保存完了通知            │
│ - 全投稿を10分バッファ    │
└────────┬─────────────────┘
         ▼
┌──────────────────────────┐
│ 10分間の投稿を集約        │
│ - バッチサイズ: 最大20件  │
│ - 古い順にソート          │
└────────┬─────────────────┘
         ▼
┌──────────────────────────┐
│ ユーザー設定確認          │
│ - LINE通知: ON/OFF        │
│ - Email通知: ON/OFF       │
│ - 通知頻度設定            │
│ - ミュート設定            │
└────────┬─────────────────┘
         ▼
┌──────────────────────────┐
│ 通知配信実行              │
│                           │
│ ① LINE Flex Message       │
│    - 最大20件まとめて配信 │
│    - センチメント別色分け │
│    - リンク付き           │
│                           │
│ ② Email (HTML)            │
│    - 美しいHTMLテンプレ   │
│    - グラフ・チャート付き │
│                           │
│ ③ Dashboard更新           │
│    - SSEでリアルタイム    │
│    - 5秒ごとに自動更新    │
└────────┬─────────────────┘
         ▼
┌──────────────────────────┐
│ NotificationLog保存       │
│ - userId                  │
│ - newsId                  │
│ - channel (line/email)    │
│ - status (sent/failed)    │
│ - sentAt                  │
└──────────────────────────┘
```

**LINE通知の例**:

```
📊 金融インテリジェンス - 10分サマリー

🔴 Negative (3件)
・keith_market: NVIDIA決算後の株価下落
・HindenburgRes: XYZ社の不正会計疑惑
・zerohedge: FRB利上げ継続の可能性

🟢 Positive (5件)
・LizAnnSonders: 雇用統計が予想上回る
・charliebilello: S&P500が史上最高値更新
・markminervini: テスラの新高値ブレイク

⚪ Neutral (4件)
・elerianm: 今週の経済指標カレンダー
・10kdiver: Amazonの10-K分析スレッド

合計12件の新着情報

[ダッシュボードで詳細を見る]
```

---

### Phase 5: ダッシュボード表示（リアルタイム更新）

```
┌──────────────────────────┐
│ Next.js 15 フロントエンド │
│ (http://localhost:3000)   │
└────────┬─────────────────┘
         ▼
┌──────────────────────────┐
│ tRPC API呼び出し          │
│                           │
│ news.getAll({             │
│   limit: 50,              │
│   offset: 0,              │
│   sector: "tech",         │
│   sentiment: "all"        │
│ })                        │
└────────┬─────────────────┘
         ▼
┌──────────────────────────┐
│ PostgreSQL クエリ実行     │
│                           │
│ SELECT * FROM news        │
│ WHERE sector = 'tech'     │
│ ORDER BY published_at DESC│
│ LIMIT 50                  │
└────────┬─────────────────┘
         ▼
┌──────────────────────────┐
│ SSE (Server-Sent Events)  │
│                           │
│ - 5秒ごとに新規チェック   │
│ - 差分のみ配信            │
│ - 自動で画面更新          │
└────────┬─────────────────┘
         ▼
┌──────────────────────────┐
│ React コンポーネント表示  │
│                           │
│ ① ニュースフィード        │
│    - 無限スクロール       │
│    - センチメント別色分け │
│                           │
│ ② センチメントグラフ      │
│    - Recharts使用         │
│    - 円グラフ/棒グラフ    │
│                           │
│ ③ セクター別フィルター    │
│    - Tech, Finance等      │
│    - ワンクリック切替     │
│                           │
│ ④ 検索・ソート機能        │
│    - 全文検索             │
│    - 日付/センチメント    │
└──────────────────────────┘
```

---

## 📊 システムパフォーマンス予測

### 処理能力

| 項目 | 数値 |
|------|------|
| **監視アカウント数** | 91件 |
| **チェック頻度** | 5分（1日288回） |
| **1日あたりAPI呼び出し** | 約26,000回 |
| **1日あたり処理投稿数** | 2,000〜3,000件（推定） |
| **平均処理時間/投稿** | 30秒（翻訳+分析） |
| **ピーク時同時処理** | 50件/分 |

### 通知配信

| 項目 | 設定 |
|------|------|
| **通知チャネル** | LINE, Email, Dashboard |
| **バッチ間隔** | 10分 |
| **最大バッチサイズ** | 20件 |
| **日次サマリー** | 毎朝8:00 |
| **通知遅延** | 最大10分 |

---

## 🚀 これからの作業フロー

### Week 1-2: コア機能実装

#### Day 1-2: Twitterスクレイパー実装
**ファイル**: `backend/src/scraper/twitter_scraper.py`

**実装内容**:
```python
class TwitterScraper:
    def __init__(self, bearer_token: str):
        self.client = tweepy.Client(bearer_token=bearer_token)
        self.accounts = self._load_all_accounts()  # 全91件読み込み

    def fetch_all_tweets(self) -> List[Dict]:
        """全91アカウントから投稿を並列取得"""
        all_tweets = []

        # 並列処理で高速化
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for account in self.accounts:
                future = executor.submit(
                    self._fetch_account_tweets,
                    account['username']
                )
                futures.append(future)

            for future in as_completed(futures):
                tweets = future.result()
                all_tweets.extend(tweets)

        return all_tweets
```

---

#### Day 3-5: Claude AI分析エージェント
**ファイル**: `backend/src/agents/intelligence_agent.py`

**実装内容**:
```python
class IntelligenceAgent:
    def analyze_deep(self, tweet: Dict) -> Dict:
        """全投稿に深層分析を適用"""

        # 1. 翻訳（必要な場合）
        if self._is_english(tweet['text']):
            translated = self._translate(tweet['text'])
        else:
            translated = None

        # 2. 深層分析（全投稿統一）
        analysis = {
            'sentiment': self._analyze_sentiment(tweet['text']),
            'sector': self._identify_sector(tweet['text']),
            'tickers': self._extract_tickers(tweet['text']),
            'impact': self._assess_impact(tweet['text']),
            'summary': self._generate_summary(tweet['text']),
            'relatedPosts': self._find_related(tweet)
        }

        return {
            'originalText': tweet['text'],
            'translatedText': translated,
            'analysis': analysis,
            'analysisDepth': 'deep'
        }
```

---

### Week 3: API & UI実装

#### Day 8-10: tRPC APIエンドポイント
**統一エンドポイント** - 全アカウント平等に取得:

```typescript
export const newsRouter = createTRPCRouter({
  getAll: publicProcedure
    .input(z.object({
      limit: z.number().min(1).max(100).default(50),
      offset: z.number().min(0).default(0),
      sector: z.string().optional(),
      sentiment: z.enum(['positive', 'negative', 'neutral', 'all']).default('all')
    }))
    .query(async ({ ctx, input }) => {
      // 全91アカウント対象、優先度なし
      const news = await ctx.db.news.findMany({
        where: {
          ...(input.sector && { sector: input.sector }),
          ...(input.sentiment !== 'all' && { sentiment: input.sentiment })
        },
        orderBy: { publishedAt: 'desc' },  // 新しい順
        take: input.limit,
        skip: input.offset
      });

      return { news, total: await ctx.db.news.count() };
    })
});
```

---

## 🎯 システムの最終形態

完成すると、以下のように動作します：

### リアルタイム監視（5分サイクル）
```
5:00 PM - 91アカウント全てチェック開始
5:02 PM - 新規投稿45件検知 → AI分析開始
5:05 PM - 分析完了（45件） → DB保存
5:10 PM - 10分バッチ通知（45件をLINE配信）
5:12 PM - ダッシュボード自動更新

5:05 PM - 91アカウント再チェック
5:07 PM - 新規投稿12件検知 → AI分析開始
5:10 PM - 分析完了（12件） → DB保存
5:15 PM - 10分バッチ通知（12件をLINE配信）
```

### 1日の処理フロー
```
00:00 - システム稼働開始
00:05 - 第1回チェック（91アカウント）
00:10 - 第2回チェック
...
08:00 - 日次サマリーメール送信
...
23:55 - 第287回チェック
23:59 - 1日の処理完了
      - 総チェック回数: 288回
      - 総処理投稿数: 約2,500件
      - 総通知配信数: 約125回（10分ごと×144回）
```

---

## 📈 期待される成果

### 情報取得の公平性
- ✅ **全91アカウントが平等に監視される**
- ✅ **どのアカウントも見逃さない**
- ✅ **全投稿に最高品質の分析を適用**

### システムの信頼性
- ✅ **処理速度の統一**（全て30秒以内）
- ✅ **通知タイミングの統一**（全て10分以内）
- ✅ **分析品質の統一**（全てDeep分析）

### ユーザー体験
- ✅ **公平な情報配信**
- ✅ **予測可能な通知タイミング**
- ✅ **高品質な日本語翻訳・要約**

---

## 🔧 次のステップ

1. **環境確認**
```bash
# データベース起動
docker-compose up -d

# 設定ファイル確認
cat config/twitter_accounts.json
```

2. **Week 1 実装開始**
   - Twitterスクレイパー（全91アカウント対応）
   - Claude AI分析エージェント（Deep分析統一）

3. **動作確認**
   - 10アカウントでテスト
   - 問題なければ91アカウントに拡大

---

**全てのアカウントが平等に扱われます！** 🎉
