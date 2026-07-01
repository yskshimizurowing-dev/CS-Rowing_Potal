import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(page_title="ボート部専用ポータル", layout="centered")

# CSSで画像を中央寄せし、ボタンの幅と合わせる設定
st.markdown("""
    <style>
    .item-container { 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center;
        margin-bottom: 20px;
    }
    .stImage { display: flex; justify-content: center; }
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
                    
                    # コンテナで囲んで中央寄せを強制する
                    st.markdown('<div class="item-container">', unsafe_allow_html=True)
                    
                    # 画像（リンク付き）
                    st.markdown(f'<a href="{url}" target="_blank">', unsafe_allow_html=True)
                    try:
                        st.image(item["icon"], width=80) 
                    except:
                        st.write("画像なし")
                    st.markdown('</a>', unsafe_allow_html=True)
                    
                    # ボタン
                    if item["type"] == "page":
                        if st.button(item["label"], key=f"btn_{i+j}", use_container_width=True):
                            st.switch_page(item["url"])
                    elif item["type"] == "dev":
                        if st.button(item["label"], key=f"btn_{i+j}", use_container_width=True):
                            st.toast("現在開発中です")
                    else:
                        st.link_button(item["label"], url, use_container_width=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("ログインしてください。")
