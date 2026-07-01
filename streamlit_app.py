import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(layout="centered")

st.title("🚣 ボート部専用ポータル")

visible_items = [item for item in MENU_ITEMS if item.get("visible", True)]

# 3列で表示（PC/スマホのレイアウト崩れ対策として、最も標準的な方法）
cols = st.columns(3)

if st.user is not None:
    for idx, item in enumerate(visible_items):
        with cols[idx % 3]:
            # 画像パスを直接指定
            icon_path = item.get("icon", "")
            
            # 画像表示
            if icon_path:
                st.image(icon_path, use_container_width=True)
            
            # ボタン
            url = get_url(item)
            if item["type"] == "page":
                if st.button(item["label"], key=f"btn_{idx}", use_container_width=True):
                    st.switch_page(item["url"])
            elif item["type"] == "dev":
                if st.button(item["label"], key=f"btn_{idx}", use_container_width=True):
                    st.toast("現在開発中です")
            else:
                st.link_button(item["label"], url, use_container_width=True)
else:
    st.warning("ログインしてください。")
