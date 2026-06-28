import streamlit as st

st.set_page_config(page_title="エルゴ レースプランナー", layout="centered")

st.title("🛶 エルゴ・レースプランシミュレーター")
st.write("カテゴリを選んで目標数値を入力し、レースプランを作成・シミュレーションします。")
st.markdown("---")

# --- セッション状態（メモリ）の初期化 ---
if "plan_generated" not in st.session_state:
    st.session_state["plan_generated"] = False

# 各Qの調整秒数
for i in range(1, 5):
    if f"calc_q{i}_diff" not in st.session_state:
        st.session_state[f"calc_q{i}_diff"] = 0.0

# 確定した計算ベースの値を記憶する用の倉庫
if "saved_base_ave" not in st.session_state:
    st.session_state["saved_base_ave"] = 0.0
if "saved_distance" not in st.session_state:
    st.session_state["saved_distance"] = 0.0
if "saved_target_seconds" not in st.session_state:
    st.session_state["saved_target_seconds"] = 0.0
if "saved_is_time_based" not in st.session_state:
    st.session_state["saved_is_time_based"] = False

# 値の変更を検知して状態を完全にクリアする関数
def reset_all_states():
    for i in range(1, 5):
        st.session_state[f"calc_q{i}_diff"] = 0.0
    st.session_state["plan_generated"] = False


# --- ① 計算したいカテゴリーを選択（セレクトボックス） ---
menu_options = [
    "距離 と 目標タイム から【全体のAverage】を出す", 
    "距離 と Average から【目標タイム】を出す",
    "合計時間 と 距離 から【全体のAverage】を出す",
    "合計時間 と Average から【目標距離】を出す（例：20分測定など）"
]

category = st.selectbox(
    "① 計算したいカテゴリーを選択してください",
    menu_options,
    on_change=reset_all_states
)

# 選択されたメニューが何番目かを取得（文字列ズレによるバグを防ぐ）
menu_index = menu_options.index(category)

st.markdown("### **入力エリア**")
col1, col2 = st.columns(2)

# 画面表示用の計算用変数
disp_distance = 0.0
disp_target_seconds = 0.0
disp_base_ave = 0.0
is_time_based = (menu_index == 3) # 4番目のメニューだけが「時間固定」

