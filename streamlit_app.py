import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(page_title="ボート部専用ポータル", layout="centered")

# CSS: 画像とボタンを完全に中央揃えにする設定
st.markdown("""
    <style>
    .item-container { 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center;
        margin-bottom: 25px;
    }
    .menu-img { 
        width: 80px; 
        height: 80px; 
        object-fit: cover; 
        margin-bottom: 10px; 
        display: block; 
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
                    st.markdown('<div class="item-container">', unsafe_allow_html=True)
                    
                    # 画像（HTMLのimgタグを直接使用して中央寄せを保証）
                    st.markdown(f'''
                        <a href="{url}" target="_blank">
                            <img src="app/static/{item["icon"]}" class="menu-img">
                        </a>
                    ''', unsafe_allow_html=True)
                    
                    # ボタン
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
