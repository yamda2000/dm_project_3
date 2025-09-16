## 要件定義書 / FAQチャットボット簡易要件定義書

### 1. プロジェクト概要

#### 1.1 目的
ローカルの製品データ（CSV）を参照し、ユーザーの要望に合致する商品を検索して提示するシンプルなレコメンド型チャットアプリを開発する。Streamlit を用いたチャット UI 上で、LangChain の Retriever（FAISS + BM25 アンサンブル）により関連商品を取得し表示する。

#### 1.2 スコープ
- Web UI（Streamlit）での対話機能
- ローカル CSV の読み込みとベクトル検索（FAISS）/語彙検索（BM25）
- 検索結果（商品情報・画像・在庫状況など）の提示

### 2. 機能要件

#### 2.1 ドキュメント（データ）管理
- 対応フォーマット: CSV（製品カタログ）。現状 PDF/TXT/Markdown は対象外
- ファイル配置: `./data/products.csv`
- 更新: アプリケーション起動時に読み込み（`CSVLoader`）

#### 2.2 チャット機能
- 入力: テキストベースの要望・条件（例:「長時間使えるワイヤレスイヤホン」）
- 処理:
  - 入力テキストのログ出力
  - ベクトル検索（FAISS, OpenAI Embeddings）と BM25 による語彙検索
  - アンサンブル（`EnsembleRetriever`）で統合し、上位 k 件を取得
- 出力:
  - 推奨商品の要約（商品名、価格、カテゴリ、メーカー、評価、説明、画像、在庫ステータス、リンク）
  - 画面上の注意/警告表示（在庫が少ない・在庫なし）

#### 2.3 基本設定
- LLMモデル: なし（生成は行わず、類似商品ドキュメントの取得に特化）
- 埋め込みモデル: OpenAI Embeddings（LangChain `OpenAIEmbeddings` のデフォルト）
- チャンクサイズ: なし（CSV 行をそのまま扱う）
- 検索結果数: 上位 5 件（`constants.TOP_K`）

### 3. 技術仕様

#### 3.1 必須コンポーネント（主要ライブラリ）
- streamlit
- langchain / langchain-community / langchain-openai
- faiss-cpu
- rank-bm25（`BM25Retriever`）
- sudachipy（日本語形態素解析・前処理で使用）
- python-dotenv
- pillow（画像表示）

※ `chromadb` は要件候補だが現状未使用（FAISS を使用）。

#### 3.2 基本アーキテクチャ
ユーザー入力
↓
前処理（日本語形態素解析・単語抽出）
↓
埋め込み生成（OpenAI Embeddings）
↓
ベクトル検索（FAISS） + 語彙検索（BM25）
↓
アンサンブルで関連ドキュメント取得
↓
結果のレンダリング（商品情報表示）

#### 3.3 ディレクトリ構造（抜粋）

project/
├── main.py                # Streamlit エントリポイント
├── initialize.py          # 初期化（ログ/セッション/Retriever 構築）
├── components.py          # 画面表示用コンポーネント
├── utils.py               # 共通関数（前処理ほか）
├── constants.py           # 設定値・メッセージ定義
├── data/
│   └── products.csv       # レコメンド元データ
├── images/                # 画像（アイコン/商品画像）
├── logs/                  # ログ出力
└── requirements.txt

### 4. 実装要件

#### 4.1 基本実装フロー
1. 初期化処理（`initialize()`）
   - セッション状態とセッション ID を生成
   - ログハンドラ設定（日次ローテーション）
   - データロード（`CSVLoader`）
   - Windows 環境向けの文字列正規化（`adjust_string`）
   - 日本語前処理関数（SudachiPy）準備
   - Embeddings 作成（OpenAIEmbeddings）
   - ベクトルストア生成（FAISS）→ Retriever 化
   - 語彙検索（BM25Retriever）生成
   - `EnsembleRetriever` で統合し `st.session_state.retriever` に格納

2. 質問応答（レコメンド）処理（`main.py`）
   - 入力受け付け: `st.chat_input`
   - 検索実行: `retriever.invoke(user_query)`
   - 表示: `components.display_product` で商品情報・在庫・画像・リンクを描画
   - 会話ログを保持し、過去メッセージを再表示

#### 4.2 エラーハンドリング
- API キー未設定時: `.env` を試行し、無い場合は `st.secrets["OPENAI_API_KEY"]` を参照
- 初期化失敗: 画面上にエラー表示し処理停止
- 会話ログ表示失敗/商品表示失敗: ログ出力・画面表示後に停止
- データ未登録・検索結果なし: 上位 k 件取得で空の場合に備えた防御的実装（今後の改善対象）
- Windows 特有の文字化け: Unicode 正規化と cp932 非対応文字の除去

### 5. 動作要件

#### 5.1 環境要件
- Python 3.11（3.8 以上を想定）
- OpenAI API キー（Embeddings 用）
- メモリ: 1GB 以上推奨
- ストレージ: 数百 MB 程度（CSV + ログ + 画像）

#### 5.2 制限事項
- 同時実行は 1 セッションを想定（Streamlit のセッション状態依存）
- データサイズは CSV ベースで数万行程度までを目安（FAISS/BM25 のパフォーマンスに依存）
- 1 回の入力は 500 文字程度までを推奨（UI・可読性観点）
- 応答は検索・描画中心で 10 秒以内目安（環境/Embeddings API レイテンシに依存）

### 付記（今後の拡張案）
- PDF/TXT/Markdown ローダーの導入とテキストスプリッターによる分割
- ChromaDB への切り替え/併用、永続ベクトルストア管理
- LLM を用いた生成型回答（商品説明の要約・比較・根拠提示）
- 検索結果メタデータ（スコアや出典）の UI 表示強化
- API 制限・レート超過時のリトライ/バックオフ強化
