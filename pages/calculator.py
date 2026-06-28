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
        # 正しくtime_baseとしてロックされている場合は、メニュー2か3を維持
        default_index = st.session_state.get("fixed_mode_idx", 0)
    else:
        default_index = st.session_state.get("fixed_mode_idx", 0)

selected_menu = st.selectbox(
    "① 計算したいカテゴリーを選択してください",
    menus,
    index=default_index,
    on_change=clear_plan_states
)
mode_idx = menus.index(selected_menu)

#st.markdown("### **入力エリア**")
col1, col2 = st.columns(2)

tmp_dist = 0.0
tmp_secs = 0.0
tmp_ave = 0.0

# ★ ここでボート競技の計算ロジックに基いて、完全に紐付けを正しました。
if mode_idx == 0:
    # 距離固定系
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
    # 距離固定系
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
    current_type = "time_base"
    
    # 全体をまず左（②時間）と右（③距離）の2列に分ける
    top_col1, top_col2 = st.columns(2)
    
    with top_col1:
        st.write("② 合計時間")
        # 時間の中でさらに「分」「秒」を横並びにするための列分割（単位用カラムも用意）
        time_cols = st.columns([2, 1, 2, 1])
        with time_cols[0]:
            v_tm = st.number_input("分ラベル", min_value=0, max_value=120, value=20, step=1, key="m2_tm", label_visibility="collapsed", on_change=clear_plan_states)
        with time_cols[1]:
            st.markdown("<div style='padding-top: 10px;'>分</div>", unsafe_html=True)
        with time_cols[2]:
            v_ts = st.number_input("秒ラベル", min_value=0, max_value=59, value=0, step=1, key="m2_ts", label_visibility="collapsed", on_change=clear_plan_states)
        with time_cols[3]:
            st.markdown("<div style='padding-top: 10px;'>秒</div>", unsafe_html=True)
        tmp_secs = (v_tm * 60) + v_ts
        
    with top_col2:
        st.write("③ 距離")
        # 距離マスの右側に「m」を置くための列分割
        dist_cols = st.columns([5, 1])
        with dist_cols[0]:
            v_dist = st.number_input("距離ラベル", value=5000, step=500, key="m2_d", label_visibility="collapsed", on_change=clear_plan_states)
        with dist_cols[1]:
            st.markdown("<div style='padding-top: 10px;'>m</div>", unsafe_html=True)
        tmp_dist = v_dist
        
    if tmp_dist > 0:
        tmp_ave = tmp_secs / (tmp_dist / 500)
        
    # ②と③の列分割（top_col）の外に出すことで、必ず2つのマスの下に縦並びで表示されます
    st.write("")  # 少し隙間を空ける
    st.info(f"④ 計算されたAverage: **{int(tmp_ave // 60)}分{tmp_ave % 60:04.1f}秒** / 500m")

elif mode_idx == 3:
    # 時間固定系
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
    st.session_state["fixed_mode_idx"] = mode_idx

st.markdown("---")

if st.button("⑤ レースプランを作成", type="primary"):
    st.session_state["active_plan_flag"] = True
    st.session_state["fixed_ave_seconds"] = tmp_ave
    st.session_state["fixed_distance_m"] = tmp_dist
    st.session_state["fixed_total_seconds"] = tmp_secs
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
    
    calculated_total_seconds = 0.0
    calculated_total_distance = 0.0

    # 動的なレイアウトヘッダー
    hc1, hc2, hc3, hc4 = st.columns([1, 2, 2, 3])
    with hc1: st.caption("🔲 Q")
    with hc2: st.caption("🏃 500m Ave")
    with hc3: st.caption("➕ ➖")
    if calc_mode == "distance_base":
        with hc4: st.caption("⏱️ Qタイム")
    else:
        with hc4: st.caption("📏 Q距離")
        
    st.markdown("---")

    # 1Q〜4Qのループ処理
    for i in range(1, 5):
        c_q, c_ave, c_btn, c_val = st.columns([1, 2, 2, 3])
        
        final_q_sec = base_ave + st.session_state[f"q{i}_offset_sec"]
        if final_q_sec < 0:
            final_q_sec = 0.0
            
        q_m = int(final_q_sec // 60)
        q_s = final_q_sec % 60

        # 正しい定義に沿ったQごとの計算
        if calc_mode == "distance_base":
            # 距離測定系：1Qあたりの距離は固定
            this_q_dist = dist_total / 4
            this_q_secs = final_q_sec * (this_q_dist / 500)
        else:
            # 時間測定系：1Qあたりの時間は固定
            this_q_secs = secs_total / 4
            if final_q_sec > 0:
                this_q_dist = (this_q_secs / final_q_sec) * 500
            else:
                this_q_dist = 0.0

        calculated_total_seconds += this_q_secs
        calculated_total_distance += this_q_dist

        with c_q:
            st.write(f"**{i}Q**")
            
        with c_ave:
            st.write(f"**{q_m:02d}:{q_s:04.1f}**")
            
        with c_btn:
            b1, b2 = st.columns(2)
            with b1:
                if st.button("➕", key=f"p_btn_{i}"):
                    st.session_state[f"q{i}_offset_sec"] += 0.5
                    st.rerun()
            with b2:
                if st.button("➖", key=f"m_btn_{i}"):
                    st.session_state[f"q{i}_offset_sec"] -= 0.5
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
    
    # ご要望のレイアウト：現在のプランの総合数値を提示
    if calc_mode == "distance_base":
        p_total_m = int(calculated_total_seconds // 60)
        p_total_s = calculated_total_seconds % 60
        st.write(f"現在のプラン合計タイム: **{p_total_m}分{p_total_s:04.1f}秒** （目標タイム: {int(secs_total//60)}分{secs_total%60:04.1f}秒）")
        
        diff_secs = calculated_total_seconds - secs_total
        if abs(diff_secs) < 0.01:
            st.success("🎉 **目標タイムとピッタリ一致しています！完璧なレースプランです。**")
        elif diff_secs > 0:
            st.error(f"⚠️ **目標より {diff_secs:.1f} 秒遅いです。** あと {diff_secs:.1f} 秒縮めてください。")
        else:
            st.info(f"💡 **目標より {abs(diff_secs):.1f} 秒速いです。** あと {abs(diff_secs):.1f} 秒余裕があります。")
    else:
        # メニュー2番、3番はこちらの時間固定系（Q距離が変動するモード）に正しく入ります！
        st.write(f"現在のプラン合計距離: **{calculated_total_distance:.1f} m** （目標距離: {dist_total:.1f} m）")
        
        diff_m = calculated_total_distance - dist_total
        if abs(diff_m) < 0.5:
            st.success("🎉 **目標距離とピッタリ一致しています！完璧なペース配分です。**")
        elif diff_m > 0:
            st.success(f"🚀 **目標より {abs(diff_m):.1f} m 多く漕げます！ （ナイスプラン）**")
        else:
            st.error(f"⚠️ **目標より {abs(diff_m):.1f} m 不足しています。** あと少しペースを上げてください。")
