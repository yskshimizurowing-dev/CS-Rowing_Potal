import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(page_title="ボート部専用ポータル", layout="centered")

# スタイルを調整して画像をボタンの上にピッタリ配置する
st.markdown("""
    <style>
    .stImage { margin-bottom: 0px !important; }
    div.stButton > button { width: 100%; }
    </style>
""", unsafe_allow_html=True)

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
                    
                    # 画像を表示（ボタンの幅に合わせる）
                    try:
                        st.image(item["icon"], use_container_width=True)
                    except:
                        st.write(" ")
                    
                    # ボタンまたはリンクの描画
                    if item["type"] == "page":
                        if st.button(item["label"], key=f"btn_{i+j}"):
                            st.switch_page(item["url"])
                    elif item["type"] == "dev":
                        if st.button(item["label"], key=f"btn_{i+j}"):
                            st.toast("現在開発中です")
                    else:
                        st.link_button(item["label"], url, use_container_width=True)
else:
    st.warning("ログインしてください。")
