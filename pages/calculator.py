import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

st.markdown("#エルゴ・<br>レースプラン<br>シミュレーター", unsafe_allow_html=True)
st.markdown("---")

if "active_plan_flag" not in st.session_state:
    st.session_state["active_plan_flag"] = False

def clear_plan_states():
    for i in range(1, 5):
        st.session_state[f"q{i}_offset_sec"] = 0.0
    st.session_state["active_plan_flag"] = False

menus = [
    "距離 と タイム から【Average】を出す", 
    "距離 と Average から【タイム】を出す",
    "合計時間 と 距離 から【Average】を出す",
    "合計時間 と Average から【距離】を出す"
]
default_index = st.session_state.get("fixed_mode_idx", 0) if st.session_state["active_plan_flag"] else 0
selected_menu = st.selectbox("① カテゴリー選択", menus, index=default_index, on_change=clear_plan_states)
mode_idx = menus.index(selected_menu)

# --- 入力 ---
# 分と秒を一つのブロックとして扱うための列構成
c_main = st.columns(2)
if mode_idx in [0, 1]:
    dist = c_main[0].number_input("② 距離 (m)", value=2000, step=500)
    c_time = c_main[1].columns(2)
    m = c_time[0].number_input("③ 分", value=2)
    s = c_time[1].number_input("秒", value=0)
    calc_secs = m * 60 + s
    calc_ave = calc_secs / (dist / 500) if mode_idx == 0 and dist > 0 else calc_secs
    if mode_idx == 0: st.info(f"④ Average: **{int(calc_ave//60)}:{calc_ave%60:05.2f}** / 500m")
    else: st.info(f"④ 合計タイム: **{int(calc_secs//60)}分{calc_secs%60:05.2f}秒**")
else:
    c_time = c_main[0].columns(2)
    m = c_time[0].number_input("② 分", value=20)
    s = c_time[1].number_input("秒", value=0)
    dist = c_main[1].number_input("③ 距離 (m)", value=5000, step=500)
    calc_secs = m * 60 + s
    calc_ave = calc_secs / (dist / 500) if mode_idx == 2 and dist > 0 else 0
    if mode_idx == 2: st.info(f"④ Average: **{int(calc_ave//60)}:{calc_ave%60:05.2f}** / 500m")
    else: st.info(f"④ 合計距離: **{dist:.1f} m**")

if st.button("⑤ レースプランを作成", type="primary"):
    st.session_state.update({
        "active_plan_flag": True, "fixed_ave_seconds": calc_ave, 
        "fixed_distance_m": dist, "fixed_total_seconds": calc_secs, 
        "fixed_calc_mode": "time_base" if mode_idx >= 2 else "distance_base", 
        "fixed_mode_idx": mode_idx
    })
    st.rerun()

# --- 調整エリア ---
if st.session_state["active_plan_flag"]:
    base_ave = st.session_state["fixed_ave_seconds"]
    dist_total = st.session_state["fixed_distance_m"]
    secs_total = st.session_state["fixed_total_seconds"]
    calc_mode = st.session_state["fixed_calc_mode"]
    
    st.subheader("各Qの調整")
    if st.button("リセット"):
        for i in range(1, 5): st.session_state[f"q{i}_offset_sec"] = 0.0
        st.rerun()

    p_total_secs, p_total_dist = 0.0, 0.0
    for i in range(1, 5):
        if f"q{i}_offset_sec" not in st.session_state: st.session_state[f"q{i}_offset_sec"] = 0.0
        q_sec = base_ave + st.session_state[f"q{i}_offset_sec"]
        
        if calc_mode == 'distance_base':
            ts = q_sec * ((dist_total / 4) / 500); p_total_secs += ts
            res_display = f"{int(ts//60)}:{ts%60:05.2f}"
        else:
            td = (secs_total / 4 / q_sec) * 500 if q_sec > 0 else 0; p_total_dist += td
            res_display = f"{td:.1f} m"
            
        st.write(f"**{i}Q** Ave {int(q_sec//60)}:{q_sec%60:05.2f} | {res_display}")
        
        b1, b2 = st.columns(2)
        if b1.button("➕", key=f"p_{i}"): st.session_state[f"q{i}_offset_sec"] += 0.5; st.rerun()
        if b2.button("➖", key=f"m_{i}"): st.session_state[f"q{i}_offset_sec"] -= 0.5; st.rerun()
        st.markdown("---")

    if calc_mode == 'distance_base':
        diff = p_total_secs - secs_total
        st.write(f"合計タイム: {int(p_total_secs//60)}:{p_total_secs%60:05.2f}")
        if abs(diff) < 0.1: st.success("設定と一致")
        elif diff > 0: st.error(f"⚠️ {diff:.2f} 秒超過")
        else: st.info(f"💡 {abs(diff):.2f} 秒猶予")
    else:
        diff = p_total_dist - dist_total
        st.write(f"合計距離: {p_total_dist:.1f} m")
        if abs(diff) < 0.5: st.success("設定と一致")
        elif diff > 0: st.success(f"💡 {diff:.1f} m 超過")
        else: st.error(f"⚠️ {abs(diff):.1f} m 不足")
