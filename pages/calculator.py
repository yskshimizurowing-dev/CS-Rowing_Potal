import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

# スマホ特化: 調整エリアを1行に収めるためのCSS
st.markdown("""
<style>
    .stButton>button { width: 100%; height: 2.5em; font-size: 12px; }
    [data-testid="column"] { padding: 0px 2px; }
    div[data-testid="stMarkdownContainer"] { font-size: 13px; }
    h3 { margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🛶 エルゴ・<br>レースプランシミュレーター", unsafe_allow_html=True)
st.markdown("---")

if "active_plan_flag" not in st.session_state: st.session_state["active_plan_flag"] = False

def clear_plan_states():
    for i in range(1, 5): st.session_state[f"q{i}_offset_sec"] = 0.0
    st.session_state["active_plan_flag"] = False

menus = ["距離と目標タイム", "距離とAverage", "合計時間と距離", "合計時間とAverage"]
selected_menu = st.selectbox("① 計算カテゴリー選択", menus, index=st.session_state.get("fixed_mode_idx", 0) if st.session_state["active_plan_flag"] else 0, on_change=clear_plan_states)
mode_idx = menus.index(selected_menu)

# --- 入力ロジック ---
calc_dist, calc_secs, calc_ave = 0.0, 0.0, 0.0
if mode_idx in [0, 1]:
    calc_dist = float(st.number_input("距離(m)", value=2000, step=500, key="d_in"))
    c1, c2 = st.columns(2)
    m = c1.number_input("分", value=8 if mode_idx==0 else 2, key="m_in"); s = c2.number_input("秒", value=0, key="s_in")
    if mode_idx == 0: calc_secs = float(m*60+s); calc_ave = calc_secs/(calc_dist/500) if calc_dist>0 else 0
    else: calc_ave = float(m*60+s); calc_secs = calc_ave*(calc_dist/500)
else:
    c1, c2 = st.columns(2)
    m = c1.number_input("合計分", value=20, key="tm_in"); s = c2.number_input("秒", value=0, key="ts_in")
    calc_secs = float(m*60+s); calc_dist = float(st.number_input("距離(m)", value=5000, step=500, key="d_in2"))
    if mode_idx == 2: calc_ave = calc_secs/(calc_dist/500) if calc_dist>0 else 0
    else: calc_ave = float(st.number_input("Ave秒", value=110, key="am3"))

if st.button("⑤ プラン作成", type="primary"):
    st.session_state.update({"active_plan_flag": True, "fixed_ave_seconds": calc_ave, "fixed_distance_m": calc_dist, "fixed_total_seconds": calc_secs, "fixed_calc_mode": "time_base" if mode_idx >= 2 else "distance_base", "fixed_mode_idx": mode_idx})
    st.rerun()

if st.session_state["active_plan_flag"]:
    base_ave, dist_total, secs_total, calc_mode = st.session_state["fixed_ave_seconds"], st.session_state["fixed_distance_m"], st.session_state["fixed_total_seconds"], st.session_state["fixed_calc_mode"]
    st.subheader("⏱️ 各Qの調整")
    
    # 全てを一行に並べる
    p_total_secs, p_total_dist = 0.0, 0.0
    for i in range(1, 5):
        if f"q{i}_offset_sec" not in st.session_state: st.session_state[f"q{i}_offset_sec"] = 0.0
        q_sec = base_ave + st.session_state[f"q{i}_offset_sec"]
        
        # [Q番号, Ave, +/-ボタン, 結果]を1行に凝縮
        c1, c2, c3, c4 = st.columns([0.5, 1.5, 2, 1.5])
        c1.write(f"**{i}**")
        c2.write(f"{int(q_sec//60)}:{q_sec%60:02.0f}")
        
        btn = c3.columns(2)
        if btn[0].button("➕", key=f"p_{i}"): st.session_state[f"q{i}_offset_sec"] += 0.5; st.rerun()
        if btn[1].button("➖", key=f"m_{i}"): st.session_state[f"q{i}_offset_sec"] -= 0.5; st.rerun()
        
        if calc_mode == 'distance_base':
            this_v = q_sec * ((dist_total/4)/500); p_total_secs += this_v
            c4.write(f"`{int(this_v//60)}:{this_v%60:02.0f}`")
        else:
            this_v = (secs_total/4/q_sec)*500 if q_sec>0 else 0; p_total_dist += this_v
            c4.write(f"`{this_v:.0f}m`")

    if st.button("全リセット"):
        for i in range(1, 5): st.session_state[f"q{i}_offset_sec"] = 0.0
        st.rerun()

    # 判定もコンパクトに
    if calc_mode == 'distance_base':
        diff = p_total_secs - secs_total
        st.write(f"合計: {int(p_total_secs//60)}:{p_total_secs%60:02.0f} / " + ("OK!" if abs(diff)<1 else f"{diff:.1f}s"))
    else:
        diff = p_total_dist - dist_total
        st.write(f"合計: {p_total_dist:.0f}m / " + ("OK!" if abs(diff)<1 else f"{diff:.1f}m"))
