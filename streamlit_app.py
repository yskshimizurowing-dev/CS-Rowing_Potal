import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(page_title="ボート部専用ポータル", layout="centered")

# CSS: コンテナ全体を中央寄せし、画像とボタンの配置を揃える設定
st.markdown("""
    <style>
    .menu-item-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin-bottom: 20px;
    }
    .stImage {
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
    }
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
                    
                    # コンテナ開始
                    st.markdown('<div class="menu-item-box">', unsafe_allow_html=True)
                    
                    # 1. 画像表示（標準のst.imageを使用）
                    try:
                        st.image(item["icon"], width=80)
                    except:
                        st.write("画像なし")
                    
                    # 2. ボタン/リンク表示
                    if item["type"] == "page":
                        if st.button(item["label"], key=f"btn_{i+j}", use_container_width=True):
                            st.switch_page(item["url"])
                    elif item["type"] == "dev":
                        if st.button(item["label"], key=f"btn_{i+j}", use_container_width=True):
                            st.toast("現在開発中です")
                    else:
                        st.link_button(item["label"], url, use_container_width=True)
                    
                    # コンテナ終了
                    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("ログインしてください。")
