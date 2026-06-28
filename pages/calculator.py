import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

# Qごとの背景色を明確にするCSS
st.markdown("""
<style>
    .q-box { 
        background-color: #f0f2f6; 
        padding: 10px; 
        border-radius: 10px; 
        margin-bottom: 10px; 
        border: 1px solid #d1d1d1;
    }
    .stButton>button { width: 100%; height: 35px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🛶 エルゴ・レースプランナー")

if "active_plan_flag" not in st.session_state: st.session_state["active_plan_flag"] = False

# --- 設定入力エリア ---
with st.expander("①～⑤ 設定入力とプラン作成", expanded=not st.session_state["active_plan_flag"]):
    menus = ["距離と目標タイム", "距離とAverage", "合計時間と距離", "合計時間とAverage"]
    mode_idx = menus.index(st.selectbox("計算カテゴリ", menus))
    dist = st.number_input("距離(m)", value=2000, step=500)
    
    st.write("時間/Ave (分:秒)")
    c1, c2 = st.columns(2)
    m = c1.number_input("分", value=2)
    s = c2.number_input("秒", value=0)
    
    if st.button("プラン作成・更新", type="primary"):
        calc_secs = m * 60 + s
        if mode_idx == 0:
            calc_ave = calc_secs / (dist / 500)
            calc_mode = 'distance_base'
        elif mode_idx == 1:
            calc_ave = calc_secs
            calc_secs = calc_ave * (dist / 500)
            calc_mode = 'distance_base'
        elif mode_idx == 2:
            calc_ave = calc_secs / (dist / 500)
            calc_mode = 'time_base'
        else:
            calc_ave = calc_secs
            calc_secs = 0
            calc_mode = 'time_base'
            
        st.session_state.update({
            "active_plan_flag": True, "fixed_ave_seconds": calc_ave, 
            "fixed_distance_m": dist, "fixed_total_seconds": calc_secs,
            "fixed_calc_mode": calc_mode
        })
        st.rerun()

# --- 調整エリア ---
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
        
        # 背景色付きコンテナ内に詳細を表示
        st.markdown('<div class="q-box">', unsafe_allow_html=True)
        if calc_mode == 'distance_base':
            this_v = q_sec * ((dist_total/4)/500)
            st.write(f"**{i}Q** Ave:{int(q_sec//60)}:{q_sec%60:04.1f} ➔ タイム:{int(this_v//60)}:{this_v%60:04.1f}")
            p_total_secs += this_v
        else:
            this_v = (secs_total/4/q_sec)*500 if q_sec > 0 else 0
            st.write(f"**{i}Q** Ave:{int(q_sec//60)}:{q_sec%60:04.1f} ➔ 距離:{this_v:.1f}m")
            p_total_dist += this_v
        
        b1, b2 = st.columns(2)
        if b1.button("➕ 0.5s", key=f"p{i}"): st.session_state[f"q{i}_off"] += 0.5; st.rerun()
        if b2.button("➖ 0.5s", key=f"m{i}"): st.session_state[f"q{i}_off"] -= 0.5; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 判定とリセット ---
    st.markdown("---")
    if calc_mode == 'distance_base':
        diff = p_total_secs - secs_total
        st.write(f"### 合計タイム: {int(p_total_secs//60)}:{p_total_secs%60:04.1f}")
        st.success("🎉 目標とピッタリ！") if abs(diff) < 0.5 else (st.error(f"⚠️ {diff:.1f}秒遅い") if diff > 0 else st.info(f"💡 {abs(diff):.1f}秒速い"))
    else:
        diff = p_total_dist - dist_total
        st.write(f"### 合計距離: {p_total_dist:.1f}m")
        st.success("🎉 目標とピッタリ！") if abs(diff) < 0.5 else (st.success(f"🚀 {diff:.1f}m多い") if diff > 0 else st.error(f"⚠️ {abs(diff):.1f}m不足"))

    if st.button("全リセット"):
        for i in range(1, 5): st.session_state[f"q{i}_off"] = 0.0
        st.rerun()
