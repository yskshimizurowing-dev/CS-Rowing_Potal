import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

st.markdown("""
<style>
    .stButton>button { width: 100%; height: 3.5em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🛶 エルゴ・<br>レースプランシミュレーター", unsafe_allow_html=True)
st.markdown("---")

if "active_plan_flag" not in st.session_state: st.session_state["active_plan_flag"] = False

def clear_plan_states():
    for i in range(1, 5): st.session_state[f"q{i}_offset_sec"] = 0.0
    st.session_state["active_plan_flag"] = False

menus = [
    "距離 と 目標タイム から【全体のAverage】を出す", 
    "距離 と Average から【目標タイム】を出す",
    "合計時間 と 距離 から【全体のAverage】を出す",
    "合計時間 と Average から【目標距離】を出す"
]
selected_menu = st.selectbox("① 計算カテゴリー選択", menus, index=st.session_state.get("fixed_mode_idx", 0) if st.session_state["active_plan_flag"] else 0, on_change=clear_plan_states)
mode_idx = menus.index(selected_menu)

calc_dist, calc_secs, calc_ave = 0.0, 0.0, 0.0

if mode_idx == 0:
    st.write("② 距離（メートル）"); calc_dist = float(st.number_input("距離", value=2000, step=500, key="d0"))
    st.write("③ 目標タイム（分:秒）")
    c1, c2 = st.columns(2)
    m = c1.number_input("分", value=8, key="m0"); s = c2.number_input("秒", value=0, key="s0")
    calc_secs = float(m * 60 + s)
    if calc_dist > 0: calc_ave = calc_secs / (calc_dist / 500)
elif mode_idx == 1:
    st.write("② 距離（メートル）"); calc_dist = float(st.number_input("距離", value=2000, step=500, key="d1"))
    st.write("③ Average（分:秒）")
    c1, c2 = st.columns(2)
    m = c1.number_input("分", value=2, key="m1"); s = c2.number_input("秒", value=0, key="s1")
    calc_ave = float(m * 60 + s)
    calc_secs = calc_ave * (calc_dist / 500)
elif mode_idx == 2:
    st.write("② 合計時間（分:秒）")
    c1, c2 = st.columns(2)
    m = c1.number_input("分", value=20, key="m2"); s = c2.number_input("秒", value=0, key="s2")
    calc_secs = float(m * 60 + s)
    st.write("③ 距離（メートル）"); calc_dist = float(st.number_input("距離", value=5000, step=500, key="d2"))
    if calc_dist > 0: calc_ave = calc_secs / (calc_dist / 500)
elif mode_idx == 3:
    st.write("② 測定時間（分:秒）")
    c1, c2 = st.columns(2)
    m = c1.number_input("分", value=20, key="m3"); s = c2.number_input("秒", value=0, key="s3")
    calc_secs = float(m * 60 + s)
    st.write("③ 目標Average（分:秒）")
    c1, c2 = st.columns(2)
    m = c1.number_input("分", value=1, key="am3"); s = c2.number_input("秒", value=50, key="as3")
    calc_ave = float(m * 60 + s)
    if calc_ave > 0: calc_dist = (calc_secs / calc_ave) * 500

if st.button("⑤ レースプランを作成", type="primary"):
    st.session_state.update({"active_plan_flag": True, "fixed_ave_seconds": calc_ave, "fixed_distance_m": calc_dist, "fixed_total_seconds": calc_secs, "fixed_calc_mode": "time_base" if mode_idx >= 2 else "distance_base", "fixed_mode_idx": mode_idx})
    st.rerun()

if st.session_state["active_plan_flag"]:
    base_ave, dist_total, secs_total, calc_mode = st.session_state["fixed_ave_seconds"], st.session_state["fixed_distance_m"], st.session_state["fixed_total_seconds"], st.session_state["fixed_calc_mode"]
    st.subheader("⏱️ 各Qの調整")
    if st.button("リセット"):
        for i in range(1, 5): st.session_state[f"q{i}_offset_sec"] = 0.0
        st.rerun()

    p_total_secs, p_total_dist = 0.0, 0.0
    for i in range(1, 5):
        if f"q{i}_offset_sec" not in st.session_state: st.session_state[f"q{i}_offset_sec"] = 0.0
        q_sec = base_ave + st.session_state[f"q{i}_offset_sec"]
        st.markdown(f"**{i}Q** (Ave: {int(q_sec//60)}:{q_sec%60:04.1f})")
        if calc_mode == 'distance_base':
            this_val = q_sec * ((dist_total / 4) / 500)
            st.write(f"➔ タイム: `{int(this_val//60)}:{this_val%60:04.1f}`")
            p_total_secs += this_val
        else:
            this_val = (secs_total / 4 / q_sec) * 500 if q_sec > 0 else 0
            st.write(f"➔ 距離: `{this_val:.1f} m`")
            p_total_dist += this_val
        
        b1, b2 = st.columns(2)
        if b1.button("➕ 0.5s", key=f"p_{i}"): st.session_state[f"q{i}_offset_sec"] += 0.5; st.rerun()
        if b2.button("➖ 0.5s", key=f"m_{i}"): st.session_state[f"q{i}_offset_sec"] -= 0.5; st.rerun()

    st.markdown("---")
    if calc_mode == 'distance_base':
        diff = p_total_secs - secs_total
        st.write(f"### 合計タイム: {int(p_total_secs//60)}:{p_total_secs%60:04.1f}")
        if abs(diff) < 0.1: st.success("🎉 目標とピッタリ！")
        elif diff > 0: st.error(f"⚠️ {diff:.1f}秒 遅い")
        else: st.info(f"💡 {abs(diff):.1f}秒 速い")
    else:
        diff = p_total_dist - dist_total
        st.write(f"### 合計距離: {p_total_dist:.1f} m")
        if abs(diff) < 0.5: st.success("🎉 目標とピッタリ！")
        elif diff > 0: st.success(f"🚀 {diff:.1f}m 多い")
        else: st.error(f"⚠️ {abs(diff):.1f}m 不足")
