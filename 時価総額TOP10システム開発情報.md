Claude CodeとModel Context Protocol (MCP) を基盤とした自律型金融市場監視・配信システムの包括的設計：50のオープンソース技術による次世代アーキテクチャ  
1\. 序論：金融インテリジェンスの自律化への転換  
現代の金融市場において、情報はもはや人間が手動で収集・分析できる規模を超越している。世界中の株式市場で刻一刻と変動する時価総額（Market Capitalization）は、企業の相対的な価値を示す最も基本的な指標でありながら、そのリアルタイムな把握には膨大なデータ処理と通貨調整、そして文脈の理解が必要となる。従来の金融データシステムは、静的なAPIコールと固定的なダッシュボードに依存していた。ユーザーが「現在の世界時価総額トップ10は？」と問えば、システムは事前にプログラムされたクエリを実行し、数値を返すだけであった。しかし、Anthropic社が提唱する Claude Code と Model Context Protocol (MCP) の登場は、このパラダイムを根本から覆そうとしている。  
本報告書は、ユーザーが求める「世界、S\&P500、NASDAQ、欧州、日本の時価総額TOP10をいつでも把握・配信できるシステム」を、最新の自律型AIエージェント技術を用いて構築するための詳細な技術調査および設計指針である。従来のシステムとの決定的な違いは、LLM（大規模言語モデル）が単なるインターフェースではなく、データソースへ動的にアクセスし、推論・計算・整形を行う「エージェント型金融インテリジェンス」の中核として機能する点にある。  
本設計では、金融データプロバイダー、エージェントフレームワーク、データベース、運用基盤に至るまで、徹底的なリサーチに基づき選定された50個のオープンソースツールおよび主要サービスを解説し、それらをMCPという共通言語で統合するアーキテクチャを提案する。特に、正確性が求められる金融データ（Determinism）と、柔軟性が求められる自然言語インターフェース（Probabilism）を、いかにしてシームレスに融合させるかが、本システムの設計における最大の論点となる。

  

2\. データ取得層：信頼できる金融情報の源泉の確保  
時価総額ランキングの生成において最大の技術的課題は、データの「正確性」と「網羅性」、そして「正規化」である。特に「全世界（Global）」のランキングを作成する場合、異なる通貨（USD, EUR, JPY）の統一的な換算レートの適用タイミングや、各取引所のタイムゾーン管理、株式分割や併合といったコーポレートアクションの反映が不可欠となる。また、日本市場においては、多くのグローバルAPIでデータの更新遅延や欠損が見られるため、専用の対策が必要となる。本章では、APIベースのアプローチと、スクレイピングやヘッドレスブラウザを用いた補助的アプローチを組み合わせ、最適なツール群を選定・評価する。  
2.1 コア・金融データAPI：市場の「真実」へのアクセス  
金融データの取得には、信頼性の高いAPIが不可欠である。無料のAPIは多数存在するが、時価総額ランキングのような集計データを正確に取得するためには、機関投資家レベルのデータ品質を持つプロバイダーが推奨される。特に Financial Modeling Prep (FMP) と Alpha Vantage は、MCPサーバーとしての親和性が高く、本システムのデータバックボーンとなる。

1\. Financial Modeling Prep (FMP)  
1

本システムにおいて最重要と位置づけられるAPIである。FMPの最大の強みは、その強力なスクリーナー機能にある。多くのAPIは「特定の銘柄（Ticker）を指定して株価を取得する」ことには長けているが、「全市場の銘柄の中から時価総額順にソートして上位10件を返す」というクエリに対しては無力である場合が多い。FMPの Stock Screener エンドポイントは、marketCap によるフィルタリングとソート、および limit パラメータをサポートしており、サーバーサイドで計算済みのランキングを直接取得できる。これにより、クライアント（Claude Code）側で数千銘柄のデータをダウンロードし、ソート処理を行う必要がなくなり、レイテンシとコストを劇的に削減できる。また、S\&P500やNASDAQなどの指数構成銘柄（Constituents）データも提供しており、インデックスベースのランキング生成にも不可欠である。

2\. Alpha Vantage  
4

Alpha Vantageは、20年以上のヒストリカルデータと広範なグローバルカバレッジを持つ、開発者に人気の高いAPIである。特筆すべきは、公式にMCPサーバーのサポートを開始した点である。これにより、開発者は自前でAPIラッパーを書くことなく、Claude Codeから直接ツールとしてAlpha Vantageの機能を呼び出すことが可能となる。時価総額データだけでなく、テクニカル指標や為替レート（Forex）の取得にも対応しており、世界ランキング作成時の通貨換算において重要な役割を果たす。FMPのバックアップとして、あるいはクロスチェック用のデータソースとして、システムに冗長性を持たせるために採用する。

3\. yfinance  
6

Yahoo Financeの非公式ラッパーライブラリであり、Pythonエコシステムにおいて最も広く使われている金融データツールの一つである。APIキーが不要で手軽に利用できる点が魅力だが、公式APIではないため、将来的な利用可能性や商用利用にはリスクが伴う。しかし、日本市場（Tokyo Stock Exchange）のデータに関しては、多くのグローバルAPIよりも速報性や銘柄カバレッジ（特に中小型株）で優れている場合がある。本システムでは、日本市場（.T サフィックスの銘柄）のリアルタイムデータ取得や、API制限時のフォールバック手段として組み込む。

