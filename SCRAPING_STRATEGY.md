# Xスクレイピング戦略 & アカウント凍結回避ガイド
## Twitter API不使用・安全なデータ収集設計

**作成日**: 2026年1月5日
**バージョン**: 1.0
**対象**: 91アカウント（1日1回チェック）

---

## 📋 基本方針

### API不使用の理由
- ✅ Twitter API有料化により高コスト
- ✅ レート制限が厳しい
- ✅ スクレイピングで十分な情報取得可能

### 安全第一の設計
- ✅ アカウント凍結リスクを最小化
- ✅ 1日で91アカウントをゆっくりチェック
- ✅ 人間の行動パターンを模倣

---

## 🕐 チェック間隔設定（1日サイクル）

### 基本スケジュール

| 時間帯 | アカウント数 | 間隔 | 備考 |
|--------|------------|------|------|
| **06:00 - 12:00** | 30件 | 12分間隔 | 朝の活動時間（人間らしい） |
| **12:00 - 14:00** | 10件 | 12分間隔 | 昼休み（アクセス少なめ） |
| **14:00 - 18:00** | 25件 | 10分間隔 | 午後の活動時間 |
| **18:00 - 22:00** | 20件 | 12分間隔 | 夜の活動時間 |
| **22:00 - 06:00** | 6件 | 80分間隔 | 深夜（最小限のアクセス） |

**総計**: 91アカウント / 24時間
**平均間隔**: 約15.8分

---

## 🛡️ アカウント凍結回避策（10の対策）

### 1. アクセス間隔のランダム化

```python
import random
import time

def get_random_interval():
    """10-20分のランダム間隔を生成"""
    base = 600  # 10分（秒）
    variance = 600  # ±10分
    interval = base + random.randint(-variance//2, variance//2)
    return interval

# 使用例
time.sleep(get_random_interval())  # 10〜20分待機
```

**効果**:
- ✅ Bot的な規則正しいアクセスを回避
- ✅ 人間のランダムな行動パターンを模倣

---

### 2. User-Agentのローテーション

```python
USER_AGENTS = [
    # Chrome (Windows)
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',

    # Chrome (Mac)
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',

    # Firefox (Windows)
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',

    # Safari (Mac)
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',

    # Edge (Windows)
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)
```

**効果**:
- ✅ 異なるブラウザからのアクセスに見える
- ✅ 単一デバイス検出を回避

---

### 3. プロキシローテーション（推奨）

```python
# プロキシプロバイダー推奨
PROXY_PROVIDERS = {
    "free": [
        # 無料プロキシ（品質は低い）
        "https://free-proxy-list.net/",
        "https://www.proxy-list.download/"
    ],
    "paid": [
        # 有料プロキシ（推奨）
        "Bright Data (元Luminati)",  # 月額$500〜、高品質
        "Smartproxy",                  # 月額$75〜、コスパ良
        "IPRoyal",                     # 月額$50〜、安価
    ]
}

# 実装例（有料プロキシ使用）
PROXIES = [
    "http://user:pass@proxy1.example.com:8080",
    "http://user:pass@proxy2.example.com:8080",
    "http://user:pass@proxy3.example.com:8080",
    # 10-20個のプロキシをローテーション
]

def get_random_proxy():
    return random.choice(PROXIES)
```

**効果**:
- ✅ 異なるIPアドレスからのアクセス
- ✅ 大量アクセス検知を回避

**予算**:
- 無料: $0（品質低、凍結リスク高）
- 有料: $50-100/月（推奨、安全性高）

---

### 4. セッション管理とCookie保持

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class SafeTwitterScraper:
    def __init__(self):
        self.session = requests.Session()

        # リトライ戦略
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Cookie保存（ログイン状態を維持）
        self.cookies_file = "twitter_cookies.json"
        self.load_cookies()

    def load_cookies(self):
        """前回のCookieを読み込み"""
        try:
            with open(self.cookies_file, 'r') as f:
                cookies = json.load(f)
                self.session.cookies.update(cookies)
        except FileNotFoundError:
            pass

    def save_cookies(self):
        """Cookieを保存"""
        with open(self.cookies_file, 'w') as f:
            json.dump(self.session.cookies.get_dict(), f)
```

**効果**:
- ✅ ログイン状態を維持
- ✅ 毎回ログインを回避（疑わしい行動を減らす）

---

### 5. ヘッドレスブラウザ検出回避（Playwright使用）

```python
from playwright.sync_api import sync_playwright

