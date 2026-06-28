import streamlit as st

# --- 1. 設定・定義 ---
SECRET_TOKEN = "your_secret_key_2026"

# ボタンの設定リスト
BUTTONS = [
    {"label": "🏋️\n\nトレーニング", "url": "https://script.google.com/macros/s/AKfycbzWNeZKPqD-V4FWsZP-90kpEP7M48O7XeUqw_DNPu1kIBvAvJMmP2A0QZ9UQW0r3yxf8w/exec", "type": "gas"},
    {"label": "📋\n\nホワイトボード", "url": "pages/whiteboard.py", "type": "page"},
    {"label": "📝\n\n欠席連絡", "url": "https://forms.gle/BRUbZgVGwcyvKd7v6", "type": "link"},
    {"label": "🚣\n\n測定記録DB", "url": "https://script.google.com/macros/s/YYYY/exec", "type": "gas"},
    {"label": "🧮\n\nAverage計算", "url": "pages/calculator.py", "type": "page"},
    {"label": "🔧\n\nリギング", "url": "https://script.google.com/macros/s/ZZZZ/exec", "type": "gas"},
    {"label": "📦\n\n備品管理", "url": "dev", "type": "dev"},
    {"label": "📊\n\n動画解析", "url": "dev", "type": "dev"},
    {"label": "☁️\n\n共有ドライブ", "url": "https://drive.google.com/drive/folders/0AKWbU0VyiymNUk9PVA", "type": "link"},
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
    .stApp { overflow-x: hidden !important; }
    div[data-testid="stHorizontalBlock"] { flex-direction: row !important; flex-wrap: nowrap !important; gap: 8px !important; }
    div[data-testid="stHorizontalBlock"] > div { width: calc((100% - 16px) / 3) !important; flex: 0 0 calc((100% - 16px) / 3) !important; }
    div.stButton > button, div.stLinkButton > a { 
        min-height: 100px !important; 
        white-space: pre-wrap !important; 
        font-weight: bold !important; 
        border-radius: 16px !important; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important; 
        font-size: 13px !important; 
        padding: 0px !important; 
    }
</style>
''', unsafe_allow_html=True)

# --- 4. ボタン描画ロジック ---
# ログイン判定が必要な場合はインデントを揃えて記述します
if st.session_state.get("logged_in"):
    for i in range(0, 9, 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            btn = BUTTONS[i + j]
            with col:
                if btn["type"] == "gas":
                    url_with_token = f"{btn['url']}?token={SECRET_TOKEN}"
                    st.link_button(btn["label"], url_with_token, use_container_width=True)
                elif btn["type"] == "link":
                    st.link_button(btn["label"], btn["url"], use_container_width=True)
                elif btn["type"] == "page":
                    if st.button(btn["label"], use_container_width=True):
                        st.switch_page(btn["url"])
                elif btn["type"] == "dev":
                    if st.button(btn["label"], use_container_width=True):
                        st.toast(f"{btn['label'].splitlines()[-1]}は現在開発中です！")
else:
    st.info("ログインしてください。")
