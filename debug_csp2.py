# iframe_debug.py
"""
iframeサンドボックス問題を特定するためのデバッグアプリ
"""

import streamlit as st
import streamlit.components.v1 as components

st.title("🔍 iframe サンドボックス問題デバッグ")

st.markdown("""
**エラーメッセージ:** 
`An iframe which has both allow-scripts and allow-same-origin for its sandbox attribute can escape its sandboxing`

このエラーは `st.components.html()` やカスタムコンポーネントが原因の可能性があります。
""")

# ========================================
# 1. 基本的なHTML埋め込みテスト
# ========================================
st.header("1. 基本HTML埋め込みテスト")
if st.checkbox("基本HTMLテスト"):
    # 安全なHTML
    components.html("""
    <div style="padding: 10px; border: 1px solid #ccc;">
        <h3>テストHTML</h3>
        <p>これは基本的なHTMLです</p>
    </div>
    """, height=100)
    st.success("✅ 基本HTML表示成功")

# ========================================
# 2. JavaScriptを含むHTMLテスト
# ========================================
st.header("2. JavaScript埋め込みテスト")
st.warning("⚠️ この部分でエラーが発生する可能性があります")
if st.checkbox("JavaScriptテスト（注意）"):
    # JavaScriptを含むHTML - これがCSPエラーの原因の可能性
    components.html("""
    <div style="padding: 10px; border: 1px solid #ccc;">
        <h3>JavaScript Test</h3>
        <button onclick="showMessage()">クリック</button>
        <p id="message"></p>
        
        <script>
        function showMessage() {
            document.getElementById('message').innerHTML = 'JavaScriptが実行されました';
        }
        </script>
    </div>
    """, height=150)

# ========================================
# 3. 外部スクリプト読み込みテスト
# ========================================
st.header("3. 外部スクリプトテスト")
if st.checkbox("外部スクリプトテスト（危険）"):
    # 外部スクリプト - これもCSPエラーの原因になりうる
    components.html("""
    <div style="padding: 10px; border: 1px solid #ccc;">
        <h3>外部スクリプトテスト</h3>
        <div id="external-content">読み込み中...</div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
        <script>
        // jQueryを使ったコード
        $(document).ready(function() {
            $('#external-content').text('外部スクリプト読み込み成功');
        });
        </script>
    </div>
    """, height=100)

# ========================================
# 4. iframeの直接使用テスト
# ========================================
st.header("4. iframe直接使用テスト")
if st.checkbox("iframe直接テスト（最も危険）"):
    # iframe の直接埋め込み
    components.html("""
    <iframe 
        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3241.747892366805!2d139.69171531525453!3d35.689489980197806!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x60188b9b16088c17%3A0x5b9a3e1c1a1a1a1a!2z5rih5bC66aeF!5e0!3m2!1sja!2sjp!4v1234567890123"
        width="100%" 
        height="200"
        style="border:0;"
        allowfullscreen=""
        loading="lazy"
        sandbox="allow-scripts allow-same-origin">
    </iframe>
    """, height=220)

# ========================================
# 5. LangChainコンポーネントのHTMLチェック
# ========================================
st.header("5. アプリで使用しているコンポーネントのチェック")

st.subheader("display_product関数のシミュレーション")
if st.checkbox("display_product シミュレーション"):
    # あなたのdisplay_product関数をシミュレート
    mock_result = [{
        'page_content': '''name: テスト商品
id: TEST001
price: ¥1,000
stock_status: あり
category: テストカテゴリ
maker: テストメーカー
score: 4.5
review_number: 100
file_name: test.jpg
description: これはテスト商品です
recommended_people: テスト用途の方'''
    }]
    
    # 商品情報の表示をシミュレート
    product_lines = mock_result[0]['page_content'].split("\n")
    try:
        product = {item.split(": ")[0]: item.split(": ")[1] for item in product_lines}
        
        st.markdown("以下の商品をご提案いたします。")
        st.success(f"商品名：{product['name']}（商品ID: {product['id']}）")
        st.code(f"商品カテゴリ：{product['category']}")
        st.info(product["recommended_people"])
        st.link_button("商品ページを開く", url="https://google.com")
        
        st.success("✅ display_product シミュレーション成功")
    except Exception as e:
        st.error(f"❌ display_product エラー: {e}")

# ========================================
# デバッグ情報
# ========================================
st.header("🔧 デバッグ情報")

st.subheader("考えられる原因")
st.info("""
1. **st.components.html()でのJavaScript使用**
   - 内部でeval()やnew Function()を使用
   - sandbox属性の不適切な設定

2. **外部ライブラリの内部処理**
   - LangChain, OpenAI, その他のライブラリが内部でiframeを使用
   - ライブラリ内のHTML/JS生成処理

3. **Streamlit自体のバグ**
   - 特定のバージョンでのiframe処理問題
""")

st.subheader("解決方法の候補")
st.success("""
1. **st.components.html()の使用を避ける**
   - 標準のStreamlitコンポーネントのみ使用
   - HTMLを直接埋め込まない

2. **ライブラリのバージョンダウン**
   - 問題のないバージョンに戻す

3. **代替実装の検討**
   - カスタムHTMLを使わない方法で同じ機能を実現
""")

# Streamlitのバージョン情報
st.subheader("環境情報")
st.code(f"Streamlit version: {st.__version__}")

st.markdown("""
**次のステップ:**
1. 上記テストでどこでエラーが発生するか確認
2. requirements.txtの全ライブラリのバージョン確認
3. エラーが発生する具体的なコンポーネントの特定
""")