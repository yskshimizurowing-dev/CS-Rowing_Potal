import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(page_title="ボート部専用ポータル", layout="centered")

st.title("🚣 ボート部専用ポータル")

visible_items = [item for item in MENU_ITEMS if item.get("visible", True)]

if st.user is not None:
    # 3列を作成
    cols = st.columns(3)
    
    # 全てのアイテムをループで回す
    for idx, item in enumerate(visible_items):
        with cols[idx % 3]:
            url = get_url(item)
            
            # 画像の配置（カラムの中で中央に寄せる）
            st.image(item["icon"], use_container_width=True)
            
            # ボタン/リンク表示
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
