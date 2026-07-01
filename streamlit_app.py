import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(layout="centered")

# CSS: 画像を中央に寄せ、ボタンの隙間を調整する最低限の設定
st.markdown("""
    <style>
    .stImage {
        display: flex;
        justify-content: center;
        margin-bottom: 2px;
    }
    div.stButton > button {
        width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚣 ボート部専用ポータル")

visible_items = [item for item in MENU_ITEMS if item.get("visible", True)]

if st.user is not None:
    # 3個ずつ安全に分割してループ
    for i in range(0, len(visible_items), 3):
        # 重要な修正：大元の st.columns を使いつつ、中のループで絶対に崩さない
        cols = st.columns(3)
        
        for j in range(3):
            if i + j < len(visible_items):
                item = visible_items[i + j]
                with cols[j]:
                    # 1. 画像の表示（安全なimagesフォルダから直接読み込み）
                    icon_path = item.get("icon", "")
                    if icon_path:
                        try:
                            st.image(icon_path, width=70)
                        except:
                            st.write("🖼️")
                    
                    # 2. ボタン/リンクの表示
                    url = get_url(item)
                    if item["type"] == "page":
                        if st.button(item["label"], key=f"btn_{i+j}", use_container_width=True):
                            st.switch_page(item["url"])
                    elif item["type"] == "dev":
                        if st.button(item["label"], key=f"btn_{i+j}", use_container_width=True):
                            st.toast("現在開発中です")
                    else:
                        st.link_button(item["label"], url, use_container_width=True)
else:
    st.warning("ログインしてください。")
