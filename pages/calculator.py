import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

# --- CSS: スマホでのボタン押しやすさとレイアウト調整 ---
st.markdown("""
<style>
    .stButton>button { width: 100%; height: 3.5em; font-weight: bold; }
    [data-testid="column"] { padding: 0.1em; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🛶 エルゴ・<br>レースプランシミュレーター", unsafe_allow_html=True)
st.markdown("---")

# --- セッションとメニュー ---
if "active_plan_flag" not in st.session_state: st.session_state["active_plan_flag"] = False

def clear_plan_states():
    for i in range(1, 5): st.session_state[f"q{i}_offset_sec"] = 0.0
    st.session_state["active_plan_flag"] = False

menus = [
    "距離 と 目標タイム から【全体のAverage】を出す", 
    "距離 と Average から【目標タイム】を出す",
    "合計時間 と 距離 から【全体のAverage】を出す",
    "合計時間 と Average から【目標距離】を出す"
]
selected_menu = st.selectbox("① 計算カテゴリー選択", menus, index=st.session_state.get("fixed_mode_idx", 0) if st.session_state["active_plan_flag"] else 0, on_change=clear_plan_states)
mode_idx = menus.index(selected_menu)

# --- 入力ロジック (省略: 前回のコードと同様) ---
# (中略: 計算ロジック部分は前回のものをそのままお使いください)
# ...

# --- プラン作成ボタン ---
if st.button("⑤ レースプランを作成", type="primary"):
    st.session_state.update({
        "active_plan_flag": True, "fixed_ave_seconds": calc_ave, "fixed_distance_m": calc_dist,
        "fixed_total_seconds": calc_secs, "fixed_calc_mode": "time_base" if mode_idx >= 2 else "distance_base",
        "fixed_mode_idx": mode_idx
    })
    st.rerun()

# --- レースプラン調整 & 最終判定エリア ---
if st.session_state["active_plan_flag"]:
    base_ave = st.session_state["fixed_ave_seconds"]
    dist_total = st.session_state["fixed_distance_m"]
    secs_total = st.session_state["fixed_total_seconds"]
    calc_mode = st.session_state["fixed_calc_mode"]

    st.subheader("⏱️ 各Qの調整")
    if st.button("リセット"):
        for i in range(1, 5): st.session_state[f"q{i}_offset_sec"] = 0.0
        st.rerun()

    p_total_secs, p_total_dist = 0.0, 0.0
    for i in range(1, 5):
        if f"q{i}_offset_sec" not in st.session_state: st.session_state[f"q{i}_offset_sec"] = 0.0
        q_sec = base_ave + st.session_state[f"q{i}_offset_sec"]
        
        st.markdown(f"**{i}Q** (Ave: {int(q_sec//60)}:{q_sec%60:04.1f})")
        b1, b2 = st.columns(2)
        if b1.button("➕ 0.5s", key=f"p_{i}"): st.session_state[f"q{i}_offset_sec"] += 0.5; st.rerun()
        if b2.button("➖ 0.5s", key=f"m_{i}"): st.session_state[f"q{i}_offset_sec"] -= 0.5; st.rerun()
        
        if calc_mode == 'distance_base':
            ts = q_sec * ((dist_total / 4) / 500); p_total_secs += ts
        else:
            td = (secs_total / 4 / q_sec) * 500 if q_sec > 0 else 0; p_total_dist += td

    # --- 復活：合計と過不足判定 ---
    st.markdown("---")
    if calc_mode == 'distance_base':
        diff = p_total_secs - secs_total
        st.write(f"### 合計タイム: {int(p_total_secs//60)}:{p_total_secs%60:04.1f}")
        if abs(diff) < 0.1: st.success("🎉 目標とピッタリです！")
        elif diff > 0: st.error(f"⚠️ 目標より {diff:.1f} 秒遅いです")
        else: st.info(f"💡 目標より {abs(diff):.1f} 秒速いです")
    else:
        diff = p_total_dist - dist_total
        st.write(f"### 合計距離: {p_total_dist:.1f} m")
        if abs(diff) < 0.5: st.success("🎉 目標とピッタリです！")
        elif diff > 0: st.success(f"🚀 目標より {diff:.1f} m 多いです")
        else: st.error(f"⚠️ 目標より {abs(diff):.1f} m 不足しています")
