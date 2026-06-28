import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

st.title("🛶 エルゴ・レースプランシミュレーター")
st.write("カテゴリを選んで目標数値を入力し、レースプランを作成・シミュレーションします。")
st.markdown("---")

# --- セッション状態の初期化（変数名を完全に一新） ---
if "active_plan_flag" not in st.session_state:
    st.session_state["active_plan_flag"] = False
if "fixed_ave_seconds" not in st.session_state:
    st.session_state["fixed_ave_seconds"] = 0.0
if "fixed_distance_m" not in st.session_state:
    st.session_state["fixed_distance_m"] = 0.0
if "fixed_total_seconds" not in st.session_state:
    st.session_state["fixed_total_seconds"] = 0.0
if "fixed_calc_mode" not in st.session_state:
    st.session_state["fixed_calc_mode"] = "distance_base"

# 1Q〜4Qのオフセット値
for i in range(1, 5):
    if f"q{i}_offset_sec" not in st.session_state:
        st.session_state[f"q{i}_offset_sec"] = 0.0

# 条件変更時のリセット関数
def clear_plan_states():
    for i in range(1, 5):
        st.session_state[f"q{i}_offset_sec"] = 0.0
    st.session_state["active_plan_flag"] = False


# --- ① カテゴリーの選択 ---
menus = [
    "距離 と 目標タイム から【全体のAverage】を出す", 
    "距離 と Average から【目標タイム】を出す",
    "合計時間 と 距離 から【全体のAverage】を出す",
    "合計時間 と Average から【目標距離】を出す（例：20分測定など）"
]

selected_menu = st.selectbox(
    "① 計算したいカテゴリーを選択してください",
    menus,
    on_change=clear_plan_states
)
mode_idx = menus.index(selected_menu)

st.markdown("### **入力エリア**")
col1, col2 = st.columns(2)

# スクリプト実行ごとの一時計算用変数
tmp_dist = 0.0
tmp_secs = 0.0
tmp_ave = 0.0

# ★ここがバグの原因でした。各モードの計算ロジックと、最終判定の「タイプ」を完全に整理しました。
if mode_idx == 0:
    # 距離ベース（目標タイムに向かって4等分したタイムの過不足を競う）
    current_type = "distance_base"
    with col1:
        v_dist = st.number_input("② 距離 (m)", value=2000, step=500, key="m0_d", on_change=clear_plan_states)
    with col2:
        st.write("③ 全体の目標タイム")
        cm, cs = st.columns(2)
        with cm:
            v_m = st.number_input("分", min_value=0, max_value=60, value=8, step=1, key="m0_m", on_change=clear_plan_states)
        with cs:
            v_s = st.number_input("秒", min_value=0, max_value=59, value=0, step=1, key="m0_s", on_change=clear_plan_states)
        tmp_dist = v_dist
        tmp_secs = (v_m * 60) + v_s
        if tmp_dist > 0:
            tmp_ave = tmp_secs / (tmp_dist / 500)
        st.info(f"④ 必要な全体のAverage: **{int(tmp_ave // 60)}分{tmp_ave % 60:04.1f}秒** / 500m")

elif mode_idx == 1:
    # 距離ベース（目標タイムに向かって4等分したタイムの過不足を競う）
    current_type = "distance_base"
    with col1:
        v_dist = st.number_input("② 距離 (m)", value=2000, step=500, key="m1_d", on_change=clear_plan_states)
    with col2:
        st.write("③ 全体のAverage (/500m)")
        cam, cas = st.columns(2)
        with cam:
            v_am = st.number_input("分 ", min_value=0, max_value=10, value=2, step=1, key="m1_am", on_change=clear_plan_states)
        with cas:
            v_as = st.number_input("秒 ", min_value=0, max_value=59, value=0, step=1, key="m1_as", on_change=clear_plan_states)
        tmp_dist = v_dist
        tmp_ave = (v_am * 60) + v_as
        if tmp_dist > 0:
            tmp_secs = tmp_ave * (tmp_dist / 500)
        st.info(f"④ 算出された合計タイム: **{int(tmp_secs // 60)}分{tmp_secs % 60:04.1f}秒**")

elif mode_idx == 2:
    # 距離ベース（合計時間から全体のタイムが固定されるため、これも4等分したタイムの過不足を競うタイプ）
    current_type = "distance_base"
    with col1:
        st.write("② 合計時間")
        ctm, cts = st.columns(2)
        with ctm:
            v_tm = st.number_input("分", min_value=0, max_value=120, value=7, step=1, key="m2_tm", on_change=clear_plan_states)
        with cts:
            v_ts = st.number_input("秒", min_value=0, max_value=59, value=30, step=1, key="m2_ts", on_change=clear_plan_states)
        tmp_secs = (v_tm * 60) + v_ts
    with col1:
        v_dist = st.number_input("③ 距離 (m)", value=2000, step=500, key="m2_d", on_change=clear_plan_states)
    tmp_dist = v_dist
    if tmp_dist > 0:
        tmp_ave = tmp_secs / (tmp_dist / 500)
    with col2:
        st.info(f"④ 計算されたAverage: **{int(tmp_ave // 60)}分{tmp_ave % 60:04.1f}秒** / 500m")

