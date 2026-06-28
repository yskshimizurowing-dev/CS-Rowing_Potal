import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

st.title("🛶 エルゴ・レースプランシミュレーター")
st.write("カテゴリを選んで目標数値を入力し、レースプランを作成・シミュレーションします。")
st.markdown("---")

# --- 値の変更を検知して状態をリセットする関数 ---
def reset_all_states():
    # 入力条件が変わったら、Qの調整秒数と「ボタン押下フラグ」をリセットする
    for i in range(1, 5):
        st.session_state[f"calc_q{i}_diff"] = 0.0
    st.session_state["plan_generated"] = False

# セッション状態の初期化
if "plan_generated" not in st.session_state:
    st.session_state["plan_generated"] = False
for i in range(1, 5):
    if f"calc_q{i}_diff" not in st.session_state:
        st.session_state[f"calc_q{i}_diff"] = 0.0


# --- ① 計算したいカテゴリーを選択 ---
category = st.selectbox(
    "① 計算したいカテゴリーを選択してください",
    ["距離と目標タイムから [Average] を出す", "距離とAverageから [目標タイム] を出す"],
    on_change=reset_all_states
)

st.markdown("### **入力エリア**")
col1, col2 = st.columns(2)

# --- ② 合計タイム又は距離を入力 ---
with col1:
    distance = st.number_input("② 距離 (m)", value=2000, step=500, on_change=reset_all_states)

# 変数の初期化
target_total_seconds = 0.0
base_ave_seconds = 0.0

# --- ③ 入力分岐 ＆ ④ 自動計算表示 ---
with col2:
    if "from [Average]" in category or "[Average] を出す" in category:
        # パターンA: タイムを入力して、Averageを自動計算
        st.write("③ 全体の目標タイム")
        col_m, col_s = st.columns(2)
        with col_m:
            target_min = st.number_input("分", min_value=0, max_value=60, value=8, step=1, on_change=reset_all_states)
        with col_s:
            target_sec = st.number_input("秒", min_value=0, max_value=59, value=0, step=1, on_change=reset_all_states)
        
        target_total_seconds = (target_min * 60) + target_sec
        if distance > 0:
            base_ave_seconds = target_total_seconds / (distance / 500)
        
        # ④ 計算結果の表示
        ave_m = int(base_ave_seconds // 60)
        ave_s = base_ave_seconds % 60
        st.info(f"④ 必要な全体のAverage: **{ave_m}分{ave_s:04.1f}秒** / 500m")

    else:
        # パターンB: Averageを入力して、タイムを自動計算
        st.write("③ 全体のAverage (/500m)")
        col_am, col_as = st.columns(2)
        with col_am:
            ave_min = st.number_input("分 ", min_value=0, max_value=10, value=2, step=1, on_change=reset_all_states)
        with col_as:
            ave_sec = st.number_input("秒 ", min_value=0, max_value=59, value=0, step=1, on_change=reset_all_states)
        
        base_ave_seconds = (ave_min * 60) + ave_sec
        if distance > 0:
            target_total_seconds = base_ave_seconds * (distance / 500)
        
        # ④ 計算結果の表示
        total_m = int(target_total_seconds // 60)
        total_s = target_total_seconds % 60
        st.info(f"④ 算出された合計タイム: **{total_m}分{total_s:04.1f}秒**")

st.markdown("---")


# --- ⑤ レースプランを作成 ボタン ---
if st.button("⑤ レースプランを作成", type="primary"):
    st.session_state["plan_generated"] = True

# ボタンが押された、またはすでに調整中の場合のみQごとの表示を行う
if st.session_state["plan_generated"]:
    st.subheader("⏱️ 各Qの調整 (500m Average)")
    
    # 個別リセットボタン
    if st.button("このプランをリセット", type="secondary"):
        for i in range(1, 5):
            st.session_state[f"calc_q{i}_diff"] = 0.0
        st.rerun()

    st.write("")
    q_times = []

    # 各Qの調整ボタンとタイム表示
    for i in range(1, 5):
        c_name, c_plus, c_minus, c_result = st.columns([2, 1, 1, 3])
        
        with c_name:
            st.markdown(f"### **{i}Q**")
            
        with c_plus:
            if st.button("➕", key=f"calc_btn_p_{i}"):
                st.session_state[f"calc_q{i}_diff"] += 0.5
                st.rerun()
                
        with c_minus:
            if st.button("➖", key=f"calc_btn_m_{i}"):
                st.session_state[f"calc_q{i}_diff"] -= 0.5
                st.rerun()
                
        q_seconds = base_ave_seconds + st.session_state[f"calc_q{i}_diff"]
        if q_seconds < 0:
            q_seconds = 0.0
        q_times.append(q_seconds)
        
        with c_result:
            q_m = int(q_seconds // 60)
            q_s = q_seconds % 60
            st.markdown(f"### `{q_m:02d}:{q_s:04.1f}`")

    st.markdown("---")

    # ⑥ 合計タイムの過不足判定アラート
    plan_total_seconds = sum(q_times)
    diff = plan_total_seconds - target_total_seconds

    p_total_m = int(plan_total_seconds // 60)
    p_total_s = plan_total_seconds % 60

    st.write(f"現在のプラン合計タイム: **{p_total_m}分{p_total_s:04.1f}秒**")

    if abs(diff) < 0.01:
        st.success("🎉 **目標タイムとピッタリ一致しています！完璧なレースプランです。**")
    elif diff > 0:
        st.error(f"⚠️ **目標より {diff:.1f} 秒遅いです。** あと {diff:.1f} 秒縮めてください。")
    else:
        st.info(f"💡 **目標より {abs(diff):.1f} 秒速いです。** あと {abs(diff):.1f} 秒余裕があります。")
