# config.py
import streamlit as st

SECRET_TOKEN = st.secrets["GAS_TOKEN"]

MENU_ITEMS = [
    {"label": "トレーニング\nメニュー", "key": "URL_TRAINING", "type": "gas", "icon": "assets/training.png", "visible": True},
    {"label": "乗艇練習\nホワイトボード", "key": "URL_WHITEBOARD", "type": "gas", "icon": "assets/whiteboard.png", "visible": True},
    {"label": "予定表", "url": "pages/schedule.py", "type": "page", "icon": "assets/schedule.png", "visible": True},
    {"label": "欠席連絡\nフォーム", "key": "URL_FORM", "type": "link", "icon": "images/googleforms.jpg", "visible": True},
    {"label": "Average\n計算ツール", "url": "pages/calculator.py", "type": "page", "icon": "assets/calculator.png", "visible": True},
    {"label": "エルゴ測定記録\nデータベース", "key": "URL_ErgDB", "type": "gas", "icon": "assets/db.png", "visible": True},
    {"label": "リギング\nサポート", "key": "URL_RIGGING", "type": "gas", "icon": "assets/rigging.png", "visible": True},
    {"label": "備品管理\nツール", "key": "URL_TOOL", "type": "gas", "icon": "assets/inventory.png", "visible": True},
    {"label": "Google\nドライブ", "key": "URL_DRIVE", "type": "link", "icon": "images/googledrive.jpg", "visible": True},
    {"label": "動画解析\nツール", "url": "dev", "type": "dev", "icon": "assets/video.png", "visible": False},
]
