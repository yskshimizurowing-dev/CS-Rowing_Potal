import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

st.title("🛶 エルゴ・レースプランシミュレーター")
st.write("カテゴリを選んで目標数値を入力し、レースプランを作成・シミュレーションします。")
st.markdown("---")

# --- ① カテゴリーの選択 ---
menus = [
    "距離 と 目標タイム から【全体のAverage】を出す", 
    "距離 と Average から【目標タイム】を出す",
    "合計時間 と 距離 から【全体のAverage】を出す",
    "合計時間 と Average から【目標距離】を出す（例：20分測定など）"
]

if "active_plan_flag" not in st.session_state:
    st.session_state["active_plan_flag"] = False

def clear_plan_states():
    for i in range(1, 5):
        st.session_state[f"q{i}_offset_sec"] = 0.0
    st.session_state["active_plan_flag"] = False

default_index = 0
if st.session_state["active_plan_flag"]:
    default_index = st.session_state.get("fixed_mode_idx", 0)

selected_menu = st.selectbox(
    "① 計算したいカテゴリーを選択してください",
    menus,
    index=default_index,
    on_change=clear_plan_states
)
mode_idx = menus.index(selected_menu)

calc_dist = 0.0
calc_secs = 0.0
calc_ave = 0.0

# 画面全体をシンプルに3列に分割（すべてのメニューで横並びを保証する安全な枠組み）
main_col1, main_col2, main_col3 = st.columns(3)

# --- メニュー0：距離 と 目標タイム から【全体のAverage】を出す ---
if mode_idx == 0:
    current_type = "distance_base"
    with main_col1:
        v_dist = st.number_input("② 距離 (m)", min_value=0, value=2000, step=500, key="m0_d_f")
        calc_dist = float(v_dist)
    with main_col2:
        v_m = st.number_input("③ 目標タイム（分）", min_value=0, max_value=60, value=8, step=1, key="m0_m_f")
    with main_col3:
        v_s = st.number_input("③ 目標タイム（秒）", min_value=0, max_value=59, value=0, step=1, key="m0_s_f")
        calc_secs = float((v_m * 60) + v_s)
        
    if calc_dist > 0:
        calc_ave = calc_secs / (calc_dist / 500)
    
    st.write("") 
    st.info(f"④ 必要な全体のAverage: **{int(calc_ave // 60)}分{calc_ave % 60:04.1f}秒** / 500m")

# --- メニュー1：距離 と Average から【目標タイム】を出す ---
elif mode_idx == 1:
    current_type = "distance_base"
    with main_col1:
        v_dist = st.number_input("② 距離 (m)", min_value=0, value=2000, step=500, key="m1_d_f")
        calc_dist = float(v_dist)
    with main_col2:
        v_am = st.number_input("③ 全体のAverage（分）", min_value=0, max_value=10, value=2, step=1, key="m1_am_f")
    with main_col3:
        v_as = st.number_input("③ 全体のAverage（秒）", min_value=0, max_value=59, value=0, step=1, key="m1_as_f")
        calc_ave = float((v_am * 60) + v_as)
        
    if calc_dist > 0:
        calc_secs = calc_ave * (calc_dist / 500)
        
    st.write("") 
    st.info(f"④ 算出された合計タイム: **{int(calc_secs // 60)}分{calc_secs % 60:04.1f}秒**")

# --- メニュー2：合計時間 と 距離 から【全体のAverage】を出す ---
elif mode_idx == 2:
    current_type = "time_base"
    with main_col1:
        v_tm = st.number_input("② 合計時間（分）", min_value=0, max_value=120, value=20, step=1, key="m2_tm_f")
    with main_col2:
        v_ts = st.number_input("② 合計時間（秒）", min_value=0, max_value=59, value=0, step=1, key="m2_ts_f")
        calc_secs = float((v_tm * 60) + v_ts)
    with main_col3:
        v_dist = st.number_input("③ 目標距離 (m)", min_value=0, value=5000, step=500, key="m2_d_f")
        calc_dist = float(v_dist)
        
    if calc_dist > 0:
        calc_ave = calc_secs / (calc_dist / 500)
        
    st.write("") 
    st.info(f"④ 計算されたAverage: **{int(calc_ave // 60)}分{calc_ave % 60:04.1f}秒** / 500m")

# --- メニュー3：合計時間 と Average から【目標距離】を出す ---
elif mode_idx == 3:
    current_type = "time_base"
    with main_col1:
        v_tm = st.number_input("② 測定時間（分）", min_value=0, max_value=120, value=20, step=1, key="m3_tm_f")
    with main_col2:
        v_ts = st.number_input("② 測定時間（秒）", min_value=0, max_value=59, value=0, step=1, key="m3_ts_f")
        calc_secs = float((v_tm * 60) + v_ts)
    with main_col3:
        v_am = st.number_input("③ 目標Average（分）", min_value=0, max_value=10, value=1, step=1, key="m3_am_f")
        v_as = st.number_input("③ 目標Average（秒）", min_value=0, max_value=59, value=50, step=1, key="m3_as_f")
        calc_ave = float((v_am * 60)
