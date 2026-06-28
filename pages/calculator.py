import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

# --- スマホ表示用CSS ---
st.markdown("""
<style>
    @media (max-width: 600px) {
        [data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; }
        .stButton button { width: 100%; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🛶 エルゴ・<br>レースプランシミュレーター", unsafe_allow_html=True)
st.write("カテゴリを選んで目標数値を入力し、<br>レースプランを作成します。", unsafe_allow_html=True)
st.markdown("---")

if "active_plan_flag" not in st.session_state:
    st.session_state["active_plan_flag"] = False

def clear_plan_states():
    for i in range(1, 5):
        st.session_state[f"q{i}_offset_sec"] = 0.0
    st.session_state["active_plan_flag"] = False

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

c1, c2 = st.columns(2)

# --- 入力関数 ---
def distance_input_aligned(col, label_text, key):
    with col:
        st.write(f"② {label_text}")
        st.caption("メートル")
        return float(st.number_input("距離", value=2000, step=500, key=key, label_visibility="collapsed"))

def time_input_aligned(col, label_text, key_m, key_s):
    with col:
        st.write(f"③ {label_text}")
        t_cols = st.columns(2)
        with t_cols[0]:
            st.caption("分")
            m = st.number_input("分", min_value=0, value=8, step=1, key=key_m, label_visibility="collapsed")
        with t_cols[1]:
            st.caption("秒")
            s = st.number_input("秒", min_value=0, max_value=59, value=0, step=1, key=key_s, label_visibility="collapsed")
        return float(m * 60 + s)

# --- ロジック分岐 ---
if mode_idx == 0:
    calc_dist = distance_input_aligned(c1, "距離", "m0_d")
    calc_secs = time_input_aligned(c2, "目標タイム", "m0_m", "m0_s")
    if calc_dist > 0: calc_ave = calc_secs / (calc_dist / 500)
    st.info(f"④ 必要なAverage: **{int(calc_ave // 60)}:{calc_ave % 60:04.1f}** / 500m")
elif mode_idx == 1:
    calc_dist = distance_input_aligned(c1, "距離", "m1_d")
    calc_secs = time_input_aligned(c2, "全体のAverage", "m1_am", "m1_as")
    calc_secs = calc_secs * (calc_dist / 500)
    st.info(f"④ 算出された合計タイム: **{int(calc_secs // 60)}:{calc_secs % 60:04.1f}**")
elif mode_idx == 2:
    calc_secs = time_input_aligned(c1, "合計時間", "m2_tm", "m2_ts")
    calc_dist = distance_input_aligned(c2, "距離", "m2_d")
    if calc_dist > 0: calc_ave = calc_secs / (calc_dist / 500)
    st.info(f"④ 計算されたAverage: **{int(calc_ave // 60)}:{calc_ave % 60:04.1f}** / 500m")
elif mode_idx == 3:
    calc_secs = time_input_aligned(c1, "測定時間", "m3_tm", "m3_ts")
    calc_ave = time_input_aligned(c2, "目標Average", "m3_am", "m3_as")
    if calc_ave > 0: calc_dist = (calc_secs / calc_ave) * 500
    st.info(f"④ 想定される合計目標距離: **{calc_dist:.1f} m**")

st.markdown("---")
if st.button("⑤ レースプランを作成", type="primary"):
    st.session_state.update({"active_plan_flag": True, "fixed_ave_seconds": calc_ave, "fixed_distance_m": calc_dist, "fixed_total_seconds": calc_secs, "fixed_calc_mode": "time_base" if mode_idx >= 2 else "distance_base", "fixed_mode_idx": mode_idx})
    st.rerun()

# --- レースプラン調整 ---
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
        if f"q{i}_offset_sec" not in st.session_state: st.session_state[f"q{i}_offset_sec"] = 0.0
        c1, c2, c3, c4 = st.columns([1, 2, 2, 3])
        c1.write(f"**{i}Q**")
        q_sec = base_ave + st.session_state[f"q{i}_offset_sec"]
        c2.write(f"**{int(q_sec//60)}:{q_sec%60:04.1f}**")
        b1, b2 = c3.columns(2)
        if b1.button("➕", key=f"p_{i}"): st.session_state[f"q{i}_offset_sec"] = st.session_state.get(f"q{i}_offset_sec", 0.0) + 0.5; st.rerun()
        if b2.button("➖", key=f"m_{i}"): st.session_state[f"q{i}_offset_sec"] = st.session_state.get(f"q{i}_offset_sec", 0.0) - 0.5; st.rerun()
        if calc_mode == 'distance_base':
            ts = q_sec * ((dist_total / 4) / 500); p_total_secs += ts
            c4.write(f"`{int(ts//60)}:{ts%60:04.1f}`")
        else:
            td = (secs_total / 4 / q_sec) * 500 if q_sec > 0 else 0; p_total_dist += td
            c4.write(f"`{td:.1f} m`")
    st.markdown("---")
    if calc_mode == 'distance_base':
        diff = p_total_secs - secs_total
        st.write(f"合計タイム: {int(p_total_secs//60)}:{p_total_secs%60:04.1f}")
        if abs(diff) < 0.1: st.success("🎉 目標とピッタリ！")
        elif diff > 0: st.error(f"⚠️ {diff:.1f}秒 遅い")
        else: st.info(f"💡 {abs(diff):.1f}秒 速い")
    else:
        diff = p_total_dist - dist_total
        st.write(f"合計距離: {p_total_dist:.1f} m")
        if abs(diff) < 0.5: st.success("🎉 目標とピッタリ！")
        elif diff > 0: st.success(f"🚀 {diff:.1f}m 多い")
        else: st.error(f"⚠️ {abs(diff):.1f}m 不足")
