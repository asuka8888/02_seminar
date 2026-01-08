"""
Proxy Manager for Twitter Scraping
プロキシローテーション管理（アカウント凍結回避）
"""
import logging
import random
import asyncio
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import aiohttp

logger = logging.getLogger(__name__)


@dataclass
class ProxyServer:
    """プロキシサーバー情報"""
    server: str  # "http://proxy.example.com:8080"
    username: Optional[str] = None
    password: Optional[str] = None
    proxy_type: str = "http"  # http, socks5
    country: Optional[str] = None
    is_residential: bool = False
    last_used: Optional[datetime] = None
    success_count: int = 0
    error_count: int = 0
    is_healthy: bool = True
    avg_response_time: float = 0.0


class ProxyManager:
    """
    プロキシローテーションマネージャー

    機能:
    1. プロキシサーバーのプール管理
    2. ラウンドロビン/ランダムローテーション
    3. ヘルスチェック
    4. エラーハンドリング・自動除外
    5. レスポンスタイム測定

    推奨プロキシサービス:
    - Bright Data (旧Luminati): $500/月〜 (residential)
    - Smartproxy: $75/月〜 (residential)
    - Oxylabs: $300/月〜 (residential + datacenter)
    - ProxyMesh: $10/月〜 (datacenter)
    """

    def __init__(
        self,
        proxies: List[Dict],
        rotation_strategy: str = "random",  # random, round_robin, least_used
        health_check_interval: int = 300,  # 5分
        max_error_threshold: int = 3,
        enable_health_check: bool = True
    ):
        """
        Args:
            proxies: プロキシ設定のリスト
            rotation_strategy: ローテーション戦略
            health_check_interval: ヘルスチェック間隔（秒）
            max_error_threshold: エラー閾値（この回数を超えたら無効化）
            enable_health_check: ヘルスチェックを有効にするか
        """
        self.rotation_strategy = rotation_strategy
        self.health_check_interval = health_check_interval
        self.max_error_threshold = max_error_threshold
        self.enable_health_check = enable_health_check

        # プロキシサーバーのプール
        self.proxy_pool: List[ProxyServer] = []
        for proxy_config in proxies:
            proxy = ProxyServer(
                server=proxy_config['server'],
                username=proxy_config.get('username'),
                password=proxy_config.get('password'),
                proxy_type=proxy_config.get('type', 'http'),
                country=proxy_config.get('country'),
                is_residential=proxy_config.get('residential', False)
            )
            self.proxy_pool.append(proxy)

        # ラウンドロビン用インデックス
        self.current_index = 0

        # ヘルスチェックタスク
        self.health_check_task = None

        logger.info(f"ProxyManager initialized with {len(self.proxy_pool)} proxies")

    def get_proxy(self) -> Optional[Dict[str, str]]:
        """
        ローテーション戦略に基づいてプロキシを取得

        Returns:
            Playwright用のプロキシ設定辞書
        """
        healthy_proxies = [p for p in self.proxy_pool if p.is_healthy]

        if not healthy_proxies:
            logger.warning("No healthy proxies available!")
            return None

        # 戦略に応じてプロキシを選択
        if self.rotation_strategy == "random":
            proxy = random.choice(healthy_proxies)

        elif self.rotation_strategy == "round_robin":
            proxy = healthy_proxies[self.current_index % len(healthy_proxies)]
            self.current_index += 1

        elif self.rotation_strategy == "least_used":
            # 使用回数が最も少ないプロキシを選択
            proxy = min(healthy_proxies, key=lambda p: p.success_count + p.error_count)

        else:
            logger.warning(f"Unknown strategy '{self.rotation_strategy}', using random")
            proxy = random.choice(healthy_proxies)

        # 最終使用時刻を更新
        proxy.last_used = datetime.now()

        # Playwright用の形式に変換
        proxy_dict = {
            'server': proxy.server
        }

        if proxy.username and proxy.password:
            proxy_dict['username'] = proxy.username
            proxy_dict['password'] = proxy.password

        logger.debug(f"Selected proxy: {proxy.server} ({proxy.country or 'unknown'})")
        return proxy_dict

    def report_success(self, proxy_dict: Dict[str, str], response_time: float = 0.0):
        """
        プロキシの成功を報告

        Args:
            proxy_dict: 使用したプロキシ設定
            response_time: レスポンスタイム（秒）
        """
        server = proxy_dict.get('server')
        proxy = self._find_proxy_by_server(server)

        if proxy:
            proxy.success_count += 1
            proxy.error_count = max(0, proxy.error_count - 1)  # エラーカウントを減少

            # 平均レスポンスタイムを更新
            if proxy.avg_response_time == 0:
                proxy.avg_response_time = response_time
            else:
                proxy.avg_response_time = (proxy.avg_response_time * 0.8) + (response_time * 0.2)

            logger.debug(
                f"Proxy success: {server} "
                f"(success={proxy.success_count}, errors={proxy.error_count}, "
                f"avg_time={proxy.avg_response_time:.2f}s)"
            )

    def report_error(self, proxy_dict: Dict[str, str], error: Exception):
        """
        プロキシのエラーを報告

        Args:
            proxy_dict: 使用したプロキシ設定
            error: 発生したエラー
        """
        server = proxy_dict.get('server')
        proxy = self._find_proxy_by_server(server)

        if proxy:
            proxy.error_count += 1

            logger.warning(
                f"Proxy error: {server} - {error} "
                f"(errors={proxy.error_count}/{self.max_error_threshold})"
            )

            # エラー閾値を超えたら無効化
            if proxy.error_count >= self.max_error_threshold:
                proxy.is_healthy = False
                logger.error(f"Proxy {server} marked as unhealthy (too many errors)")

    def _find_proxy_by_server(self, server: str) -> Optional[ProxyServer]:
        """サーバーアドレスからプロキシオブジェクトを検索"""
        for proxy in self.proxy_pool:
            if proxy.server == server:
                return proxy
        return None

    async def health_check(self):
        """全プロキシのヘルスチェック"""
        logger.info("Running proxy health check...")

        test_url = "https://httpbin.org/ip"  # IPアドレス確認用

        for proxy in self.proxy_pool:
            try:
                proxy_url = proxy.server
                if proxy.username and proxy.password:
                    # 認証情報を含むプロキシURL
                    protocol = proxy.proxy_type
                    host_port = proxy.server.replace(f'{protocol}://', '')
                    proxy_url = f"{protocol}://{proxy.username}:{proxy.password}@{host_port}"

                start_time = datetime.now()

                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        test_url,
                        proxy=proxy_url,
                        timeout=aiohttp.ClientTimeout(total=10)
                    ) as response:
                        if response.status == 200:
                            response_time = (datetime.now() - start_time).total_seconds()

                            # プロキシが正常
                            proxy.is_healthy = True
                            proxy.error_count = max(0, proxy.error_count - 1)
                            proxy.avg_response_time = response_time

                            data = await response.json()
                            logger.info(
                                f"✓ Proxy {proxy.server} healthy "
                                f"(IP: {data.get('origin', 'unknown')}, "
                                f"time: {response_time:.2f}s)"
                            )
                        else:
                            raise Exception(f"HTTP {response.status}")

            except Exception as e:
                proxy.error_count += 1
                logger.warning(f"✗ Proxy {proxy.server} unhealthy: {e}")

                if proxy.error_count >= self.max_error_threshold:
                    proxy.is_healthy = False
                    logger.error(f"Proxy {proxy.server} marked as unhealthy")

            # レート制限回避
            await asyncio.sleep(1)

        healthy_count = sum(1 for p in self.proxy_pool if p.is_healthy)
        logger.info(f"Health check complete: {healthy_count}/{len(self.proxy_pool)} proxies healthy")

    async def start_health_check_loop(self):
        """ヘルスチェックループを開始"""
        if not self.enable_health_check:
            logger.info("Health check disabled")
            return

        logger.info(f"Starting health check loop (interval: {self.health_check_interval}s)")

        while True:
            await self.health_check()
            await asyncio.sleep(self.health_check_interval)

    def get_statistics(self) -> Dict:
        """プロキシプールの統計情報を取得"""
        healthy_proxies = [p for p in self.proxy_pool if p.is_healthy]

        stats = {
            'total_proxies': len(self.proxy_pool),
            'healthy_proxies': len(healthy_proxies),
            'unhealthy_proxies': len(self.proxy_pool) - len(healthy_proxies),
            'total_success': sum(p.success_count for p in self.proxy_pool),
            'total_errors': sum(p.error_count for p in self.proxy_pool),
            'avg_response_time': sum(p.avg_response_time for p in healthy_proxies) / len(healthy_proxies) if healthy_proxies else 0,
            'proxy_details': [
                {
                    'server': p.server,
                    'country': p.country,
                    'residential': p.is_residential,
                    'healthy': p.is_healthy,
                    'success': p.success_count,
                    'errors': p.error_count,
                    'avg_time': p.avg_response_time
                }
                for p in self.proxy_pool
            ]
        }

        return stats


