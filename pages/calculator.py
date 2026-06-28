import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

st.title("🛶 エルゴ・レースプランシミュレーター")
st.write("カテゴリを選んで目標数値を入力し、レースプランを作成・シミュレーションします。")
st.markdown("---")

# --- 値の変更を検知して状態をリセットする関数 ---
def reset_all_states():
    for i in range(1, 5):
        st.session_state[f"calc_q{i}_diff"] = 0.0
    st.session_state["plan_generated"] = False

if "plan_generated" not in st.session_state:
    st.session_state["plan_generated"] = False
for i in range(1, 5):
    if f"calc_q{i}_diff" not in st.session_state:
        st.session_state[f"calc_q{i}_diff"] = 0.0

# --- ① 計算したいカテゴリーを選択（4つのパターン） ---
category = st.selectbox(
    "① 計算したいカテゴリーを選択してください",
    [
        "距離 と 目標タイム から【全体のAverage】を出す", 
        "距離 と Average から【目標タイム】を出す",
        "合計時間 と 距離 から【全体のAverage】を出す",
        "合計時間 と Average から【目標距離】を出す（例：20分測定など）"
    ],
    on_change=reset_all_states
)

st.markdown("### **入力エリア**")
col1, col2 = st.columns(2)

# 変数の初期化
distance = 0.0
target_total_seconds = 0.0
base_ave_seconds = 0.0
is_time_based = "合計時間 と Average" in category  # 20分測定などの時間固定フラグ

# --- 各カテゴリーに応じた入力・計算処理 ---
if category == "距離 と 目標タイム から【全体のAverage】を出す":
    with col1:
        distance = st.number_input("② 距離 (m)", value=2000, step=500, on_change=reset_all_states)
    with col2:
        st.write("③ 全体の目標タイム")
        col_m, col_s = st.columns(2)
        with col_m:
            target_min = st.number_input("分", min_value=0, max_value=60, value=8, step=1, on_change=reset_all_states)
        with col_s:
            target_sec = st.number_input("秒", min_value=0, max_value=59, value=0, step=1, on_change=reset_all_states)
        
        target_total_seconds = (target_min * 60) + target_sec
        if distance > 0:
            base_ave_seconds = target_total_seconds / (distance / 500)
        
        ave_m = int(base_ave_seconds // 60)
        ave_s = base_ave_seconds % 60
        st.info(f"④ 必要な全体のAverage: **{ave_m}分{ave_s:04.1f}秒** / 500m")

elif category == "距離 と Average から【目標タイム】を出す":
    with col1:
        distance = st.number_input("② 距離 (m)", value=2000, step=500, on_change=reset_all_states)
    with col2:
        st.write("③ 全体のAverage (/500m)")
        col_am, col_as = st.columns(2)
        with col_am:
            ave_min = st.number_input("分 ", min_value=0, max_value=10, value=2, step=1, on_change=reset_all_states)
        with col_as:
            ave_sec = st.number_input("秒 ", min_value=0, max_value=59, value=0, step=1, on_change=reset_all_states)
        
        base_ave_seconds = (ave_min * 60) + ave_sec
        if distance > 0:
            target_total_seconds = base_ave_seconds * (distance / 500)
        
        total_m = int(target_total_
