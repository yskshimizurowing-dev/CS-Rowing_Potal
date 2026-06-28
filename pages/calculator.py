import streamlit as st

# ページ個別の設定（タイトル等）
st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

st.title("🛶 エルゴ・レースプランシミュレーター")
st.write("目標タイムを設定し、各Q（500m）のペースを調整してレースプランを作成します。")
st.markdown("---")

# --- 1. 目標設定エリア ---
col_dist, col_time = st.columns(2)
with col_dist:
    distance = st.number_input("目標距離 (m)", value=2000, step=500)

with col_time:
    st.write("全体の目標タイム")
    col_m, col_s = st.columns(2)
    with col_m:
        target_min = st.number_input("分", min_value=0, max_value=30, value=8, step=1)
    with col_s:
        target_sec = st.number_input("秒", min_value=0, max_value=59, value=0, step=1)

# 全体の目標タイムを秒換算
target_total_seconds = (target_min * 60) + target_sec
# ベースとなる500m Ave（初期値）を計算
base_ave_seconds = target_total_seconds / (distance / 500)

st.subheader("⏱️ 各Qの調整 (500m Average)")

# --- 2. 各Qの増減秒数を管理するシステム（Session State） ---
# マルチページ移行に伴い、他ページとキーが衝突しないよう「calc_」の接頭辞を推奨
for i in range(1, 5):
    if f"calc_q{i}_diff" not in st.session_state:
        st.session_state[f"calc_q{i}_diff"] = 0.0

# リセットボタン
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
            
    # 実際のタイムを計算（ベースタイム ＋ ボタンでの調整分）
    q_seconds = base_ave_seconds + st.session_state[f"calc_q{i}_diff"]
    q_times.append(q_seconds)
    
    with c_result:
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

# 条件分岐でメッセージを切り替え
if abs(diff) < 0.01:
    st.success("🎉 **目標タイムとピッタリ一致しています！完璧なレースプランです。**")
elif diff > 0:
    st.error(f"⚠️ **目標より {diff:.1f} 秒遅いです。** あと {diff:.1f} 秒縮めてください。")
else:
    st.info(f"💡 **目標より {abs(diff):.1f} 秒速いです。** あと {abs(diff):.1f} 秒余裕があります。")
