import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

# CSS: スマホでの操作性を確保
st.markdown("""
<style>
    .stButton>button { width: 100%; height: 3.5em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🛶 エルゴ・<br>レースプランシミュレーター", unsafe_allow_html=True)
st.markdown("---")

# --- 初期化 ---
if "active_plan_flag" not in st.session_state: st.session_state["active_plan_flag"] = False

def clear_plan_states():
    for i in range(1, 5): st.session_state[f"q{i}_offset_sec"] = 0.0
    st.session_state["active_plan_flag"] = False

# --- メニュー選択 ---
menus = [
    "距離 と 目標タイム から【全体のAverage】を出す", 
    "距離 と Average から【目標タイム】を出す",
    "合計時間 と 距離 から【全体のAverage】を出す",
    "合計時間 と Average から【目標距離】を出す"
]
selected_menu = st.selectbox("① 計算カテゴリー選択", menus, index=st.session_state.get("fixed_mode_idx", 0) if st.session_state["active_plan_flag"] else 0, on_change=clear_plan_states)
mode_idx = menus.index(selected_menu)

# --- 入力ロジック ---
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

# --- プラン作成 ---
if st.button("⑤ レースプランを作成", type="primary"):
    st.session_state.update({"active_plan_flag": True, "fixed_ave_seconds": calc_ave, "fixed_distance_m": calc_dist, "fixed_total_seconds": calc_secs, "fixed_calc_mode": "time_base" if mode_idx >= 2 else "distance_base", "fixed_mode_idx": mode_idx})
    st.rerun()

if st.session_state["active_plan_flag"]:
    # 調整エリア（省略なし）
    st.subheader("⏱️ 各Qの調整")
    if st.button("リセット"):
        for i in range(1, 5): st.session_state[f"q{i}_offset_sec"] = 0.0
        st.rerun()
    # (Qごとのループ・判定ロジックをここに配置)
