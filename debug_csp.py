# debug_csp.py
"""
CSPエラーの原因を特定するためのデバッグアプリ
段階的に機能を有効化してエラーの原因を特定する
"""

import streamlit as st
import logging

# 基本設定
st.set_page_config(page_title="CSP Debug App")

st.title("🔍 CSPエラーデバッグアプリ")
st.markdown("各ステップでエラーが発生しないか確認してください")

# ========================================
# Step 1: 基本的なStreamlit機能
# ========================================
st.header("Step 1: 基本Streamlit機能")
if st.checkbox("✅ Step 1を実行", value=True):
    st.success("基本的なStreamlit機能は正常動作中")
    st.write("マークダウン表示OK")
    st.info("info表示OK")
    st.warning("warning表示OK")
    st.error("error表示OK")

# ========================================
# Step 2: constants.pyの読み込み
# ========================================
st.header("Step 2: constants.py読み込み")
if st.checkbox("Step 2を実行"):
    try:
        import constants as ct
        st.success("✅ constants.py読み込み成功")
        st.write(f"APP_NAME: {getattr(ct, 'APP_NAME', '未定義')}")
    except Exception as e:
        st.error(f"❌ constants.py読み込みエラー: {e}")

# ========================================
# Step 3: components.pyの各関数テスト
# ========================================
st.header("Step 3: components.py各関数テスト")

if st.checkbox("Step 3-1: display_app_title"):
    try:
        import components as cn
        cn.display_app_title()
        st.success("✅ display_app_title成功")
    except Exception as e:
        st.error(f"❌ display_app_title エラー: {e}")

if st.checkbox("Step 3-2: display_initial_ai_message"):
    try:
        import components as cn
        cn.display_initial_ai_message()
        st.success("✅ display_initial_ai_message成功")
    except Exception as e:
        st.error(f"❌ display_initial_ai_message エラー: {e}")

if st.checkbox("Step 3-3: display_conversation_log"):
    try:
        import components as cn
        # 最小限のsession_state設定
        if "messages" not in st.session_state:
            st.session_state.messages = []
        cn.display_conversation_log()
        st.success("✅ display_conversation_log成功")
    except Exception as e:
        st.error(f"❌ display_conversation_log エラー: {e}")

# ========================================
# Step 4: utils.pyの読み込み
# ========================================
st.header("Step 4: utils.py読み込み")
if st.checkbox("Step 4を実行"):
    try:
        import utils
        st.success("✅ utils.py読み込み成功")
        # utilsに関数がある場合はテスト
        test_message = utils.build_error_message("テストエラー")
        st.write(f"build_error_message結果: {test_message}")
    except Exception as e:
        st.error(f"❌ utils.py読み込みエラー: {e}")

# ========================================
# Step 5: initialize.pyの読み込み（注意が必要）
# ========================================
st.header("Step 5: initialize.py読み込み")
st.warning("⚠️ この段階でCSPエラーが発生する可能性があります")
if st.checkbox("Step 5を実行（危険）"):
    try:
        from initialize import initialize
        st.success("✅ initialize.py読み込み成功")
        st.info("initialize関数の実行は別途テストしてください")
    except Exception as e:
        st.error(f"❌ initialize.py読み込みエラー: {e}")

# ========================================
# Step 6: LangChain関連の確認
# ========================================
st.header("Step 6: LangChain関連")
st.warning("⚠️ LangChainがCSPエラーの原因の可能性があります")
if st.checkbox("Step 6を実行（危険）"):
    try:
        # LangChain関連のインポートをテスト
        from langchain.embeddings import OpenAIEmbeddings
        from langchain.vectorstores import FAISS
        st.success("✅ LangChain基本インポート成功")
    except Exception as e:
        st.error(f"❌ LangChain関連エラー: {e}")

# ========================================
# デバッグ情報の表示
# ========================================
st.header("🔧 デバッグ情報")
st.subheader("ブラウザコンソールの確認方法")
st.code("""
1. F12キーを押して開発者ツールを開く
2. Consoleタブを選択
3. 以下のようなエラーメッセージを探す：
   
   "Refused to evaluate a string as JavaScript because 'unsafe-eval' is not an allowed source"
   
4. エラーメッセージをクリックしてスタックトレースを確認
5. どのファイル・行でエラーが発生しているか特定
""")

st.subheader("次にチェックすべきファイル")
st.info("""
1. initialize.py - LangChainの初期化処理
2. utils.py - ユーティリティ関数
3. requirements.txt - 使用ライブラリのバージョン
4. LangChain関連のコード - RAG実装部分
""")

# session_stateの内容確認
st.subheader("Session State確認")
if st.checkbox("Session State表示"):
    st.json(dict(st.session_state))