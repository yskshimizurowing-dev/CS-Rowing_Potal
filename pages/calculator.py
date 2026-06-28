import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered", initial_sidebar_state="collapsed")

# スマホ特化: 調整エリアを2x2のマトリクスにするためのCSS
st.markdown("""
<style>
    .stButton>button { width: 100%; height: 35px; font-size: 11px; padding: 0px; }
    [data-testid="column"] { padding: 0px 1px; }
    div[data-testid="stMarkdownContainer"] { font-size: 11px; }
</style>
""", unsafe_allow_html=True)

# タイトルを極小化
st.markdown("##### 🛶 レースプランナー")

if "active_plan_flag" not in st.session_state: st.session_state["active_plan_flag"] = False

# (入力ロジック部分は省略せず前回と同じものをそのまま使用してください)

if st.session_state["active_plan_flag"]:
    # 2x2の配置にするために、1Q,2Qを上段、3Q,4Qを下段に配置
    for row in range(2):
        cols = st.columns(2)
        for col_idx in range(2):
            i = row * 2 + col_idx + 1
            with cols[col_idx]:
                q_sec = base_ave + st.session_state.get(f"q{i}_offset_sec", 0.0)
                st.write(f"**{i}Q**:{int(q_sec//60)}:{q_sec%60:02.0f}")
                b_cols = st.columns(2)
                if b_cols[0].button("➕", key=f"p_{i}"): st.session_state[f"q{i}_offset_sec"] += 0.5; st.rerun()
                if b_cols[1].button("➖", key=f"m_{i}"): st.session_state[f"q{i}_offset_sec"] -= 0.5; st.rerun()
