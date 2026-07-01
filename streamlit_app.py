import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(page_title="ボート部専用ポータル", layout="centered", initial_sidebar_state="collapsed")

# スタイル設定
st.markdown('''
<style>
    header[data-testid="stHeader"] { display: none !important; }
    .menu-container { text-align: center; margin-bottom: 10px; }
</style>
''', unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>🚣 ボート部専用ポータル</h2>", unsafe_allow_html=True)
st.write("---")

visible_items = [item for item in MENU_ITEMS if item.get("visible", True)]

if st.user is not None:
    for i in range(0, len(visible_items), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(visible_items):
                item = visible_items[i + j]
                with col:
                    url = get_url(item)
                    # HTMLタグをインデントなしで記述
                    st.markdown(f'<a href="{url}" target="_blank">', unsafe_allow_html=True)
                    st.image(item["icon"], use_container_width=True)
                    st.markdown('</a>', unsafe_allow_html=True)
                    
                    if item["type"] == "page":
                        if st.button(item["label"], use_container_width=True, key=f"btn_{i+j}"): 
                            st.switch_page(item["url"])
                    elif item["type"] == "dev":
                        if st.button(item["label"], use_container_width=True, key=f"btn_{i+j}"): 
                            st.toast("現在開発中です！")
                    else:
                        st.link_button(item["label"], url, use_container_width=True)
else:
    st.warning("ポータルを利用するにはログインが必要です。")
