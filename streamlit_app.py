import streamlit as st
from config import MENU_ITEMS
from utils import get_url

st.set_page_config(layout="centered")

st.title("🚣 ボート部専用ポータル")

visible_items = [item for item in MENU_ITEMS if item.get("visible", True)]

if st.user is not None:
    # 自分のGitHubリポジトリのURLを特定するためのハック（画像絶対URL用）
    # 画像が表示されない問題を避けるため、生URLを生成します
    # ※もし動かない場合は、ご自身の「ユーザー名/リポジトリ名」に置き換えてください
    repo_base = "https://raw.githubusercontent.com/cs-rowing/cs-rowing_potal/main/"

    # 全てを強制的に3列の表にするHTMLの構築
    html_code = '<table style="width:100%; border-collapse: separate; border-spacing: 10px; table-layout: fixed;">'
    
    for i in range(0, len(visible_items), 3):
        html_code += '<tr>'
        for j in range(3):
            if i + j < len(visible_items):
                item = visible_items[i + j]
                url = get_url(item)
                label_display = item["label"].replace('\n', '<br>')
                
                # 画像のフルURLを合成
                img_url = repo_base + item["icon"]
                
                # 1つのマス（ボタン風のデザイン）を作成
                html_code += f'''
                <td style="text-align: center; vertical-align: top; width: 33.3%; background-color: #f0f2f6; padding: 12px 5px; border-radius: 8px;">
                    <a href="{url}" target="_blank" style="text-decoration: none; color: #31333F; display: block; width: 100%; height: 100%;">
                        <img src="{img_url}" style="width: 50px; height: 50px; object-fit: contain; margin-bottom: 8px;" onerror="this.src='https://img.icons8.com/ios/50/image.png'">
                        <div style="font-size: 11px; font-weight: 500; line-height: 1.3; word-wrap: break-word;">{label_display}</div>
                    </a>
                </td>
                '''
            else:
                # 3枚に満たない場合の空マス
                html_code += '<td style="width: 33.3%;"></td>'
        html_code += '</tr>'
    
    html_code += '</table>'
    
    # StreamlitにHTMLを直接レンダリングさせる（これでスマホでも絶対に縦並びになりません）
    st.markdown(html_code, unsafe_allow_html=True)

else:
    st.warning("ログインしてください。")
