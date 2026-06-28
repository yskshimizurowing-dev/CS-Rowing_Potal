import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="wide")

# スクロール抑制のため余白を最小化
st.markdown("""
<style>
    .stButton>button { width: 100%; height: 28px; font-size: 10px; padding: 0px; }
    div[data-testid="stMarkdownContainer"] { font-size: 10px; }
    .block-container { padding: 1rem 1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("##### 🛶 レースプランナー")

if "active_plan_flag" not in st.session_state: st.session_state["active_plan_flag"] = False

# 入力項目（スマホで1行に収めるためカテゴリ選択のみ表示）
menus = ["距離/タイム", "距離/Ave", "時間/距離", "時間/Ave"]
mode_idx = menus.index(st.selectbox("① カテゴリ", menus))
calc_dist, calc_secs, calc_ave = 2000.0, 480.0, 120.0 # 初期値
if st.button("作成", type="primary"):
    st.session_state.update({"active_plan_flag": True, "fixed_ave_seconds": calc_ave, "fixed_distance_m": calc_dist, "fixed_total_seconds": calc_secs, "fixed_calc_mode": "time_base" if mode_idx >= 2 else "distance_base"})
    st.rerun()

if st.session_state["active_plan_flag"]:
    base_ave, dist_total, secs_total, calc_mode = st.session_state["fixed_ave_seconds"], st.session_state["fixed_distance_m"], st.session_state["fixed_total_seconds"], st.session_state["fixed_calc_mode"]
    
    # 2x2 マトリクス配置（各セル内も極小化）
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
                
                # 結果表示を1行に
                if calc_mode == 'distance_base':
                    v = q_sec * ((dist_total/4)/500)
                    st.write(f"👉{int(v//60)}:{v%60:02.0f}")
                else:
                    v = (secs_total/4/q_sec)*500 if q_sec > 0 else 0
                    st.write(f"👉{v:.0f}m")

    if st.button("リセット"):
        for i in range(1, 5): st.session_state[f"q{i}_off"] = 0.0
        st.rerun()
