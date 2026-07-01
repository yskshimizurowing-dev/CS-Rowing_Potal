import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(page_title="ボート部専用ポータル", layout="centered")

# CSS: 画像のサイズを制限し、マウスオーバーでポインタを表示する
st.markdown("""
    <style>
    .menu-img { width: 100px; height: 100px; object-fit: cover; border-radius: 10px; margin-bottom: 5px; }
    .item-container { text-align: center; margin-bottom: 20px; }
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
                    
                    # 画像をクリック可能なリンクにする
                    st.markdown(f'<div class="item-container"><a href="{url}" target="_blank">', unsafe_allow_html=True)
                    try:
                        # 画像サイズをCSSのクラスで制限
                        st.image(item["icon"], width=100) 
                    except:
                        st.write("画像なし")
                    st.markdown('</a>', unsafe_allow_html=True)
                    
                    # ボタンでリンク遷移
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