4\. OpenBB Platform  
8

OpenBBは、単なるデータラッパーではなく、複数のデータプロバイダー（FMP, Polygon, Alpha Vantageなど）を統合し、統一されたインターフェースで提供するオープンソースの金融投資プラットフォームである。AIエージェント統合用のSDKを提供しており、データソースの違いを抽象化できるため、バックエンドのプロバイダーを切り替える際にコードの修正を最小限に抑えることができる。「データ取得のハブ」として機能し、システムの保守性を高める。

5\. Twelve Data  
10

Twelve Dataは、1分足などの日中（Intraday）データに強く、APIの設計が非常にモダンで統一されている。複数国のデータを扱う際、取引所ごとに異なるデータ形式をパースする必要がなく、開発効率が高い。特に、欧州市場や新興国市場のデータ取得において、他のメジャーなAPIがカバーしていない領域を補完する役割を果たす。WebSocketによるストリーミング配信にも対応しており、将来的にリアルタイム性をさらに高める場合に有用である。

6\. Marketstack  
11

70以上のグローバル取引所をカバーしており、特に欧州やアジア市場のデータ取得において強力なバックアップとして機能する。リアルタイムデータだけでなく、過去の特定時点における時価総額データを取得する際にも信頼性が高い。APIレスポンスが軽量で高速であるため、定期的なバッチ処理での全銘柄スキャンなどに適している。

7\. Pandas-Datareader  
12

古典的だが堅牢なデータ取得ライブラリであり、特にFRED（セントルイス連邦準備銀行）などの公的機関からの経済指標取得に強みを持つ。時価総額ランキングの変動要因として、金利やGDPなどのマクロ経済指標を分析する際、このライブラリを通じて信頼できる一次情報を取得することができる。

8\. Finnhub  
13

機関投資家レベルのデータ品質を誇り、特にIPOカレンダー、決算サプライズ、インサイダー取引情報など、時価総額変動の「定性的な要因」を分析するために必要なデータが豊富である。ランキングが変動した際、その背景にあるニュースやイベントを特定するためのサブデータソースとして活用する。

9\. YahooQuery  
14

yfinanceの代替として開発されたライブラリであり、より高速で、特に財務諸表やファンダメンタルズデータの取得においてパフォーマンスが優れている。yfinanceがスクレイピング対策で不安定になった場合の代替手段として、あるいは大量の銘柄の財務データを一括取得する際のツールとして採用する。

10\. S\&P Dow Jones Indices API  
15

S\&P500やダウ平均などの指数の「正解」データを提供する公式ソースである。指数構成銘柄の変更（Rebalancing）や、指数の算出ロジックに関する公式情報を取得するために参照する。API利用には契約が必要な場合があるが、正確なインデックス組成を把握するためには最も信頼できる情報源である。  
2.2 Webスクレイピング & ブラウザ操作：APIの隙間を埋める  
APIは構造化されたデータの取得には最適だが、最新のニュースや、API非公開の公式サイト（例：日本取引所グループの公式サイト）からのデータ取得には、Webスクレイピング技術が必要となる。特に、昨今のウェブサイトは動的なJavaScriptで構築されていることが多く、単純なHTTPリクエストではデータを取得できないため、ヘッドレスブラウザの活用が必須となる。

11\. Browserbase  
16

AIエージェント向けに最適化されたヘッドレスブラウザ基盤である。自前でPuppeteerやPlaywrightのインフラを管理するのは、IPブロックやCAPTCHA回避、メモリリーク対策などで非常にコストがかかる。Browserbaseはこれらをマネージドサービスとして提供し、CAPTCHAの自動回避やセッションの永続化を行う。Claude Codeが「ウェブを見てきて」と指示した際、安定してページ内容を取得するための「目」として機能する。

12\. Firecrawl  
18

ウェブサイト全体をクロールし、LLMが理解しやすいMarkdown形式に変換することに特化したツールである。企業のIRページやニュースサイトから、非構造化データを取得し、時価総額変動の理由を分析するためのテキストデータとしてClaude Codeに供給する。HTMLのノイズを除去し、純粋なコンテンツのみを抽出する能力に優れている。

13\. Steel  
19

Browserbaseと同様のブラウザAPIだが、より「対ボット対策の回避」に重点を置いている。指紋（Fingerprint）対策が施されており、金融機関やニュースサイトなど、スクレイピング対策が厳しいサイトからのデータ抽出において強みを発揮する。オープンソースのブラウザAPIとして提供されており、自前のインフラでホストすることも可能である。

14\. Crawl4AI  
21

非同期処理に優れたオープンソースのクローラーであり、大量のURLを高速に処理することに長けている。ランキングトップ10の企業に関連する最新ニュース記事を数百件規模で収集し、センチメント分析を行う際のデータ収集エンジンとして利用する。

15\. Playwright (Python)  
18

