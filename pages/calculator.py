import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

st.title("🛶 エルゴ・レースプランシミュレーター")
st.write("カテゴリを選んで目標数値を入力し、レースプランを作成・シミュレーションします。")
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
    "合計時間 と Average から【目標距離】を出す（例：20分測定など）"
]
default_index = st.session_state.get("fixed_mode_idx", 0) if st.session_state["active_plan_flag"] else 0

selected_menu = st.selectbox("① 計算したいカテゴリーを選択してください", menus, index=default_index, on_change=clear_plan_states)
mode_idx = menus.index(selected_menu)

calc_dist, calc_secs, calc_ave = 0.0, 0.0, 0.0
main_col1, main_col2 = st.columns([1, 1])

# --- メニュー入力処理 ---
if mode_idx == 0:
    with main_col1:
        st.write("② 距離")
        d_cols = st.columns([4, 1])
        v_dist = d_cols[0].number_input("距離", min_value=0, value=2000, step=500, key="m0_d", label_visibility="collapsed")
        d_cols[1].write("m")
        calc_dist = float(v_dist)
    with main_col2:
        st.write("③ 目標タイム")
        t_cols = st.columns(2)
        v_m = t_cols[0].number_input("分", min_value=0, max_value=60, value=8, step=1, key="m0_m")
        v_s = t_cols[1].number_input("秒", min_value=0, max_value=59, value=0, step=1, key="m0_s")
        calc_secs = float((v_m * 60) + v_s)
    if calc_dist > 0: calc_ave = calc_secs / (calc_dist / 500)
    st.info(f"④ 必要なAverage: **{int(calc_ave // 60)}分{calc_ave % 60:04.1f}秒** / 500m")

elif mode_idx == 1:
    with main_col1:
        st.write("② 距離")
        d_cols = st.columns([4, 1])
        v_dist = d_cols[0].number_input("距離", min_value=0, value=2000, step=500, key="m1_d", label_visibility="collapsed")
        d_cols[1].write("m")
        calc_dist = float(v_dist)
    with main_col2:
        st.write("③ 全体のAverage")
        a_cols = st.columns(2)
        v_am = a_cols[0].number_input("分", min_value=0, max_value=10, value=2, step=1, key="m1_am")
        v_as = a_cols[1].number_input("秒", min_value=0, max_value=59, value=0, step=1, key="m1_as")
        calc_ave = float((v_am * 60) + v_as)
    if calc_dist > 0: calc_secs = calc_ave * (calc_dist / 500)
    st.info(f"④ 算出された合計タイム: **{int(calc_secs // 60)}分{calc_secs % 60:04.1f}秒**")

elif mode_idx == 2:
    with main_col1:
        st.write("② 合計時間")
        t_cols = st.columns(2)
        v_tm = t_cols[0].number_input("分", min_value=0, max_value=120, value=20, step=1, key="m2_tm")
        v_ts = t_cols[1].number_input("秒", min_value=0, max_value=59, value=0, step=1, key="m2_ts")
        calc_secs = float((v_tm * 60) + v_ts)
    with main_col2:
        st.write("③ 距離")
        d_cols = st.columns([4, 1])
        v_dist = d_cols[0].number_input("距離", min_value=0, value=5000, step=500, key="m2_d", label_visibility="collapsed")
        d_cols[1].write("m")
        calc_dist = float(v_dist)
    if calc_dist > 0: calc_ave = calc_secs / (calc_dist / 500)
    st.info(f"④ 計算されたAverage: **{int(calc_ave // 60)}分{calc_ave % 60:04.1f}秒** / 500m")

elif mode_idx == 3:
    with main_col1:
        st.write("② 測定時間")
        t_cols = st.columns(2)
        v_tm = t_cols[0].number_input("分", min_value=0, max_value=120, value=20, step=1, key="m3_tm")
        v_ts = t_cols[1].number_input("秒", min_value=0, max_value=59, value=0, step=1, key="m3_ts")
        calc_secs = float((v_tm * 60) + v_ts)
    with main_col2:
        st.write("③ 目標Average")
        a_cols = st.columns(2)
        v_am = a_cols[0].number_input("分", min_value=0, max_value=10, value=1, step=1, key="m3_am")
        v_as = a_cols[1].number_input("秒", min_value=0, max_value=59, value=50, step=1, key="m3_as")
        calc_ave = float((v_am * 60) + v_as)
    if calc_ave > 0: calc_dist = (calc_secs / calc_ave) * 500
    st.info(f"④ 想定される合計目標距離: **{calc_dist:.1f} m**")

# --- プラン作成ボタン ---
if st.button("⑤ レースプランを作成", type="primary"):
    st.session_state.update({"active_plan_flag": True, "fixed_ave_seconds": calc_ave, "fixed_distance_m": calc_dist, "fixed_total_seconds": calc_secs, "fixed_calc_mode": "time_base" if mode_idx >= 2 else "distance_base", "fixed_mode_idx": mode_idx})
    st.rerun()

# --- レースプラン作成エリア ---
if st.session_state["active_plan_flag"]:
    base_ave, dist_total, secs_total, calc_mode = st.session_state["fixed_ave_seconds"], st.session_state["fixed_distance_m"], st.session_state["fixed_total_seconds"], st.session_state["fixed_calc_mode"]
    st.subheader("⏱️ 各Qの調整")
    if st.button("リセット"):
        for i in range(1, 5): st.session_state[f"q{i}_offset_sec"] = 0.0
        st.rerun()

    p_total_secs, p_total_dist = 0.0, 0.0
    for i in range(1, 5):
        c_q, c_ave, c_btn, c_val = st.columns([1, 2, 2, 3])
        q_sec = base_ave + st.session_state.get(f"q{i}_offset_sec", 0.0)
        q_m, q_s = int(q_sec // 60), q_sec % 60
        
        with c_q: st.write(f"**{i}Q**")
        with c_ave: st.write(f"**{q_m:02d}:{q_s:04.1f}**")
        with c_btn:
            b1, b2 = st.columns(2)
            if b1.button("➕", key=f"p_{i}"): st.session_state[f"q{i}_offset_sec"] = st.session_state.get(f"q{i}_offset_sec", 0.0) + 0.5; st.rerun()
            if b2.button("➖", key=f"m_{i}"): st.session_state[f"q{i}_offset_sec"] = st.session_state.get(f"q{i}_offset_sec", 0.0) - 0.5; st.rerun()
        with c_val: st.write(f"`{(dist_total/4)*q_sec/500 if calc_mode == 'distance_base' else (secs_total/4/q_sec)*500:.1f} {'m' if calc_mode != 'distance_base' else '秒'}`")