# --- 各カテゴリーに応じた入力・計算処理 ---
if menu_index == 0:
    # パターン1: 距離 ＋ タイム
    with col1:
        v_dist = st.number_input("② 距離 (m)", value=2000, step=500, key="in_dist_0", on_change=reset_all_states)
    with col2:
        st.write("③ 全体の目標タイム")
        col_m, col_s = st.columns(2)
        with col_m:
            v_min = st.number_input("分", min_value=0, max_value=60, value=8, step=1, key="in_min_0", on_change=reset_all_states)
        with col_s:
            v_sec = st.number_input("秒", min_value=0, max_value=59, value=0, step=1, key="in_sec_0", on_change=reset_all_states)
        
        disp_distance = v_dist
        disp_target_seconds = (v_min * 60) + v_sec
        if disp_distance > 0:
            disp_base_ave = disp_target_seconds / (disp_distance / 500)
        
        ave_m = int(disp_base_ave // 60)
        ave_s = disp_base_ave % 60
        st.info(f"④ 必要な全体のAverage: **{ave_m}分{ave_s:04.1f}秒** / 500m")

elif menu_index == 1:
    # パターン2: 距離 ＋ Average
    with col1:
        v_dist = st.number_input("② 距離 (m)", value=2000, step=500, key="in_dist_1", on_change=reset_all_states)
    with col2:
        st.write("③ 全体のAverage (/500m)")
        col_am, col_as = st.columns(2)
        with col_am:
            v_amin = st.number_input("分 ", min_value=0, max_value=10, value=2, step=1, key="in_amin_1", on_change=reset_all_states)
        with col_as:
            v_asec = st.number_input("秒 ", min_value=0, max_value=59, value=0, step=1, key="in_asec_1", on_change=reset_all_states)
        
        disp_distance = v_dist
        disp_base_ave = (v_amin * 60) + v_asec
        if disp_distance > 0:
            disp_target_seconds = disp_base_ave * (disp_distance / 500)
        
        total_m = int(disp_target_seconds // 60)
        total_s = disp_target_seconds % 60
        st.info(f"④ 算出された合計タイム: **{total_m}分{total_s:04.1f}秒**")

elif menu_index == 2:
    # パターン3: 合計時間 ＋ 距離
    with col1:
        st.write("② 合計時間")
        col_tm, col_ts = st.columns(2)
        with col_tm:
            v_tmin = st.number_input("分", min_value=0, max_value=120, value=7, step=1, key="in_tmin_2", on_change=reset_all_states)
        with col_ts:
            v_tsec = st.number_input("秒", min_value=0, max_value=59, value=30, step=1, key="in_tsec_2", on_change=reset_all_states)
        disp_target_seconds = (v_tmin * 60) + v_tsec
    with col1:
        v_dist = st.number_input("③ 距離 (m)", value=2000, step=500, key="in_dist_2", on_change=reset_all_states)
    
    disp_distance = v_dist
    if disp_distance > 0:
        disp_base_ave = disp_target_seconds / (disp_distance / 500)
    
    ave_m = int(disp_base_ave // 60)
    ave_s = disp_base_ave % 60
    with col2:
        st.info(f"④ 計算されたAverage: **{ave_m}分{ave_s:04.1f}秒** / 500m")

elif menu_index == 3:
    # パターン4: 合計時間 ＋ Average（20分測定など）
    with col1:
        st.write("② 合計の測定時間")
        col_tm, col_ts = st.columns(2)
        with col_tm:
            v_tmin = st.number_input("分", min_value=0, max_value=120, value=20, step=1, key="in_tmin_3", on_change=reset_all_states)
        with col_ts:
            v_tsec = st.number_input("秒", min_value=0, max_value=59, value=0, step=1, key="in_tsec_3", on_change=reset_all_states)
        disp_target_seconds = (v_tmin * 60) + v_tsec
    with col2:
        st.write("③ 目標のAverage (/500m)")
        col_am, col_as = st.columns(2)
        with col_am:
            v_amin = st.number_input("分  ", min_value=0, max_value=10, value=1, step=1, key="in_amin_3", on_change=reset_all_states)
        with col_as:
            v_asec = st.number_input("秒  ", min_value=0, max_value=59, value=50, step=1, key="in_asec_3", on_change=reset_all_states)
        
        disp_base_ave = (v_amin * 60) + v_asec
        if disp_base_ave > 0:
            disp_distance = (disp_target_seconds / disp_base_ave) * 500
        
        st.info(f"④ 想定される合計の目標距離: **{disp_distance:.1f} m**")


# プラン作成ボタンを押す前、または入力値を弄っている間は常に最新値を同期
if not st.session_state["plan_generated"]:
    st.session_state["saved_base_ave"] = disp_base_ave
    st.session_state["saved_distance"] = disp_distance
    st.session_state["saved_target_seconds"] = disp_target_seconds
    st.session_state["saved_is_time_based"] = is_time_based

st.markdown("---")

# --- ⑤ レースプランを作成 ボタン ---
if st.button("⑤ レースプランを作成", type="primary"):
    st.session_state["plan_generated"] = True
    st.session_state["saved_base_ave"] = disp_base_ave
    st.session_state["saved_distance"] = disp_distance
    st.session_state["saved_target_seconds"] = disp_target_seconds
    st.session_state["saved_is_time_based"] = is_time_based
    st.rerun()

# --- レースプラン作成エリア ---
if st.session_state["plan_generated"]:
    # 完全に倉庫（メモリ）にロックされた数値を使用する
    base_ave = st.session_state["saved_base_ave"]
    dist_total = st.session_state["saved_distance"]
    secs_total = st.session_state["saved_target_seconds"]
    time_flag = st.session_state["saved_is_time_based"]

    if time_flag:
        q_info = f"各Qの長さ（時間固定）: {int((secs_total/4)//60)}分 {int((secs_total/4)%60)}秒"
    else:
        q_info = f"各Qの長さ（距離固定）: {dist_total/4:.0f}m"
        
    st.subheader(f"⏱️ 各Qの調整 (500m Average)")
    st.caption(f"💡 {q_info}")
    
    if st.button("このプランをリセット", type="secondary"):
        for i in range(1, 5):
            st.session_state[f"calc_q{i}_diff"] = 0.0
        st.rerun()

    st.write("")
    q_times = []

    # 1Q〜4Qの入力行
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
                
        q_seconds = base_ave + st.session_state[f"calc_q{i}_diff"]
        if q_seconds < 0:
            q_seconds = 0.0
        q_times.append(q_seconds)
        
        with c_result:
            q_m = int(q_seconds // 60)
            q_s = q_seconds % 60
            st.markdown(f"### `{q_m:02d}:{q_s:04.1f}`")

    st.markdown("---")

    # ==========================================
    # 最終判定・計算表示エリア
    # ==========================================
    if not time_flag:
        # 【距離ベース（メニュー1〜3番目）の場合】
        plan_total_seconds = sum(q_times)
        diff = plan_total_seconds - secs_total
        p_total_m = int(plan_total_seconds // 60)
        p_total_s = plan_total_seconds % 60

        st.write(f"現在のプラン合計タイム: **{p_total_m}分{p_total_s:04.1f}秒**")

        if abs(diff) < 0.01:
            st.success("🎉 **目標タイムとピッタリ一致しています！完璧なレースプランです。**")
        elif diff > 0:
            st.error(f"⚠️ **目標より {diff:.1f} 秒遅いです。** あと {diff:.1f} 秒縮めてください。")
        else:
            st.info(f"💡 **目標より {abs(diff):.1f} 秒速いです。** あと {abs(diff):.1f} 秒余裕があります。")
            
    else:
        # 【時間ベース（メニュー4番目：20分測定など）の場合】
        q_duration = secs_total / 4
        plan_distance = 0.0
        for q_sec in q_times:
            if q_sec > 0:
                plan_distance += (q_duration / q_sec) * 500
                
        diff_dist = plan_distance - dist_total
        st.write(f"現在のプラン合計距離: **{plan_distance:.1f} m** （目標: {dist_total:.1f} m）")

        if abs(diff_dist) < 0.5:
            st.success("🎉 **目標距離とピッタリ一致しています！完璧なペース配分です。**")
        elif diff_dist > 0:
            st.success(f"🚀 **目標より {abs(diff_dist):.1f} m 多く漕げます！ （ナイスプラン）**")
        else:
            st.error(f"⚠️ **目標より {abs(diff_dist):.1f} m 不足しています。** あと少しペースを上げてください。")
