"""
Twitter Account Scraping Scheduler
91アカウントを24時間で巡回監視するスケジューラー
"""
import asyncio
import random
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from pathlib import Path
from dataclasses import dataclass, asdict
import time

from twitter_playwright import TwitterPlaywrightScraper, Tweet
import sys
sys.path.append(str(Path(__file__).parent.parent))
from agents.local_ai_analyzer import LocalAIAnalyzer, AnalysisResult

logger = logging.getLogger(__name__)


@dataclass
class ScrapingTask:
    """スクレイピングタスク"""
    username: str
    url: str
    category: str
    priority: str
    check_interval: str
    note: Optional[str] = None
    last_scraped: Optional[datetime] = None
    next_scrape_time: Optional[datetime] = None
    scrape_count: int = 0
    error_count: int = 0


@dataclass
class ProcessedTweet:
    """処理済みツイート（スクレイピング + AI分析）"""
    tweet: Tweet
    analysis: AnalysisResult
    processed_at: datetime
    account_username: str
    account_category: str


class TwitterScheduler:
    """
    Twitter監視スケジューラー

    機能:
    1. 91アカウントを24時間で均等に分散
    2. ランダム間隔でアカウント凍結を回避
    3. AI分析パイプライン統合
    4. エラーハンドリング・リトライ
    5. 進捗状況の保存・復元
    """

    def __init__(
        self,
        config_path: str,
        state_file: str = "scheduler_state.json",
        max_tweets_per_account: int = 20,
        lookback_hours: int = 24,
        use_proxy: bool = False,
        proxy_list: Optional[List[Dict[str, str]]] = None
    ):
        """
        Args:
            config_path: twitter_accounts.json のパス
            state_file: スケジューラー状態保存ファイル
            max_tweets_per_account: 1アカウントあたりの最大取得ツイート数
            lookback_hours: 過去何時間分のツイートを取得するか
            use_proxy: プロキシを使用するか
            proxy_list: プロキシリスト
        """
        self.config_path = Path(config_path)
        self.state_file = Path(state_file)
        self.max_tweets_per_account = max_tweets_per_account
        self.lookback_hours = lookback_hours
        self.use_proxy = use_proxy
        self.proxy_list = proxy_list or []

        # タスクリスト
        self.tasks: List[ScrapingTask] = []

        # AI Analyzer
        self.ai_analyzer = LocalAIAnalyzer()

        # 統計情報
        self.stats = {
            'total_accounts': 0,
            'scraped_accounts': 0,
            'total_tweets': 0,
            'total_errors': 0,
            'start_time': None,
            'end_time': None
        }

        # 設定読み込み
        self._load_config()
        self._load_state()

    def _load_config(self):
        """twitter_accounts.json から設定を読み込む"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            logger.info(f"Loading config from {self.config_path}")
            logger.info(f"Total accounts: {config.get('totalAccounts', 0)}")

            # 全カテゴリからアカウントを抽出
            for category_name, category_data in config.get('categories', {}).items():
                accounts = category_data.get('accounts', [])
                priority = category_data.get('priority', 'medium')
                check_interval = category_data.get('checkInterval', '10m')

                for account in accounts:
                    task = ScrapingTask(
                        username=account['username'],
                        url=account['url'],
                        category=category_name,
                        priority=priority,
                        check_interval=check_interval,
                        note=account.get('note'),
                        last_scraped=None,
                        next_scrape_time=None,
                        scrape_count=0,
                        error_count=0
                    )
                    self.tasks.append(task)

            self.stats['total_accounts'] = len(self.tasks)
            logger.info(f"Loaded {len(self.tasks)} accounts from config")

        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise

    def _load_state(self):
        """前回の状態を復元"""
        if not self.state_file.exists():
            logger.info("No previous state found, starting fresh")
            return

        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)

            # タスクの状態を復元
            for task in self.tasks:
                task_state = state.get('tasks', {}).get(task.username)
                if task_state:
                    task.last_scraped = datetime.fromisoformat(task_state['last_scraped']) if task_state.get('last_scraped') else None
                    task.scrape_count = task_state.get('scrape_count', 0)
                    task.error_count = task_state.get('error_count', 0)

            logger.info(f"Restored state from {self.state_file}")

        except Exception as e:
            logger.warning(f"Failed to load state: {e}")

    def _save_state(self):
        """現在の状態を保存"""
        try:
            state = {
                'tasks': {
                    task.username: {
                        'last_scraped': task.last_scraped.isoformat() if task.last_scraped else None,
                        'scrape_count': task.scrape_count,
                        'error_count': task.error_count
                    }
                    for task in self.tasks
                },
                'stats': self.stats,
                'last_updated': datetime.now().isoformat()
            }

            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)

            logger.debug("State saved")

        except Exception as e:
            logger.warning(f"Failed to save state: {e}")

    def _calculate_schedule(self):
        """24時間でタスクを均等に分散"""
        total_tasks = len(self.tasks)
        if total_tasks == 0:
            return

        # 24時間 = 1440分
        total_minutes = 24 * 60
        average_interval_minutes = total_minutes / total_tasks

        logger.info(f"Scheduling {total_tasks} accounts over 24 hours")
        logger.info(f"Average interval: {average_interval_minutes:.1f} minutes")

        # 現在時刻
        now = datetime.now()

        # タスクをランダムシャッフル（同じアカウントが毎回同じ時間にならないように）
        shuffled_tasks = self.tasks.copy()
        random.shuffle(shuffled_tasks)

        # スケジュールを計算
        for i, task in enumerate(shuffled_tasks):
            # ベース時間 + ランダムな揺らぎ (±30%)
            base_delay_minutes = i * average_interval_minutes
            random_factor = random.uniform(0.7, 1.3)
            delay_minutes = base_delay_minutes * random_factor

            task.next_scrape_time = now + timedelta(minutes=delay_minutes)

            logger.debug(
                f"Scheduled @{task.username} at {task.next_scrape_time.strftime('%H:%M:%S')} "
                f"(in {delay_minutes:.1f} min)"
            )

        # 時刻順にソート
        self.tasks.sort(key=lambda t: t.next_scrape_time)

    async def scrape_account(self, task: ScrapingTask, scraper: TwitterPlaywrightScraper) -> List[ProcessedTweet]:
        """
        1アカウントをスクレイピング + AI分析

        Args:
            task: スクレイピングタスク
            scraper: Playwrightスクレイパー

        Returns:
            処理済みツイートのリスト
        """
        try:
            logger.info(f"[{task.category}] Scraping @{task.username}...")

            # ツイートを取得
            since_date = datetime.now() - timedelta(hours=self.lookback_hours)
            tweets = await scraper.scrape_user_timeline(
                username=task.username,
                max_tweets=self.max_tweets_per_account,
                since_date=since_date
            )

            logger.info(f"Found {len(tweets)} tweets from @{task.username}")

            # AI分析
            processed_tweets = []
            for tweet in tweets:
                try:
                    # 翻訳 + センチメント分析 + 市場インパクト分析
                    analysis = self.ai_analyzer.full_analysis(
                        text=tweet.content,
                        language=tweet.lang
                    )

                    processed = ProcessedTweet(
                        tweet=tweet,
                        analysis=analysis,
                        processed_at=datetime.now(),
                        account_username=task.username,
                        account_category=task.category
                    )
                    processed_tweets.append(processed)

                    # ログ出力
                    logger.info(
                        f"  ✓ Tweet {tweet.tweet_id}: "
                        f"sentiment={analysis.sentiment}, "
                        f"impact={analysis.market_impact}"
                    )

                except Exception as e:
                    logger.error(f"Failed to analyze tweet {tweet.tweet_id}: {e}")

            # タスク状態更新
            task.last_scraped = datetime.now()
            task.scrape_count += 1
            task.error_count = 0  # リセット

            # 統計更新
            self.stats['scraped_accounts'] += 1
            self.stats['total_tweets'] += len(processed_tweets)

            return processed_tweets

        except Exception as e:
            logger.error(f"Error scraping @{task.username}: {e}")
            task.error_count += 1
            self.stats['total_errors'] += 1
            return []

    async def run_continuous(self, cycle_count: int = 1):
        """
        連続実行モード（複数サイクル）

        Args:
            cycle_count: サイクル数（1サイクル = 24時間で全アカウント）
        """
        logger.info(f"Starting continuous scraping for {cycle_count} cycles")
        self.stats['start_time'] = datetime.now().isoformat()

        for cycle in range(1, cycle_count + 1):
            logger.info(f"\n{'='*80}")
            logger.info(f"CYCLE {cycle}/{cycle_count}")
            logger.info(f"{'='*80}\n")

            await self.run_once()

            if cycle < cycle_count:
                logger.info(f"Cycle {cycle} complete. Starting next cycle...")

        self.stats['end_time'] = datetime.now().isoformat()
        logger.info("\n" + "="*80)
        logger.info("ALL CYCLES COMPLETE")
        logger.info("="*80)
        logger.info(f"Total accounts scraped: {self.stats['scraped_accounts']}")
        logger.info(f"Total tweets collected: {self.stats['total_tweets']}")
        logger.info(f"Total errors: {self.stats['total_errors']}")

    async def run_once(self):
        """1サイクル実行（24時間で全アカウント）"""
        # スケジュール計算
        self._calculate_schedule()

        # プロキシ設定
        proxy = None
        if self.use_proxy and self.proxy_list:
            proxy = random.choice(self.proxy_list)
            logger.info(f"Using proxy: {proxy.get('server', 'unknown')}")

        # スクレイパー起動
        async with TwitterPlaywrightScraper(proxy=proxy, headless=True) as scraper:
            for i, task in enumerate(self.tasks):
                # 次のスケジュール時刻まで待機
                now = datetime.now()
                if task.next_scrape_time > now:
                    wait_seconds = (task.next_scrape_time - now).total_seconds()
                    logger.info(
                        f"[{i+1}/{len(self.tasks)}] "
                        f"Waiting {wait_seconds:.1f}s until next scrape "
                        f"(@{task.username} at {task.next_scrape_time.strftime('%H:%M:%S')})"
                    )
                    await asyncio.sleep(wait_seconds)

                # スクレイピング実行
                processed_tweets = await self.scrape_account(task, scraper)

                # データベース保存（ここでは省略、後で実装）
                if processed_tweets:
                    await self._save_to_database(processed_tweets)

                # 状態保存
                self._save_state()

                # 人間らしいランダム遅延 (10-20分)
                random_delay = random.uniform(600, 1200)  # 10-20分
                logger.info(f"Random delay: {random_delay/60:.1f} minutes")
                await asyncio.sleep(random_delay)

        logger.info("Cycle complete!")

    async def _save_to_database(self, processed_tweets: List[ProcessedTweet]):
        """
        処理済みツイートをデータベースに保存

        TODO: Prisma または SQLAlchemy で実装
        """
        # 現時点ではJSON形式でログ出力
        for pt in processed_tweets:
            logger.debug(f"[DB] Saving tweet {pt.tweet.tweet_id} from @{pt.account_username}")

            # データベース保存処理を実装する場合:
            # await db.news.create({
            #     'title': pt.analysis.summary,
            #     'content': pt.tweet.content,
            #     'translated_content': pt.analysis.translated_text,
            #     'sentiment': pt.analysis.sentiment,
            #     'market_impact': pt.analysis.market_impact,
            #     'source_url': pt.tweet.url,
            #     'published_at': pt.tweet.timestamp,
            #     ...
            # })


async def main():
    """メイン実行"""
    # 設定ファイルパス
    config_path = Path(__file__).parent.parent.parent / "config" / "twitter_accounts.json"

    # スケジューラー作成
    scheduler = TwitterScheduler(
        config_path=str(config_path),
        max_tweets_per_account=10,  # テスト用に少なめ
        lookback_hours=24,
        use_proxy=False  # プロキシ使用する場合は True
    )

    # 1サイクル実行
    await scheduler.run_once()

    # 連続実行する場合:
    # await scheduler.run_continuous(cycle_count=7)  # 7日間


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    asyncio.run(main())
