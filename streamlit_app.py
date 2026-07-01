import streamlit as st
from config import MENU_ITEMS
from utils import get_url

# ★超重要: 画面幅の自動縮小を防ぐためのCSSを最優先で適用
st.set_page_config(layout="wide")

st.markdown("""
    <style>
    /* アプリ全体の最小横幅を1000pxに固定し、スマホでもPC表示を強制する */
    .stApp {
        min-width: 1000px !important;
    }
    /* 画像を中央寄せにする設定 */
    .stImage {
        display: flex;
        justify-content: center;
        margin-bottom: 5px;
    }
    /* ボタンを横幅いっぱいに広げる */
    div.stButton > button {
        width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚣 ボート部専用ポータル")

visible_items = [item for item in MENU_ITEMS if item.get("visible", True)]

if st.user is not None:
    # 3個ずつ安全に分割してループ
    for i in range(0, len(visible_items), 3):
        cols = st.columns(3)
        
        for j in range(3):
            if i + j < len(visible_items):
                item = visible_items[i + j]
                with cols[j]:
                    # 1. 画像の表示（安全な純正機能）
                    icon_path = item.get("icon", "")
                    if icon_path:
                        try:
                            st.image(icon_path, width=70)
                        except:
                            st.write("🖼️")
                    
                    # 2. ボタン/リンクの表示（安全な純正機能）
                    url = get_url(item)
                    if item["type"] == "page":
                        if st.button(item["label"], key=f"btn_{i+j}", use_container_width=True):
                            st.switch_page(item["url"])
                    elif item["type"] == "dev":
                        if st.button(item["label"], key=f"btn_{i+j}", use_container_width=True):
                            st.toast("現在開発中です")
                    else:
                        st.link_button(item["label"], url, use_container_width=True)
else:
    st.warning("ログインしてください。")
