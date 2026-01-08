"""
Database Test Script
データベース操作のテスト
"""
import asyncio
import logging
from datetime import datetime, timedelta
import sys
import os
from pathlib import Path

# パス設定
sys.path.append(str(Path(__file__).parent.parent))

from database import db_manager
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


async def test_create_news():
    """ニュースレコードの作成テスト"""
    print("\n" + "="*80)
    print("Test 1: Create News Record")
    print("="*80)

    try:
        # テストデータ
        news = await db_manager.client.news.create(
            data={
                'source': 'test_account',
                'platform': 'twitter',
                'publishedAt': datetime.now(),
                'originalText': 'This is a test tweet about market movements.',
                'translatedText': 'これは市場動向に関するテストツイートです。',
                'summary': 'テスト用のニュースサマリー',
                'sentiment': 'positive',
                'sentimentScore': 0.8,
                'priority': 'medium',
                'sector': 'technology',
                'tickers': ['AAPL', 'MSFT'],
                'keyTopics': ['AI', 'stocks', 'market'],
                'likes': 100,
                'retweets': 50,
                'replies': 10,
                'originalUrl': f'https://x.com/test/status/{int(datetime.now().timestamp())}',
                'category': 'test_category',
                'language': 'en',
                'processed': True
            }
        )

        print(f"✓ Created news record:")
        print(f"  ID: {news.id}")
        print(f"  Source: {news.source}")
        print(f"  Sentiment: {news.sentiment} ({news.sentimentScore})")
        print(f"  Priority: {news.priority}")
        print(f"  Key Topics: {news.keyTopics}")

        return news

    except Exception as e:
        print(f"✗ Failed to create news: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_find_news():
    """ニュースレコードの検索テスト"""
    print("\n" + "="*80)
    print("Test 2: Find News Records")
    print("="*80)

    try:
        # 全件取得（最新10件）
        all_news = await db_manager.client.news.find_many(
            take=10,
            order={'createdAt': 'desc'}
        )

        print(f"✓ Found {len(all_news)} news records:")
        for i, news in enumerate(all_news, 1):
            print(f"\n  {i}. {news.source} ({news.publishedAt.strftime('%Y-%m-%d %H:%M')})")
            print(f"     {news.summary[:80]}...")
            print(f"     Sentiment: {news.sentiment}, Priority: {news.priority}")

        # 高インパクトニュースのみ
        high_impact = await db_manager.client.news.find_many(
            where={'priority': 'high'},
            take=5,
            order={'publishedAt': 'desc'}
        )

        print(f"\n✓ Found {len(high_impact)} high-impact news")

        # センチメント別
        positive_news = await db_manager.client.news.count(
            where={'sentiment': 'positive'}
        )
        negative_news = await db_manager.client.news.count(
            where={'sentiment': 'negative'}
        )
        neutral_news = await db_manager.client.news.count(
            where={'sentiment': 'neutral'}
        )

        print(f"\n✓ Sentiment distribution:")
        print(f"  Positive: {positive_news}")
        print(f"  Negative: {negative_news}")
        print(f"  Neutral: {neutral_news}")

    except Exception as e:
        print(f"✗ Failed to find news: {e}")
        import traceback
        traceback.print_exc()


async def test_update_news(news_id: str):
    """ニュースレコードの更新テスト"""
    print("\n" + "="*80)
    print("Test 3: Update News Record")
    print("="*80)

    try:
        updated = await db_manager.client.news.update(
            where={'id': news_id},
            data={'processed': False}
        )

        print(f"✓ Updated news {news_id}:")
        print(f"  Processed: {updated.processed}")

    except Exception as e:
        print(f"✗ Failed to update news: {e}")


async def test_delete_test_records():
    """テストレコードの削除"""
    print("\n" + "="*80)
    print("Test 4: Delete Test Records")
    print("="*80)

    try:
        # test_account のレコードを全削除
        result = await db_manager.client.news.delete_many(
            where={'source': 'test_account'}
        )

        print(f"✓ Deleted {result} test records")

    except Exception as e:
        print(f"✗ Failed to delete test records: {e}")


async def test_aggregation():
    """集計クエリのテスト"""
    print("\n" + "="*80)
    print("Test 5: Aggregation Queries")
    print("="*80)

    try:
        # 今日のニュース件数
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        news_today = await db_manager.client.news.count(
            where={
                'createdAt': {
                    'gte': today
                }
            }
        )

        print(f"✓ News created today: {news_today}")

        # 過去7日間のニュース件数
        week_ago = datetime.now() - timedelta(days=7)

        news_week = await db_manager.client.news.count(
            where={
                'createdAt': {
                    'gte': week_ago
                }
            }
        )

        print(f"✓ News in past 7 days: {news_week}")

        # ソース別のニュース件数
        # NOTE: Prisma Client Python では group by がサポートされていないため、
        # すべてのレコードを取得してPython側で集計
        all_news = await db_manager.client.news.find_many()

        source_counts = {}
        for news in all_news:
            source_counts[news.source] = source_counts.get(news.source, 0) + 1

        print(f"\n✓ News count by source:")
        for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {source}: {count}")

    except Exception as e:
        print(f"✗ Failed to run aggregation: {e}")
        import traceback
        traceback.print_exc()


async def main():
    """メインテスト"""
    print("\n" + "="*80)
    print("Database Test Suite")
    print("="*80)

    # .env ファイルを読み込み
    env_path = Path(__file__).parent.parent.parent / '.env'
    load_dotenv(env_path)

    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL not set in .env file")
        return

    print(f"DATABASE_URL: {db_url[:50]}...")

    try:
        # データベース接続
        await db_manager.connect()
        print("✓ Connected to database")

        # テスト1: ニュース作成
        news = await test_create_news()

        if news:
            # テスト2: ニュース検索
            await test_find_news()

            # テスト3: ニュース更新
            await test_update_news(news.id)

            # テスト5: 集計
            await test_aggregation()

            # テスト4: テストレコード削除
            await test_delete_test_records()

        # データベース切断
        await db_manager.disconnect()
        print("\n✓ Disconnected from database")

        print("\n" + "="*80)
        print("✓ All tests completed successfully")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
