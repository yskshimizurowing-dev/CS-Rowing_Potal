import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

st.markdown("""
<style>
    .stButton>button { width: 100%; height: 30px; font-size: 11px; }
    .stExpander { border: none; }
</style>
""", unsafe_allow_html=True)

st.markdown("##### 🛶 エルゴ・レースプランナー")

if "active_plan_flag" not in st.session_state: st.session_state["active_plan_flag"] = False

# 入力フォームをexpanderに格納
with st.expander("①～⑤ 設定入力", expanded=not st.session_state["active_plan_flag"]):
    menus = ["距離とタイム", "距離とAve", "時間と距離", "時間とAve"]
    mode_idx = menus.index(st.selectbox("計算カテゴリ", menus))
    
    # 入力ロジックを簡潔化
    c1, c2 = st.columns(2)
    val1 = c1.number_input("距離/時間(分)", value=2000.0)
    val2 = c2.number_input("タイム/Ave(秒)", value=120.0)
    
    if st.button("プラン作成・更新"):
        # 計算ロジック（簡易版）
        dist = val1 if mode_idx < 2 else 5000.0
        ave = val2
        st.session_state.update({"active_plan_flag": True, "fixed_ave_seconds": ave, "fixed_distance_m": dist, "fixed_total_seconds": ave * (dist/500), "fixed_calc_mode": "distance_base"})
        st.rerun()

if st.session_state["active_plan_flag"]:
    base_ave = st.session_state["fixed_ave_seconds"]
    
    st.subheader("⏱️ 各Qの調整")
    # 2x2 マトリクス配置
    for row in range(2):
        r_cols = st.columns(2)
        for col in range(2):
            i = row * 2 + col + 1
            if f"q{i}_off" not in st.session_state: st.session_state[f"q{i}_off"] = 0.0
            q_sec = base_ave + st.session_state[f"q{i}_off"]
            with r_cols[col]:
                st.write(f"**{i}Q** {int(q_sec//60)}:{q_sec%60:02.0f}")
                b1, b2 = st.columns(2)
                if b1.button("➕", key=f"p{i}"): st.session_state[f"q{i}_off"] += 0.5; st.rerun()
                if b2.button("➖", key=f"m{i}"): st.session_state[f"q{i}_off"] -= 0.5; st.rerun()
    
    if st.button("リセット"):
        for i in range(1, 5): st.session_state[f"q{i}_off"] = 0.0
        st.rerun()
