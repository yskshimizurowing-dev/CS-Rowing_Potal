import streamlit as st
from config import MENU_ITEMS
from utils import get_url
import base64
import os

st.set_page_config(layout="centered")

st.title("中杉ボート部<br>専用ポータル")

visible_items = [item for item in MENU_ITEMS if item.get("visible", True)]

if st.user is not None:
    html_buttons = ""
    
    for item in visible_items:
        url = get_url(item)
        label_display = item["label"]
        icon_path = item.get("icon", "")
        
        # 画像ファイルをBase64（テキストデータ）に変換してHTMLに直接埋め込む（これで100%表示されます）
        img_tag = ""
        if icon_path and os.path.exists(icon_path):
            try:
                with open(icon_path, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode()
                img_tag = f'<img src="data:image/png;base64,{encoded}" style="width: 40px; height: 40px; object-fit: contain; margin-bottom: 8px;">'
            except:
                img_tag = '<div style="font-size:24px; margin-bottom:8px;">🖼️</div>'
        else:
            img_tag = '<div style="font-size:24px; margin-bottom:8px;">🖼️</div>'
        
        # ボタンのHTML（横幅を30%に固定してきれいな3列を維持）
        html_buttons += f'''
        <a href="{url}" target="_blank" style="
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 30%;
            background-color: #f0f2f6;
            padding: 12px 4px;
            border-radius: 8px;
            text-decoration: none;
            color: #31333F;
            box-sizing: border-box;
            font-family: sans-serif;
            margin-bottom: 10px;
        ">
            {img_tag}
            <span style="font-size: 11px; font-weight: bold; text-align: center; line-height: 1.2; display: block; width: 100%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{label_display}</span>
        </a>
        '''

    # 全体を包むコンテナ（スマホの横幅に綺麗に収まり、絶対に間延びも折り返しもしない）
    full_html = f'''
    <div style="
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-start;
        gap: 12px;
        width: 100%;
        box-sizing: border-box;
    ">
        {html_buttons}
    </div>
    '''
    
    # 隔離された安全なWEB枠として出力（コード漏れは絶対に起きません）
    st.components.v1.html(full_html, height=450, scrolling=False)

else:
    st.warning("ログインしてください。")
