import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

st.markdown("""
<style>
    .stButton>button { width: 100%; height: 32px; font-size: 11px; font-weight: bold; }
    [data-testid="column"] { padding: 0.1em; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🛶 エルゴ・<br>レースプランシミュレーター", unsafe_allow_html=True)

if "active_plan_flag" not in st.session_state: st.session_state["active_plan_flag"] = False

# 入力欄
with st.expander("①～⑤ 設定入力と作成", expanded=not st.session_state["active_plan_flag"]):
    menus = ["距離と目標タイム", "距離とAverage", "合計時間と距離", "合計時間とAverage"]
    mode_idx = menus.index(st.selectbox("カテゴリ", menus))
    if mode_idx in [0, 1]:
        calc_dist = st.number_input("距離(m)", value=2000, step=500)
        c1, c2 = st.columns(2)
        m, s = c1.number_input("分", value=8 if mode_idx==0 else 2), c2.number_input("秒", value=0)
        calc_ave = (m*60+s)/(calc_dist/500) if mode_idx==0 and calc_dist>0 else (m*60+s)
        calc_secs = (m*60+s) if mode_idx==0 else (m*60+s)*(calc_dist/500)
    else:
        c1, c2 = st.columns(2)
        m, s = c1.number_input("分", value=20), c2.number_input("秒", value=0)
        calc_secs = float(m*60+s)
        calc_dist = st.number_input("距離(m)", value=5000, step=500)
        calc_ave = calc_secs/(calc_dist/500) if calc_dist>0 else 0
    if st.button("プラン作成", type="primary"):
        st.session_state.update({"active_plan_flag": True, "fixed_ave_seconds": calc_ave, "fixed_distance_m": calc_dist, "fixed_total_seconds": calc_secs, "fixed_calc_mode": "time_base" if mode_idx >= 2 else "distance_base"})
        st.rerun()

# 調整エリア
if st.session_state["active_plan_flag"]:
    base_ave = st.session_state["fixed_ave_seconds"]
    dist_total = st.session_state["fixed_distance_m"]
    secs_total = st.session_state["fixed_total_seconds"]
    calc_mode = st.session_state["fixed_calc_mode"]

    st.subheader("⏱️ 各Qの調整")
    p_total_secs, p_total_dist = 0.0, 0.0
    for i in range(1, 5):
        if f"q{i}_off" not in st.session_state: st.session_state[f"q{i}_off"] = 0.0
        q_sec = base_ave + st.session_state[f"q{i}_off"]
        
        # 1行目: 情報表示
        if calc_mode == 'distance_base':
            this_v = q_sec * ((dist_total/4)/500)
            st.markdown(f"**{i}Q** (Ave:{int(q_sec//60)}:{q_sec%60:02.0f}) ➔ `{int(this_v//60)}:{this_v%60:02.0f}`")
            p_total_secs += this_v
        else:
            this_v = (secs_total/4/q_sec)*500 if q_sec > 0 else 0
            st.markdown(f"**{i}Q** (Ave:{int(q_sec//60)}:{q_sec%60:02.0f}) ➔ `{this_v:.0f}m`")
            p_total_dist += this_v
        
        # 2行目: プラスマイナスボタンを横並び
        b_cols = st.columns(2)
        if b_cols[0].button("➕ 0.5s", key=f"p{i}"): st.session_state[f"q{i}_off"] += 0.5; st.rerun()
        if b_cols[1].button("➖ 0.5s", key=f"m{i}"): st.session_state[f"q{i}_off"] -= 0.5; st.rerun()

    if st.button("全リセット"):
        for i in range(1, 5): st.session_state[f"q{i}_off"] = 0.0
        st.rerun()

    st.markdown("---")
    if calc_mode == 'distance_base':
        diff = p_total_secs - secs_total
        st.write(f"合計: {int(p_total_secs//60)}:{p_total_secs%60:02.0f} / " + ("OK!" if abs(diff)<0.5 else f"{diff:.1f}s"))
    else:
        diff = p_total_dist - dist_total
        st.write(f"合計: {p_total_dist:.0f}m / " + ("OK!" if abs(diff)<0.5 else f"{diff:.1f}m"))
