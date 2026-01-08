# Xアカウント取得に関する技術ログ

## 📋 プロジェクト概要

女性起業家向け金融インテリジェンス配信システムにおいて、**50個の「Must Follow」なTwitter (X) アカウント**を監視し、リアルタイムで情報を収集・分析・配信するシステムを構築します。

## 🎯 監視対象アカウント (全50件)

### マクロ経済・市場戦略 (15件)
1. `@LizAnnSonders` - Charles Schwabチーフ投資ストラテジスト
2. `@elerianm` - Mohamed A. El-Erian (Allianz主任経済顧問)
3. `@Schuldensuehner` - Holger Zschaepitz (ドイツ金融ジャーナリスト)
4. `@lisaabramowicz1` - Lisa Abramowicz (Bloomberg)
5. `@charliebilello` - Charlie Bilello (データ分析)
6. `@jsblokland` - Jeroen Blokland (マルチアセット分析)
7. `@NorthmanTrader` - Sven Henrich (逆張り分析)
8. `@DiMartinoBooth` - Danielle DiMartino Booth (元FRB顧問)
9. `@LynAldenContact` - Lyn Alden (構造的経済分析)
10. `@RaoulGMI` - Raoul Pal (Real Vision CEO)
11. `@GRDecter` - Genevieve Roch-Decter, CFA
12. `@jessefelder` - Jesse Felder (The Felder Report)
13. `@biancoresearch` - Jim Bianco (定量分析)
14. `@MacroAlf` - Alf (元銀行トレーダー)
15. `@yardeni` - Yardeni Research

### テクニカル分析 (11件)
16. `@markminervini` - Mark Minervini (VCPパターン)
17. `@WilliamONeil` - William O'Neil + Co (CAN SLIM)
18. `@IBDinvestors` - IBD Investors
19. `@TrendSpider` - TrendSpider (AI分析)
20. `@PeterLBrandt` - Peter Brandt (古典的チャート)
21. `@alphatrends` - Brian Shannon (VWAP分析)
22. `@allstarcharts` - JC Parets (トップダウン)
23. `@Stocktwits` - Stocktwits (センチメント)
24. `@InvestorsLive` - Nathan Michaud (デイトレード)
25. `@OptionsHawk` - Joe Kunkle (オプション監視)
26. `@RedDogT3` - Scott Redler (ピボット分析)

### ショートセラー・リスク分析 (3件)
27. `@HindenburgRes` - Hindenburg Research
28. `@muddywatersre` - Muddy Waters
29. `@CitronResearch` - Citron Research

### ファンダメンタルズ分析 (10件)
30. `@AswathDamodaran` - Aswath Damodaran (NYU教授)
31. `@BrianFeroldi` - Brian Feroldi (財務指標解説)
32. `@AppEconomyIns` - App Economy Insights (決算ビジュアル)
33. `@10kdiver` - 10-K Diver (10-K分析)
34. `@awealthofcs` - Ben Carlson
35. `@morganhousel` - Morgan Housel (行動心理)
36. `@iancassel` - Ian Cassel (MicroCap)
37. `@SahilBloom` - Sahil Bloom (メンタルモデル)
38. `@bespokeinvest` - Bespoke
39. `@ValueStockGeek` - ValueStockGeek

### テクノロジー・暗号資産 (4件)
40. `@paulg` - Paul Graham (Y Combinator)
41. `@balajis` - Balaji Srinivasan (元Coinbase CTO)
42. `@VitalikButerin` - Vitalik Buterin (Ethereum創設者)
43. `@100trillionUSD` - PlanB (S2Fモデル)

### 速報・オルタナティブ情報 (7件)
44. `@DeItaone` - Walter Bloomberg (Bloomberg速報)
45. `@zerohedge` - Zerohedge
46. `@unusual_whales` - Unusual Whales (政治家取引追跡)
47. `@VCBrags` - VCs Congratulating Themselves (VC風刺)
48. `@TrungTPhan` - Trung Phan (ビジネス歴史)
49. `@gurgavin` - Gurgavin Chandhoke (チャート速報)
50. `@Benzinga` - Benzinga (触媒ニュース)

## 🔧 技術スタック

### Twitter API設定

| 項目 | 詳細 |
|---|---|
| **ライブラリ** | `tweepy` 4.14.x |
| **API** | Twitter API v2 |
| **認証方式** | Bearer Token |
| **環境変数** | `TWITTER_BEARER_TOKEN` |

### 環境変数設定例

```env
# Data Collection
TWITTER_BEARER_TOKEN="AAAAAAAAAAAAAAAAAAAAAMLheAAAAAAA..."
```

### 実装要件

```python
# src/scraper モジュール実装
# crawl4ai ライブラリを使用してスクレイピング
# 過去24時間の投稿テキストを取得する TwitterScraper クラス
```

## 📚 設計ドキュメント参照

以下のドキュメントに詳細な設計情報を記載しています：

1. **要件定義書（憲法）** - `01_要件定義書_憲法.md`
2. **要件定義書（全文・人間用）** - `02_要件定義書_全文_人間用.md`
3. **仕様書（UI/API/DB）** - `03_仕様書_UI_API_DB.md`
4. **ワークフロー** - `04_ワークフロー.md`
5. **実行計画書** - `05_実行計画書.md`
6. **技術要件書** - `06_技術要件書.md`

## 🚀 次のステップ

1. Twitter Developer Portal で Bearer Token を取得
2. 環境変数 `TWITTER_BEARER_TOKEN` を設定
3. `tweepy` 4.14.0 をインストール
4. 50個のアカウントを監視するスクレイパーを実装
5. Claude Code + LangGraph でインテリジェンス処理パイプラインを構築

## 📖 参考文献

- Twitter API v2 公式ドキュメント
- Tweepy 公式ドキュメント
- 株情報収集・配信システム開発.md (詳細設計)
- 技術要件書 (06_技術要件書.md)

---

**作成日**: 2026年1月5日
**リポジトリ**: https://github.com/asuka8888/02_seminar.git
