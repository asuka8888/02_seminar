#!/bin/bash

# Facebook MCP Server クイック起動スクリプト
# 作成日: 2026-01-05

# 色の定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================================"
echo -e "${BLUE}🚀 Facebook MCP Server 起動${NC}"
echo "================================================"
echo ""

# ディレクトリの存在確認
MCP_DIR="$HOME/mcp-servers/facebook-mcp-server"

if [ ! -d "$MCP_DIR" ]; then
    echo -e "${RED}❌ エラー:${NC} Facebook MCP Serverが見つかりません"
    echo ""
    echo "まず、セットアップスクリプトを実行してください:"
    echo "  bash ~/mcp-servers-setup.sh"
    echo ""
    exit 1
fi

# .envファイルの確認
if [ ! -f "$MCP_DIR/.env" ]; then
    echo -e "${RED}❌ エラー:${NC} .envファイルが見つかりません"
    echo ""
    echo "先に.envファイルを作成し、認証情報を設定してください"
    echo ""
    exit 1
fi

# 認証情報が設定されているか確認
if grep -q "your_facebook_page_access_token_here" "$MCP_DIR/.env" || \
   grep -q "your_page_id_here" "$MCP_DIR/.env"; then
    echo -e "${YELLOW}⚠️  警告:${NC} .envファイルに認証情報が設定されていません"
    echo ""
    echo "以下のファイルを編集して、Facebookの認証情報を設定してください:"
    echo "  $MCP_DIR/.env"
    echo ""
    read -p "それでも起動しますか？ (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "起動をキャンセルしました"
        exit 0
    fi
fi

# サーバーを起動
echo -e "${GREEN}✓${NC} Facebook MCP Serverを起動します..."
echo -e "${BLUE}場所:${NC} $MCP_DIR"
echo ""
echo "================================================"
echo ""

cd "$MCP_DIR"
exec "$MCP_DIR/.venv/bin/python" "$MCP_DIR/server.py"
