import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(page_title="ボート部専用ポータル", layout="centered")

# CSS: スマホでも3列を維持する設定
st.markdown("""
    <style>
    /* カラムの親要素に固定幅を適用し、縦並びを防ぐ */
    [data-testid="column"] {
        flex: 1 1 30% !important;
        max-width: 30% !important;
    }
    .stButton > button { width: 100%; }
    </style>
""", unsafe_allow_html=True)

st.title("🚣 ボート部専用ポータル")

visible_items = [item for item in MENU_ITEMS if item.get("visible", True)]

if st.user is not None:
    # 3列を作る
    cols = st.columns(3)
    # 全てのアイテムを並べる（列をループさせる）
    for idx, item in enumerate(visible_items):
        with cols[idx % 3]:
            url = get_url(item)
            
            # 画像の配置（中央寄せ）
            img_col1, img_col2, img_col3 = st.columns([1, 4, 1])
            with img_col2:
                try:
                    st.image(item["icon"], use_container_width=True)
                except:
                    st.write(" ")
            
            # ボタン/リンク
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
