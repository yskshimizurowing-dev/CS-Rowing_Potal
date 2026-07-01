import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(layout="centered")

# CSS: 画像を中央に寄せ、ボタンの幅をカラムいっぱいに広げる
st.markdown("""
    <style>
    .stImage {
        display: flex;
        justify-content: center;
        margin-bottom: 5px;
    }
    div.stButton > button {
        width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚣 ボート部専用ポータル")

visible_items = [item for item in MENU_ITEMS if item.get("visible", True)]

if st.user is not None:
    # 3個ずつアイテムを取り出して行（Row）を作る
    for i in range(0, len(visible_items), 3):
        # ★重要: gap="small" で余白を詰め、内部のスマホ縦積み挙動を抑制する公式アプローチ
        cols = st.columns(3, gap="small")
        
        for j in range(3):
            if i + j < len(visible_items):
                item = visible_items[i + j]
                with cols[j]:
                    # 1. 画像表示（Streamlit標準機能に戻すことで100%表示されます）
                    icon_path = item.get("icon", "")
                    if icon_path:
                        try:
                            # 画像が大きすぎないようにサイズを固定（80ピクセル）
                            st.image(icon_path, width=80)
                        except:
                            st.write("🖼️")
                    
                    # 2. ボタン/リンク表示（ボタン幅は自動でカラムにフィットします）
                    url = get_url(item)
                    if item["type"] == "page":
                        if st.button(item["label"], key=f"btn_{i+j}"):
                            st.switch_page(item["url"])
                    elif item["type"] == "dev":
                        if st.button(item["label"], key=f"btn_{i+j}"):
                            st.toast("現在開発中です")
                    else:
                        st.link_button(item["label"], url)
else:
    st.warning("ログインしてください。")
