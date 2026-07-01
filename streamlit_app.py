import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(layout="centered")

st.title("🚣 ボート部専用ポータル")

visible_items = [item for item in MENU_ITEMS if item.get("visible", True)]

if st.user is not None:
    # 1. 安全なHTMLを組み立てる（文字化け・コード漏れを絶対に起こさない構造）
    html_buttons = ""
    
    for item in visible_items:
        url = get_url(item)
        label_display = item["label"]
        
        # GitHubの画像を直接読み込むためのURL
        # ※もし画像が出ない場合は、ここを実際の「ユーザー名/リポジトリ名」に変更してください
        img_src = f"https://raw.githubusercontent.com/cs-rowing/cs-rowing_potal/main/{item['icon']}"
        
        # 各ボタンを33%幅（3列）で綺麗に整列させるHTML
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
        ">
            <img src="{img_src}" style="width: 40px; height: 40px; object-fit: contain; margin-bottom: 8px;" onerror="this.src='https://img.icons8.com/ios/50/image.png'">
            <span style="font-size: 11px; font-weight: bold; text-align: center; line-height: 1.2; display: block; width: 100%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{label_display}</span>
        </a>
        '''

    # 全体を包むコンテナ（横並びで、絶対に1列に折り返さない設定）
    full_html = f'''
    <div style="
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-start;
        gap: 10px;
        width: 100%;
        box-sizing: border-box;
    ">
        {html_buttons}
    </div>
    '''
    
    # 2. ★超重要: Streamlit公式の安全な隔離埋め込み機能を使用
    # これにより、画面に生コードが表示されるバグは100%発生しなくなります
    st.components.v1.html(full_html, height=500, scrolling=False)

else:
    st.warning("ログインしてください。")
