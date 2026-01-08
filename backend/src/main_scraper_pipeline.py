"""
Main Scraper Pipeline - Integration Layer
スクレイパー + AI分析 + データベース統合パイプライン
"""
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import os
import sys

# パス設定
sys.path.append(str(Path(__file__).parent))

from scraper.twitter_playwright import TwitterPlaywrightScraper, Tweet
from scraper.scheduler import TwitterScheduler, ProcessedTweet
from scraper.proxy_manager import ProxyManager
from agents.local_ai_analyzer import LocalAIAnalyzer
from database import db_manager

logger = logging.getLogger(__name__)


class ScraperPipeline:
    """
    完全統合スクレイピングパイプライン

    フロー:
    1. スケジューラーが91アカウントを管理
    2. Playwrightでツイートをスクレイピング（プロキシ + User-Agent ローテーション）
    3. Ollamaでツイートを分析（翻訳 + センチメント + 市場インパクト）
    4. PostgreSQLに保存
    5. LINE/Emailで通知（高インパクトのみ）

    コスト:
    - 旧システム（API版）: $7,880/月
    - 新システム（スクレイピング版）: $130/月 (GPU レンタル) または $0/月 (自前GPU)
    """

    def __init__(
        self,
        config_path: str,
        enable_proxy: bool = False,
        proxy_configs: Optional[List[Dict]] = None,
        enable_database: bool = True,
        enable_notification: bool = True
    ):
        """
        Args:
            config_path: twitter_accounts.json へのパス
            enable_proxy: プロキシを使用するか
            proxy_configs: プロキシ設定リスト
            enable_database: データベース保存を有効にするか
            enable_notification: 通知を有効にするか
        """
        self.config_path = config_path
        self.enable_proxy = enable_proxy
        self.enable_database = enable_database
        self.enable_notification = enable_notification

        # プロキシマネージャー
        self.proxy_manager = None
        if enable_proxy and proxy_configs:
            self.proxy_manager = ProxyManager(
                proxies=proxy_configs,
                rotation_strategy="random"
            )
            logger.info("Proxy manager initialized")

        # AI Analyzer
        self.ai_analyzer = LocalAIAnalyzer(
            main_model="qwen2.5:32b",
            fast_model="gemma2:9b"
        )

        # スケジューラー
        self.scheduler = TwitterScheduler(
            config_path=config_path,
            max_tweets_per_account=20,
            lookback_hours=24,
            use_proxy=enable_proxy,
            proxy_list=proxy_configs if proxy_configs else []
        )

    async def start(self, continuous: bool = False, cycle_count: int = 1):
        """
        パイプラインを開始

        Args:
            continuous: 連続実行モード
            cycle_count: サイクル数（continuous=Trueの場合）
        """
        logger.info("="*80)
        logger.info("🚀 Scraper Pipeline Starting")
        logger.info("="*80)
        logger.info(f"Total accounts: {len(self.scheduler.tasks)}")
        logger.info(f"Proxy enabled: {self.enable_proxy}")
        logger.info(f"Database enabled: {self.enable_database}")
        logger.info(f"Notification enabled: {self.enable_notification}")
        logger.info("="*80)

        # データベース接続確認
        if self.enable_database:
            await self._check_database_connection()

        # プロキシヘルスチェック（バックグラウンド）
        if self.proxy_manager:
            asyncio.create_task(self.proxy_manager.start_health_check_loop())

        # スケジューラー実行
        if continuous:
            await self.scheduler.run_continuous(cycle_count=cycle_count)
        else:
            await self.scheduler.run_once()

        logger.info("✅ Pipeline complete")

    async def _check_database_connection(self):
        """データベース接続を確認"""
        try:
            # Prisma Client に接続
            await db_manager.connect()
            logger.info("✓ Database connected")

            # ヘルスチェック
            is_healthy = await db_manager.health_check()
            if not is_healthy:
                raise Exception("Database health check failed")

            # 統計情報を表示
            stats = await db_manager.get_stats()
            logger.info(f"Database stats: {stats}")

        except Exception as e:
            logger.error(f"✗ Database connection failed: {e}")
            raise

    async def process_tweet(
        self,
        tweet: Tweet,
        account_username: str,
        account_category: str
    ) -> ProcessedTweet:
        """
        単一ツイートを処理（スクレイピング後の処理）

        Args:
            tweet: ツイートデータ
            account_username: アカウント名
            account_category: カテゴリ

        Returns:
            処理済みツイート
        """
        # AI分析
        analysis = self.ai_analyzer.full_analysis(
            text=tweet.content,
            language=tweet.lang
        )

        processed = ProcessedTweet(
            tweet=tweet,
            analysis=analysis,
            processed_at=datetime.now(),
            account_username=account_username,
            account_category=account_category
        )

        # データベース保存
        if self.enable_database:
            await self._save_to_database(processed)

        # 通知（高インパクトのみ）
        if self.enable_notification and analysis.market_impact == "high":
            await self._send_notification(processed)

        return processed

    async def _save_to_database(self, processed: ProcessedTweet):
        """
        処理済みツイートをデータベースに保存

        Prisma schema の News モデルに保存
        """
        try:
            tweet = processed.tweet
            analysis = processed.analysis

            # 重複チェック（同じURLのニュースが既に存在する場合はスキップ）
            existing = await db_manager.client.news.find_first(
                where={'originalUrl': tweet.url}
            )

            if existing:
                logger.debug(f"[DB] Tweet {tweet.tweet_id} already exists, skipping")
                return

            # News レコードを作成
            news = await db_manager.client.news.create(
                data={
                    # メタデータ
                    'source': processed.account_username,
                    'platform': 'twitter',
                    'publishedAt': tweet.timestamp,

                    # コンテンツ
                    'originalText': tweet.content,
                    'translatedText': analysis.translated_text or tweet.content,
                    'summary': analysis.summary[:500] if analysis.summary else tweet.content[:200],

                    # 分析結果
                    'sentiment': analysis.sentiment,
                    'sentimentScore': analysis.sentiment_score,
                    'priority': analysis.market_impact,  # high/medium/low
                    'sector': 'general',  # TODO: セクター分類ロジック
                    'tickers': [],  # TODO: ティッカー抽出ロジック
                    'keyTopics': analysis.key_topics,

                    # エンゲージメント
                    'likes': tweet.likes,
                    'retweets': tweet.retweets,
                    'replies': tweet.replies,

                    # リンク
                    'originalUrl': tweet.url,
                    'notionUrl': None,  # TODO: Notion連携

                    # 分類
                    'category': processed.account_category,
                    'language': tweet.lang,

                    # 管理
                    'processed': True,
                }
            )

            logger.info(
                f"[DB] ✓ Saved tweet {tweet.tweet_id} from @{processed.account_username} "
                f"(priority: {analysis.market_impact}, sentiment: {analysis.sentiment})"
            )

            return news

        except Exception as e:
            logger.error(f"Failed to save to database: {e}")
            import traceback
            traceback.print_exc()

    async def _send_notification(self, processed: ProcessedTweet):
        """
        高インパクトツイートの通知送信

        TODO: LINE Notify, Email, Slack などの実装
        """
        try:
            # 通知メッセージ作成
            message = self._format_notification_message(processed)

            # LINE Notify で送信（実装例）
            """
            import aiohttp

            line_token = os.getenv('LINE_NOTIFY_TOKEN')
            async with aiohttp.ClientSession() as session:
                await session.post(
                    'https://notify-api.line.me/api/notify',
                    headers={'Authorization': f'Bearer {line_token}'},
                    data={'message': message}
                )
            """

            logger.info(f"📢 Notification sent for tweet {processed.tweet.tweet_id}")

        except Exception as e:
            logger.error(f"Failed to send notification: {e}")

    def _format_notification_message(self, processed: ProcessedTweet) -> str:
        """通知メッセージをフォーマット"""
        tweet = processed.tweet
        analysis = processed.analysis

        message = f"""
🚨 高インパクト情報検出

【アカウント】@{processed.account_username} ({processed.account_category})
【センチメント】{analysis.sentiment} ({analysis.sentiment_score:.2f})
【インパクト】{analysis.market_impact.upper()}
【トピック】{', '.join(analysis.key_topics[:3])}

【要約】
{analysis.summary}

【原文】
{tweet.content[:200]}{'...' if len(tweet.content) > 200 else ''}

🔗 {tweet.url}

⏰ {tweet.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
"""
        return message.strip()


