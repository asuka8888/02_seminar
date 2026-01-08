"""
Twitter/X Scraper using Playwright with ban prevention strategies
スクレイピングベースのTwitter/X取得システム（アカウント凍結回避対策実装）
"""
import asyncio
import random
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import json
import logging

from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)


@dataclass
class Tweet:
    """ツイートデータクラス"""
    tweet_id: str
    username: str
    content: str
    timestamp: datetime
    likes: int
    retweets: int
    replies: int
    url: str
    lang: str = "unknown"


class TwitterPlaywrightScraper:
    """
    Playwrightベースのステルス型Twitterスクレイパー

    凍結回避機能:
    1. ヘッドレス検出回避
    2. User-Agent ローテーション
    3. ランダム遅延（人間的な動作）
    4. プロキシローテーション対応
    5. セッション管理（Cookie保存・再利用）
    """

    def __init__(
        self,
        proxy: Optional[Dict[str, str]] = None,
        headless: bool = True,
        user_data_dir: Optional[str] = None
    ):
        self.proxy = proxy
        self.headless = headless
        self.user_data_dir = user_data_dir
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    async def __aenter__(self):
        """コンテキストマネージャー開始"""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """コンテキストマネージャー終了"""
        await self.close()

    def _get_random_user_agent(self) -> str:
        """ランダムなUser-Agentを取得"""
        user_agents = [
            # Chrome on Windows
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            # Chrome on Mac
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            # Firefox on Windows
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            # Safari on Mac
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        ]
        return random.choice(user_agents)

    async def start(self):
        """ブラウザを起動してステルス設定を適用"""
        playwright = await async_playwright().start()

        # Chromiumを起動（ステルスオプション）
        launch_options = {
            'headless': self.headless,
            'args': [
                '--disable-blink-features=AutomationControlled',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu',
                '--window-size=1920,1080',
            ]
        }

        # プロキシ設定
        if self.proxy:
            launch_options['proxy'] = self.proxy

        self.browser = await playwright.chromium.launch(**launch_options)

        # コンテキスト作成
        context_options = {
            'user_agent': self._get_random_user_agent(),
            'viewport': {'width': 1920, 'height': 1080},
            'locale': 'ja-JP',
            'timezone_id': 'Asia/Tokyo',
            'permissions': [],
            'geolocation': None,
            'color_scheme': 'light',
        }

        # 永続化されたセッション（Cookie保存）
        if self.user_data_dir:
            self.context = await self.browser.new_context(
                **context_options,
                storage_state=self.user_data_dir
            )
        else:
            self.context = await self.browser.new_context(**context_options)

        # ステルススクリプト注入（webdriver検出回避）
        await self.context.add_init_script("""
            // WebDriver プロパティを隠す
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });

            // Chrome プロパティを追加
            window.chrome = {
                runtime: {}
            };

            // Permissions API をオーバーライド
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );

            // Plugin配列を実際のブラウザのように見せる
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });

            // Languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['ja-JP', 'ja', 'en-US', 'en']
            });
        """)

        self.page = await self.context.new_page()

        # リクエストヘッダーの設定
        await self.page.set_extra_http_headers({
            'Accept-Language': 'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

        logger.info("Playwright browser started with stealth mode")

    async def close(self):
        """ブラウザを終了"""
        if self.context and self.user_data_dir:
            # セッション状態を保存
            await self.context.storage_state(path=self.user_data_dir)

        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()

        logger.info("Playwright browser closed")

    async def _human_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """人間らしいランダム遅延"""
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)

    async def _scroll_page(self, scrolls: int = 3):
        """ページをスクロール（人間的な動作）"""
        for _ in range(scrolls):
            # ランダムなスクロール量
            scroll_amount = random.randint(300, 800)
            await self.page.evaluate(f'window.scrollBy(0, {scroll_amount})')
            await self._human_delay(0.5, 1.5)

    async def scrape_user_timeline(
        self,
        username: str,
        max_tweets: int = 20,
        since_date: Optional[datetime] = None
    ) -> List[Tweet]:
        """
        ユーザーのタイムラインをスクレイピング

        Args:
            username: Twitterユーザー名（@なし）
            max_tweets: 取得する最大ツイート数
            since_date: この日時以降のツイートのみ取得

        Returns:
            ツイートのリスト
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")

        url = f"https://x.com/{username}"
        tweets = []

        try:
            logger.info(f"Scraping timeline for @{username}")

            # ページに移動
            await self.page.goto(url, wait_until='domcontentloaded', timeout=30000)
            await self._human_delay(2, 4)

            # ページが読み込まれるまで待機
            try:
                await self.page.wait_for_selector('article', timeout=10000)
            except PlaywrightTimeoutError:
                logger.warning(f"No tweets found for @{username} (account may be private or suspended)")
                return []

            # スクロールしてツイートを読み込む
            previous_height = 0
            scroll_attempts = 0
            max_scroll_attempts = 10

            while len(tweets) < max_tweets and scroll_attempts < max_scroll_attempts:
                # 現在表示されているツイートを取得
                articles = await self.page.query_selector_all('article')

                for article in articles:
                    if len(tweets) >= max_tweets:
                        break

                    try:
                        # ツイートの情報を抽出
                        tweet_data = await self._extract_tweet_from_article(article, username)

                        if tweet_data and tweet_data.tweet_id not in [t.tweet_id for t in tweets]:
                            # since_date フィルタ
                            if since_date and tweet_data.timestamp < since_date:
                                continue

                            tweets.append(tweet_data)
                            logger.debug(f"Extracted tweet: {tweet_data.tweet_id}")

                    except Exception as e:
                        logger.debug(f"Failed to extract tweet: {e}")
                        continue

                # スクロール
                current_height = await self.page.evaluate('document.body.scrollHeight')
                if current_height == previous_height:
                    scroll_attempts += 1
                else:
                    scroll_attempts = 0

                previous_height = current_height
                await self._scroll_page(2)
                await self._human_delay(2, 4)

            logger.info(f"Scraped {len(tweets)} tweets from @{username}")
            return tweets

        except Exception as e:
            logger.error(f"Error scraping @{username}: {e}")
            return tweets

    async def _extract_tweet_from_article(
        self,
        article,
        username: str
    ) -> Optional[Tweet]:
        """article要素からツイート情報を抽出"""
        try:
            # ツイートテキスト
            text_element = await article.query_selector('[data-testid="tweetText"]')
            content = await text_element.inner_text() if text_element else ""

            # タイムスタンプ
            time_element = await article.query_selector('time')
            timestamp_str = await time_element.get_attribute('datetime') if time_element else None
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')) if timestamp_str else datetime.now()

            # ツイートURL（ツイートID取得）
            link_element = await article.query_selector('a[href*="/status/"]')
            if link_element:
                href = await link_element.get_attribute('href')
                tweet_id = href.split('/status/')[-1].split('?')[0] if href else str(int(time.time()))
                url = f"https://x.com{href}" if href else f"https://x.com/{username}"
            else:
                tweet_id = str(int(time.time()))
                url = f"https://x.com/{username}"

            # エンゲージメント指標
            likes = await self._extract_metric(article, 'like')
            retweets = await self._extract_metric(article, 'retweet')
            replies = await self._extract_metric(article, 'reply')

            # 言語検出（簡易版）
            lang = self._detect_language(content)

            return Tweet(
                tweet_id=tweet_id,
                username=username,
                content=content,
                timestamp=timestamp,
                likes=likes,
                retweets=retweets,
                replies=replies,
                url=url,
                lang=lang
            )

        except Exception as e:
            logger.debug(f"Failed to extract tweet data: {e}")
            return None

    async def _extract_metric(self, article, metric_type: str) -> int:
        """エンゲージメント指標を抽出"""
        try:
            selector = f'[data-testid="{metric_type}"]'
            element = await article.query_selector(selector)
            if element:
                text = await element.inner_text()
                # "1.2K" -> 1200 などの変換
                return self._parse_count(text)
            return 0
        except Exception:
            return 0

    def _parse_count(self, text: str) -> int:
        """カウント文字列を数値に変換 (例: "1.2K" -> 1200)"""
        text = text.strip().upper()
        if not text or text == '—':
            return 0

        multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}

        for suffix, multiplier in multipliers.items():
            if suffix in text:
                try:
                    number = float(text.replace(suffix, '').replace(',', ''))
                    return int(number * multiplier)
                except ValueError:
                    return 0

        try:
            return int(text.replace(',', ''))
        except ValueError:
            return 0

    def _detect_language(self, text: str) -> str:
        """簡易言語検出（日本語 vs 英語）"""
        if not text:
            return "unknown"

        # 日本語文字（ひらがな・カタカナ・漢字）の数をカウント
        japanese_chars = sum(1 for char in text if '\u3040' <= char <= '\u309F' or  # ひらがな
                                                     '\u30A0' <= char <= '\u30FF' or  # カタカナ
                                                     '\u4E00' <= char <= '\u9FFF')    # 漢字

        # 全体の30%以上が日本語文字なら日本語と判定
        if len(text) > 0 and (japanese_chars / len(text)) > 0.3:
            return "ja"
        return "en"


async def main_test():
    """テスト用のメイン関数"""
    # 使用例
    async with TwitterPlaywrightScraper(headless=False) as scraper:
        # 1アカウントのみテスト
        tweets = await scraper.scrape_user_timeline(
            username="elonmusk",
            max_tweets=10,
            since_date=datetime.now() - timedelta(days=7)
        )

        for tweet in tweets:
            print(f"\n{'='*80}")
            print(f"ID: {tweet.tweet_id}")
            print(f"Time: {tweet.timestamp}")
            print(f"Lang: {tweet.lang}")
            print(f"Content: {tweet.content[:100]}...")
            print(f"Engagement: ❤️ {tweet.likes} | 🔁 {tweet.retweets} | 💬 {tweet.replies}")
            print(f"URL: {tweet.url}")


if __name__ == "__main__":
    # テスト実行
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main_test())
