import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

# スマホ向け：ボタンの大きさとカラムの折り返しをCSSで調整
st.markdown("""
<style>
    .stButton>button { width: 100%; height: 3em; font-size: 14px; }
    .q-container { background: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🛶 エルゴ・<br>レースプランシミュレーター", unsafe_allow_html=True)
st.markdown("---")

# --- 初期化・メニュー ---
if "active_plan_flag" not in st.session_state: st.session_state["active_plan_flag"] = False
def clear_plan_states():
    for i in range(1, 5): st.session_state[f"q{i}_offset_sec"] = 0.0
    st.session_state["active_plan_flag"] = False

menus = ["距離 と 目標タイム", "距離 と Average", "合計時間 と 距離", "合計時間 と Average"]
selected_menu = st.selectbox("① カテゴリー選択", menus, index=st.session_state.get("fixed_mode_idx", 0) if st.session_state["active_plan_flag"] else 0, on_change=clear_plan_states)
mode_idx = menus.index(selected_menu)

# --- 入力ロジック (省略: 以前の通り) ---
# (中略: 入力ロジックは前回までのものをお使いください)

if st.button("⑤ レースプランを作成", type="primary"):
    # (セッション更新)
    st.rerun()

# --- レースプラン調整 (リスト形式UI) ---
if st.session_state["active_plan_flag"]:
    base_ave, dist_total, secs_total, calc_mode = st.session_state["fixed_ave_seconds"], st.session_state["fixed_distance_m"], st.session_state["fixed_total_seconds"], st.session_state["fixed_calc_mode"]
    
    st.subheader("⏱️ 各Qの調整")
    if st.button("リセット"):
        for i in range(1, 5): st.session_state[f"q{i}_offset_sec"] = 0.0
        st.rerun()

    p_total_secs, p_total_dist = 0.0, 0.0
    for i in range(1, 5):
        if f"q{i}_offset_sec" not in st.session_state: st.session_state[f"q{i}_offset_sec"] = 0.0
        q_sec = base_ave + st.session_state[f"q{i}_offset_sec"]
        
        # リスト形式で表示（カラムに頼らない）
        with st.container():
            st.markdown(f"**{i}Q** | Ave: `{int(q_sec//60)}:{q_sec%60:02.1f}`")
            if calc_mode == 'distance_base':
                this_v = q_sec * ((dist_total / 4) / 500); p_total_secs += this_v
                st.write(f"➔ タイム: `{int(this_v//60)}:{this_v%60:02.1f}`")
            else:
                this_v = (secs_total / 4 / q_sec) * 500 if q_sec > 0 else 0; p_total_dist += this_v
                st.write(f"➔ 距離: `{this_v:.1f} m`")
            
            # ボタンは上下に並べて押しやすさを確保
            b1, b2 = st.columns(2)
            if b1.button("➕ 0.5s", key=f"p_{i}"): st.session_state[f"q{i}_offset_sec"] += 0.5; st.rerun()
            if b2.button("➖ 0.5s", key=f"m_{i}"): st.session_state[f"q{i}_offset_sec"] -= 0.5; st.rerun()
            st.write("---")
