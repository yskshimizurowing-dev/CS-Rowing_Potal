import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

st.title("🛶 エルゴ・レースプランシミュレーター")
st.write("カテゴリを選んで目標数値を入力し、レースプランを作成・シミュレーションします。")
st.markdown("---")

# --- セッション状態の初期化 ---
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

default_index = 0
if st.session_state["active_plan_flag"]:
    if st.session_state["fixed_calc_mode"] == "time_base":
        default_index = 3
    else:
        default_index = 0

selected_menu = st.selectbox(
    "① 計算したいカテゴリーを選択してください",
    menus,
    index=default_index,
    on_change=clear_plan_states
)
mode_idx = menus.index(selected_menu)

st.markdown("### **入力エリア**")
col1, col2 = st.columns(2)

tmp_dist = 0.0
tmp_secs = 0.0
tmp_ave = 0.0

if mode_idx == 0:
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
    current_type = "distance_base"
    with col1:
        st.write("② 合計時間")
        ctm, cts = st.columns(2)
        with ctm:
            v_tm = st.number_input("分", min_value=0, max_value=120, value=20, step=1, key="m2_tm", on_change=clear_plan_states)
        with cts:
            v_ts = st.number_input("秒", min_value=0, max_value=59, value=0, step=1, key="m2_ts", on_change=clear_plan_states)
        tmp_secs = (v_tm * 60) + v_ts
    with col1:
        v_dist = st.number_input("③ 距離 (m)", value=5000, step=500, key="m2_d", on_change=clear_plan_states)
    tmp_dist = v_dist
    if tmp_dist > 0:
        tmp_ave = tmp_secs / (tmp_dist / 500)
    with col2:
        st.info(f"④ 計算されたAverage: **{int(tmp_ave // 60)}分{tmp_ave % 60:04.1f}秒** / 500m")

elif mode_idx == 3:
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


if not st.session_state["active_plan_flag"]:
    st.session_state["fixed_ave_seconds"] = tmp_ave
    st.session_state["fixed_distance_m"] = tmp_dist
    st.session_state["fixed_total_seconds"] = tmp_secs
    st.session_state["fixed_calc_mode"] = current_type

st.markdown("---")

if st.button("⑤ レースプランを作成", type="primary"):
    st.session_state["active_plan_flag"] = True
    st.session_state["fixed_ave_seconds"] = tmp_ave
    st.session_state["fixed_distance_m"] = tmp_dist
    st.session_state["fixed_total_seconds"] = tmp_secs
    st.session_state["fixed_calc_mode"] = current_type
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
    
    # 最終合計を計算するための作業用変数
    calculated_total_seconds = 0.0
    calculated_total_distance = 0.0

    # 横一列のヘッダーを表示（PCやブラウザ幅で見やすいように）
    hc1, hc2, hc3, hc4, hc5 = st.columns([1, 2, 1.5, 2.5, 2.5])
    with hc1: st.caption("🔲 Q")
    with hc2: st.caption("🏃 500m Ave")
    with hc3: st.caption("➕ ➖")
    with hc4: st.caption("⏱️ Qタイム")
    with hc5: st.caption("📏 Q距離")
    st.markdown("---")

    # 1Q〜4Qのループ処理
    for i in range(1, 5):
        c_q, c_ave, c_btn, c_time, c_dist = st.columns([1, 2, 1.5, 2.5, 2.5])
        
        # 現在のQのAverage(500m)の秒数を算出
        final_q_sec = base_ave + st.session_state[f"q{i}_offset_sec"]
        if final_q_sec < 0:
            final_q_sec = 0.0
            
        q_m = int(final_q_sec // 60)
        q_s = final_q_sec % 60

        # 各Qにかかる時間・距離の計算
        if calc_mode == "distance_base":
            # 距離測定系：1Qあたりの距離は「全体の総距離 ÷ 4」で固定
            this_q_dist = dist_total / 4
            # タイム ＝ 500m Ave × (Q距離 / 500)
            this_q_secs = final_q_sec * (this_q_dist / 500)
        else:
            # 時間測定系：1Qあたりの時間は「全体の総秒数 ÷ 4」で固定
            this_q_secs = secs_total / 4
            # 距離 ＝ (Q秒数 / 500m Ave) * 500
            if final_q_sec > 0:
                this_q_dist = (this_q_secs / final_q_sec) * 500
            else:
                this_q_dist = 0.0

        # 合計用に加算していく
        calculated_total_seconds += this_q_secs
        calculated_total_distance += this_q_dist

        this_q_m = int(this_q_secs // 60)
        this_q_s = this_q_secs % 60

        # 画面への1列配置
        with c_q:
            st.write(f"**{i}Q**")
            
        with c_ave:
            st.write(f"**{q_m:02d}:{q_s:04.1f}**")
            
        with c_btn:
            # 省スペースのボタングループ
            b1, b2 = st.columns(2)
            with b1:
                if st.button("➕", key=f"p_btn_{i}"):
                    st.session_state[f"q{i}_offset_sec"] += 0.5
                    st.rerun()
            with b2:
                if st.button("➖", key=f"m_btn_{i}"):
                    st.session_state[f"q{i}_offset_sec"] -= 0.5
                    st.rerun()
                    
        with c_time:
            st.write(f"`{this_q_m:02d}:{this_q_s:04.1f}`")
            
        with c_dist:
            st.write(f"`{this_q_dist:.1f} m`")

    st.markdown("---")

    # --- 最終結果表示エリア（ユーザー様のご要望レイアウト） ---
    st.markdown("### **現在の合計**")
    
    total_m = int(calculated_total_seconds // 60)
    total_s = calculated_total_seconds % 60
    
    # タイムと距離を横並びで大きく表示
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric(label="⏱️ 合計タイム", value=f"{total_m}分 {total_s:04.1f}秒")
    with res_col2:
        st.metric(label="📏 合計距離", value=f"{calculated_total_distance:.1f} m")

    # フィードバックメッセージ
    if calc_mode == "distance_base":
        diff_secs = calculated_total_seconds - secs_total
        if abs(diff_secs) < 0.01:
            st.success("🎉 **目標タイムとピッタリ一致しています！完璧なレースプランです。**")
        elif diff_secs > 0:
            st.error(f"⚠️ **目標より {diff_secs:.1f} 秒遅いです。** あと {diff_secs:.1f} 秒縮めてください。")
        else:
            st.info(f"💡 **目標より {abs(diff_secs):.1f} 秒速いです。** あと {abs(diff_secs):.1f} 秒余裕があります。")
    else:
        diff_m = calculated_total_distance - dist_total
        if abs(diff_m) < 0.5:
            st.success("🎉 **目標距離とピッタリ一致しています！完璧なペース配分です。**")
        elif diff_m > 0:
            st.success(f"🚀 **目標より {abs(diff_m):.1f} m 多く漕げます！**")
        else:
            st.error(f"⚠️ **目標より {abs(diff_m):.1f} m 不足しています。** あと少しペースを上げてください。")
