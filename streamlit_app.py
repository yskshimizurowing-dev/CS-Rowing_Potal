import streamlit as st

import streamlit as st
import os

# --- 1. 設定・定義 ---
SECRET_TOKEN = st.secrets["GAS_TOKEN"]

# ボタンの設定リスト
# ※ すべてのURLを Secrets.toml に登録し、ここではキー名を指定します
BUTTONS = [
    {"label": "🏋️\n\nトレーニング", "key": "URL_TRAINING", "type": "gas"},
    {"label": "📋\n\nホワイトボード", "key": "URL_WHITEBOARD", "type": "gas"},
    {"label": "📝\n\n欠席連絡", "key": "URL_FORM", "type": "link"},
    {"label": "🚣\n\n測定記録DB", "key": "URL_DB", "type": "gas"},
    {"label": "🧮\n\nAverage計算", "url": "pages/calculator.py", "type": "page"},
    {"label": "🔧\n\nリギング", "key": "URL_RIGGING", "type": "gas"},
    {"label": "📦\n\n備品管理", "key": "URL_TOOL", "type": "gas"},
    {"label": "📊\n\n動画解析", "url": "dev", "type": "dev"},
    {"label": "☁️\n\nGoogleドライブ", "key": "URL_DRIVE", "type": "link"}, 
]

# --- 2. 基本設定 ---
st.set_page_config(
    page_title="ボート部専用ポータル",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("<h1 style='text-align: center; color: #333;'>ボート部専用ポータル</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>メニューを選択してください</p>", unsafe_allow_html=True)
st.write("---")

# --- 3. デザインCSS ---
st.markdown('''
<style>
    /* 1. 画面全体の横幅とマージンを調整 */
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* 2. ボタンの配置用コンテナの制御 */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        gap: 10px !important; /* 隙間を固定 */
    }

    /* 3. 各カラムを確実に3等分する */
    div[data-testid="stHorizontalBlock"] > div {
        flex: 1 !important;
        min-width: 0 !important; /* これが重要：幅を強制的に収める */
    }
    
    /* 4. ボタンの見た目調整 */
    div.stButton > button, div.stLinkButton > a {
        width: 100% !important;
        height: 100px !important; /* 高さを固定して正方形に近づける */
        padding: 5px !important;
        font-size: 12px !important;
        white-space: pre-line !important; /* 改行を有効にする */
        border-radius: 12px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
    }
</style>
''', unsafe_allow_html=True)

# --- 4. ログイン認証確認とボタン描画 ---
if st.user is not None:
    for i in range(0, 9, 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            btn = BUTTONS[i + j]
            with col:
                # リンク先URLの取得ロジック（URL直接指定 or Secrets参照）
                target_url = st.secrets.get(btn["key"]) if "key" in btn else btn.get("url")

                if btn["type"] == "gas":
                    url_with_token = f"{target_url}?token={SECRET_TOKEN}"
                    st.link_button(btn["label"], url_with_token, use_container_width=True)
                
                elif btn["type"] == "link":
                    st.link_button(btn["label"], target_url, use_container_width=True)
                
                elif btn["type"] == "page":
                    if st.button(btn["label"], use_container_width=True):
                        st.switch_page(btn["url"])
                
                elif btn["type"] == "dev":
                    if st.button(btn["label"], use_container_width=True):
                        st.toast(f"{btn['label'].splitlines()[-1]}は現在開発中です！")
else:
    st.warning("ポータルを利用するにはログインが必要です。")
