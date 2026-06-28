import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

st.title("🛶 エルゴ・レースプランシミュレーター")
st.write("カテゴリを選んで目標数値を入力し、レースプランを作成します。")
st.markdown("---")

if "active_plan_flag" not in st.session_state:
    st.session_state["active_plan_flag"] = False

def clear_plan_states():
    for i in range(1, 5):
        st.session_state[f"q{i}_offset_sec"] = 0.0
    st.session_state["active_plan_flag"] = False

menus = [
    "距離 と 目標タイム から【全体のAverage】を出す", 
    "距離 と Average から【目標タイム】を出す",
    "合計時間 と 距離 から【全体のAverage】を出す",
    "合計時間 と Average から【目標距離】を出す"
]
default_index = st.session_state.get("fixed_mode_idx", 0) if st.session_state["active_plan_flag"] else 0
selected_menu = st.selectbox("① 計算したいカテゴリーを選択してください", menus, index=default_index, on_change=clear_plan_states)
mode_idx = menus.index(selected_menu)

calc_dist, calc_secs, calc_ave = 0.0, 0.0, 0.0

# 左右のメインカラム
c1, c2 = st.columns(2)

# --- 共通の入力パーツ関数 ---
def distance_input_custom(col, label_num_text, key):
    with col:
        st.write(label_num_text)
        st.write("メートル")
        return float(st.number_input("距離", value=2000, step=500, key=key, label_visibility="collapsed"))

def time_input_custom(col, label_num_text, key_m, key_s):
    with col:
        st.write(label_num_text)
        cols = st.columns(2)
        m = cols[0].number_input("分", min_value=0, value=8, step=1, key=key_m)
        s = cols[1].number_input("秒", min_value=0, max_value=59, value=0, step=1, key=key_s)
        return float(m * 60 + s)

# ロジック分岐
if mode_idx == 0:
    calc_dist = distance_input_custom(c1, "② 距離", "m0_d")
    calc_secs = time_input_custom(c2, "③ 目標タイム", "m0_m", "m0_s")
    if calc_dist > 0: calc_ave = calc_secs / (calc_dist / 500)
    st.info(f"④ 必要なAverage: **{int(calc_ave // 60)}分{calc_ave % 60:04.1f}秒** / 500m")

elif mode_idx == 1:
    calc_dist = distance_input_custom(c1, "② 距離", "m1_d")
    calc_secs = time_input_custom(c2, "③ 全体のAverage", "m1_am", "m1_as")
    calc_secs = calc_secs * (calc_dist / 500)
    st.info(f"④ 算出された合計タイム: **{int(calc_secs // 60)}分{calc_secs % 60:04.1f}秒**")

elif mode_idx == 2:
    calc_secs = time_input_custom(c1, "② 合計時間", "m2_tm", "m2_ts")
    calc_dist = distance_input_custom(c2, "③ 距離", "m2_d")
    if calc_dist > 0: calc_ave = calc_secs / (calc_dist / 500)
    st.info(f"④ 計算されたAverage: **{int(calc_ave // 60)}分{calc_ave % 60:04.1f}秒** / 500m")

elif mode_idx == 3:
    calc_secs = time_input_custom(c1, "② 測定時間", "m3_tm", "m3_ts")
    calc_ave = time_input_custom(c2, "③ 目標Average", "m3_am", "m3_as")
    if calc_ave > 0: calc_dist = (calc_secs / calc_ave) * 500
    st.info(f"④ 想定される合計目標距離: **{calc_dist:.1f} m**")

# プラン作成・調整ロジック（以前のものと同一）
st.markdown("---")
if st.button("⑤ レースプランを作成", type="primary"):
    st.session_state.update({"active_plan_flag": True, "fixed_ave_seconds": calc_ave, "fixed_distance_m": calc_dist, "fixed_total_seconds": calc_secs, "fixed_calc_mode": "time_base" if mode_idx >= 2 else "distance_base", "fixed_mode_idx": mode_idx})
    st.rerun()
# 以下、プラン作成・調整ロジック
st.markdown("---")
if st.button("⑤ レースプランを作成", type="primary"):
    st.session_state.update({"active_plan_flag": True, "fixed_ave_seconds": calc_ave, "fixed_distance_m": calc_dist, "fixed_total_seconds": calc_secs, "fixed_calc_mode": "time_base" if mode_idx >= 2 else "distance_base", "fixed_mode_idx": mode_idx})
    st.rerun()

if st.session_state["active_plan_flag"]:
    base_ave = st.session_state["fixed_ave_seconds"]
    dist_total = st.session_state["fixed_distance_m"]
    secs_total = st.session_state["fixed_total_seconds"]
    calc_mode = st.session_state["fixed_calc_mode"]

    st.subheader("⏱️ 各Qの調整")
    if st.button("このプランをリセット"):
        for i in range(1, 5): st.session_state[f"q{i}_offset_sec"] = 0.0
        st.rerun()

    p_total_secs, p_total_dist = 0.0, 0.0
    for i in range(1, 5):
        c1, c2, c3, c4 = st.columns([1, 2, 2, 3])
        c1.write(f"**{i}Q**")
        q_sec = base_ave + st.session_state.get(f"q{i}_offset_sec", 0.0)
        c2.write(f"**{int(q_sec//60):02d}:{q_sec%60:04.1f}**")
        b1, b2 = c3.columns(2)
        if b1.button("➕", key=f"p_{i}"): st.session_state[f"q{i}_offset_sec"] += 0.5; st.rerun()
        if b2.button("➖", key=f"m_{i}"): st.session_state[f"q{i}_offset_sec"] -= 0.5; st.rerun()
        if calc_mode == 'distance_base':
            ts = q_sec * ((dist_total / 4) / 500); p_total_secs += ts
            c4.write(f"`{int(ts//60):02d}:{ts%60:04.1f}`")
        else:
            td = (secs_total / 4 / q_sec) * 500 if q_sec > 0 else 0; p_total_dist += td
            c4.write(f"`{td:.1f} m`")
    st.markdown("---")
    if calc_mode == 'distance_base':
        diff = p_total_secs - secs_total
        st.write(f"合計タイム: {int(p_total_secs//60)}分{p_total_secs%60:.1f}秒")
        if abs(diff) < 0.1: st.success("🎉 目標とピッタリです！")
        elif diff > 0: st.error(f"⚠️ 目標より {diff:.1f} 秒遅いです")
        else: st.info(f"💡 目標より {abs(diff):.1f} 秒速いです")
    else:
        diff = p_total_dist - dist_total
        st.write(f"合計距離: {p_total_dist:.1f} m")
        if abs(diff) < 0.5: st.success("🎉 目標とピッタリです！")
        elif diff > 0: st.success(f"🚀 目標より {diff:.1f} m 多いです")
        else: st.error(f"⚠️ 目標より {abs(diff):.1f} m 不足しています")
