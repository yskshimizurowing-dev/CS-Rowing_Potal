import streamlit as st
from streamlit_gsheets import GSheetsConnection

# 接続設定
conn = st.connection("gsheets", type=GSheetsConnection)
import pandas as pd
import requests
import datetime

# ページの設定（スマホ向けにタイトなレイアウト、タイトル設定）
st.set_page_config(page_title="ボート部 クルー＆メニュー", layout="centered")

# --- スプレッドシートからのデータ取得処理 ---
import streamlit as st
#from streamlit_gsheets import GSheetsConnection

@st.cache_data(ttl=10) # 10秒間キャッシュ
def fetch_boat_data():
    
    conn = st.connection("gsheets", type="gsheets")
    df = conn.read()
    
    # 1. 【修正】「クルー編成」シートの読み込みに変更
    df_main = conn.read(worksheet="クルー編成", header=None)
    
    sheet_date = str(df_main.iloc[0, 1]).strip() if pd.notna(df_main.iloc[0, 1]) else "本日のクルー＆メニュー" # B1
    location = str(df_main.iloc[1, 1]).strip() if pd.notna(df_main.iloc[1, 1]) else "戸田" # B2
    am_menu = df_main.iloc[2, 1] if pd.notna(df_main.iloc[2, 1]) else "未入力" # B3
    pm_menu = df_main.iloc[3, 1] if pd.notna(df_main.iloc[3, 1]) else "未入力" # B4
    
    # 6行目（インデックス5）以降のクルーデータを抽出
    crew_rows = df_main.iloc[5:].values.tolist()
    
    # 2. 「部員名簿」シートの読み込み
    member_map = {}
    try:
        df_member = conn.read(worksheet="部員名簿")
        for _, row in df_member.iterrows():
            name = str(row.iloc[0]).strip()
            ki = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
            gender = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else "男子"
            if name:
                member_map[name] = {"ki": ki, "gender": gender}
    except Exception as e:
        pass 
        
    return am_menu, pm_menu, location, sheet_date, crew_rows, member_map

# --- 天気情報取得処理 ---
def fetch_weather(location):
    lat, lng = 35.805, 139.678 # デフォルト：戸田
    if location == "相模湖":
        lat, lng = 35.614, 139.190
        
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    
    day_label = "今日"
    target_date = now
    if now.hour >= 18:
        target_date = now + datetime.timedelta(days=1)
        day_label = "明日"
        
    target_date_str = target_date.strftime("%Y-%m-%d")
    date_label = target_date.strftime("%m/%d")
    
    weather_data = []
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&hourly=temperature_2m,precipitation,weather_code,wind_speed_10m,wind_direction_10m&timezone=Asia%2FTokyo"
        res = requests.get(url).json()
        
        target_hours = [9, 11, 13, 15, 17]
        for hour in target_hours:
            hour_str = f"{hour:02d}:00"
            target_time_str = f"{target_date_str}T{hour_str}"
            
            if target_time_str in res["hourly"]["time"]:
                idx = res["hourly"]["time"].index(target_time_str)
                weather_data.append({
                    "time": hour_str,
                    "temp": round(res["hourly"]["temperature_2m"][idx]),
                    "rain": f"{res['hourly']['precipitation'][idx]:.1f}",
                    "wind_speed": round(res["hourly"]["wind_speed_10m"][idx] / 3.6),
                    "wind_dir": get_wind_direction(res["hourly"]["wind_direction_10m"][idx]),
                    "icon": get_weather_icon(res["hourly"]["weather_code"][idx])
                })
    except Exception as e:
        st.error(f"天気情報の取得に失敗しました: {e}")
        
    return weather_data, day_label, date_label

def get_wind_direction(deg):
    directions = ['北', '北東', '東', '南東', '南', '南西', '西', '北西']
    return directions[round((deg % 360) / 45) % 8]

def get_weather_icon(code):
    if code == 0: return '☀️'
    if 1 <= code <= 3: return '☁️'
    if 51 <= code <= 67: return '☔'
    if 80 <= code <= 82: return '🌦️'
    if 71 <= code <= 77: return '❄️'
    if code >= 95: return '⚡'
    return '☁️'


