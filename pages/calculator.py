import streamlit as st

st.set_page_config(page_title="Race Planner", layout="centered")

st.title("🛶 Ergo Race Plan Simulator")
st.write("Select category, input values, and generate your race plan.")
st.markdown("---")

def reset_all_states():
    for i in range(1, 5):
        st.session_state[f"calc_q{i}_diff"] = 0.0
    st.session_state["plan_generated"] = False

if "plan_generated" not in st.session_state:
    st.session_state["plan_generated"] = False
for i in range(1, 5):
    if f"calc_q{i}_diff" not in st.session_state:
        st.session_state[f"calc_q{i}_diff"] = 0.0

# --- ① 計算したいカテゴリーを選択（時間固定パターンを追加） ---
category = st.selectbox(
    "1. Select Category",
    [
        "Distance & Target Time -> Calculate Average", 
        "Distance & Average -> Calculate Target Time",
        "Total Time & Average -> Calculate Target Distance (e.g., 20min Test)"
    ],
    on_change=reset_all_states
)

st.markdown("### **Input Area**")
col1, col2 = st.columns(2)

# 変数の初期化
distance = 0.0
target_total_seconds = 0.0
base_ave_seconds = 0.0
is_time_based = "Total Time" in category  # 時間固定メニューかどうかのフラグ

if not is_time_based:
    # ==========================================
    # 従来の「距離ベース」の入力処理
    # ==========================================
    with col1:
        distance = st.number_input("2. Distance (m)", value=2000, step=500, on_change=reset_all_states)

    with col2:
        if "Target Time" in category:
            st.write("3. Target Total Time")
            col_m, col_s = st.columns(2)
            with col_m:
                target_min = st.number_input("Min", min_value=0, max_value=60, value=8, step=1, on_change=reset_all_states)
            with col_s:
                target_sec = st.number_input("Sec", min_value=0, max_value=59, value=0, step=1, on_change=reset_all_states)
            
            target_total_seconds = (target_min * 60) + target_sec
            if distance > 0:
                base_ave_seconds = target_total_seconds / (distance / 500)
            
            ave_m = int(base_ave_seconds // 60)
            ave_s = base_ave_seconds % 60
            st.info(f"4. Required Average: **{ave_m}m {ave_s:04.1f}s** / 500m")

        else:
            st.write("3. Overall Average (/500m)")
            col_am, col_as = st.columns(2)
            with col_am:
                ave_min = st.number_input("Min ", min_value=0, max_value=10, value=2, step=1, on_change=reset_all_states)
            with col_as:
                ave_sec = st.number_input("Sec ", min_value=0, max_value=59, value=0, step=1, on_change=reset_all_states)
            
            base_ave_seconds = (ave_min * 60) + ave_sec
            if distance > 0:
                target_total_seconds = base_ave_seconds * (distance / 500)
            
            total_m = int(target_total_seconds // 60)
            total_s = target_total_seconds % 60
            st.info(f"4. Calculated Total Time: **{total_m}m {total_s:04.1f}s**")

else:
    # ==========================================
    # 新設：「時間固定（20分測定など）」の入力処理
    # ==========================================
    with col1:
        st.write("2. Total Test Time")
