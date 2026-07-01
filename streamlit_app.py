import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(layout="centered")

st.title("🚣 ボート部専用ポータル")

visible_items = [item for item in MENU_ITEMS if item.get("visible", True)]

if st.user is not None:
    # 1. 画面にコードが漏れるのを防ぐため、HTMLを安全に構築するためのリスト
    html_elements = []
    
    # 全体を包む、スマホでも絶対に折り返さない3列のコンテナ
    html_elements.append('<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px; width: 100%;">')
    
    for item in visible_items:
        url = get_url(item)
        label_display = item["label"]
        
        # Streamlitのローカル画像をHTMLから直接読み込むための正しいパスに変換
        # (Streamlit Cloud上で 'images/xxx.png' を直接参照するための指定)
        img_src = f"./app/{item['icon']}"
        
        # 各ボタンのHTML（幅を31%に固定することで、スマホでも絶対に3列を維持します）
        item_html = f'''
        <a href="{url}" target="_self" style="display: flex; flex-direction: column; align-items: center; justify-content: center; width: 31%; background-color: #f0f2f6; padding: 10px 4px; border-radius: 8px; text-decoration: none; color: #31333F; box-sizing: border-box; margin-bottom: 8px;">
            <img src="{img_src}" style="width: 45px; height: 45px; object-fit: contain; margin-bottom: 6px;" onerror="this.style.display='none';">
            <span style="font-size: 10px; font-weight: 500; text-align: center; line-height: 1.2; display: block; width: 100%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{label_display}</span>
        </a>
        '''
        html_elements.append(item_html)
        
    html_elements.append('</div>')
    
    # 2. まとめて一回だけ出力（これで文字化けやコード漏れを完全に防ぎます）
    st.markdown("".join(html_elements), unsafe_allow_html=True)

else:
    st.warning("ログインしてください。")
