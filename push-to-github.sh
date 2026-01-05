#!/bin/bash

# GitHub リポジトリへプッシュするスクリプト
# リポジトリ: https://github.com/asuka8888/02_seminar.git

set -e  # エラーが発生したら停止

echo "================================================"
echo "📤 GitHub リポジトリへプッシュ"
echo "================================================"
echo ""

# 色の定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 現在のディレクトリを確認
CURRENT_DIR=$(pwd)
echo -e "${BLUE}現在のディレクトリ:${NC} $CURRENT_DIR"
echo ""

# ファイルを確認
echo -e "${BLUE}[1/6]${NC} ファイルを確認中..."
ls -la
echo ""

# Git初期化
echo -e "${BLUE}[2/6]${NC} Gitリポジトリを初期化中..."
if [ ! -d ".git" ]; then
    git init
    echo -e "${GREEN}✓${NC} Git初期化完了"
else
    echo -e "${YELLOW}⚠${NC}  既にGitリポジトリが存在します"
fi
echo ""

# リモートリポジトリを設定
echo -e "${BLUE}[3/6]${NC} リモートリポジトリを設定中..."
if git remote | grep -q "origin"; then
    echo -e "${YELLOW}⚠${NC}  既存のoriginを削除します"
    git remote remove origin
fi
git remote add origin https://github.com/asuka8888/02_seminar.git
echo -e "${GREEN}✓${NC} リモートリポジトリ設定完了"
echo ""

# ファイルを追加
echo -e "${BLUE}[4/6]${NC} ファイルをステージング中..."
git add .
echo -e "${GREEN}✓${NC} ファイル追加完了"
echo ""

# ステータスを確認
echo -e "${BLUE}ステージング状態:${NC}"
git status
echo ""

# コミット
echo -e "${BLUE}[5/6]${NC} コミットを作成中..."
git commit -m "feat: Facebook MCP Serverセットアップキット追加

- セットアップスクリプト (mcp-servers-setup.sh)
- クイック起動スクリプト (mcp-servers-run-facebook.sh)
- 詳細ガイド (倉庫セットアップ完了.md)
- README.md
- .gitignore

Facebook MCP Serverを簡単にセットアップして
Claude Codeから自然言語でFacebookページを管理できるようにするツールキット"

echo -e "${GREEN}✓${NC} コミット完了"
echo ""

# プッシュ
echo -e "${BLUE}[6/6]${NC} GitHubにプッシュ中..."
echo -e "${YELLOW}注意:${NC} 初回プッシュ時は認証が必要な場合があります"
echo ""

# メインブランチ名を確認（main または master）
BRANCH=$(git branch --show-current)
echo -e "${BLUE}ブランチ:${NC} $BRANCH"
echo ""

# プッシュを実行
if git push -u origin $BRANCH; then
    echo ""
    echo "================================================"
    echo -e "${GREEN}🎉 プッシュ完了！${NC}"
    echo "================================================"
    echo ""
    echo "リポジトリURL:"
    echo "https://github.com/asuka8888/02_seminar"
    echo ""
else
    echo ""
    echo "================================================"
    echo -e "${YELLOW}⚠️  プッシュに失敗しました${NC}"
    echo "================================================"
    echo ""
    echo "以下を確認してください:"
    echo "1. GitHubへの認証が完了しているか"
    echo "2. リポジトリが存在するか"
    echo "3. プッシュ権限があるか"
    echo ""
    echo "手動でプッシュする場合:"
    echo "  git push -u origin $BRANCH"
    echo ""
fi
