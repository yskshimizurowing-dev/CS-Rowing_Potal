import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

st.title("🛶 エルゴ・レースプランシミュレーター")
st.write("カテゴリを選んで目標数値を入力し、レースプランを作成・シミュレーションします。")
st.markdown("---")

# --- ① カテゴリーの選択 ---
menus = [
    "距離 と 目標タイム から【全体のAverage】を出す", 
    "距離 と Average から【目標タイム】を出す",
    "合計時間 と 距離 から【全体のAverage】を出す",
    "合計時間 と Average から【目標距離】を出す（例：20分測定など）"
]

if "active_plan_flag" not in st.session_state:
    st.session_state["active_plan_flag"] = False

def clear_plan_states():
    for i in range(1, 5):
        st.session_state[f"q{i}_offset_sec"] = 0.0
    st.session_state["active_plan_flag"] = False

default_index = 0
if st.session_state["active_plan_flag"]:
    default_index = st.session_state.get("fixed_mode_idx", 0)

selected_menu = st.selectbox(
    "① 計算したいカテゴリーを選択してください",
    menus,
    index=default_index,
    on_change=clear_plan_states
)
mode_idx = menus.index(selected_menu)

calc_dist = 0.0
calc_secs = 0.0
calc_ave = 0.0

# 画面全体の左右2列分割（すべてのメニューで共通の安全な50:50枠を使用）
main_col1, main_col2 = st.columns(2)

# --- 各メニューの入力制御（入れ子カラムを完全排除） ---
if mode_idx == 0:
    current_type = "distance_base"
    with main_col1:
        st.write("② 距離")
        v_dist = st.number_input("距離 (m)", min_value=0, value=2000, step=500, key="m0_d_f")
        calc_dist = float(v_dist)
    with main_col2:
        st.write("③ 全体の目標タイム")
        v_m = st.number_input("目標タイム（分）", min_value=0, max_value=60, value=8, step=1, key="m0_m_f")
        v_s = st.number_input("目標タイム（秒）", min_value=0, max_value=59, value=0, step=1, key="m0_s_f")
        calc_secs = float((v_m * 60) + v_s)
    if calc_dist > 0:
        calc_ave = calc_secs / (calc_dist / 500)
    
    st.write("") 
    st.info(f"④ 必要な全体のAverage: **{int(calc_ave // 60)}分{calc_ave % 60:04.1f}秒** / 500m")

elif mode_idx == 1:
    current_type = "distance_base"
    with main_col1:
        st.write("② 距離")
        v_dist = st.number_input("距離 (m)", min_value=0, value=2000, step=500, key="m1_d_f")
        calc_dist = float(v_dist)
    with main_col2:
        st.write("③ 全体のAverage (/500m)")
        v_am = st.number_input("Average（分）", min_value=0, max_value=10, value=2, step=1, key="m1_am_f")
        v_as = st.number_input("Average（秒）", min_value=0, max_value=59, value=0, step=1, key="m1_as_f")
        calc_ave = float((v_am * 60) + v_as)
    if calc_dist > 0:
        calc_secs = calc_ave * (calc_dist / 500)
        
    st.write("") 
    st.info(f"④ 算出された合計タイム: **{int(calc_secs // 60)}分{calc_secs % 60:04.1f}秒**")

elif mode_idx == 2:
    # エラー原因（value_type）を完全除去した時間測定モード
    current_type = "time_base"
    with main_col1:
        st.write("② 合計時間")
        v_tm = st.number_input("合計時間（分）", min_value=0, max_value=120, value=20, step=1, key="m2_tm_f")
        v_ts = st.number_input("合計時間（秒）", min_value=0, max_value=59, value=0, step=1, key="m2_ts_f")
        calc_secs = float((v_tm * 60) + v_ts)
    with main_col2:
        st.write("③ 距離")
        v_dist = st.number_input("目標距離 (m)", min_value=0, value=5000, step=500, key="m2_d_f")
        calc_dist = float(v_dist)
    if calc_dist > 0:
        calc_ave = calc_secs / (calc_dist / 500)
        
    st.write("") 
    st.info(f"④ 計算されたAverage: **{int(calc_ave // 60)}分{calc_ave % 60:04.1f}秒** / 500m")

elif mode_idx == 3:
    current_type = "time_base"
    with main_col1:
        st.write("② 合計の測定時間")
        v_tm = st.number_input("測定時間（分）", min_value=0, max_value=120, value=20, step=1, key="m3_tm_f")
        v_ts = st.number_input("測定時間（秒）", min_value=0, max_value=59, value=0, step=1, key="m3_ts_f")
        calc_secs = float((v_tm * 60) + v_ts)
    with main_col2:
        st.write("③ 目標のAverage (/500m)")
        v_am = st.number_input("目標Average（分）", min_value=0, max_value=10, value=1, step=1, key="m3_am_f")
        v_as = st.number_input("目標Average（秒）", min_value=0, max_value=59, value=50, step=1, key="m3_as_f")
        calc_ave = float((v_am * 60) + v_as)
    if calc_ave > 0:
        calc_dist = (calc_secs / calc_ave) * 500
        
    st.write("") 
    st.info(f"④ 想定される合計の目標距離: **{calc_dist:.1f} m**")


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
