import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

# スマホでの視認性を高めるCSS
st.markdown("""
<style>
    .stButton>button { width: 100%; height: 40px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🛶 レースプランナー")

if "active_plan_flag" not in st.session_state: st.session_state["active_plan_flag"] = False

# 入力欄
with st.expander("①～⑤ 設定とプラン作成", expanded=not st.session_state["active_plan_flag"]):
    menus = ["距離とタイム", "距離とAve", "時間と距離", "時間とAve"]
    mode_idx = menus.index(st.selectbox("計算カテゴリ", menus))
    c1, c2 = st.columns(2)
    val1 = c1.number_input("距離/時間", value=2000.0)
    val2 = c2.number_input("タイム/Ave", value=120.0)
    if st.button("プラン作成・更新", type="primary"):
        st.session_state.update({
            "active_plan_flag": True, "fixed_ave_seconds": val2, 
            "fixed_distance_m": val1 if mode_idx < 2 else 5000.0,
            "fixed_total_seconds": val2 * (val1/500) if mode_idx < 2 else val2,
            "fixed_calc_mode": "distance_base" if mode_idx < 2 else "time_base"
        })
        st.rerun()

# 調整エリア
if st.session_state["active_plan_flag"]:
    base_ave = st.session_state["fixed_ave_seconds"]
    dist_total = st.session_state["fixed_distance_m"]
    secs_total = st.session_state["fixed_total_seconds"]
    calc_mode = st.session_state["fixed_calc_mode"]

    st.subheader("⏱️ 各Qの調整")
    
    for i in range(1, 5):
        if f"q{i}_off" not in st.session_state: st.session_state[f"q{i}_off"] = 0.0
        q_sec = base_ave + st.session_state[f"q{i}_off"]
        
        # Q情報を1行で表示
        if calc_mode == 'distance_base':
            v = q_sec * ((dist_total/4)/500)
            st.write(f"**{i}Q** Ave:{int(q_sec//60)}:{q_sec%60:02.0f} ➔ タイム:{int(v//60)}:{v%60:02.0f}")
        else:
            v = (secs_total/4/q_sec)*500 if q_sec > 0 else 0
            st.write(f"**{i}Q** Ave:{int(q_sec//60)}:{q_sec%60:02.0f} ➔ 距離:{v:.0f}m")
        
        # ボタンを横配置
        b1, b2 = st.columns(2)
        if b1.button("➕ 0.5s", key=f"p{i}"): st.session_state[f"q{i}_off"] += 0.5; st.rerun()
        if b2.button("➖ 0.5s", key=f"m{i}"): st.session_state[f"q{i}_off"] -= 0.5; st.rerun()

    if st.button("全リセット"):
        for i in range(1, 5): st.session_state[f"q{i}_off"] = 0.0
        st.rerun()
