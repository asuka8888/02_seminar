#!/bin/bash
#
# Database Setup Script
# PostgreSQL + Prisma Client Python のセットアップ
#

set -e

echo "=================================="
echo "Database Setup for Scraper System"
echo "=================================="
echo ""

# カラーコード
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. 環境変数確認
echo -e "${BLUE}[1/6] Checking environment variables...${NC}"
if [ ! -f ".env" ]; then
    echo -e "  ${YELLOW}⚠ .env file not found${NC}"
    echo "  Creating from .env.example..."
    cp .env.example .env
    echo -e "  ${GREEN}✓ .env created${NC}"
    echo "  Please edit .env with your DATABASE_URL"
    exit 1
fi

# DATABASE_URL の確認
source .env
if [ -z "$DATABASE_URL" ]; then
    echo -e "  ${RED}✗ DATABASE_URL not set in .env${NC}"
    echo "  Please set DATABASE_URL in .env file:"
    echo "  DATABASE_URL=postgresql://finuser:finpass123@localhost:5432/fin_intel"
    exit 1
fi

echo -e "  ${GREEN}✓ DATABASE_URL found${NC}"

# 2. Prisma Client Python のインストール
echo -e "${BLUE}[2/6] Installing Prisma Client Python...${NC}"
pip install -q prisma
echo -e "  ${GREEN}✓ Prisma installed${NC}"

# 3. Prisma Client の生成
echo -e "${BLUE}[3/6] Generating Prisma Client...${NC}"
prisma generate --schema=schema.prisma
echo -e "  ${GREEN}✓ Prisma Client generated${NC}"

# 4. データベースマイグレーション
echo -e "${BLUE}[4/6] Running database migrations...${NC}"
echo "  This will create all tables in the database..."

# Prisma migrate は Prisma Client Python ではサポートされていないため、
# Prisma CLI (Node.js版) または手動でマイグレーションを実行する必要があります

# オプション1: Prisma CLI (Node.js) を使用
if command -v npx &> /dev/null; then
    echo "  Using Prisma CLI (Node.js)..."
    npx prisma db push --schema=schema.prisma --skip-generate
    echo -e "  ${GREEN}✓ Database schema pushed${NC}"
else
    echo -e "  ${YELLOW}⚠ npx not found, skipping automatic migration${NC}"
    echo "  Please run manually:"
    echo "    npx prisma db push --schema=schema.prisma"
fi

# 5. データベース接続テスト
echo -e "${BLUE}[5/6] Testing database connection...${NC}"
python src/database/db_manager.py
if [ $? -eq 0 ]; then
    echo -e "  ${GREEN}✓ Database connection test passed${NC}"
else
    echo -e "  ${RED}✗ Database connection test failed${NC}"
    exit 1
fi

# 6. 完了
echo ""
echo "=================================="
echo -e "${GREEN}✓ Database Setup Complete!${NC}"
echo "=================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Verify database schema:"
echo "   npx prisma studio --schema=schema.prisma"
echo ""
echo "2. Test scraper with database:"
echo "   python src/main_scraper_pipeline.py"
echo ""
echo "3. Check database stats:"
echo "   python src/database/db_manager.py"
echo ""
echo "=================================="
