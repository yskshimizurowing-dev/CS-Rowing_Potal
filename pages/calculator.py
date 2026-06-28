import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

# スマホ特化: 調整エリアの密度を高めるCSS
st.markdown("""
<style>
    .stButton>button { width: 100%; height: 36px; font-size: 13px; font-weight: bold; }
    div[data-testid="stMarkdownContainer"] { font-size: 13px; margin: 0; }
    .q-row { display: flex; align-items: center; justify-content: space-between; padding: 2px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("##### 🛶 エルゴ・レースプランナー")

if "active_plan_flag" not in st.session_state: st.session_state["active_plan_flag"] = False

# 入力設定エリア（折りたたみ）
with st.expander("設定入力"):
    menus = ["距離と目標タイム", "距離とAverage", "合計時間と距離", "合計時間とAverage"]
    mode_idx = menus.index(st.selectbox("計算カテゴリ", menus))
    
    col1, col2 = st.columns(2)
    val1 = col1.number_input("距離/時間(分)", value=2000.0)
    val2 = col2.number_input("タイム/Ave(秒)", value=120.0)
    
    if st.button("プラン更新"):
        st.session_state.update({
            "active_plan_flag": True,
            "fixed_ave_seconds": val2,
            "fixed_distance_m": val1 if mode_idx < 2 else 5000.0,
            "fixed_total_seconds": val2 * (val1/500) if mode_idx < 2 else val2,
            "fixed_calc_mode": "distance_base" if mode_idx < 2 else "time_base"
        })
        st.rerun()

# 調整エリア
if st.session_state["active_plan_flag"]:
    base_ave = st.session_state["fixed_ave_seconds"]
    
    st.markdown("---")
    for i in range(1, 5):
        if f"q{i}_off" not in st.session_state: st.session_state[f"q{i}_off"] = 0.0
        q_sec = base_ave + st.session_state[f"q{i}_off"]
        
        # 1行に表示を集約
        st.markdown(f"**{i}Q** `{int(q_sec//60)}:{q_sec%60:02.0f}`")
        
        # ボタンを横並びに
        cols = st.columns(2)
        if cols[0].button("➕ 0.5s", key=f"p{i}"):
            st.session_state[f"q{i}_off"] += 0.5
            st.rerun()
        if cols[1].button("➖ 0.5s", key=f"m{i}"):
            st.session_state[f"q{i}_off"] -= 0.5
            st.rerun()
            
    if st.button("全リセット"):
        for i in range(1, 5): st.session_state[f"q{i}_off"] = 0.0
        st.rerun()