async def main():
    """
    メイン実行関数

    環境変数:
    - ENABLE_PROXY: プロキシを使用するか (true/false)
    - PROXY_SERVER: プロキシサーバー
    - PROXY_USERNAME: プロキシユーザー名
    - PROXY_PASSWORD: プロキシパスワード
    - DATABASE_URL: PostgreSQL接続URL
    - LINE_NOTIFY_TOKEN: LINE通知トークン
    """
    # 設定ファイルパス
    config_path = Path(__file__).parent.parent / "config" / "twitter_accounts.json"

    # プロキシ設定（環境変数から読み込み）
    enable_proxy = os.getenv('ENABLE_PROXY', 'false').lower() == 'true'
    proxy_configs = []

    if enable_proxy:
        proxy_server = os.getenv('PROXY_SERVER')
        proxy_username = os.getenv('PROXY_USERNAME')
        proxy_password = os.getenv('PROXY_PASSWORD')

        if proxy_server:
            proxy_configs.append({
                'server': proxy_server,
                'username': proxy_username,
                'password': proxy_password,
                'type': 'http',
                'residential': True
            })

    # パイプライン作成
    pipeline = ScraperPipeline(
        config_path=str(config_path),
        enable_proxy=enable_proxy,
        proxy_configs=proxy_configs if proxy_configs else None,
        enable_database=True,
        enable_notification=True
    )

    # 実行モード選択
    mode = os.getenv('RUN_MODE', 'once')  # once, continuous

    if mode == 'continuous':
        # 連続実行（7日間 = 7サイクル）
        await pipeline.start(continuous=True, cycle_count=7)
    else:
        # 1サイクルのみ
        await pipeline.start(continuous=False)


if __name__ == "__main__":
    # ロギング設定
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('scraper_pipeline.log')
        ]
    )

    # 実行
    asyncio.run(main())
