import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(layout="centered")

# CSS: 画像を中央寄せし、ボタンのサイズを統一する
st.markdown("""
    <style>
    .menu-box {
        text-align: center;
        padding: 10px;
    }
    .stButton > button {
        width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚣 ボート部専用ポータル")

visible_items = [item for item in MENU_ITEMS if item.get("visible", True)]

if st.user is not None:
    # 3列のレイアウトを動的に作成
    for i in range(0, len(visible_items), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(visible_items):
                item = visible_items[i + j]
                with cols[j]:
                    # 画像とボタンを囲む箱（中央寄せ用）
                    st.markdown('<div class="menu-box">', unsafe_allow_html=True)
                    
                    # 画像の表示（横幅を調整）
                    icon_path = item.get("icon", "")
                    if icon_path:
                        try:
                            # widthを指定して大きすぎないサイズに調整
                            st.image(icon_path, width=80)
                        except:
                            st.write("🖼️")
                    
                    # ボタン/リンクの表示
                    url = get_url(item)
                    if item["type"] == "page":
                        if st.button(item["label"], key=f"btn_{i+j}"):
                            st.switch_page(item["url"])
                    elif item["type"] == "dev":
                        if st.button(item["label"], key=f"btn_{i+j}"):
                            st.toast("現在開発中です")
                    else:
                        st.link_button(item["label"], url)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("ログインしてください。")
