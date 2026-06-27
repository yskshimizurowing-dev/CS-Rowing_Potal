import streamlit as st
import pandas as pd
import requests
import datetime

# --- 【設定】スプレッドシートIDをここに入れる ---
SHEET_ID = "あなたのスプレッドシートID"
# クルー編成シートのCSV取得用URL
MAIN_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
# 部員名簿シートのCSV取得用URL (GIDはシートごとに異なります)
MEMBER_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=123456789" 

@st.cache_data(ttl=60)
def fetch_boat_data():
    # 認証なしで直接Pandasで読み込む
    df_main = pd.read_csv(MAIN_URL, header=None)
    df_member = pd.read_csv(MEMBER_URL)
    
    # データの抽出（元のロジックを維持）
    sheet_date = str(df_main.iloc[0, 1])
    location = str(df_main.iloc[1, 1])
    am_menu = df_main.iloc[2, 1]
    pm_menu = df_main.iloc[3, 1]
    crew_rows = df_main.iloc[5:].values.tolist()
    
    member_map = {}
    for _, row in df_member.iterrows():
        name = str(row.iloc[0]).strip()
        ki = str(row.iloc[1]).strip()
        gender = str(row.iloc[2]).strip()
        member_map[name] = {"ki": ki, "gender": gender}
        
    return am_menu, pm_menu, location, sheet_date, crew_rows, member_map

# --- ここから下は、以前のコードの「天気予報」や「画面表示」処理をそのまま貼り付けます ---
# (fetch_weather関数などは元のものをそのまま利用してください)
    st.error(f"データの読み込み中にエラーが発生しました。スプレッドシートの設定を確認してください。: {e}")