# --- メイン処理 (画面描画) ---
try:
    am_menu, pm_menu, location, sheet_date, crew_rows, member_map = fetch_boat_data()
    weather_list, day_label, date_label = fetch_weather(location)
    
    now_str = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%m/%d %H:%M")
    
    # 名簿から「期」の一覧（スタッフ等の文字列を除く）を抽出し、古い順（上級生順）に自動ソート
    all_kis = sorted(list(set([info["ki"] for info in member_map.values() if info["ki"] and "期" in info["ki"]])))
    
    st.markdown("""
        <style>
        .header { background-color: #1a365d; color: white; padding: 10px; border-radius: 6px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
        .header h1 { margin: 0; font-size: 16px; color: white; }
        .time { font-size: 11px; opacity: 0.9; color: white; }
        .menu-box { background-color: #fff; border-left: 5px solid #dd6b20; padding: 6px 10px; border-radius: 4px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .menu-title { font-weight: bold; color: #dd6b20; margin-bottom: 2px; font-size: 12px; }
        .menu-item { margin: 1px 0; font-size: 12px; line-height: 1.4; color: #333; }
        .boat-card { background-color: white; border-radius: 6px; padding: 8px; margin-bottom: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); display: flex; align-items: center; }
        .boat-name { width: 80px; font-weight: bold; color: #2d3748; border-right: 2px solid #e2e8f0; padding-right: 4px; margin-right: 6px; flex-shrink: 0; font-size: 13px; }
        .member-list { display: flex; flex-wrap: wrap; gap: 4px; align-items: center; }
        .user-badge { display: inline-block; padding: 3px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; list-style: none;}
        
        /* 期・スタッフに応じた背景色 */
        .ki-senior1 { background-color: #fed7d7; } /* 最上級生（例:62期）: 薄赤 */
        .ki-senior2 { background-color: #fef3c7; } /* 2番目（例:63期）  : 薄黄 */
        .ki-senior3 { background-color: #e0f2fe; } /* 3番目（例:64期）  : 薄水 */
        .ki-staff   { background-color: #d1fae5; } /* スタッフ   : 薄緑 */
        .ki-default { background-color: #f3f4f6; } /* その他           : 薄グレー */
        
        /* 性別に応じた文字色 */
        .gender-male { color: #1e3a8a !important; }   /* 男子: 濃紺 */
        .gender-female { color: #7f1d1d !important; } /* 女子: 濃赤 */
        
        .weather-box { background-color: white; padding: 8px; border-radius: 6px; margin-top: 20px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .weather-title { font-weight: bold; color: #2b6cb0; margin-bottom: 4px; font-size: 12px; }
        .weather-table { width: 100%; border-collapse: collapse; text-align: center; font-size: 12px; }
        .weather-table th { background-color: #ebf8ff; color: #2b6cb0; font-weight: bold; padding: 4px; border: 1px solid #e2e8f0; }
        .weather-table td { padding: 4px; border: 1px solid #e2e8f0; font-weight: 500; color: #333; }
        .w-label { background-color: #f7fafc; color: #4a5568; font-weight: bold !important; }
        </style>
    """, unsafe_allow_html=True)

    # 1. ヘッダー
    st.markdown(f"""
        <div class="header">
          <h1>🚣‍♂️ {sheet_date}</h1>
          <div class="time">更新: {now_str}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. 練習メニュー
    st.markdown(f"""
        <div class="menu-box">
          <div class="menu-title">📢 本日の練習メニュー</div>
          <div class="menu-item"><b>【AM】</b>{am_menu}</div>
          <div class="menu-item"><b>【PM】</b>{pm_menu}</div>
        </div>
    """, unsafe_allow_html=True)

    # 3. クルー編成カード
    for row in crew_rows:
        if len(row) < 3 or pd.isna(row[2]) or str(row[2]).strip() == "":
            continue
        boat_name = str(row[2]).strip()
        
        member_badges_html = ""
        for mem_name in row[3:8]: 
            if pd.isna(mem_name) or str(mem_name).strip() == "":
                continue
            name = str(mem_name).strip()
            
            info = member_map.get(name, {"ki": "", "gender": "男子"})
            ki = info["ki"]
            gender = info["gender"]
            
            badge_class = "ki-default"
            gender_class = "gender-male" if gender == "男子" else "gender-female"
            label = f"{ki} {name}" if ki else name
            
            if ki == "スタッフ":
                badge_class = "ki-staff"
            elif ki in all_kis:
                idx = all_kis.index(ki)
                if idx == 0:
                    badge_class = "ki-senior1"
                elif idx == 1:
                    badge_class = "ki-senior2"
                elif idx == 2:
                    badge_class = "ki-senior3"
                    
            member_badges_html += f'<span class="user-badge {badge_class} {gender_class}">{label}</span>'
            
        if member_badges_html:
            st.markdown(f"""
                <div class="boat-card">
                    <div class="boat-name">{boat_name}</div>
                    <div class="member-list">{member_badges_html}</div>
                </div>
            """, unsafe_allow_html=True)

    # 4. 天気予報テーブル
    if weather_list:
        th_hours = "".join([f"<th>{w['time']}</th>" for w in weather_list])
        td_icons = "".join([f"<td style='font-size:14px;'>{w['icon']}</td>" for w in weather_list])
        td_temps = "".join([f"<td>{w['temp']}℃</td>" for w in weather_list])
        td_dirs  = "".join([f"<td>{w['wind_dir']}</td>" for w in weather_list])
        td_speeds = "".join([f"<td>{w['wind_speed']}m</td>" for w in weather_list])
        td_rains = "".join([f"<td>{w['rain']}mm</td>" for w in weather_list])
        
        st.markdown(f"""
          <div class="weather-box">
            <div class="weather-title">☀️ {day_label}（{date_label}）の{location}天気予報</div>
            <table class="weather-table">
              <tr><th class="w-label">時間</th>{th_hours}</tr>
              <tr><td class="w-label">天気</td>{td_icons}</tr>
              <tr><td class="w-label">気温</td>{td_temps}</tr>
              <tr><td class="w-label">風向</td>{td_dirs}</tr>
              <tr><td class="w-label">風速</td>{td_speeds}</tr>
              <tr><td class="w-label">降水</td>{td_rains}</tr>
            </table>
          </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"データの読み込み中にエラーが発生しました。スプレッドシートの設定を確認してください。: {e}")