Microsoftが開発するブラウザ自動化ライブラリ。動的なJavaScriptで描画されるチャートや、ユーザー操作が必要なランキング表のデータ抽出に必須のツールである。BrowserbaseやSteelの内部エンジンとしても使われているが、ローカル環境での開発や、特定の複雑なインタラクションをスクリプト化する際には、直接Playwrightを使用することが最も柔軟性が高い。  
3\. エージェント・フレームワークとMCP実装：自律的思考の核  
データ取得ツールが揃ったとしても、それらを適切に呼び出し、結果を統合し、ユーザーに届けるための「頭脳」が必要である。ここでは、Claude Codeを中核に据えつつ、より複雑なワークフローを制御するためのエージェントフレームワークと、システム全体を結合するModel Context Protocol (MCP) の実装について詳述する。  
3.1 Model Context Protocol (MCP)：標準化された接続  
MCPは、AIモデルと外部ツール（データソース、リポジトリ、API）を接続するためのオープン標準である。これまで、各AIアシスタントは独自のプラグイン機構を持っていたが、MCPにより、一度作成したサーバーはClaude Desktop、Cursor、VS Codeなど、あらゆるMCP対応クライアントから利用可能となる。

  

16\. MCP Python SDK  
22

公式SDKであり、自作の金融データ取得スクリプト（例：yfinanceを使って日本株のランキングを取得するPython関数）をMCPサーバーとしてラップするために必須となる。@mcp.tool() デコレータを使用するだけで、既存の関数をAIから呼び出し可能なツールとして公開できるため、既存資産の活用が容易である。

17\. SQLite MCP Server  
21

時価総額データの履歴をローカルのSQLiteデータベースに保存し、ClaudeからSQLクエリを通じて分析可能にするためのサーバー。ユーザーが「過去一ヶ月で最も順位を上げた企業は？」と質問した際、Claudeはこのサーバーを通じてSQLを発行し、正確な統計情報を取得できる。CSVファイルなどを都度読み込むよりも効率的で、構造化データの扱いに適している。

18\. Filesystem MCP Server  
21

生成したレポート（Markdown、PDF、Excel）をローカルファイルシステムに保存・管理するために使用する。また、ユーザーがローカルに持っている設定ファイルや、過去のレポートを参照させる際にも、セキュアなファイルアクセス手段を提供する。

19\. Fetch MCP Server  
21

Claude Codeから直接Webページの内容を取得し、コンテキストとして取り込むための公式ツール。前述のFirecrawlなどの外部サービスを使うまでもない簡易なページ確認や、特定のニュース記事の本文取得など、軽量なブラウジングタスクに使用される。

20\. Alpha Vantage MCP Server  
5

公式に提供されている株価データ用MCPサーバー。これを導入するだけで、get\_stock\_price や get\_currency\_exchange\_rate といった基本的な関数が即座に利用可能となる。自前で実装する部分を減らし、システムのコアロジック（ランキング生成や分析）に注力するために、この公式サーバーを積極的に活用する。  
3.2 自律型エージェント構築フレームワーク：オーケストレーション  
Claude Code自体もエージェントとして振る舞うが、より複雑で長期的なタスク（例：「毎日市場を監視し、異常があればニュースを検索してレポートを作成し、Slackに通知する」）を実行するには、専用のフレームワークが必要となる。

21\. LangChain / LangGraph  
24

LLMアプリケーション構築の業界標準である。特に LangGraph は、エージェントの行動を「グラフ構造（ノードとエッジ）」として定義できるため、循環的なワークフロー（Cycles）の構築に適している。例えば、「データ取得」→「品質チェック」→（NGなら）「再取得」→（OKなら）「分析」といった、条件分岐を含む堅牢なパイプラインを構築する上で不可欠なフレームワークである。

22\. Microsoft AutoGen  
24

マルチエージェント対話に特化したフレームワーク。「データ収集担当（Researcher）」エージェントと、「レポート執筆担当（Writer）」エージェント、そしてそれをレビューする「管理者（User Proxy）」エージェントを定義し、それらを会話させることでタスクを遂行する。単一のエージェントでは見落としがちな視点を、複数の役割を持ったエージェントが相互に指摘し合うことで、分析の質を高めることが可能となる。

23\. DSPy  
27

スタンフォード大学発の、プロンプトエンジニアリングを「プログラミング」に置き換える革新的なフレームワークである。金融システムにおいて、LLMのハルシネーション（嘘の数値生成）は致命的である。DSPyは、プロンプトをニューラルネットワークの「重み」のように扱い、最適化（コンパイル）することで、期待する出力精度を体系的に向上させる。これにより、例えば「必ず特定のJSONスキーマでランキングデータを返す」といった制約を厳守させることができ、後段のシステム連携の安定性が飛躍的に向上する。

24\. CrewAI  
29

ロールプレイングベースのエージェント構築フレームワーク。各エージェントに明確な「役割（Role）」、「目標（Goal）」、「背景（Backstory）」を与えることで、人間のようなチーム（Crew）として協調作業を行わせる。構造化されたタスクの順次実行に強みがあり、定期的なレポート作成のような定型業務の自動化に適している。

25\. LlamaIndex  
31

