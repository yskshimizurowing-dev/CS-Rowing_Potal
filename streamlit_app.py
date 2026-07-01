import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(page_title="ボート部専用ポータル", layout="centered")

# スマホでも絶対に3列を維持するCSS
st.markdown("""
    <style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        width: 100%;
    }
    .grid-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }
    .menu-img { width: 100%; max-width: 80px; height: auto; }
    </style>
""", unsafe_allow_html=True)

st.title("🚣 ボート部専用ポータル")

visible_items = [item for item in MENU_ITEMS if item.get("visible", True)]

if st.user is not None:
    # グリッドコンテナを開始
    st.markdown('<div class="grid-container">', unsafe_allow_html=True)
    
    for item in visible_items:
        url = get_url(item)
        
        # 各アイテムをdivで囲む
        st.markdown('<div class="grid-item">', unsafe_allow_html=True)
        
        # 画像表示
        try:
            st.image(item["icon"], width=80)
        except:
            st.write(" ")
            
        # ボタン/リンク表示
        if item["type"] == "page":
            if st.button(item["label"], key=f"btn_{item['label']}", use_container_width=True):
                st.switch_page(item["url"])
        elif item["type"] == "dev":
            if st.button(item["label"], key=f"btn_{item['label']}", use_container_width=True):
                st.toast("現在開発中です")
        else:
            st.link_button(item["label"], url, use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True) # grid-container終了
else:
    st.warning("ログインしてください。")