def create_stealth_browser():
    """検出されにくいブラウザを作成"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
            ]
        )

        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent=get_random_user_agent(),
            locale='ja-JP',
            timezone_id='Asia/Tokyo',
        )

        # WebDriverプロパティを隠蔽
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        page = context.new_page()
        return page
```

**効果**:
- ✅ ヘッドレスブラウザとして検出されない
- ✅ 自動化ツール検知を回避

---

### 6. 人間らしい行動パターンの模倣

```python
import random
import time

class HumanBehavior:
    @staticmethod
    def random_scroll(page):
        """ランダムにスクロール"""
        scroll_amount = random.randint(300, 800)
        page.evaluate(f"window.scrollBy(0, {scroll_amount})")
        time.sleep(random.uniform(0.5, 2.0))

    @staticmethod
    def random_mouse_movement(page):
        """ランダムにマウス移動"""
        x = random.randint(100, 1000)
        y = random.randint(100, 800)
        page.mouse.move(x, y)
        time.sleep(random.uniform(0.1, 0.5))

    @staticmethod
    def random_pause():
        """ランダムに一時停止（考える時間）"""
        time.sleep(random.uniform(1.0, 3.0))

# 使用例
def scrape_with_human_behavior(page, url):
    page.goto(url)
    HumanBehavior.random_pause()  # ページ読み込み後の考える時間
    HumanBehavior.random_scroll(page)  # スクロール
    HumanBehavior.random_mouse_movement(page)  # マウス移動
    # データ取得
    content = page.content()
    return content
```

**効果**:
- ✅ Bot的な即座の行動を回避
- ✅ 人間の自然な閲覧パターンを再現

---

### 7. エラー処理とリトライ戦略

```python
from tenacity import retry, stop_after_attempt, wait_exponential

class TwitterScraper:
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=60, max=300),
    )
    def fetch_account(self, username):
        """アカウント情報を取得（失敗時は自動リトライ）"""
        try:
            page = self.create_browser()
            url = f"https://x.com/{username}"

            response = page.goto(url)

            # ステータスコードチェック
            if response.status == 429:  # レート制限
                print(f"Rate limited. Waiting 15 minutes...")
                time.sleep(900)  # 15分待機
                raise Exception("Rate limited")

            if response.status == 403:  # アクセス拒否
                print(f"Access denied. Switching proxy...")
                self.switch_proxy()
                raise Exception("Access denied")

            # データ取得
            tweets = self.extract_tweets(page)
            return tweets

        except Exception as e:
            print(f"Error fetching {username}: {e}")
            raise
        finally:
            page.close()
```

**効果**:
- ✅ 一時的なエラーから自動復旧
- ✅ レート制限を検知して自動待機

---

### 8. アクセスログの記録と分析

```python
import logging
from datetime import datetime

class AccessLogger:
    def __init__(self):
        logging.basicConfig(
            filename='twitter_access.log',
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )

    def log_access(self, username, status, proxy=None):
        """アクセスログを記録"""
        logging.info(f"Account: {username} | Status: {status} | Proxy: {proxy}")

    def check_suspicious_pattern(self):
        """疑わしいパターンを検出"""
        # 短時間に大量アクセスしていないかチェック
        # エラー率が高くないかチェック
        pass
```

**効果**:
- ✅ アクセスパターンを監視
- ✅ 問題を早期発見

---

### 9. 時間帯別のアクセス戦略

```python
from datetime import datetime

class TimeBasedStrategy:
    @staticmethod
    def get_interval_for_current_time():
        """現在時刻に応じた待機時間を返す"""
        hour = datetime.now().hour

        if 6 <= hour < 12:  # 朝（活動的）
            return random.randint(600, 900)  # 10-15分
        elif 12 <= hour < 14:  # 昼（控えめ）
            return random.randint(900, 1200)  # 15-20分
        elif 14 <= hour < 18:  # 午後（活動的）
            return random.randint(600, 900)  # 10-15分
        elif 18 <= hour < 22:  # 夜（活動的）
            return random.randint(600, 900)  # 10-15分
        else:  # 深夜（最小限）
            return random.randint(3600, 7200)  # 1-2時間

    @staticmethod
    def should_access_now():
        """今アクセスすべきか判定"""
        hour = datetime.now().hour

        # 深夜2-5時はアクセスしない（メンテナンス時間）
        if 2 <= hour < 5:
            return False

        return True
```

**効果**:
- ✅ 人間の活動パターンに合わせる
- ✅ 深夜の不自然なアクセスを回避

---

### 10. 複数アカウントの使用（最終手段）

```python
TWITTER_ACCOUNTS = [
    {
        "username": "scraper_account_1",
        "password": "password1",
        "cookie_file": "cookies_1.json"
    },
    {
        "username": "scraper_account_2",
        "password": "password2",
        "cookie_file": "cookies_2.json"
    },
    # 3-5個のアカウントをローテーション
]

class MultiAccountScraper:
    def __init__(self):
        self.accounts = TWITTER_ACCOUNTS
        self.current_account_index = 0

    def rotate_account(self):
        """アカウントを切り替え"""
        self.current_account_index = (self.current_account_index + 1) % len(self.accounts)
        current = self.accounts[self.current_account_index]
        print(f"Switching to account: {current['username']}")
        return current
```

**効果**:
- ✅ 1アカウントあたりの負荷を分散
- ✅ 1つ凍結されても他で継続可能

**注意**:
- ⚠️ Twitterの利用規約に注意
- ⚠️ 最終手段として使用

---

## 🔧 推奨スクレイピングツール

### 1. Playwright（最推奨）

**特徴**:
- ✅ ヘッドレスブラウザ検出回避が容易
- ✅ JavaScriptレンダリング対応
- ✅ 高速で安定
- ✅ ステルス機能充実

**インストール**:
```bash
pip install playwright
playwright install chromium
```

**基本実装**:
```python
from playwright.sync_api import sync_playwright
import time
import random

class TwitterPlaywrightScraper:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )
        self.context = self.browser.new_context(
            user_agent=get_random_user_agent(),
            viewport={'width': 1920, 'height': 1080}
        )
        self.page = self.context.new_page()

    def scrape_account(self, username):
        """アカウントの投稿を取得"""
        url = f"https://x.com/{username}"

        # ランダムな待機時間
        time.sleep(random.uniform(2, 5))

        # ページへアクセス
        self.page.goto(url, wait_until='networkidle')

        # スクロールして投稿を読み込み
        for _ in range(3):
            self.page.evaluate('window.scrollBy(0, 1000)')
            time.sleep(random.uniform(1, 2))

        # 投稿を抽出
        tweets = self.page.query_selector_all('article[data-testid="tweet"]')

        results = []
        for tweet in tweets[:10]:  # 最新10件
            try:
                text = tweet.query_selector('[data-testid="tweetText"]').inner_text()
                time_elem = tweet.query_selector('time')
                timestamp = time_elem.get_attribute('datetime') if time_elem else None

                results.append({
                    'text': text,
                    'timestamp': timestamp,
                    'username': username
                })
            except:
                continue

        return results

    def close(self):
        self.browser.close()
        self.playwright.stop()
```

---

### 2. Selenium（代替案）

**特徴**:
- ✅ 成熟したエコシステム
- ✅ 豊富なドキュメント
- ❌ Playwrightより遅い
- ❌ ヘッドレス検出されやすい

---

### 3. BeautifulSoup + Requests（非推奨）

**理由**:
- ❌ JavaScriptレンダリング非対応
- ❌ TwitterはReactで動的生成のため取得困難
- ❌ すぐにブロックされる

---

## 📊 1日のスクレイピングスケジュール例

```python
import schedule
import time
from datetime import datetime

class DailyScrapingScheduler:
    def __init__(self):
        self.accounts = self.load_91_accounts()
        self.scraper = TwitterPlaywrightScraper()

    def setup_schedule(self):
        """1日のスケジュールを設定"""

        # 朝の30アカウント（06:00-12:00）
        morning_accounts = self.accounts[0:30]
        for i, account in enumerate(morning_accounts):
            time_str = f"06:{i*12:02d}"  # 06:00, 06:12, 06:24...
            schedule.every().day.at(time_str).do(
                self.safe_scrape, account
            )

        # 昼の10アカウント（12:00-14:00）
        lunch_accounts = self.accounts[30:40]
        for i, account in enumerate(lunch_accounts):
            time_str = f"12:{i*12:02d}"
            schedule.every().day.at(time_str).do(
                self.safe_scrape, account
            )

        # 午後の25アカウント（14:00-18:00）
        afternoon_accounts = self.accounts[40:65]
        for i, account in enumerate(afternoon_accounts):
            hour = 14 + (i * 10) // 60
            minute = (i * 10) % 60
            time_str = f"{hour:02d}:{minute:02d}"
            schedule.every().day.at(time_str).do(
                self.safe_scrape, account
            )

        # 夜の20アカウント（18:00-22:00）
        evening_accounts = self.accounts[65:85]
        for i, account in enumerate(evening_accounts):
            hour = 18 + (i * 12) // 60
            minute = (i * 12) % 60
            time_str = f"{hour:02d}:{minute:02d}"
            schedule.every().day.at(time_str).do(
                self.safe_scrape, account
            )

        # 深夜の6アカウント（22:00-06:00）
        night_accounts = self.accounts[85:91]
        night_times = ["22:00", "23:20", "00:40", "02:00", "03:20", "04:40"]
        for account, time_str in zip(night_accounts, night_times):
            schedule.every().day.at(time_str).do(
                self.safe_scrape, account
            )

    def safe_scrape(self, account):
        """安全にスクレイピング"""
        try:
            print(f"[{datetime.now()}] Scraping: {account['username']}")

            # ランダム待機（±3分）
            jitter = random.randint(-180, 180)
            if jitter > 0:
                time.sleep(jitter)

            # スクレイピング実行
            tweets = self.scraper.scrape_account(account['username'])

            # データベースに保存
            self.save_to_db(tweets)

            print(f"✓ Success: {account['username']} ({len(tweets)} tweets)")

        except Exception as e:
            print(f"✗ Error: {account['username']} - {e}")

    def run(self):
        """スケジューラー起動"""
        self.setup_schedule()
        print("Daily scraping scheduler started...")

        while True:
            schedule.run_pending()
            time.sleep(60)  # 1分ごとにチェック

# 起動
if __name__ == "__main__":
    scheduler = DailyScrapingScheduler()
    scheduler.run()
```

---

## 🚨 凍結された場合の対処法

### 即座に行うこと

1. **スクレイピングを即座に停止**
   ```bash
   pkill -f twitter_scraper
   ```

2. **アクセスログを確認**
   - 何が原因か特定
   - 短時間の大量アクセス？
   - 特定のアカウントへの集中アクセス？

3. **待機期間を設ける**
   - 24-48時間は完全に停止
   - Twitterの監視が緩むのを待つ

4. **戦略を見直す**
   - アクセス間隔をさらに延ばす
   - プロキシを変更
   - User-Agentを変更
   - 異なるアカウントを使用

---

## 📈 推奨設定まとめ

| 項目 | 推奨値 | 理由 |
|------|--------|------|
| **アクセス間隔** | 10-20分（ランダム） | Bot検知回避 |
| **1日のアクセス数** | 91件 | 適度な負荷 |
| **プロキシ** | 有料10-20個ローテーション | IP分散 |
| **User-Agent** | 5-10種類ローテーション | デバイス分散 |
| **スクレイピングツール** | Playwright | 検出回避性能高 |
| **リトライ回数** | 3回（指数バックオフ） | 安定性向上 |
| **深夜アクセス** | 最小限（6件のみ） | 不自然さ回避 |

---

## 💰 コスト試算

### 推奨構成の月額コスト

| 項目 | コスト | 備考 |
|------|--------|------|
| **サーバー** | $20-50/月 | VPS（2GB RAM） |
| **プロキシ** | $50-100/月 | 有料プロキシサービス |
| **合計** | **$70-150/月** | Twitter API ($100/月)より安価 |

### 無料構成（リスク高）

| 項目 | コスト | 備考 |
|------|--------|------|
| **サーバー** | $0 | ローカル実行 |
| **プロキシ** | $0 | プロキシなし |
| **合計** | **$0/月** | 凍結リスク高 |

---

## 🎯 次のステップ

1. **Playwright環境構築**
   ```bash
   pip install playwright schedule
   playwright install chromium
   ```

2. **基本スクレイパーの実装**
   - 1アカウントでテスト
   - 動作確認後、91アカウントに拡大

3. **スケジューラーの設定**
   - 1日のスケジュール設定
   - 自動実行の確認

4. **監視とログ**
   - アクセスログの記録
   - エラー監視

---

**安全第一で運用しましょう！** 🛡️