データ連携、特にRAG（Retrieval-Augmented Generation）に特化したフレームワーク。金融ドキュメント（PDFの決算資料や有価証券報告書）のインデックス化と検索において、LangChainよりも優れた性能を発揮する場合がある。時価総額ランキングの変動理由を企業の一次資料から検索する際、LlamaIndexの高度な検索戦略（階層的インデックスなど）が役立つ。

26\. Microsoft Semantic Kernel  
24

エンタープライズ向けの堅牢なSDK。Azure OpenAI ServiceなどのMicrosoft製品との親和性が高く、C\#やPythonでバックエンドを構築する場合の有力な選択肢となる。企業のセキュリティ基準に準拠したエージェント開発を行う場合に推奨される。

27\. Phidata  
29

金融エージェントやリサーチエージェントのテンプレートが豊富なフレームワーク。アシスタント機能に特化しており、データベースやWeb検索ツールを備えたエージェントを短期間で開発するのに適している。

28\. MetaGPT  
33

「1行の要件からPRD（製品要求仕様書）まで生成する」など、ソフトウェアエンジニアリングタスクの自律化で有名だが、その高い自律性は金融レポートの自動生成にも応用可能である。複雑なデータ構造を理解し、多角的な視点からドキュメントを構成する能力が高い。

29\. Swarm (OpenAI)  
29

OpenAIが実験的に公開した、軽量なマルチエージェント・オーケストレーション・フレームワーク。エージェント間の「ハンドオフ（Handoff）」パターンに焦点を当てており、低レイテンシでエージェント間の連携を行いたい場合に有利である。サーバーサイドでの実装がシンプルで、スケーラビリティが高い。

30\. Sakana AI (The AI Scientist)  
34

日本発の自律型研究エージェントのコンセプトである。自律的に仮説を立て、実験（データ分析）を行い、論文（レポート）を執筆し、査読するというプロセス全体を自動化するアーキテクチャは、本システムの「市場分析レポートの自動生成」機能において大いに参考になるモデルである。  
4\. 記憶と文脈の管理：データ永続化とRAG  
システムが「いつでも」状況を把握できるためには、過去のデータとの比較や、前回取得時からの変動を記憶しておく必要がある。また、数値データの背後にある「意味（Context）」を理解するための知識ベースも重要となる。  
4.1 データベースとベクターストア：エージェントの長期記憶

31\. LanceDB  
36

推奨。LanceDBは、マルチモーダル（テキスト、画像、音声）対応かつサーバーレスで動作可能な、非常に軽量で高速なベクターデータベースである。エージェントの長期記憶として非常に扱いやすく、Pythonアプリケーションに埋め込んで使用することもできる。時価総額の数値データだけでなく、関連するチャート画像やニュース記事のベクトル埋め込みを一元管理できるため、エージェントが「過去のこのチャートパターンの時に何が起きたか」を検索するのに最適である。

32\. GraphRAG (Microsoft)  
38

単なるベクトル検索（Semantic Search）では、キーワードの類似性は見つけられても、複雑な因果関係を見抜くことは難しい。GraphRAGは、テキストから知識グラフ（Knowledge Graph）を構築し、エンティティ（企業、人物、製品）間の関係性を利用して検索を行う。これにより、「NVIDIAの時価総額上昇」の理由として、直接的な言及がなくても「AIチップ需要」→「TSMCの増産」→「NVIDIAへの供給増」といった、つながり（Graph）を辿った深い洞察を提供することが可能になる。

33\. Mem0  
40

エージェント専用のメモリ管理レイヤー。ユーザーごとの関心（例：「Aさんはハイテク株を重視する」、「Bさんは欧州市場に興味がある」）を記憶し、パーソナライズされたランキング配信を実現する。単なる会話履歴の保存ではなく、ユーザーの嗜好や事実を抽出して構造化データとして保持するため、長期的な対話においてエージェントがユーザーの意図を汲み取りやすくなる。

34\. GPTCache  
42

LLMの応答をキャッシュするツール。時価総額ランキングのようなデータは、数分〜数時間単位では変化しない場合が多い。同じ質問（「今のTOP10は？」）に対して、都度APIコールとLLM推論を行うのは無駄である。GPTCacheを導入することで、類似のクエリに対してはキャッシュされた結果を即座に返し、コスト削減と応答速度の向上を実現する。

35\. DuckDB  
44

インプロセスで動作する高速な分析用SQLデータベース。時系列の時価総額データを集計・分析するのに、Pandas以上の性能を発揮する。数百万行規模のデータになっても高速にクエリを実行できるため、過去数年分の全銘柄の時価総額推移を保存し、オンデマンドで分析する際のバックエンドとして最適である。

36\. Chroma  
45

オープンソースで人気の高いベクターデータベース。LangChainなどのフレームワークとの統合事例が多く、ドキュメントも豊富であるため、導入障壁が低い。開発初期のプロトタイピングにおいて、手軽にRAGシステムを構築するために利用できる。

37\. Qdrant  
45

Rust製の高速なベクター検索エンジン。強力なフィルタリング機能を持っており、例えば「時価総額1兆円以上（メタデータフィルタ）」かつ「AIに関連するニュースが多い（ベクトル検索）」といった、複合的な条件での検索が得意である。

38\. Pinecone  
45

