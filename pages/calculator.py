import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

# スマホ特化: 調整エリアを1行に凝縮するCSS
st.markdown("""
<style>
    .stButton>button { width: 100%; height: 30px; font-size: 11px; padding: 0px; margin: 0px; }
    [data-testid="column"] { padding: 0px 2px; }
    div[data-testid="stMarkdownContainer"] { font-size: 12px; }
</style>
""", unsafe_allow_html=True)

st.markdown("🛶 **レースプランナー**")

if "active_plan_flag" not in st.session_state: st.session_state["active_plan_flag"] = False

# 入力欄
with st.expander("設定"):
    menus = ["距離/タイム", "距離/Ave", "時間/距離", "時間/Ave"]
    mode_idx = menus.index(st.selectbox("カテゴリ", menus))
    c1, c2 = st.columns(2)
    val1 = c1.number_input("距離/時間", value=2000.0)
    val2 = c2.number_input("タイム/Ave", value=120.0)
    if st.button("作成"):
        st.session_state.update({
            "active_plan_flag": True, "fixed_ave_seconds": val2, 
            "fixed_distance_m": val1 if mode_idx < 2 else 5000.0,
            "fixed_total_seconds": val2 * (val1/500) if mode_idx < 2 else val2,
            "fixed_calc_mode": "distance_base" if mode_idx < 2 else "time_base"
        })
        st.rerun()

# 調整エリア
if st.session_state["active_plan_flag"]:
    base_ave, dist_total, secs_total, calc_mode = st.session_state["fixed_ave_seconds"], st.session_state["fixed_distance_m"], st.session_state["fixed_total_seconds"], st.session_state["fixed_calc_mode"]
    
    for i in range(1, 5):
        if f"q{i}_off" not in st.session_state: st.session_state[f"q{i}_off"] = 0.0
        q_sec = base_ave + st.session_state[f"q{i}_off"]
        
        # 1行に [Q番号] [Ave/結果] [+ボタン] [-ボタン] を横並び配置
        cols = st.columns([0.8, 2.5, 1.2, 1.2])
        cols[0].write(f"**{i}Q**")
        
        # 計算結果表示
        if calc_mode == 'distance_base':
            v = q_sec * ((dist_total/4)/500)
            cols[1].write(f"{int(q_sec//60)}:{q_sec%60:02.0f}➔{int(v//60)}:{v%60:02.0f}")
        else:
            v = (secs_total/4/q_sec)*500 if q_sec > 0 else 0
            cols[1].write(f"{int(q_sec//60)}:{q_sec%60:02.0f}➔{v:.0f}m")
            
        # ボタンを横配置
        if cols[2].button("➕", key=f"p{i}"): st.session_state[f"q{i}_off"] += 0.5; st.rerun()
        if cols[3].button("➖", key=f"m{i}"): st.session_state[f"q{i}_off"] -= 0.5; st.rerun()
            
    if st.button("全リセット"):
        for i in range(1, 5): st.session_state[f"q{i}_off"] = 0.0
        st.rerun()
