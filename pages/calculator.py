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
        
        total_m = int(target_total_seconds // 60)
        total_s = target_total_seconds % 60
        st.info(f"④ 算出された合計タイム: **{total_m}分{total_s:04.1f}秒**")

elif category == "合計時間 と 距離 から【全体のAverage】を出す":
    with col1:
        st.write("② 合計時間")
        col_tm, col_ts = st.columns(2)
        with col_tm:
            target_min = st.number_input("分", min_value=0, max_value=120, value=7, step=1, on_change=reset_all_states)
        with col_ts:
            target_sec = st.number_input("秒", min_value=0, max_value=59, value=30, step=1, on_change=reset_all_states)
        target_total_seconds = (target_min * 60) + target_sec
    with col2:
        distance = st.number_input("③ 距離 (m)", value=2000, step=500, on_change=reset_all_states)
        
        if distance > 0:
            base_ave_seconds = target_total_seconds / (distance / 500)
        
        ave_m = int(base_ave_seconds // 60)
        ave_s = base_ave_seconds % 60
        st.info(f"④ 計算されたAverage: **{ave_m}分{ave_s:04.1f}秒** / 500m")

elif category == "合計時間 と Average から【目標距離】を出す（例：20分測定など）":
    with col1:
        st.write("② 合計の測定時間")
        col_tm, col_ts = st.columns(2)
        with col_tm:
            target_min = st.number_input("分", min_value=0, max_value=120, value=20, step=1, on_change=reset_all_states)
        with col_ts:
            target_sec = st.number_input("秒", min_value=0, max_value=59, value=0, step=1, on_change=reset_all_states)
        target_total_seconds = (target_min * 60) + target_sec
    with col2:
        st.write("③ 目標のAverage (/500m)")
        col_am, col_as = st.columns(2)
        with col_am:
            ave_min = st.number_input("分  ", min_value=0, max_value=10, value=1, step=1, on_change=reset_all_states)
        with col_as:
            ave_sec = st.number_input("秒  ", min_value=0, max_value=59, value=50, step=1, on_change=reset_all_states)
        
        base_ave_seconds = (ave_min * 60) + ave_sec
        if base_ave_seconds > 0:
            distance = (target_total_seconds / base_ave_seconds) * 500
        
        st.info(f"④ 想定される合計の目標距離: **{distance:.1f} m**")

st.markdown("---")

# --- ⑤ レースプランを作成 ボタン ---
if st.button("⑤ レースプランを作成", type="primary"):
    st.session_state["plan_generated"] = True

if st.session_state["plan_generated"]:
    if is_time_based:
        q_info = f"各Qの長さ（時間固定）: {int((target_total_seconds/4)//60)}分 {int((target_total_seconds/4)%60)}秒"
    else:
        q_info = f"各Qの長さ（距離固定）: {distance/4:.0f}m"
        
    st.subheader(f"⏱️ 各Qの調整 (500m Average)")
    st.caption(f"💡 {q_info}")
    
    if st.button("このプランをリセット", type="secondary"):
        for i in range(1, 5):
            st.session_state[f"calc_q{i}_diff"] = 0.0
        st.rerun()

    st.write("")
    q_times = []

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

    # ==========================================
    # 最終判定エリア
    # ==========================================
    if not is_time_based:
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
            
    else:
        q_duration = target_total_seconds / 4
        plan_distance = 0.0
        for q_sec in q_times:
            if q_sec > 0:
                plan_distance += (q_duration / q_sec) * 500
                
        diff_dist = plan_distance - distance
        st.write(f"現在のプラン合計距離: **{plan_distance:.1f} m** （目標: {distance:.1f} m）")

        if abs(diff_dist) < 0.5:
            st.success("🎉 **目標距離とピッタリ一致しています！完璧なペース配分です。**")
        elif diff_dist > 0:
            st.success(f"🚀 **目標より {abs(diff_dist):.1f} m 多く漕げます！ （ナイスプラン）**")
        else:
            st.error(f"⚠️ **目標より {abs(diff_dist):.1f} m 不足しています。** あと少しペースを上げてください。")
