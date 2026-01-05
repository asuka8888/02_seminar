#!/bin/bash

# Facebook MCP Server 倉庫セットアップスクリプト
# 作成日: 2026-01-05

set -e  # エラーが発生したら停止

echo "================================================"
echo "📦 Facebook MCP Server 倉庫セットアップ"
echo "================================================"
echo ""

# 色の定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: 倉庫ディレクトリの作成
echo -e "${BLUE}[1/6]${NC} MCP専用倉庫ディレクトリを作成中..."
mkdir -p ~/mcp-servers
echo -e "${GREEN}✓${NC} ディレクトリ作成完了: ~/mcp-servers"
echo ""

# Step 2: Facebook MCP Serverのクローン
echo -e "${BLUE}[2/6]${NC} Facebook MCP Serverをクローン中..."
cd ~/mcp-servers

if [ -d "facebook-mcp-server" ]; then
    echo -e "${YELLOW}⚠${NC}  既存のfacebook-mcp-serverディレクトリが見つかりました"
    read -p "削除して再クローンしますか？ (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf facebook-mcp-server
        git clone https://github.com/hagaihen/facebook-mcp-server.git
    fi
else
    git clone https://github.com/hagaihen/facebook-mcp-server.git
fi

echo -e "${GREEN}✓${NC} クローン完了"
echo ""

# Step 3: ディレクトリに移動
cd facebook-mcp-server
echo -e "${BLUE}[3/6]${NC} 作業ディレクトリ: $(pwd)"
echo ""

# Step 4: Python 3.11仮想環境の作成
echo -e "${BLUE}[4/6]${NC} Python 3.11仮想環境を作成中..."
if command -v ~/.local/bin/uv &> /dev/null; then
    ~/.local/bin/uv venv --python 3.11
    echo -e "${GREEN}✓${NC} 仮想環境作成完了"
else
    echo -e "${YELLOW}⚠${NC}  uvが見つかりません。インストール中..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ~/.local/bin/uv venv --python 3.11
    echo -e "${GREEN}✓${NC} uv インストール＆仮想環境作成完了"
fi
echo ""

# Step 5: 依存関係のインストール
echo -e "${BLUE}[5/6]${NC} 依存関係をインストール中..."
~/.local/bin/uv pip install -r requirements.txt
echo -e "${GREEN}✓${NC} 依存関係インストール完了"
echo ""

# Step 6: .envファイルの作成
echo -e "${BLUE}[6/6]${NC} .envファイルを作成中..."
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# Facebook MCP Server 環境変数設定

# Facebook Page Access Token
# 取得方法: https://developers.facebook.com/tools/explorer
# 1. Graph API Explorer にアクセス
# 2. "User or Page" を "Page" に変更
# 3. 必要な権限を選択: pages_manage_posts, pages_read_engagement, pages_manage_metadata
# 4. "Generate Access Token" をクリック
FACEBOOK_ACCESS_TOKEN=your_facebook_page_access_token_here

# Facebook Page ID
# 取得方法:
# 1. Facebookページにアクセス
# 2. ページ設定 → ページ情報 で確認できます
# または、https://findmyfbid.com/ を使用
FACEBOOK_PAGE_ID=your_page_id_here
EOF
    echo -e "${GREEN}✓${NC} .env ファイル作成完了"
else
    echo -e "${YELLOW}⚠${NC}  .env ファイルは既に存在します（スキップ）"
fi
echo ""

# 完了メッセージ
echo "================================================"
echo -e "${GREEN}🎉 セットアップ完了！${NC}"
echo "================================================"
echo ""
echo "📂 Facebook MCP Server の場所:"
echo "   ~/mcp-servers/facebook-mcp-server/"
echo ""
echo "📝 次のステップ:"
echo "   1. .envファイルを編集して認証情報を設定"
echo "      nano ~/mcp-servers/facebook-mcp-server/.env"
echo ""
echo "   2. 接続テストを実行"
echo "      cd ~/mcp-servers/facebook-mcp-server"
echo "      source .venv/bin/activate"
echo "      python test_connection.py"
echo ""
echo "   3. Claude Codeで使用"
echo "      ~/mcp-servers/facebook-mcp-server/.venv/bin/python \\"
echo "        ~/mcp-servers/facebook-mcp-server/server.py"
echo ""
echo "📖 詳細なガイド:"
echo "   ~/mcp-servers/facebook-mcp-server/README_ja.md"
echo ""
