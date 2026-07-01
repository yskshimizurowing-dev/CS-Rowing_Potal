import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(page_title="ボート部専用ポータル", layout="centered")

st.markdown("<style>header{display:none !important;}</style>", unsafe_allow_html=True)
st.title("🚣 ボート部専用ポータル")

visible_items = [item for item in MENU_ITEMS if item.get("visible", True)]

if st.user is not None:
    for i in range(0, len(visible_items), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(visible_items):
                item = visible_items[i + j]
                with col:
                    url = get_url(item)
                    # 画像表示（エラー回避のためtry-exceptを使用）
                    try:
                        st.image(item["icon"], use_container_width=True)
                    except:
                        st.write("画像なし")
                    
                    # ボタンまたはリンク
                    if item["type"] == "page":
                        if st.button(item["label"], key=f"btn_{i+j}"):
                            st.switch_page(item["url"])
                    elif item["type"] == "dev":
                        if st.button(item["label"], key=f"btn_{i+j}"):
                            st.toast("現在開発中です")
                    else:
                        st.link_button(item["label"], url)
else:
    st.warning("ログインしてください。")
