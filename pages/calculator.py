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

# --- 入力処理 ---
if mode_idx == 0:
    with main_col1:
        st.write("② 距離 (m)")
        calc_dist = float(st.number_input("距離", value=2000, step=500, key="m0_d", label_visibility="collapsed"))
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
        st.write("② 距離 (m)")
        calc_dist = float(st.number_input("距離", value=2000, step=500, key="m1_d", label_visibility="collapsed"))
    with main_col2:
        st.write("③ 全体のAverage")
        a_cols = st.columns(2)
        v_am = a_cols[0].number_input("分", min_value=0, value=2, step=1, key="m1_am")
        v_as = a_cols[1].number_input("秒", min_value=0, max_value=59, value=0, step=1, key="m1_as")
        calc_ave = float((v_am * 60) + v_as)
    if calc_dist > 0: calc_secs = calc_ave * (calc_dist / 500)
    st.info(f"④ 算出された合計タイム: **{int(calc_secs // 60)}分{calc_secs % 60:04.1f}秒**")

elif mode_idx == 2:
    with main_col1:
        st.write("② 合計時間")
        t_cols = st.columns(2)
        v_tm = t_cols[0].number_input("分", min_value=0, value=20, step=1, key="m2_tm")
        v_ts = t_cols[1].number_input("秒", min_value=0, max_value=59, value=0, step=1, key="m2_ts")
        calc_secs = float((v_tm * 60) + v_ts)
    with main_col2:
        st.write("③ 距離 (m)")
        calc_dist = float(st.number_input("距離", value=5000, step=500, key="m2_d", label_visibility="collapsed"))
    if calc_dist > 0: calc_ave = calc_secs / (calc_dist / 500)
    st.info(f"④ 計算されたAverage: **{int(calc_ave // 60)}分{calc_ave % 60:04.1f}秒** / 500m")

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
    st.info(f"④ 想定される合計目標距離: **{calc_dist:.1f} m**")

# --- レースプラン作成ボタン ---
st.markdown("---")
if st.button("⑤ レースプランを作成", type="primary"):
    st.session_state.update({
        "active_plan_flag": True, 
        "fixed_ave_seconds": calc_ave, 
        "fixed_distance_m": calc_dist, 
        "fixed_total_seconds": calc_secs, 
        "fixed_calc_mode": "time_base" if mode_idx >= 2 else "distance_base", 
        "fixed_mode_idx": mode_idx
    })
    st.rerun()

# --- レースプラン調整・結果表示 ---
if st.session_state["active_plan_flag"]:
    base_ave = st.session_state["fixed_ave_seconds"]
    dist_total = st.session_state["fixed_distance_m"]
    secs_total = st.session_state["fixed_total_seconds"]
    calc_mode = st.session_state["fixed_calc_mode"]

    st.subheader("⏱️ 各Qの調整")
    if st.button("このプランをリセット"):
        for i in range(1, 5): st.session_state[f"q{i}_offset_sec"] = 0.0
        st.rerun()

    p_total_secs, p_total_dist = 0.0, 0.0
    for i in range(1, 5):
        c1, c2, c3, c4 = st.columns([1, 2, 2, 3])
        c1.write(f"**{i}Q**")
        q_sec = base_ave + st.session_state.get(f"q{i}_offset_sec", 0.0)
        c2.write(f"**{int(q_sec//60):02d}:{q_sec%60:04.1f}**")
        
        btn_c1, btn_c2 = c3.columns(2)
        if btn_c1.button("➕", key=f"p_{i}"): st.session_state[f"q{i}_offset_sec"] = st.session_state.get(f"q{i}_offset_sec", 0.0) + 0.5; st.rerun()
        if btn_c2.button("➖", key=f"m_{i}"): st.session_state[f"q{i}_offset_sec"] = st.session_state.get(f"q{i}_offset_sec", 0.0) - 0.5; st.rerun()
        
        # 集計計算
        if calc_mode == 'distance_base':
            this_dist = dist_total / 4
            this_sec = q_sec * (this_dist / 500)
            p_total_secs += this_sec
            c4.write(f"`{int(this_sec//60):02d}:{this_sec%60:04.1f}`")
        else:
            this_sec = secs_total / 4
            this_dist = (this_sec / q_sec) * 500 if q_sec > 0 else 0
            p_total_dist += this_dist
            c4.write(f"`{this_dist:.1f} m`")

    # --- 過不足の表示 ---
    st.markdown("---")
    if calc_mode == 'distance_base':
        diff = p_total_secs - secs_total
        st.write(f"合計タイム: {int(p_total_secs//60)}分{p_total_secs%60:.1f}秒")
        if abs(diff) < 0.1: st.success("🎉 目標とピッタリです！")
        elif diff > 0: st.error(f"⚠️ 目標より {diff:.1f} 秒遅いです")
        else: st.info(f"💡 目標より {abs(diff):.1f} 秒速いです")
    else:
        diff = p_total_dist - dist_total
        st.write(f"合計距離: {p_total_dist:.1f} m")
        if abs(diff) < 0.5: st.success("🎉 目標とピッタリです！")
        elif diff > 0: st.success(f"🚀 目標より {diff:.1f} m 多いです")
        else: st.error(f"⚠️ 目標より {abs(diff):.1f} m 不足しています")
