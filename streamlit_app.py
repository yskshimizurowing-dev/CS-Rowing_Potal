import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(layout="centered")

# スマホでもPCでも絶対に3列を維持し、画像と文字を中央に揃えるCSS
st.markdown("""
    <style>
    /* 3列のグリッドを強制指定（スマホでも崩れない） */
    .portal-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        width: 100%;
        margin-top: 20px;
    }
    /* ボタン風の見た目を作る設定 */
    .portal-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        text-decoration: none !important;
        color: inherit !important;
        background-color: #f0f2f6; /* Streamlitの標準ボタンに近い背景色 */
        padding: 12px 8px;
        border-radius: 8px;
        transition: background-color 0.2s;
    }
    .portal-item:hover {
        background-color: #e0e4ec; /* タップ/ホバー時の色 */
    }
    .portal-img {
        width: 50px;
        height: 50px;
        object-fit: contain;
        margin-bottom: 8px;
    }
    .portal-label {
        font-size: 12px;
        font-weight: 500;
        line-height: 1.3;
        white-space: pre-wrap; /* 補正：改行文字を有効にする */
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚣 ボート部専用ポータル")

visible_items = [item for item in MENU_ITEMS if item.get("visible", True)]

if st.user is not None:
    # グリッドの器を開始
    st.markdown('<div class="portal-grid">', unsafe_allow_html=True)
    
    for item in visible_items:
        url = get_url(item)
        label_display = item["label"].replace('\n', '<br>') # 改行をHTML用に変換
        
        # ページ内遷移(page)や開発中(dev)の挙動をHTMLのリンクやStreamlitのクエリ等で処理する簡易的なハック
        # ※今回は一番確実な「すべてのボタンをリンクとして機能させる」形で配置します
        st.markdown(f'''
            <a href="{url}" target="_self" class="portal-item">
                <img src="app/static/{item["icon"]}" class="portal-img" onerror="this.src='https://img.icons8.com/ios/50/image.png'">
                <div class="portal-label">{label_display}</div>
            </a>
        ''', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True) # グリッド終了
else:
    st.warning("ログインしてください。")
