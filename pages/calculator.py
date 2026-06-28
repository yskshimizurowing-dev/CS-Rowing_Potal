import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

st.title("🛶 エルゴ・レースプランシミュレーター")
st.write("カテゴリを選んで目標数値を入力し、レースプランを作成・シミュレーションします。")
st.markdown("---")

# 完全新規の変数名でセッション状態を初期化（古いキャッシュとの衝突を避ける）
if "final_plan_active" not in st.session_state:
    st.session_state["final_plan_active"] = False
if "final_lock_ave" not in st.session_state:
    st.session_state["final_lock_ave"] = 0.0
if "final_lock_dist" not in st.session_state:
    st.session_state["final_lock_dist"] = 0.0
if "final_lock_secs" not in st.session_state:
    st.session_state["final_lock_secs"] = 0.0
if "final_lock_time_mode" not in st.session_state:
    st.session_state["final_lock_time_mode"] = False

# 各Qの調整秒数
for i in range(1, 5):
    if f"final_q{i}_offset" not in st.session_state:
        st.session_state[f"final_q{i}_offset"] = 0.0

def hard_reset_states():
    for i in range(1, 5):
        st.session_state[f"final_q{i}_offset"] = 0.0
    st.session_state["final_plan_active"] = False

# --- ① カテゴリーの選択 ---
select_menus = [
    "距離 と 目標タイム から【全体のAverage】を出す", 
    "距離 と Average から【目標タイム】を出す",
    "合計時間 と 距離 から【全体のAverage】を出す",
    "合計時間 と Average から【目標距離】を出す（例：20分測定など）"
]

selected_category = st.selectbox(
    "① 計算したいカテゴリーを選択してください",
    select_menus,
    on_change=hard_reset_states
)
current_mode_idx = select_menus.index(selected_category)

st.markdown("### **入力エリア**")
col1, col2 = st.columns(2)

calc_out_dist = 0.0
calc_out_secs = 0.0
calc_out_ave = 0.0
is_time_fixed_mode = (current_mode_idx == 3)

# 各パターンに応じた入力
if current_mode_idx == 0:
    with col1:
        in_d = st.number_input("② 距離 (m)", value=2000, step=500, key="fixed_k_0_d", on_change=hard_reset_states)
    with col2:
        st.write("③ 全体の目標タイム")
        cm, cs = st.columns(2)
        with cm:
            in_m = st.number_input("分", min_value=0, max_value=60, value=8, step=1, key="fixed_k_0_m", on_change=hard_reset_states)
        with cs:
            in_s = st.number_input("秒", min_value=0, max_value=59, value=0, step=1, key="fixed_k_0_s", on_change=hard_reset_states)
        calc_out_dist = in_d
        calc_out_secs = (in_m * 60) + in_s
        if calc_out_dist > 0:
            calc_out_ave = calc_out_secs / (calc_out_dist / 500)
        st.info(f"④ 必要な全体のAverage: **{int(calc_out_ave // 60)}分{calc_out_ave % 60:04.1f}秒** / 500m")

elif current_mode_idx == 1:
    with col1:
        in_d = st.number_input("② 距離 (m)", value=2000, step=500, key="fixed_k_1_d", on_change=hard_reset_states)
    with col2:
        st.write("③ 全体のAverage (/500m)")
        cam, cas = st.columns(2)
        with cam:
            in_am = st.number_input("分 ", min_value=0, max_value=10, value=2, step=1, key="fixed_k_1_am", on_change=hard_reset_states)
        with cas:
            in_as = st.number_input("秒 ", min_value=0, max_value=59, value=0, step=1, key="fixed_k_1_as", on_change=hard_reset_states)
        calc_out_dist = in_d
        calc_out_ave = (in_am * 60) + in_as
        if calc_out_dist > 0:
            calc_out_secs = calc_out_ave * (calc_out_dist / 500)
        st.info(f"④ 算出された合計タイム: **{int(calc_out_secs // 60)}分{calc_out_secs % 60:04.1f}秒**")

elif current_mode_idx == 2:
    with col1:
        st.write("② 合計時間")
        ctm, cts = st.columns(2)
        with ctm:
            in_tm = st.number_input("分", min_value=0, max_value=120, value=7, step=1, key="fixed_k_2_tm", on_change=hard_reset_states)
        with cts:
            in_ts = st.number_input("秒", min_value=0, max_value=59, value=30, step=1, key="fixed_k_2_ts", on_change=hard_reset_states)
        calc_out_secs = (in_tm * 60) + in_ts
    with col1:
        in_d = st.number_input("③ 距離 (m)", value=2000, step=500, key="fixed_k_2_d", on_change=hard_reset_states)
    calc_out_dist = in_d
    if calc_out_dist > 0:
        calc_out_ave = calc_out_secs / (calc_out_dist / 500)
    with col2:
        st.info(f"④ 計算されたAverage: **{int(calc_out_ave // 60)}分{calc_out_ave % 60:04.1f}秒** / 500m")

