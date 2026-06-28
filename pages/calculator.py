import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered", initial_sidebar_state="expanded")

# スマホ特化: 高さを節約しつつ、ボタンを押しやすくするCSS
st.markdown("""
<style>
    .stButton>button { width: 100%; height: 32px; font-size: 11px; padding: 0px; }
    div[data-testid="stMarkdownContainer"] { font-size: 12px; }
    .css-1544g2n { padding-top: 0rem; } /* 余白を削減 */
</style>
""", unsafe_allow_html=True)

st.markdown("##### 🛶 レースプランナー")

if "active_plan_flag" not in st.session_state: st.session_state["active_plan_flag"] = False

# 入力欄をサイドバーへ移動（メインエリアの高さ確保のため）
with st.sidebar:
    st.write("---")
    menus = ["距離と目標タイム", "距離とAverage", "合計時間と距離", "合計時間とAverage"]
    selected_menu = st.selectbox("カテゴリ", menus, index=st.session_state.get("fixed_mode_idx", 0) if st.session_state["active_plan_flag"] else 0)
    mode_idx = menus.index(selected_menu)
    calc_dist, calc_secs, calc_ave = 0.0, 0.0, 0.0
    if mode_idx in [0, 1]:
        calc_dist = float(st.number_input("距離(m)", value=2000, step=500))
        c1, c2 = st.columns(2)
        m = c1.number_input("分", value=8 if mode_idx==0 else 2); s = c2.number_input("秒", value=0)
        if mode_idx == 0: calc_secs = float(m*60+s); calc_ave = calc_secs/(calc_dist/500) if calc_dist>0 else 0
        else: calc_ave = float(m*60+s); calc_secs = calc_ave*(calc_dist/500)
    else:
        c1, c2 = st.columns(2)
        m = c1.number_input("分", value=20); s = c2.number_input("秒", value=0)
        calc_secs = float(m*60+s); calc_dist = float(st.number_input("距離(m)", value=5000, step=500))
        if mode_idx == 2: calc_ave = calc_secs/(calc_dist/500) if calc_dist>0 else 0
        else: calc_ave = float(st.number_input("Ave(秒)", value=110))
    
    if st.button("プラン作成", type="primary"):
        st.session_state.update({"active_plan_flag": True, "fixed_ave_seconds": calc_ave, "fixed_distance_m": calc_dist, "fixed_total_seconds": calc_secs, "fixed_calc_mode": "time_base" if mode_idx >= 2 else "distance_base", "fixed_mode_idx": mode_idx})
        st.rerun()

# メインエリアに調整機能のみを配置
if st.session_state["active_plan_flag"]:
    base_ave, dist_total, secs_total, calc_mode = st.session_state["fixed_ave_seconds"], st.session_state["fixed_distance_m"], st.session_state["fixed_total_seconds"], st.session_state["fixed_calc_mode"]
    
    # 2x2 マトリクス配置でスクロールを極限まで抑制
    for row in range(2):
        row_cols = st.columns(2)
        for col_idx in range(2):
            i = row * 2 + col_idx + 1
            if f"q{i}_offset_sec" not in st.session_state: st.session_state[f"q{i}_offset_sec"] = 0.0
            q_sec = base_ave + st.session_state[f"q{i}_offset_sec"]
            with row_cols[col_idx]:
                st.write(f"**{i}Q** {int(q_sec//60)}:{q_sec%60:02.0f}")
                b_cols = st.columns(2)
                if b_cols[0].button("➕", key=f"p_{i}"): st.session_state[f"q{i}_offset_sec"] += 0.5; st.rerun()
                if b_cols[1].button("➖", key=f"m_{i}"): st.session_state[f"q{i}_offset_sec"] -= 0.5; st.rerun()
                if calc_mode == 'distance_base':
                    this_v = q_sec * ((dist_total/4)/500)
                    st.write(f"`{int(this_v//60)}:{this_v%60:02.0f}`")
                else:
                    this_v = (secs_total/4/q_sec)*500 if q_sec > 0 else 0
                    st.write(f"`{this_v:.0f}m`")

    if st.button("リセット"):
        for i in range(1, 5): st.session_state[f"q{i}_offset_sec"] = 0.0
        st.rerun()

    # 判定結果
    p_total_secs = sum([base_ave + st.session_state.get(f"q{i}_offset_sec", 0.0) for i in range(1,5)]) * (dist_total/4/500) if calc_mode == 'distance_base' else 0
    p_total_dist = sum([(secs_total/4/(base_ave + st.session_state.get(f"q{i}_offset_sec", 0.0)))*500 for i in range(1,5)]) if calc_mode != 'distance_base' else 0
    
    if calc_mode == 'distance_base':
        diff = p_total_secs - secs_total
        st.write(f"合計: {int(p_total_secs//60)}:{p_total_secs%60:02.0f} / " + ("OK!" if abs(diff)<1 else f"{diff:.1f}s"))
    else:
        diff = p_total_dist - dist_total
        st.write(f"合計: {p_total_dist:.0f}m / " + ("OK!" if abs(diff)<1 else f"{diff:.1f}m"))
