import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

st.title("🛶 エルゴ・レースプランシミュレーター")
st.write("カテゴリを選んで目標数値を入力し、レースプランを作成します。")
st.markdown("---")

# --- 初期化 ---
if "active_plan_flag" not in st.session_state:
    st.session_state["active_plan_flag"] = False

def clear_plan_states():
    for i in range(1, 5):
        st.session_state[f"q{i}_offset_sec"] = 0.0
    st.session_state["active_plan_flag"] = False

# --- カテゴリー選択 ---
menus = [
    "距離 と 目標タイム から【全体のAverage】を出す", 
    "距離 と Average から【目標タイム】を出す",
    "合計時間 と 距離 から【全体のAverage】を出す",
    "合計時間 と Average から【目標距離】を出す"
]
default_index = st.session_state.get("fixed_mode_idx", 0) if st.session_state["active_plan_flag"] else 0

selected_menu = st.selectbox("① 計算したいカテゴリーを選択してください", menus, index=default_index, on_change=clear_plan_states)
mode_idx = menus.index(selected_menu)

calc_dist, calc_secs, calc_ave = 0.0, 0.0, 0.0
main_col1, main_col2 = st.columns([1, 1])

# --- 入力処理：距離のm単位をラベルとして統合して高さを一致させる ---
if mode_idx == 0:
    with main_col1:
        st.write("② 距離")
        calc_dist = float(st.number_input("距離(m)", value=2000, step=500, key="m0_d"))
    with main_col2:
        st.write("③ 目標タイム")
        t_cols = st.columns(2)
        v_m = t_cols[0].number_input("分", min_value=0, value=8, step=1, key="m0_m")
        v_s = t_cols[1].number_input("秒", min_value=0, max_value=59, value=0, step=1, key="m0_s")
        calc_secs = float((v_m * 60) + v_s)
    if calc_dist > 0: calc_ave = calc_secs / (calc_dist / 500)
    st.info(f"④ 必要なAverage: **{int(calc_ave // 60)}分{calc_ave % 60:04.1f}秒** / 500m")

elif mode_idx == 1:
    with main_col1:
        st.write("② 距離")
        calc_dist = float(st.number_input("距離(m)", value=2000, step=500, key="m1_d"))
    with main_col2:
        st.write("③ 全体のAverage")
        a_cols = st.columns(2)
        v_am = a_cols[0].number_input("分", min_value=0, value=2, step=1, key="m1_am")
        v_as = a_cols[1].number_input("秒", min_value=0, max_value=59, value=0, step=1, key="m1_as")
        calc_ave = float((v_am * 60) + v_as)
    if calc_dist > 0: calc_secs = calc_ave * (calc_dist / 500)
    st.info(f"④ 合計タイム: **{int(calc_secs // 60)}分{calc_secs % 60:04.1f}秒**")

elif mode_idx == 2:
    with main_col1:
        st.write("② 合計時間")
        t_cols = st.columns(2)
        v_tm = t_cols[0].number_input("分", min_value=0, value=20, step=1, key="m2_tm")
        v_ts = t_cols[1].number_input("秒", min_value=0, max_value=59, value=0, step=1, key="m2_ts")
        calc_secs = float((v_tm * 60) + v_ts)
    with main_col2:
        st.write("③ 距離")
        calc_dist = float(st.number_input("距離(m)", value=5000, step=500, key="m2_d"))
    if calc_dist > 0: calc_ave = calc_secs / (calc_dist / 500)
    st.info(f"④ 計算Average: **{int(calc_ave // 60)}分{calc_ave % 60:04.1f}秒** / 500m")

elif mode_idx == 3:
    with main_col1:
        st.write("② 測定時間")
        t_cols = st.columns(2)
        v_tm = t_cols[0].number_input("分", min_value=0, value=20, step=1, key="m3_tm")
        v_ts = t_cols[1].number_input("秒", min_value=0, max_value=59, value=0, step=1, key="m3_ts")
        calc_secs = float((v_tm * 60) + v_ts)
    with main_col2:
        st.write("③ 目標Average")
        a_cols = st.columns(2)
        v_am = a_cols[0].number_input("分", min_value=0, value=1, step=1, key="m3_am")
        v_as = a_cols[1].number_input("秒", min_value=0, max_value=59, value=50, step=1, key="m3_as")
        calc_ave = float((v_am * 60) + v_as)
    if calc_ave > 0: calc_dist = (calc_secs / calc_ave) * 500
    st.info(f"④ 想定目標距離: **{calc_dist:.1f} m**")

# --- レースプラン作成ボタン・ロジック ---
if st.button("⑤ レースプランを作成", type="primary"):
    st.session_state.update({"active_plan_flag": True, "fixed_ave_seconds": calc_ave, "fixed_distance_m": calc_dist, "fixed_total_seconds": calc_secs, "fixed_calc_mode": "time_base" if mode_idx >= 2 else "distance_base", "fixed_mode_idx": mode_idx})
    st.rerun()

if st.session_state["active_plan_flag"]:
    # ... (プラン調整エリアのロジックは変更なしでOK)
    st.write("プラン調整エリアを表示中...")
