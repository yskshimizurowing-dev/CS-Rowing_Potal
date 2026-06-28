import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

# スマホ表示を考慮したスタイル設定
st.markdown("""
<style>
    .stButton>button { width: 100%; height: 3em; }
    [data-testid="column"] { min-width: 100px; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🛶 エルゴ・<br>レースプランシミュレーター", unsafe_allow_html=True)
st.markdown("---")

# 初期化・メニュー選択（以前と共通のため略）
if "active_plan_flag" not in st.session_state: st.session_state["active_plan_flag"] = False

# 入力部分：スマホで崩れないよう、ラベルと入力欄を一体化
def distance_input(label, key):
    st.write(f"② {label}")
    st.caption("メートル")
    return float(st.number_input("距離", value=2000, step=500, key=key, label_visibility="collapsed"))

def time_input(label, key_m, key_s):
    st.write(f"③ {label}")
    c1, c2 = st.columns(2)
    with c1:
        st.caption("分")
        m = st.number_input("分", value=8, step=1, key=key_m, label_visibility="collapsed")
    with c2:
        st.caption("秒")
        s = st.number_input("秒", value=0, step=1, key=key_s, label_visibility="collapsed")
    return float(m * 60 + s)

# （メニュー分岐ロジックは以前のものを流用）

# --- レースプラン調整 ---
if st.session_state["active_plan_flag"]:
    # （中略：変数は以前のものを流用）
    st.subheader("⏱️ 各Qの調整")
    
    for i in range(1, 5):
        st.markdown("---")
        st.write(f"**{i}Q**")
        q_sec = base_ave + st.session_state.get(f"q{i}_offset_sec", 0.0)
        
        # スマホでも押しやすいようボタンを大きく配置
        b_col1, b_col2 = st.columns(2)
        if b_col1.button("➕ 0.5秒", key=f"p_{i}"): 
            st.session_state[f"q{i}_offset_sec"] = st.session_state.get(f"q{i}_offset_sec", 0.0) + 0.5
            st.rerun()
        if b_col2.button("➖ 0.5秒", key=f"m_{i}"): 
            st.session_state[f"q{i}_offset_sec"] = st.session_state.get(f"q{i}_offset_sec", 0.0) - 0.5
            st.rerun()
            
        # 結果は分かりやすく大きな文字で
        if calc_mode == 'distance_base':
            ts = q_sec * ((dist_total / 4) / 500)
            st.write(f"設定Ave: **{int(q_sec//60)}:{q_sec%60:04.1f}** | タイム: **{int(ts//60)}:{ts%60:04.1f}**")
        else:
            td = (secs_total / 4 / q_sec) * 500 if q_sec > 0 else 0
            st.write(f"設定Ave: **{int(q_sec//60)}:{q_sec%60:04.1f}** | 距離: **{td:.1f}m**")
