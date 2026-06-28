import streamlit as st

# (中略：ヘッダー・メニュー選択・セッション状態初期化部分は同じです)

# 左右50:50の枠を作成
main_col1, main_col2 = st.columns([1, 1])

# --- 各メニューの入力レイアウト（距離はmのみ、すべて高さ揃え） ---

if mode_idx == 0:
    current_type = "distance_base"
    with main_col1:
        st.write("② 距離 (m)")
        # 距離マスの右に「m」を置いて高さを揃える
        d_cols = st.columns([4, 1])
        v_dist = d_cols[0].number_input("距離", min_value=0, value=2000, step=500, key="m0_d", label_visibility="collapsed")
        d_cols[1].write("m")
        calc_dist = float(v_dist)
    with main_col2:
        st.write("③ 目標タイム")
        t_cols = st.columns(2)
        v_m = t_cols[0].number_input("分", min_value=0, max_value=60, value=8, step=1, key="m0_m")
        v_s = t_cols[1].number_input("秒", min_value=0, max_value=59, value=0, step=1, key="m0_s")
        calc_secs = float((v_m * 60) + v_s)
    if calc_dist > 0: calc_ave = calc_secs / (calc_dist / 500)
    st.info(f"④ 計算Average: **{int(calc_ave // 60)}分{calc_ave % 60:04.1f}秒** / 500m")

elif mode_idx == 1:
    current_type = "distance_base"
    with main_col1:
        st.write("② 距離 (m)")
        d_cols = st.columns([4, 1])
        v_dist = d_cols[0].number_input("距離", min_value=0, value=2000, step=500, key="m1_d", label_visibility="collapsed")
        d_cols[1].write("m")
        calc_dist = float(v_dist)
    with main_col2:
        st.write("③ 全体のAverage")
        a_cols = st.columns(2)
        v_am = a_cols[0].number_input("分", min_value=0, max_value=10, value=2, step=1, key="m1_am")
        v_as = a_cols[1].number_input("秒", min_value=0, max_value=59, value=0, step=1, key="m1_as")
        calc_ave = float((v_am * 60) + v_as)
    if calc_dist > 0: calc_secs = calc_ave * (calc_dist / 500)
    st.info(f"④ 合計タイム: **{int(calc_secs // 60)}分{calc_secs % 60:04.1f}秒**")

elif mode_idx == 2:
    current_type = "time_base"
    with main_col1:
        st.write("② 合計時間")
        t_cols = st.columns(2)
        v_tm = t_cols[0].number_input("分", min_value=0, max_value=120, value=20, step=1, key="m2_tm")
        v_ts = t_cols[1].number_input("秒", min_value=0, max_value=59, value=0, step=1, key="m2_ts")
        calc_secs = float((v_tm * 60) + v_ts)
    with main_col2:
        st.write("③ 距離 (m)")
        d_cols = st.columns([4, 1])
        v_dist = d_cols[0].number_input("距離", min_value=0, value=5000, step=500, key="m2_d", label_visibility="collapsed")
        d_cols[1].write("m")
        calc_dist = float(v_dist)
    if calc_dist > 0: calc_ave = calc_secs / (calc_dist / 500)
    st.info(f"④ 計算Average: **{int(calc_ave // 60)}分{calc_ave % 60:04.1f}秒** / 500m")

elif mode_idx == 3:
    current_type = "time_base"
    with main_col1:
        st.write("② 測定時間")
        t_cols = st.columns(2)
        v_tm = t_cols[0].number_input("分", min_value=0, max_value=120, value=20, step=1, key="m3_tm")
        v_ts = t_cols[1].number_input("秒", min_value=0, max_value=59, value=0, step=1, key="m3_ts")
        calc_secs = float((v_tm * 60) + v_ts)
    with main_col2:
        st.write("③ 目標Average")
        a_cols = st.columns(2)
        v_am = a_cols[0].number_input("分", min_value=0, max_value=10, value=1, step=1, key="m3_am")
        v_as = a_cols[1].number_input("秒", min_value=0, max_value=59, value=50, step=1, key="m3_as")
        calc_ave = float((v_am * 60) + v_as)
    if calc_ave > 0: calc_dist = (calc_secs / calc_ave) * 500
    st.info(f"④ 想定目標距離: **{calc_dist:.1f} m**")

# (以降はプラン作成ロジック等の共通コードを接続してください)

# --- ⑤ レースプランを作成 ボタン ---
if f"q1_offset_sec" not in st.session_state:
    for i in range(1, 5):
        st.session_state[f"q{i}_offset_sec"] = 0.0

if not st.session_state["active_plan_flag"]:
    st.session_state["fixed_ave_seconds"] = calc_ave
    st.session_state["fixed_distance_m"] = calc_dist
    st.session_state["fixed_total_seconds"] = calc_secs
    st.session_state["fixed_calc_mode"] = current_type
    st.session_state["fixed_mode_idx"] = mode_idx

st.markdown("---")