完全マネージド型のベクターデータベース。インフラ管理の手間を完全にゼロにしたい場合の選択肢。スケーラビリティが高く、本番運用において信頼性が求められる場合に採用を検討する。

39\. Zep  
46

長期記憶に特化したメモリストア。会話履歴からの事実抽出機能があり、過去の分析結果を「知識」として蓄積できる。エージェントが過去に行った市場分析の結果を忘れずに、次回の分析に活かすための「経験知」の保存場所として機能する。

40\. Redis Stack  
45

ベクトル検索機能も備えた高速KVS（Key-Value Store）。リアルタイム性が最優先される配信キャッシュとして利用する。最新のランキングデータや、直近のニュースヘッドラインをメモリ上に保持し、ミリ秒単位でのアクセスを可能にする。  
5\. インフラ・運用・可視化：システムを支える基盤  
構築したエージェントシステムを安定稼働させ、その結果をユーザーに美しく配信するためのツール群である。  
5.1 デプロイメントとランタイム：どこで動かすか

41\. Modal  
47

Pythonコードをクラウド上で瞬時に実行できるサーバーレス基盤。コンテナのビルドやインフラ管理を意識することなく、関数単位でコードをデプロイできる。定期的なデータ取得ジョブ（Cron Job）や、重い計算処理（RAGのインデックス作成）を、必要な時だけGPU/CPUリソースを割り当てて実行するのに最適である。

42\. Railway  
49

PaaS（Platform as a Service）。LangChainや各種エージェントのテンプレートが豊富で、GitHubと連携して即座にデプロイ可能。バックエンドAPIサーバーや、Streamlitなどのフロントエンドアプリケーションのホスティングに適している。

43\. Docker  
51

開発環境と本番環境の差異をなくすためのコンテナ技術のデファクトスタンダード。特にMCPサーバーは、依存関係が複雑になる場合があるため、Dockerコンテナとしてパッケージングし、配布・実行することで、環境依存のトラブルを防ぐことができる。

44\. LiteLLM  
52

複数のLLM（Claude, GPT-4, Local Models）へのアクセスを統一インターフェースで管理するゲートウェイ。コスト管理やフォールバック（Claudeがダウンしている時にGPT-4に切り替えるなど）に役立つ。また、各エージェントがどの程度トークンを消費しているかを監視するためにも重要である。

45\. vLLM  
54

ローカルLLMを使用する場合の高速推論エンジン。コスト削減やプライバシー保護のために、分析の一部（例：ニュース記事の要約）を自前のサーバー上のオープンソースモデル（Llama 3など）にオフロードする場合に使用する。  
5.2 可視化とオブザーバビリティ：何が起きているかを見る

46\. Streamlit  
56

推奨。Pythonスクリプトだけでインタラクティブなダッシュボードを作成可能なフレームワーク。時価総額ヒートマップ、ランキング表、推移グラフなどを、フロントエンドの専門知識なしで高速に構築できる。本システムのユーザーインターフェース（UI）の第一候補である。

47\. Arize Phoenix  
58

エージェントの挙動（トレース）を可視化するオープンソースのオブザーバビリティツール。Claude CodeがどのMCPツールを呼び出し、どのようなパラメータを渡し、どのような結果を得て、どう判断したか（Chain of Thought）を詳細に記録・可視化できる。エージェントのデバッグや改善に不可欠である。

48\. LangSmith  
59

LangChainの開発元が提供するプラットフォーム。LangChainエコシステムとの親和性が高く、プロンプトのバージョン管理や、エージェントの評価（Evaluation）に強みを持つ。開発チームでプロンプトを共有・管理する場合に有用である。

49\. Chainlit  
56

ChatGPTのようなチャットインターフェースをPythonで構築するためのフレームワーク。Streamlitが「ダッシュボード」寄りであるのに対し、Chainlitは「対話」にフォーカスしている。Claude Codeとの対話型インターフェースとして、ユーザーが自然言語で質問し、エージェントがグラフや表で回答する形式を実装する場合に適している。

50\. OpenTelemetry  
60

分散トレーシングの標準規格。Arize PhoenixやLangSmithと連携し、システム全体のパフォーマンスを監視するための基盤技術。特定の処理に時間がかかっている場合や、エラーが発生している箇所を特定するために利用する。

  

6\. システム統合設計：3層アーキテクチャの実装  
選定した50のツールを有機的に結合し、実用的なシステムとして機能させるための統合設計を示す。システムは、「データ取得・正規化層 (Batch Layer)」、「自律分析層 (Agent Layer)」、「配信・可視化層 (Interactive Layer)」 の3層構造とする。  
6.1 データ取得・正規化層 (Batch Layer)  
この層の目的は、信頼できる「マスターデータ」を作成することである。  
\* 実行環境: Modal 47 上でスケジュール実行（例：毎時00分）。  
\* プロセス:  
   1\. US/Global: FMPの Stock Screener APIを叩き、時価総額上位500件を取得。  
   2\. Japan: yfinance 6 またはBrowserbase 16 を使用し、東証プライム上位銘柄のデータを取得。  
   3\. Europe: Marketstack 11 を使用し、主要取引所（LSE, Euronext）のデータを補完。  
   4\. 正規化: Alpha Vantage 5 のForex APIを使用し、全ての時価総額をUSD（米ドル）に換算。  
   5\. 保存: 処理結果を raw\_data および normalized\_ranking テーブルとして DuckDB 44 または LanceDB 36 に保存。  
