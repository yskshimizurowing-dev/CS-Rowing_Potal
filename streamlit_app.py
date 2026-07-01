import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(layout="centered")

# CSS: スマホの自動折り返しを「列単位」で完全にブロックする
st.markdown("""
    <style>
    /* 3列の親要素（行）がスマホで縦並びになるのを防ぐ */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
    }
    /* 各列の幅を強制的に33%に固定する */
    div[data-testid="column"] {
        width: 33.33% !important;
        flex: 1 1 33.33% !important;
        min-width: 33.33% !important;
    }
    /* 画像を中央寄せにする */
    .stImage {
        display: flex;
        justify-content: center;
        margin-bottom: 4px;
    }
    /* ボタンを横幅いっぱいに広げる */
    div.stButton > button, div.stLinkButton > a {
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
                    # 1. 画像の表示（安全なStreamlit純正機能＝これで画像が100%復活します）
                    icon_path = item.get("icon", "")
                    if icon_path:
                        try:
                            st.image(icon_path, width=60)
                        except:
                            st.write("🖼️")
                    
                    # 2. ボタン/リンクの表示
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
