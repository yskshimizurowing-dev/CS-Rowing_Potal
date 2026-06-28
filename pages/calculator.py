import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

st.title("🛶 エルゴ・レースプランシミュレーター")
st.write("目標タイムを設定し、各Q（500m）のペースを調整してレースプランを作成します。")
st.markdown("---")

# --- 【重要】値の変更を検知してリセットする関数 ---
def reset_if_changed():
    # 入力された値が、前回保存した値と違う場合は調整秒数をリセットする
    if (st.session_state.get("prev_dist") != st.session_state.calc_dist or 
        st.session_state.get("prev_min") != st.session_state.calc_min or 
        st.session_state.get("prev_sec") != st.session_state.calc_sec):
        
        for i in range(1, 5):
            st.session_state[f"calc_q{i}_diff"] = 0.0
            
    # 今回の値を「前回の値」として保存
    st.session_state["prev_dist"] = st.session_state.calc_dist
    st.session_state["prev_min"] = st.session_state.calc_min
    st.session_state["prev_sec"] = st.session_state.calc_sec


# --- 1. 目標設定エリア ---
# on_change を指定して、入力が変わったらリセット関数を動かす
col_dist, col_time = st.columns(2)
with col_dist:
    distance = st.number_input("目標距離 (m)", value=2000, step=500, key="calc_dist", on_change=reset_if_changed)

with col_time:
    st.write("全体の目標タイム")
    col_m, col_s = st.columns(2)
    with col_m:
        target_min = st.number_input("分", min_value=0, max_value=30, value=8, step=1, key="calc_min", on_change=reset_if_changed)
    with col_s:
        target_sec = st.number_input("秒", min_value=0, max_value=59, value=0, step=1, key="calc_sec", on_change=reset_if_changed)

# 全体の目標タイムを秒換算
target_total_seconds = (target_min * 60) + target_sec

# ⚠️ 距離が0のときにエラー（ゼロ除算）が出ないように対策
if distance > 0:
    base_ave_seconds = target_total_seconds / (distance / 500)
else:
    base_ave_seconds = 0.0

st.subheader("⏱️ 各Qの調整 (500m Average)")

# --- 2. 各Qの増減秒数を管理するシステム ---
for i in range(1, 5):
    if f"calc_q{i}_diff" not in st.session_state:
        st.session_state[f"calc_q{i}_diff"] = 0.0

# 最初の一回目の実行用に、現在の値を保存しておく
if "prev_dist" not in st.session_state:
    st.session_state["prev_dist"] = distance
    st.session_state["prev_min"] = target_min
    st.session_state["prev_sec"] = target_sec

# 手動リセットボタン
if st.button("プランをリセット", type="secondary"):
    for i in range(1, 5):
        st.session_state[f"calc_q{i}_diff"] = 0.0
    st.rerun()

st.write("")

# --- 3. 各Qの調整ボタンとタイム表示 ---
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
            
    # 実際のタイムを計算
    q_seconds = base_ave_seconds + st.session_state[f"calc_q{i}_diff"]
    q_times.append(q_seconds)
    
    with c_result:
        # マイナスになってしまった場合のバグを防ぐガード
        if q_seconds < 0:
            q_seconds = 0.0
        q_m = int(q_seconds // 60)
        q_s = q_seconds % 60
        st.markdown(f"### `{q_m:02d}:{q_s:04.1f}`")

st.markdown("---")

# --- 4. 合計タイムの過不足判定アラート ---
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