# プロキシサービスの設定例
def get_example_proxy_configs() -> List[Dict]:
    """
    プロキシサービスの設定例

    実際の運用では環境変数や設定ファイルから読み込む
    """
    return [
        # Smartproxy (Residential)
        {
            'server': 'http://gate.smartproxy.com:7000',
            'username': 'your_smartproxy_username',
            'password': 'your_smartproxy_password',
            'type': 'http',
            'country': 'JP',  # 日本のIP
            'residential': True
        },
        # Bright Data (旧Luminati)
        {
            'server': 'http://zproxy.lum-superproxy.io:22225',
            'username': 'your_brightdata_username',
            'password': 'your_brightdata_password',
            'type': 'http',
            'country': 'US',
            'residential': True
        },
        # Oxylabs (Datacenter)
        {
            'server': 'http://dc.oxylabs.io:8000',
            'username': 'your_oxylabs_username',
            'password': 'your_oxylabs_password',
            'type': 'http',
            'country': 'DE',
            'residential': False
        },
        # 無料プロキシ（推奨しない - テスト用のみ）
        {
            'server': 'http://proxy.example.com:8080',
            'type': 'http',
            'country': 'unknown',
            'residential': False
        }
    ]


async def main_test():
    """テスト用のメイン関数"""
    # テスト用のプロキシ設定（実際には動作しない例）
    test_proxies = [
        {
            'server': 'http://proxy1.example.com:8080',
            'country': 'US',
            'residential': True
        },
        {
            'server': 'http://proxy2.example.com:8080',
            'country': 'JP',
            'residential': False
        },
        {
            'server': 'http://proxy3.example.com:8080',
            'username': 'user',
            'password': 'pass',
            'country': 'GB',
            'residential': True
        }
    ]

    # マネージャー作成
    manager = ProxyManager(
        proxies=test_proxies,
        rotation_strategy="random",
        enable_health_check=False  # テストではヘルスチェック無効
    )

    # プロキシ取得テスト
    print("\n" + "="*80)
    print("Proxy Rotation Test")
    print("="*80)

    for i in range(10):
        proxy = manager.get_proxy()
        print(f"{i+1}. {proxy}")

    # 統計情報
    print("\n" + "="*80)
    print("Proxy Statistics")
    print("="*80)

    stats = manager.get_statistics()
    print(f"Total: {stats['total_proxies']}")
    print(f"Healthy: {stats['healthy_proxies']}")
    print(f"Unhealthy: {stats['unhealthy_proxies']}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main_test())
