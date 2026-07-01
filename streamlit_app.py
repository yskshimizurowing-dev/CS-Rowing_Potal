import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(layout="centered")

st.title("🚣 ボート部専用ポータル")

visible_items = [item for item in MENU_ITEMS if item.get("visible", True)]

if st.user is not None:
    # 3個ずつ安全に分割してループ
    for i in range(0, len(visible_items), 3):
        # コンポーネントの干渉を防ぐため、1行（3つ）ごとに「絶対に折り返さない」コンテナを作る
        cols = st.columns(3)
        
        for j in range(3):
            if i + j < len(visible_items):
                item = visible_items[i + j]
                with cols[j]:
                    # htmlのインラインCSSを使って、この枠の中だけ強制的に中央揃えにする
                    st.markdown('<div style="text-align: center; width: 100%;">', unsafe_allow_html=True)
                    
                    # 1. 画像の表示（安全なimagesフォルダから直接読み込み）
                    icon_path = item.get("icon", "")
                    if icon_path:
                        try:
                            st.image(icon_path, width=65)
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
                    
                    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("ログインしてください。")