elif current_mode_idx == 3:
    with col1:
        st.write("② 合計の測定時間")
        ctm, cts = st.columns(2)
        with ctm:
            in_tm = st.number_input("分", min_value=0, max_value=120, value=20, step=1, key="fixed_k_3_tm", on_change=hard_reset_states)
        with cts:
            in_ts = st.number_input("秒", min_value=0, max_value=59, value=0, step=1, key="fixed_k_3_ts", on_change=hard_reset_states)
        calc_out_secs = (in_tm * 60) + in_ts
    with col2:
        st.write("③ 目標のAverage (/500m)")
        cam, cas = st.columns(2)
        with cam:
            in_am = st.number_input("分  ", min_value=0, max_value=10, value=1, step=1, key="fixed_k_3_am", on_change=hard_reset_states)
        with cas:
            in_as = st.number_input("秒  ", min_value=0, max_value=59, value=50, step=1, key="fixed_k_3_as", on_change=hard_reset_states)
        calc_out_ave = (in_am * 60) + in_as
        if calc_out_ave > 0:
            calc_out_dist = (calc_out_secs / calc_out_ave) * 500
        st.info(f"④ 想定される合計の目標距離: **{calc_out_dist:.1f} m**")


# 入力値を常にセッションに仮保存
if not st.session_state["final_plan_active"]:
    st.session_state["final_lock_ave"] = calc_out_ave
    st.session_state["final_lock_dist"] = calc_out_dist
    st.session_state["final_lock_secs"] = calc_out_secs
    st.session_state["final_lock_time_mode"] = is_time_fixed_mode

st.markdown("---")

# --- ⑤ レースプランを作成 ボタン ---
if st.button("⑤ レースプランを作成", type="primary"):
    st.session_state["final_plan_active"] = True
    st.session_state["final_lock_ave"] = calc_out_ave
    st.session_state["final_lock_dist"] = calc_out_dist
    st.session_state["final_lock_secs"] = calc_out_secs
    st.session_state["final_lock_time_mode"] = is_time_fixed_mode
    st.rerun()


# --- ⑥ レースプラン作成エリア ---
if st.session_state["final_plan_active"]:
    active_ave = st.session_state["final_lock_ave"]
    active_dist = st.session_state["final_lock_dist"]
    active_secs = st.session_state["final_lock_secs"]
    active_mode = st.session_state["final_lock_time_mode"]

    if active_mode:
        q_label = f"各Qの長さ（時間固定）: {int((active_secs/4)//60)}分 {int((active_secs/4)%60)}秒"
    else:
        q_label = f"各Qの長さ（距離固定）: {active_dist/4:.0f}m"
        
    st.subheader(f"⏱️ 各Qの調整 (500m Average)")
    st.caption(f"💡 {q_label}")
    
    if st.button("このプランをリセット", type="secondary"):
        for i in range(1, 5):
            st.session_state[f"final_q{i}_offset"] = 0.0
        st.rerun()

    st.write("")
    running_q_times = []

    for i in range(1, 5):
        c_name, c_plus, c_minus, c_result = st.columns([2, 1, 1, 3])
        with c_name:
            st.markdown(f"### **{i}Q**")
        with c_plus:
            if st.button("➕", key=f"f_btn_p_{i}"):
                st.session_state[f"final_q{i}_offset"] += 0.5
                st.rerun()
        with c_minus:
            if st.button("➖", key=f"f_btn_m_{i}"):
                st.session_state[f"final_q{i}_offset"] -= 0.5
                st.rerun()
                
        final_q_sec = active_ave + st.session_state[f"final_q{i}_offset"]
        if final_q_sec < 0:
            final_q_sec = 0.0
        running_q_times.append(final_q_sec)
        
        with c_result:
            st.markdown(f"### `{int(final_q_sec // 60):02d}:{final_q_sec % 60:04.1f}`")

    st.markdown("---")

    # 結果表示
    if not active_mode:
        total_p_secs = sum(running_q_times)
        diff_secs = total_p_secs - active_secs

        st.write(f"現在のプラン合計タイム: **{int(total_p_secs // 60)}分{total_p_secs % 60:04.1f}秒**")

        if abs(diff_secs) < 0.01:
            st.success("🎉 **目標タイムとピッタリ一致しています！完璧なレースプランです。**")
        elif diff_secs > 0:
            st.error(f"⚠️ **目標より {diff_secs:.1f} 秒遅いです。** あと {diff_secs:.1f} 秒縮めてください。")
        else:
            st.info(f"💡 **目標より {abs(diff_secs):.1f} 秒速いです。** あと {abs(diff_secs):.1f} 秒余裕があります。")
            
    else:
        q_time_slice = active_secs / 4
        calculated_total_dist = 0.0
        for q_s_val in running_q_times:
            if q_s_val > 0:
                calculated_total_dist += (q_time_slice / q_s_val) * 500
                
        diff_m = calculated_total_dist - active_dist
        st.write(f"現在のプラン合計距離: **{calculated_total_dist:.1f} m** （目標距離: {active_dist:.1f} m）")

        if abs(diff_m) < 0.5:
            st.success("🎉 **目標距離とピッタリ一致しています！完璧なペース配分です。**")
        elif diff_m > 0:
            st.success(f"🚀 **目標より {abs(diff_m):.1f} m 多く漕げます！ （ナイスプラン）**")
        else:
            st.error(f"⚠️ **目標より {abs(diff_m):.1f} m 不足しています。** あと少しペースを上げてください。")
