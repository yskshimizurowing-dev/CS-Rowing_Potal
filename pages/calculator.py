import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

# スマホのボタンサイズと余白を最適化
st.markdown("""
<style>
    .stButton>button { width: 100%; height: 35px; font-size: 13px; font-weight: bold; }
    [data-testid="column"] { padding: 0.1em; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🛶 エルゴ・レースプランナー")

if "active_plan_flag" not in st.session_state: st.session_state["active_plan_flag"] = False

# 入力欄（すべてのカテゴリに対応）
with st.expander("設定入力", expanded=not st.session_state["active_plan_flag"]):
    menus = ["距離と目標タイム", "距離とAverage", "合計時間と距離", "合計時間とAverage"]
    mode_idx = menus.index(st.selectbox("計算カテゴリ", menus))
    
    col1, col2 = st.columns(2)
    val1 = col1.number_input("距離(m)/時間(分)", value=2000.0)
    val2 = col2.number_input("タイム(秒)/Ave(秒)", value=120.0)
    
    if st.button("プラン作成・更新", type="primary"):
        st.session_state.update({
            "active_plan_flag": True,
            "fixed_ave_seconds": val2,
            "fixed_distance_m": val1 if mode_idx < 2 else 5000.0,
            "fixed_total_seconds": val2 * (val1/500) if mode_idx < 2 else val2,
            "fixed_calc_mode": "distance_base" if mode_idx < 2 else "time_base"
        })
        st.rerun()

# 調整および結果判定エリア
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
        
        # Q情報の表示
        if calc_mode == 'distance_base':
            this_v = q_sec * ((dist_total/4)/500)
            st.write(f"**{i}Q** Ave:{int(q_sec//60)}:{q_sec%60:02.0f} ➔ タイム:{int(this_v//60)}:{this_v%60:02.0f}")
            p_total_secs += this_v
        else:
            this_v = (secs_total/4/q_sec)*500 if q_sec > 0 else 0
            st.write(f"**{i}Q** Ave:{int(q_sec//60)}:{q_sec%60:02.0f} ➔ 距離:{this_v:.1f}m")
            p_total_dist += this_v
        
        # 操作ボタン
        b1, b2 = st.columns(2)
        if b1.button("➕ 0.5s", key=f"p{i}"): st.session_state[f"q{i}_off"] += 0.5; st.rerun()
        if b2.button("➖ 0.5s", key=f"m{i}"): st.session_state[f"q{i}_off"] -= 0.5; st.rerun()

    # 判定エリア
    st.markdown("---")
    if calc_mode == 'distance_base':
        diff = p_total_secs - secs_total
        st.write(f"### 合計タイム: {int(p_total_secs//60)}:{p_total_secs%60:02.0f}")
        st.success("🎉 目標とピッタリ！") if abs(diff) < 0.5 else (st.error(f"⚠️ {diff:.1f}秒遅い") if diff > 0 else st.info(f"💡 {abs(diff):.1f}秒速い"))
    else:
        diff = p_total_dist - dist_total
        st.write(f"### 合計距離: {p_total_dist:.1f}m")
        st.success("🎉 目標とピッタリ！") if abs(diff) < 0.5 else (st.success(f"🚀 {diff:.1f}m多い") if diff > 0 else st.error(f"⚠️ {abs(diff):.1f}m不足"))

    if st.button("全リセット"):
        for i in range(1, 5): st.session_state[f"q{i}_off"] = 0.0
        st.rerun()
