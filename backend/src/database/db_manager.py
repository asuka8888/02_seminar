"""
Database Manager - Prisma Client Python 接続管理
"""
import logging
import asyncio
from typing import Optional
from contextlib import asynccontextmanager
import os

try:
    from prisma import Prisma
    from prisma.models import News
except ImportError:
    raise ImportError(
        "Prisma Client Python not installed. "
        "Run: pip install prisma && prisma generate"
    )

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Prisma Client の接続管理

    シングルトンパターンで実装し、アプリケーション全体で1つの接続を共有
    """

    _instance: Optional['DatabaseManager'] = None
    _prisma: Optional[Prisma] = None
    _is_connected: bool = False

    def __new__(cls):
        """シングルトンインスタンス"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def client(self) -> Prisma:
        """Prisma Client を取得"""
        if self._prisma is None:
            self._prisma = Prisma()
        return self._prisma

    async def connect(self):
        """データベースに接続"""
        if self._is_connected:
            logger.debug("Database already connected")
            return

        try:
            logger.info("Connecting to database...")
            await self.client.connect()
            self._is_connected = True
            logger.info("✓ Database connected successfully")

        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    async def disconnect(self):
        """データベースから切断"""
        if not self._is_connected:
            logger.debug("Database already disconnected")
            return

        try:
            logger.info("Disconnecting from database...")
            await self.client.disconnect()
            self._is_connected = False
            logger.info("✓ Database disconnected")

        except Exception as e:
            logger.error(f"Failed to disconnect from database: {e}")
            raise

    @asynccontextmanager
    async def session(self):
        """
        データベースセッションのコンテキストマネージャー

        使用例:
            db = DatabaseManager()
            async with db.session():
                await db.client.news.create(...)
        """
        try:
            await self.connect()
            yield self.client
        finally:
            # セッション終了時は接続を維持（パフォーマンス向上）
            pass

    async def health_check(self) -> bool:
        """
        データベース接続のヘルスチェック

        Returns:
            接続が正常なら True
        """
        try:
            # シンプルなクエリで接続確認
            await self.client.execute_raw("SELECT 1")
            logger.debug("Database health check: OK")
            return True

        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

    async def get_stats(self) -> dict:
        """
        データベース統計情報を取得

        Returns:
            統計情報の辞書
        """
        try:
            stats = {}

            # ニュース件数
            stats['total_news'] = await self.client.news.count()

            # 今日のニュース件数
            from datetime import datetime, timedelta
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            stats['news_today'] = await self.client.news.count(
                where={
                    'createdAt': {
                        'gte': today
                    }
                }
            )

            # 高インパクトニュース件数
            stats['high_impact_news'] = await self.client.news.count(
                where={
                    'priority': 'high'
                }
            )

            # 処理済みニュース件数
            stats['processed_news'] = await self.client.news.count(
                where={
                    'processed': True
                }
            )

            return stats

        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            return {}


# グローバルインスタンス（シングルトン）
db_manager = DatabaseManager()


async def get_db() -> Prisma:
    """
    Dependency Injection 用の関数

    FastAPI などで使用:
        @app.get("/news")
        async def get_news(db: Prisma = Depends(get_db)):
            return await db.news.find_many()
    """
    if not db_manager._is_connected:
        await db_manager.connect()
    return db_manager.client


async def test_connection():
    """接続テスト用の関数"""
    print("\n" + "="*80)
    print("Database Connection Test")
    print("="*80)

    # 環境変数確認
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL environment variable not set")
        print("   Please set it in .env file:")
        print("   DATABASE_URL=postgresql://user:password@localhost:5432/dbname")
        return

    print(f"DATABASE_URL: {db_url[:50]}...")

    # 接続テスト
    db = DatabaseManager()

    try:
        await db.connect()
        print("✓ Connection successful")

        # ヘルスチェック
        is_healthy = await db.health_check()
        print(f"✓ Health check: {'OK' if is_healthy else 'FAILED'}")

        # 統計情報
        stats = await db.get_stats()
        print("\nDatabase Statistics:")
        for key, value in stats.items():
            print(f"  - {key}: {value}")

        # 切断
        await db.disconnect()
        print("\n✓ Test completed successfully")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # テスト実行
    logging.basicConfig(level=logging.INFO)

    # .env ファイルを読み込み
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

    asyncio.run(test_connection())