if st.button("⑤ レースプランを作成", type="primary"):
    st.session_state["active_plan_flag"] = True
    st.session_state["fixed_ave_seconds"] = calc_ave
    st.session_state["fixed_distance_m"] = calc_dist
    st.session_state["fixed_total_seconds"] = calc_secs
    st.session_state["fixed_calc_mode"] = current_type
    st.session_state["fixed_mode_idx"] = mode_idx
    st.rerun()


# --- ⑥ レースプラン作成エリア ---
if st.session_state["active_plan_flag"]:
    base_ave = st.session_state["fixed_ave_seconds"]
    dist_total = st.session_state["fixed_distance_m"]
    secs_total = st.session_state["fixed_total_seconds"]
    calc_mode = st.session_state["fixed_calc_mode"]

    st.subheader(f"⏱️ 各Qの調整 (500m Average)")
    
    if st.button("このプランをリセット", type="secondary"):
        for i in range(1, 5):
            st.session_state[f"q{i}_offset_sec"] = 0.0
        st.rerun()

    st.write("")
    
    plan_total_secs = 0.0
    plan_total_dist = 0.0

    hc1, hc2, hc3, hc4 = st.columns([1, 2, 2, 3])
    with hc1: st.caption("🔲 Q")
    with hc2: st.caption("🏃 500m Ave")
    with hc3: st.caption("➕ ➖")
    if calc_mode == "distance_base":
        with hc4: st.caption("⏱️ Qタイム")
    else:
        with hc4: st.caption("📏 Q距離")
        
    st.markdown("---")

    for i in range(1, 5):
        c_q, c_ave, c_btn, c_val = st.columns([1, 2, 2, 3])
        
        final_q_sec = base_ave + st.session_state.get(f"q{i}_offset_sec", 0.0)
        if final_q_sec < 0:
            final_q_sec = 0.0
            
        q_m = int(final_q_sec // 60)
        q_s = final_q_sec % 60

        if calc_mode == "distance_base":
            this_q_dist = dist_total / 4
            this_q_secs = final_q_sec * (this_q_dist / 500)
        else:
            this_q_secs = secs_total / 4
            if final_q_sec > 0:
                this_q_dist = (this_q_secs / final_q_sec) * 500
            else:
                this_q_dist = 0.0

        plan_total_secs += this_q_secs
        plan_total_dist += this_q_dist

        with c_q:
            st.write(f"**{i}Q**")
            
        with c_ave:
            st.write(f"**{q_m:02d}:{q_s:04.1f}**")
            
        with c_btn:
            b1, b2 = st.columns(2)
            with b1:
                if st.button("➕", key=f"p_btn_{i}"):
                    st.session_state[f"q{i}_offset_sec"] = st.session_state.get(f"q{i}_offset_sec", 0.0) + 0.5
                    st.rerun()
            with b2:
                if st.button("➖", key=f"m_btn_{i}"):
                    st.session_state[f"q{i}_offset_sec"] = st.session_state.get(f"q{i}_offset_sec", 0.0) - 0.5
                    st.rerun()
                    
        with c_val:
            if calc_mode == "distance_base":
                this_q_m = int(this_q_secs // 60)
                this_q_s = this_q_secs % 60
                st.write(f"`{this_q_m:02d}:{this_q_s:04.1f}`")
            else:
                st.write(f"`{this_q_dist:.1f} m`")

    st.markdown("---")

    # --- ⑦ 最終結果表示エリア ---
    st.markdown("### **現在の合計**")
    
    if calc_mode == "distance_base":
        p_total_m = int(plan_total_secs // 60)
        p_total_s = plan_total_secs % 60
        st.write(f"現在のプラン合計タイム: **{p_total_m}分{p_total_s:04.1f}秒** （目標タイム: {int(secs_total//60)}分{secs_total%60:04.1f}秒）")
        
        diff_secs = plan_total_secs - secs_total
        if abs(diff_secs) < 0.01:
            st.success("🎉 **目標タイムとピッタリ一致しています！完璧なレースプランです。**")
        elif diff_secs > 0:
            st.error(f"⚠️ **目標より {diff_secs:.1f} 秒遅いです。** あと {diff_secs:.1f} 秒縮めてください。")
        else:
            st.info(f"💡 **目標より {abs(diff_secs):.1f} 秒速いです。** あと {abs(diff_secs):.1f} 秒余裕があります。")
    else:
        st.write(f"現在のプラン合計距離: **{plan_total_dist:.1f} m** （目標距離: {dist_total:.1f} m）")
        
        diff_m = plan_total_dist - dist_total
        if abs(diff_m) < 0.5:
            st.success("🎉 **目標距離とピッタリ一致しています！完璧なペース配分です。**")
        elif diff_m > 0:
            st.success(f"🚀 **目標より {abs(diff_m):.1f} m 多く漕げます！ （ナイスプラン）**")
        else:
            st.error(f"⚠️ **目標より {abs(diff_m):.1f} m 不足しています。** あと少しペースを上げてください。")