6.2 自律分析層 (Agent Layer)  
この層の目的は、データの「意味」を解釈することである。  
\* 実行環境: Claude Code \+ MCP Servers。  
\* プロセス:  
   1\. 異常検知: LangGraphエージェントが前回のランキングと今回を比較。「順位の入れ替わり」や「5%以上の変動」を検知。  
   2\. リサーチ: 変動があった銘柄について、Crawl4AI 21 でニュースを検索。  
   3\. 推論: Claude Codeがニュースの内容を読み、変動の理由（例：「決算発表」「FDA承認」）を要約。  
   4\. 記憶: 要約結果とベクトル化されたニュースを GraphRAG 39 に追加。  
6.3 配信・可視化層 (Interactive Layer)  
この層の目的は、ユーザーに情報を届けることである。  
\* 実行環境: Railway 49 上でホストされた Streamlit 56 アプリ。  
\* プロセス:  
   1\. ダッシュボード: 最新のランキング表を表示。  
   2\. チャット: Chainlit 61 を組み込み、ユーザーが「なぜAppleが下がった？」と聞くと、GraphRAGから理由を検索して回答。  
   3\. プッシュ通知: 変動検知時に、MCP経由でSlack/Discordへ通知を送信。  
7\. 実装ロードマップと結論  
7.1 開発フェーズ  
1\. 基盤構築 (Week 1-2): FMPおよびAlpha VantageのAPIキー取得。Modal上でのデータ取得スクリプト作成。通貨換算ロジックの実装と検証。  
2\. MCPサーバー実装 (Week 3): Python SDKを用いて、データ取得機能をMCPサーバー化。Claude Desktopに接続し、チャットから「現在の日本TOP10」を取得できるかテスト。  
3\. エージェント高度化 (Week 4): LangGraphを用いて、監視→分析のループを実装。LanceDBへのベクトル保存とGraphRAGの構築。  
4\. UI/配信実装 (Week 5): Streamlitによるダッシュボード作成。Slackボットの実装。  
7.2 結論  
本システムは、単なる情報の羅列ではなく、Claude Codeという高度なLLMをインターフェースとし、背後で堅牢な金融データAPIと最新のRAG技術が支える「インテリジェントな金融アシスタント」である。選定した50のツールは、それぞれがオープンソース界隈で高い評価を得ており、これらをMCPという共通プロトコルで結合することで、将来的な拡張性（新しいデータソースやモデルの追加）と保守性の高いシステムが実現できる。特に、FMP (データ)、LanceDB (記憶)、LangGraph (自律性)、MCP (接続性) の4本柱が、本プロジェクトの成功の鍵となる。  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
免責事項: 本報告書は技術的な設計指針を提供するものであり、投資助言ではありません。金融データの利用にあたっては、各APIプロバイダーの利用規約およびライセンスを遵守してください。  
引用文献  
1\. Market Cap API \- Legacy \- Financial Modeling Prep, 1月 3, 2026にアクセス、 https://site.financialmodelingprep.com/developer/docs/market-capitalization-api  
2\. Company Market Cap API \- Financial Modeling Prep, 1月 3, 2026にアクセス、 https://site.financialmodelingprep.com/developer/docs/stable/market-cap  
3\. Free Stock Market API and Financial Statements API... | FMP, 1月 3, 2026にアクセス、 https://site.financialmodelingprep.com/developer/docs  
4\. Alpha Vantage: Free Stock APIs in JSON & Excel, 1月 3, 2026にアクセス、 https://www.alphavantage.co/  
5\. Alpha Vantage MCP for Stock Market Data, 1月 3, 2026にアクセス、 https://mcp.alphavantage.co/  
6\. yfinance · PyPI, 1月 3, 2026にアクセス、 https://pypi.org/project/yfinance/  
7\. yfinance \- Zoo, 1月 3, 2026にアクセス、 https://zoo.cs.yale.edu/classes/cs458/lectures/yfinance.html  
8\. OpenBB-finance/agents-for-openbb: Custom agents for ... \- GitHub, 1月 3, 2026にアクセス、 https://github.com/OpenBB-finance/agents-for-openbb  
9\. OpenBB-finance/OpenBB: Financial data platform for analysts, quants and AI agents. \- GitHub, 1月 3, 2026にアクセス、 https://github.com/OpenBB-finance/OpenBB  
10\. Stock Market Data APIs (Real Time & Historical) \- Twelve Data, 1月 3, 2026にアクセス、 https://twelvedata.com/stocks  
11\. Free Stock Market Data API for Real-Time & Historical Data, 1月 3, 2026にアクセス、 https://marketstack.com/  
12\. Stock Market Data: Obtaining Data, Visualization & Analysis in Python, 1月 3, 2026にアクセス、 https://www.interactivebrokers.com/campus/ibkr-quant-news/stock-market-data-obtaining-data-visualization-analysis-in-python/  
13\. Finnhub Stock APIs \- Real-time stock prices, Company fundamentals, Estimates, and Alternative data., 1月 3, 2026にアクセス、 https://finnhub.io/  
14\. Yahoo Finance API \- A Complete Guide \- AlgoTrading101 Blog, 1月 3, 2026にアクセス、 https://algotrading101.com/learn/yahoo-finance-api-guide/  
15\. API Data Solutions | S\&P Dow Jones Indices, 1月 3, 2026にアクセス、 https://www.spglobal.com/spdji/en/landing/topic/api-data-solutions/  
16\. Browserbase: A web browser for AI agents & applications, 1月 3, 2026にアクセス、 https://www.browserbase.com/  
17\. What is Browserbase? \- Browserbase Documentation, 1月 3, 2026にアクセス、 https://docs.browserbase.com/introduction/what-is-browserbase  
18\. 50+ Open-Source Tools for Building AI Agents, 1月 3, 2026にアクセス、 https://aiagent.marktechpost.com/post/50-open-source-tools-for-building-ai-agents  
19\. Steel.dev \- The Open-source Browser API for AI Agents : r/LocalLLaMA \- Reddit, 1月 3, 2026にアクセス、 https://www.reddit.com/r/LocalLLaMA/comments/1h1ni3c/steeldev\_the\_opensource\_browser\_api\_for\_ai\_agents/  
20\. Intro to Steel, 1月 3, 2026にアクセス、 https://docs.steel.dev/overview/intro-to-steel  
21\. riza-io/modelcontextprotocol-servers: Model Context Protocol Servers \- GitHub, 1月 3, 2026にアクセス、 https://github.com/riza-io/modelcontextprotocol-servers  
22\. modelcontextprotocol/servers: Model Context Protocol Servers \- GitHub, 1月 3, 2026にアクセス、 https://github.com/modelcontextprotocol/servers  
23\. The MCP Server Stack: 10 Open-Source Essentials for 2026 | by TechLatest.Net | Dec, 2025, 1月 3, 2026にアクセス、 https://medium.com/@techlatest.net/the-mcp-server-stack-10-open-source-essentials-for-2026-cb13f080ca5c  
24\. Top 7 AI Agent Frameworks in 2025 — Ultimate Guide \- Ampcome, 1月 3, 2026にアクセス、 https://www.ampcome.com/post/top-7-ai-agent-frameworks-in-2025  
25\. 10 Open-Source Agent Frameworks for Building Custom Agents in 2026 | by TechLatest.Net | Dec, 2025, 1月 3, 2026にアクセス、 https://medium.com/@techlatest.net/10-open-source-agent-frameworks-for-building-custom-agents-in-2026-4fead61fdc7c  
26\. Top 10 Agentic AI Frameworks to build AI Agents in 2026 | by javinpaul | Javarevisited | Nov, 2025, 1月 3, 2026にアクセス、 https://medium.com/javarevisited/top-10-agentic-ai-frameworks-to-build-ai-agents-in-2026-290618402302  
27\. DSPy: Automating Prompt Engineering — A Complete Tutorial | by Fares Sayah | Dec, 2025, 1月 3, 2026にアクセス、 https://medium.com/@sayahfares19/dspy-automating-prompt-engineering-a-complete-tutorial-42fc3e40a449  
28\. DSPy: The framework for programming—not prompting—language models \- GitHub, 1月 3, 2026にアクセス、 https://github.com/stanfordnlp/dspy  
29\. 20 Best Agent-to-Agent Frameworks (Micro → Medium) for 2025 | by Md Mazaharul Huq | Oct, 2025, 1月 3, 2026にアクセス、 https://medium.com/@jewelhuq/20-best-agent-to-agent-frameworks-micro-medium-for-2025-80c726a48d06  
30\. Framework for orchestrating role-playing, autonomous AI agents. By fostering collaborative intelligence, CrewAI empowers agents to work together seamlessly, tackling complex tasks. \- GitHub, 1月 3, 2026にアクセス、 https://github.com/crewAIInc/crewAI  
31\. Danielskry/Awesome-RAG: Awesome list of Retrieval ... \- GitHub, 1月 3, 2026にアクセス、 https://github.com/Danielskry/Awesome-RAG  
32\. A curated list of awesome LLM agents frameworks. \- GitHub, 1月 3, 2026にアクセス、 https://github.com/kaushikb11/awesome-llm-agents  
33\. FoundationAgents/MetaGPT: The Multi-Agent Framework: First AI Software Company, Towards Natural Language Programming \- GitHub, 1月 3, 2026にアクセス、 https://github.com/FoundationAgents/MetaGPT  
34\. The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery ‍ \- GitHub, 1月 3, 2026にアクセス、 https://github.com/SakanaAI/AI-Scientist  
35\. The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery \- Sakana AI, 1月 3, 2026にアクセス、 https://sakana.ai/ai-scientist/  
36\. LanceDB | Vector Database for RAG, Agents & Hybrid Search, 1月 3, 2026にアクセス、 https://lancedb.com/  
37\. AI Agents Tutorials \- LanceDB, 1月 3, 2026にアクセス、 https://lancedb.com/docs/tutorials/agents/  
38\. Project GraphRAG \- Microsoft Research, 1月 3, 2026にアクセス、 https://www.microsoft.com/en-us/research/project/graphrag/  
39\. Welcome \- GraphRAG, 1月 3, 2026にアクセス、 https://microsoft.github.io/graphrag/  
40\. AI Memory Systems Benchmark: Mem0 vs OpenAI vs LangMem 2025 \- Deepak Gupta, 1月 3, 2026にアクセス、 https://guptadeepak.com/the-ai-memory-wars-why-one-system-crushed-the-competition-and-its-not-openai/  
41\. AI Memory Benchmark: Mem0 vs OpenAI vs LangMem vs MemGPT, 1月 3, 2026にアクセス、 https://mem0.ai/blog/benchmarked-openai-memory-vs-langmem-vs-memgpt-vs-mem0-for-long-term-memory-here-s-how-they-stacked-up  
42\. What is GPTCache \- an open-source tool for AI Apps \- Zilliz, 1月 3, 2026にアクセス、 https://zilliz.com/what-is-gptcache  
43\. Reducing LLM Costs and Latency via Semantic Embedding Caching \- arXiv, 1月 3, 2026にアクセス、 https://arxiv.org/html/2411.05276v2?ref=edony.ink  
44\. Build a coding agent with Modal Sandboxes and LangGraph | Modal Docs, 1月 3, 2026にアクセス、 https://modal.com/docs/examples/agent  
45\. llm-orchestration · GitHub Topics, 1月 3, 2026にアクセス、 https://github.com/topics/llm-orchestration  
46\. Survey of AI Agent Memory Frameworks | Graphlit Blog, 1月 3, 2026にアクセス、 https://www.graphlit.com/blog/survey-of-ai-agent-memory-frameworks  
47\. Deploy Any AI Model with Modal \- Medium, 1月 3, 2026にアクセス、 https://medium.com/@shridharathi/deploy-any-ai-model-with-modal-578b6526c544  
48\. Introduction | Modal Docs, 1月 3, 2026にアクセス、 https://modal.com/docs/guide  
49\. Deploy Langfuse v3 on Railway, 1月 3, 2026にアクセス、 https://langfuse.com/self-hosting/deployment/railway  
50\. We need feedback on a new open-source Railway.app, the Render.com alternative platform, which is running on Kubernetes clusters. \- Reddit, 1月 3, 2026にアクセス、 https://www.reddit.com/r/kubernetes/comments/1f4sqmb/we\_need\_feedback\_on\_a\_new\_opensource\_railwayapp/  
51\. Run Enterprise AI Agents Locally (Open Source), 1月 3, 2026にアクセス、 https://www.youtube.com/watch?v=nIjQ11GaxZo  
52\. LiteLLM Review 2025 | AI Infrastructure & MLOps Tool \- Pricing & Features \- AI Agents List, 1月 3, 2026にアクセス、 https://aiagentslist.com/agents/litellm  
53\. AI Gateway Benchmark: Kong AI Gateway, Portkey, and LiteLLM | Kong Inc., 1月 3, 2026にアクセス、 https://konghq.com/blog/engineering/ai-gateway-benchmark-kong-ai-gateway-portkey-litellm  
54\. vllm-project/vllm: A high-throughput and memory-efficient inference and serving engine for LLMs \- GitHub, 1月 3, 2026にアクセス、 https://github.com/vllm-project/vllm  
55\. Comparing the Top 6 Inference Runtimes for LLM Serving in 2025 \- MarkTechPost, 1月 3, 2026にアクセス、 https://www.marktechpost.com/2025/11/07/comparing-the-top-6-inference-runtimes-for-llm-serving-in-2025/  
56\. Streamlit vs Chainlit: Which is Better for AI Apps? | Beginners Guide \- YouTube, 1月 3, 2026にアクセス、 https://www.youtube.com/watch?v=GqltEDPixX0  
57\. Lakshya-Ag/Streamlit-Dashboard: Interactive data science and machine learning dashboards on the stock market analysis and making predictions for companies' stock prices. \- GitHub, 1月 3, 2026にアクセス、 https://github.com/Lakshya-Ag/Streamlit-Dashboard  
58\. Open Source LangSmith Alternative: Arize Phoenix vs. LangSmith, 1月 3, 2026にアクセス、 https://arize.com/docs/phoenix/resources/frequently-asked-questions/open-source-langsmith-alternative-arize-phoenix-vs.-langsmith  
59\. LangSmith vs. Phoenix by Arize AI: Choosing the Right Tool for LLM Observability \- Medium, 1月 3, 2026にアクセス、 https://medium.com/@aunraza021/langsmith-vs-phoenix-by-arize-ai-choosing-the-right-tool-for-llm-observability-0b4c2f21c077  
60\. What are the best open source LLM observability platforms/packages? : r/LangChain, 1月 3, 2026にアクセス、 https://www.reddit.com/r/LangChain/comments/1neh5sw/what\_are\_the\_best\_open\_source\_llm\_observability/  
61\. Compare Chainlit vs. Streamlit in 2025 \- Slashdot, 1月 3, 2026にアクセス、 https://slashdot.org/software/comparison/Chainlit-vs-Streamlit/  