elif mode_idx == 3:
    # 時間ベース（20分測定など：時間が固定され、各QのAve変化によって「最終的な総距離」の過不足を競う）
    current_type = "time_base"
    with col1:
        st.write("② 合計の測定時間")
        ctm, cts = st.columns(2)
        with ctm:
            v_tm = st.number_input("分", min_value=0, max_value=120, value=20, step=1, key="m3_tm", on_change=clear_plan_states)
        with cts:
            v_ts = st.number_input("秒", min_value=0, max_value=59, value=0, step=1, key="m3_ts", on_change=clear_plan_states)
        tmp_secs = (v_tm * 60) + v_ts
    with col2:
        st.write("③ 目標のAverage (/500m)")
        cam, cas = st.columns(2)
        with cam:
            v_am = st.number_input("分  ", min_value=0, max_value=10, value=1, step=1, key="m3_am", on_change=clear_plan_states)
        with cas:
            v_as = st.number_input("秒  ", min_value=0, max_value=59, value=50, step=1, key="m3_as", on_change=clear_plan_states)
        tmp_ave = (v_am * 60) + v_as
        if tmp_ave > 0:
            tmp_dist = (tmp_secs / tmp_ave) * 500
        st.info(f"④ 想定される合計の目標距離: **{tmp_dist:.1f} m**")


# ボタンを押す前は、入力値を常にセッション状態に最新同期し続ける
if not st.session_state["active_plan_flag"]:
    st.session_state["fixed_ave_seconds"] = tmp_ave
    st.session_state["fixed_distance_m"] = tmp_dist
    st.session_state["fixed_total_seconds"] = tmp_secs
    st.session_state["fixed_calc_mode"] = current_type

st.markdown("---")

# --- ⑤ レースプランを作成 ボタン ---
if st.button("⑤ レースプランを作成", type="primary"):
    st.session_state["active_plan_flag"] = True
    st.session_state["fixed_ave_seconds"] = tmp_ave
    st.session_state["fixed_distance_m"] = tmp_dist
    st.session_state["fixed_total_seconds"] = tmp_secs
    st.session_state["fixed_calc_mode"] = current_type
    st.rerun()


# --- ⑥ レースプラン作成エリア ---
if st.session_state["active_plan_flag"]:
    # 完全にロックされた状態の数値を安全に使用
    base_ave = st.session_state["fixed_ave_seconds"]
    dist_total = st.session_state["fixed_distance_m"]
    secs_total = st.session_state["fixed_total_seconds"]
    calc_mode = st.session_state["fixed_calc_mode"]

    if calc_mode == "time_base":
        q_label = f"各Qの長さ（時間固定）: {int((secs_total/4)//60)}分 {int((secs_total/4)%60)}秒"
    else:
        q_label = f"各Qの長さ（距離固定）: {dist_total/4:.0f}m"
        
    st.subheader(f"⏱️ 各Qの調整 (500m Average)")
    st.caption(f"💡 {q_label}")
    
    if st.button("このプランをリセット", type="secondary"):
        for i in range(1, 5):
            st.session_state[f"q{i}_offset_sec"] = 0.0
        st.rerun()

    st.write("")
    running_q_times = []

    # 1Q〜4Qの増減ボタン
    for i in range(1, 5):
        c_name, c_plus, c_minus, c_result = st.columns([2, 1, 1, 3])
        with c_name:
            st.markdown(f"### **{i}Q**")
        with c_plus:
            if st.button("➕", key=f"p_btn_{i}"):
                st.session_state[f"q{i}_offset_sec"] += 0.5
                st.rerun()
        with c_minus:
            if st.button("➖", key=f"m_btn_{i}"):
                st.session_state[f"q{i}_offset_sec"] -= 0.5
                st.rerun()
                
        final_q_sec = base_ave + st.session_state[f"q{i}_offset_sec"]
        if final_q_sec < 0:
            final_q_sec = 0.0
        running_q_times.append(final_q_sec)
        
        with c_result:
            st.markdown(f"### `{int(final_q_sec // 60):02d}:{final_q_sec % 60:04.1f}`")

    st.markdown("---")

    # --- 最終結果表示エリア（★ここが完全に分離して正しく動作します） ---
    if calc_mode == "distance_base":
        # 距離固定系（メニュー0, 1, 2番）
        total_p_secs = sum(running_q_times)
        diff_secs = total_p_secs - secs_total
        p_total_m = int(total_p_secs // 60)
        p_total_s = total_p_secs % 60

        st.write(f"現在のプラン合計タイム: **{p_total_m}分{p_total_s:04.1f}秒**")

        if abs(diff_secs) < 0.01:
            st.success("🎉 **目標タイムとピッタリ一致しています！完璧なレースプランです。**")
        elif diff_secs > 0:
            st.error(f"⚠️ **目標より {diff_secs:.1f} 秒遅いです。** あと {diff_secs:.1f} 秒縮めてください。")
        else:
            st.info(f"💡 **目標より {abs(diff_secs):.1f} 秒速いです。** あと {abs(diff_secs):.1f} 秒余裕があります。")
            
    else:
        # 時間固定系（メニュー3番：20分測定など）
        q_time_slice = secs_total / 4
        calculated_total_dist = 0.0
        for q_s_val in running_q_times:
            if q_s_val > 0:
                calculated_total_dist += (q_time_slice / q_s_val) * 500
                
        diff_m = calculated_total_dist - dist_total
        st.write(f"現在のプラン合計距離: **{calculated_total_dist:.1f} m** （目標距離: {dist_total:.1f} m）")

        if abs(diff_m) < 0.5:
            st.success("🎉 **目標距離とピッタリ一致しています！完璧なペース配分です。**")
        elif diff_m > 0:
            st.success(f"🚀 **目標より {abs(diff_m):.1f} m 多く漕げます！ （ナイスプラン）**")
        else:
            st.error(f"⚠️ **目標より {abs(diff_m):.1f} m 不足しています。** あと少しペースを上げてください。")
