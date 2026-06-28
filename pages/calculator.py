import streamlit as st

# ページ設定とCSS
st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")
st.markdown("""
<style>
    .stButton>button { width: 100%; height: 2.5em; padding: 0; font-size: 14px; }
    [data-testid="column"] { padding: 0.1em; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🛶 エルゴ・<br>レースプランシミュレーター", unsafe_allow_html=True)
st.markdown("---")

# --- セッションとメニュー ---
if "active_plan_flag" not in st.session_state: st.session_state["active_plan_flag"] = False

def clear_plan_states():
    for i in range(1, 5): st.session_state[f"q{i}_offset_sec"] = 0.0
    st.session_state["active_plan_flag"] = False

menus = ["距離 と 目標タイム から【全体のAverage】を出す", "距離 と Average から【目標タイム】を出す", "合計時間 と 距離 から【全体のAverage】を出す", "合計時間 と Average から【目標距離】を出す"]
selected_menu = st.selectbox("① 計算カテゴリー選択", menus, index=st.session_state.get("fixed_mode_idx", 0) if st.session_state["active_plan_flag"] else 0, on_change=clear_plan_states)
mode_idx = menus.index(selected_menu)

# --- 入力ロジック ---
calc_dist, calc_secs, calc_ave = 0.0, 0.0, 0.0
if mode_idx in [0, 1]:
    st.write("② 距離（メートル）"); calc_dist = float(st.number_input("距離", value=2000, step=500, key="d_in"))
    st.write("③ タイム/Ave（分:秒）")
    c1, c2 = st.columns(2)
    m = c1.number_input("分", value=8 if mode_idx==0 else 2, key="m_in")
    s = c2.number_input("秒", value=0, key="s_in")
    if mode_idx == 0:
        calc_secs = float(m * 60 + s)
        if calc_dist > 0: calc_ave = calc_secs / (calc_dist / 500)
    else:
        calc_ave = float(m * 60 + s)
        calc_secs = calc_ave * (calc_dist / 500)
else:
    st.write("② 合計時間（分:秒）")
    c1, c2 = st.columns(2)
    m = c1.number_input("分", value=20, key="tm_in"); s = c2.number_input("秒", value=0, key="ts_in")
    calc_secs = float(m * 60 + s)
    st.write("③ 距離（メートル）"); calc_dist = float(st.number_input("距離", value=5000, step=500, key="d_in2"))
    if mode_idx == 2:
        if calc_dist > 0: calc_ave = calc_secs / (calc_dist / 500)
    else:
        st.write("③ 目標Average（分:秒）")
        c1, c2 = st.columns(2)
        m = c1.number_input("分", value=1, key="am_in2"); s = c2.number_input("秒", value=50, key="as_in2")
        calc_ave = float(m * 60 + s)
        if calc_ave > 0: calc_dist = (calc_secs / calc_ave) * 500

if st.button("⑤ レースプランを作成", type="primary"):
    st.session_state.update({"active_plan_flag": True, "fixed_ave_seconds": calc_ave, "fixed_distance_m": calc_dist, "fixed_total_seconds": calc_secs, "fixed_calc_mode": "time_base" if mode_idx >= 2 else "distance_base", "fixed_mode_idx": mode_idx})
    st.rerun()

# --- レースプラン調整 & 結果 ---
if st.session_state["active_plan_flag"]:
    base_ave, dist_total, secs_total, calc_mode = st.session_state["fixed_ave_seconds"], st.session_state["fixed_distance_m"], st.session_state["fixed_total_seconds"], st.session_state["fixed_calc_mode"]
    st.subheader("⏱️ 各Qの調整")
    if st.button("全リセット"):
        for i in range(1, 5): st.session_state[f"q{i}_offset_sec"] = 0.0
        st.rerun()

    h1, h2, h3, h4 = st.columns([0.8, 2, 2.5, 2])
    h1.caption("Q"); h2.caption("Ave"); h3.caption("±0.5s"); h4.caption("結果")

    p_total_secs, p_total_dist = 0.0, 0.0
    for i in range(1, 5):
        if f"q{i}_offset_sec" not in st.session_state: st.session_state[f"q{i}_offset_sec"] = 0.0
        q_sec = base_ave + st.session_state[f"q{i}_offset_sec"]
        c1, c2, c3, c4 = st.columns([0.8, 2, 2.5, 2])
        c1.write(f"**{i}**"); c2.write(f"**{int(q_sec//60)}:{q_sec%60:02.1f}**")
        b1, b2 = c3.columns(2)
        if b1.button("➕", key=f"p_{i}"): st.session_state[f"q{i}_offset_sec"] += 0.5; st.rerun()
        if b2.button("➖", key=f"m_{i}"): st.session_state[f"q{i}_offset_sec"] -= 0.5; st.rerun()
        
        if calc_mode == 'distance_base':
            this_v = q_sec * ((dist_total / 4) / 500); p_total_secs += this_v; c4.write(f"`{int(this_v//60)}:{this_v%60:02.1f}`")
        else:
            this_v = (secs_total / 4 / q_sec) * 500 if q_sec > 0 else 0; p_total_dist += this_v; c4.write(f"`{this_v:.0f}m`")

    st.markdown("---")
    if calc_mode == 'distance_base':
        diff = p_total_secs - secs_total
        st.write(f"### 合計: {int(p_total_secs//60)}:{p_total_secs%60:02.1f}")
        st.success("🎉 ピッタリ！") if abs(diff) < 0.1 else (st.error(f"⚠️ {diff:.1f}秒遅") if diff > 0 else st.info(f"💡 {abs(diff):.1f}秒速"))
    else:
        diff = p_total_dist - dist_total
        st.write(f"### 合計: {p_total_dist:.1f}m")
        st.success("🎉 ピッタリ！") if abs(diff) < 0.5 else (st.success(f"🚀 {diff:.1f}m多") if diff > 0 else st.error(f"⚠️ {abs(diff):.1f}m不足"))
