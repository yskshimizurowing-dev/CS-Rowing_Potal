import streamlit as st
import pandas as pd
import requests
import datetime

# --- 【設定】スプレッドシートIDをここに入れる ---
SHEET_ID = "1Gy3_HwI4ESQpMXrdF6XJI5G-94dQM2sEUd4zYgDkVgY"
MAIN_URL = f"https://docs.google.com/spreadsheets/d/1Gy3_HwI4ESQpMXrdF6XJI5G-94dQM2sEUd4zYgDkVgY//export?format=csv&gid=0"
MEMBER_URL = f"https://docs.google.com/spreadsheets/d/1Gy3_HwI4ESQpMXrdF6XJI5G-94dQM2sEUd4zYgDkVgY/edit?gid=1884915706#gid=1884915706" # 部員名簿のGID

# --- データ取得 ---
@st.cache_data(ttl=60)
def fetch_all_data():
    df_main = pd.read_csv(MAIN_URL, header=None)
    df_member = pd.read_csv(MEMBER_URL)
    
    # 部員名簿の辞書化
    member_map = {}
    for _, row in df_member.iterrows():
        name = str(row.iloc[0]).strip()
        ki = str(row.iloc[1]).strip()
        gender = str(row.iloc[2]).strip()
        member_map[name] = {"ki": ki, "gender": gender}
        
    return df_main, member_map

# --- 天気予報関数（そのまま再利用） ---
def fetch_weather(location):
    lat, lng = (35.805, 139.678) if location == "戸田" else (35.614, 139.190)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&hourly=temperature_2m,precipitation,weather_code,wind_speed_10m,wind_direction_10m&timezone=Asia%2FTokyo"
    try:
        res = requests.get(url).json()
        return res # 天気処理に必要なデータを返す
    except:
        return None

# --- メイン処理 ---
df_main, member_map = fetch_all_data()

# データの抽出
sheet_date = str(df_main.iloc[0, 1])
am_menu = df_main.iloc[2, 1]
pm_menu = df_main.iloc[3, 1]
crew_rows = df_main.iloc[5:].values.tolist()

# 表示処理（元のHTMLデザインをそのまま反映）
st.markdown("""<style>...ここに元のCSSを貼り付ける...</style>""", unsafe_allow_html=True)
st.markdown(f"<h1>🚣‍♂️ {sheet_date}</h1>", unsafe_allow_html=True)
st.write(f"【AM】{am_menu}")
st.write(f"【PM】{pm_menu}")

# クルー編成ループ処理
for row in crew_rows:
    if len(row) > 2 and pd.notna(row[2]):
        st.write(f"**{row[2]}**: {', '.join([str(x) for x in row[3:8] if pd.notna(x)])}")
