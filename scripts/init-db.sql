-- Financial Intelligence System Database Initialization
-- 初期化スクリプト

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- Full-text search

-- 初期データベースの確認
SELECT 'Database fin_intel initialized successfully' AS status;

-- タイムゾーン設定
SET timezone = 'Asia/Tokyo';

-- 初期化完了メッセージ
DO $$
BEGIN
    RAISE NOTICE 'Financial Intelligence System Database initialized at %', NOW();
END $$;
