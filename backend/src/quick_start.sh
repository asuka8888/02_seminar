#!/bin/bash
#
# Twitter Scraper Quick Start Script
# クイックスタートスクリプト
#

set -e

echo "=================================="
echo "Twitter Scraper Quick Start"
echo "=================================="
echo ""

# カラーコード
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Python 環境確認
echo -e "${BLUE}[1/7] Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  ✓ Python $python_version"

# 2. 仮想環境確認
echo -e "${BLUE}[2/7] Checking virtual environment...${NC}"
if [ -d "../venv" ]; then
    echo "  ✓ Virtual environment exists"
    source ../venv/bin/activate
else
    echo -e "  ${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv ../venv
    source ../venv/bin/activate
    echo "  ✓ Virtual environment created"
fi

# 3. 依存関係インストール
echo -e "${BLUE}[3/7] Installing dependencies...${NC}"
pip install -q -r ../requirements.txt
echo "  ✓ Dependencies installed"

# 4. Playwright ブラウザ
echo -e "${BLUE}[4/7] Installing Playwright browsers...${NC}"
playwright install chromium > /dev/null 2>&1
echo "  ✓ Playwright chromium installed"

# 5. Ollama 確認
echo -e "${BLUE}[5/7] Checking Ollama...${NC}"
if command -v ollama &> /dev/null; then
    echo "  ✓ Ollama is installed"

    # Ollamaサービス確認
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "  ✓ Ollama service is running"

        # モデル確認
        models=$(ollama list 2>&1)
        if echo "$models" | grep -q "qwen2.5:32b"; then
            echo "  ✓ qwen2.5:32b model found"
        else
            echo -e "  ${YELLOW}⚠ qwen2.5:32b model not found${NC}"
            echo "  Run: ollama pull qwen2.5:32b"
        fi

        if echo "$models" | grep -q "gemma2:9b"; then
            echo "  ✓ gemma2:9b model found"
        else
            echo -e "  ${YELLOW}⚠ gemma2:9b model not found${NC}"
            echo "  Run: ollama pull gemma2:9b"
        fi
    else
        echo -e "  ${YELLOW}⚠ Ollama service not running${NC}"
        echo "  Run: ollama serve"
    fi
else
    echo -e "  ${RED}✗ Ollama not installed${NC}"
    echo "  Install from: https://ollama.com"
    exit 1
fi

# 6. データベース確認
echo -e "${BLUE}[6/7] Checking database...${NC}"
if command -v docker &> /dev/null; then
    # Docker で PostgreSQL を起動
    if docker ps | grep -q postgres; then
        echo "  ✓ PostgreSQL running in Docker"
    else
        echo -e "  ${YELLOW}Starting PostgreSQL with Docker Compose...${NC}"
        cd ../..
        docker-compose up -d postgres redis
        cd backend/src
        sleep 3
        echo "  ✓ PostgreSQL started"
    fi
else
    echo -e "  ${YELLOW}⚠ Docker not found, skipping database check${NC}"
fi

# 7. 設定ファイル確認
echo -e "${BLUE}[7/7] Checking configuration...${NC}"
if [ -f "../.env" ]; then
    echo "  ✓ .env file exists"
else
    echo -e "  ${YELLOW}Creating .env from template...${NC}"
    cp ../.env.example ../.env
    echo "  ✓ .env created (please edit with your settings)"
fi

if [ -f "../../config/twitter_accounts.json" ]; then
    account_count=$(grep -o '"username"' ../../config/twitter_accounts.json | wc -l | tr -d ' ')
    echo "  ✓ twitter_accounts.json found ($account_count accounts)"
else
    echo -e "  ${RED}✗ twitter_accounts.json not found${NC}"
    exit 1
fi

echo ""
echo "=================================="
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "=================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Test Playwright scraper:"
echo "   cd scraper && python twitter_playwright.py"
echo ""
echo "2. Test Ollama analyzer:"
echo "   cd agents && python local_ai_analyzer.py"
echo ""
echo "3. Run 1 cycle (24h for 91 accounts):"
echo "   python main_scraper_pipeline.py"
echo ""
echo "4. Run continuous (7 days):"
echo "   export RUN_MODE=continuous"
echo "   python main_scraper_pipeline.py"
echo ""
echo "5. Run in background:"
echo "   nohup python main_scraper_pipeline.py > scraper.log 2>&1 &"
echo "   tail -f scraper.log"
echo ""
echo "=================================="
