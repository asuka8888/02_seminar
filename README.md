# 02_seminar - Facebook MCP Server セットアップキット

## 📦 このリポジトリについて

Facebook MCP (Model Context Protocol) Serverを簡単にセットアップ・管理するためのツール集です。
Claude Codeから自然言語でFacebookページを管理できるようになります。

## 🎯 機能概要

### Facebook MCP Server の機能（28ツール）

- **投稿管理** (6ツール): 作成、編集、削除、スケジュール
- **コメント管理** (10ツール): 返信、削除、非表示、ネガティブコメントフィルタ
- **インサイト分析** (11ツール): インプレッション、エンゲージメント、リーチ分析
- **メッセージング** (1ツール): DM送信

### Claude Codeでの使用例

```
あなた: Facebookページに新製品のお知らせを投稿して
Claude: 投稿を作成しました！

あなた: 最新投稿のパフォーマンスを教えて
Claude: インプレッション 1,234回、いいね 89件です

あなた: ネガティブなコメントを非表示にして
Claude: 3件のコメントを非表示にしました
```

## 📂 ファイル構成

```
02_seminar_files/
├── README.md                       # このファイル
├── mcp-servers-setup.sh            # 初回セットアップスクリプト
├── mcp-servers-run-facebook.sh     # クイック起動スクリプト
└── 倉庫セットアップ完了.md         # 詳細ガイド（日本語）
```

## 🚀 クイックスタート

### 1. セットアップスクリプトをホームディレクトリにコピー

```bash
# リポジトリをクローン
git clone https://github.com/asuka8888/02_seminar.git
cd 02_seminar

# スクリプトをホームディレクトリにコピー
cp mcp-servers-setup.sh ~/
cp mcp-servers-run-facebook.sh ~/
```

### 2. セットアップを実行

```bash
bash ~/mcp-servers-setup.sh
```

このスクリプトは以下を自動実行します:
- ✅ `~/mcp-servers/` ディレクトリの作成
- ✅ Facebook MCP Serverのクローン
- ✅ Python 3.11仮想環境の作成
- ✅ 依存関係のインストール
- ✅ .envファイルのテンプレート作成

### 3. Facebook認証情報を設定

#### アクセストークンの取得

1. [Facebook Graph API Explorer](https://developers.facebook.com/tools/explorer) にアクセス
2. 「User Token」→「Page Access Token」に変更
3. 必要な権限を追加:
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_manage_metadata`
   - `pages_read_user_content`
   - `pages_messaging`
4. 「Generate Access Token」をクリック

#### .envファイルに設定

```bash
nano ~/mcp-servers/facebook-mcp-server/.env
```

```env
FACEBOOK_ACCESS_TOKEN=あなたのトークン
FACEBOOK_PAGE_ID=あなたのページID
```

### 4. 接続テストと起動

```bash
# 接続テスト
cd ~/mcp-servers/facebook-mcp-server
source .venv/bin/activate
python test_connection.py

# サーバー起動
bash ~/mcp-servers-run-facebook.sh
```

## 💡 使い方

### クイック起動

```bash
bash ~/mcp-servers-run-facebook.sh
```

### Claude Codeから利用

```bash
~/mcp-servers/facebook-mcp-server/.venv/bin/python \
  ~/mcp-servers/facebook-mcp-server/server.py
```

## 📖 詳細ドキュメント

- **倉庫セットアップ完了.md** - 詳細なセットアップガイド（日本語）
- [オリジナルリポジトリ](https://github.com/hagaihen/facebook-mcp-server) - Facebook MCP Server

## 🔧 トラブルシューティング

### セットアップスクリプトが実行できない

```bash
chmod +x ~/mcp-servers-setup.sh
chmod +x ~/mcp-servers-run-facebook.sh
bash ~/mcp-servers-setup.sh
```

### アクセストークンエラー

1. Graph API Explorerで新しいトークンを生成
2. .envファイルを更新
3. サーバーを再起動

### Pythonバージョンエラー

```bash
cd ~/mcp-servers/facebook-mcp-server
~/.local/bin/uv venv --python 3.11
~/.local/bin/uv pip install -r requirements.txt
```

## 🔒 セキュリティ

⚠️ **重要:**
- `.env` ファイルは機密情報を含むため、公開リポジトリにコミットしない
- アクセストークンは定期的に更新する
- 不要になった権限は削除する

## 📚 参考リンク

- [Facebook Graph API](https://developers.facebook.com/docs/graph-api)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Claude Code](https://code.claude.com/)

## 📝 ライセンス

このセットアップキットはMITライセンスです。
Facebook MCP Server本体は[オリジナルリポジトリ](https://github.com/hagaihen/facebook-mcp-server)のライセンスに従います。

## 🤝 貢献

改善案やバグ報告は Issues または Pull Requests でお願いします。

---

**作成日:** 2026年1月5日
**リポジトリ:** https://github.com/asuka8888/02_seminar
