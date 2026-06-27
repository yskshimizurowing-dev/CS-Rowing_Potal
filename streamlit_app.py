import streamlit as st

# 画面全体の基本設定（タイトルや幅）
st.set_page_config(
    page_title="ボート部専用ポータル",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# タイトル部分
st.markdown("<h1 style='text-align: center; color: #333;'>ボート部専用ポータル</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>メニューを選択してください</p>", unsafe_allow_html=True)
st.write("---")

# --- スマホでも強制的に3列横並びにするためのCSS ---
st.markdown('''
<style>
    /* カラム全体を包むブロックを強制的に横並び(row)にする */
    div[data-testid="stHorizontalBlock"] {
        flex-direction: row !important;
    }
    /* 各カラムの幅を強制的に33.33%に固定する */
    div[data-testid="column"] {
        width: calc(33.3333% - 0.5rem) !important;
        flex: 1 1 calc(33.3333% - 0.5rem) !important;
        min-width: calc(33.3333% - 0.5rem) !important;
    }
</style>
''', unsafe_allow_html=True)


# ★ここから3×3のタイル配置を作る（行ごとに3列ずつ分ける）

# 【1行目】
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏋️\n\nトレーニング", use_container_width=True):
        st.toast("トレーニングメニューは現在開発中です！")
with col2:
    if st.button("📋\n\nホワイトボード", use_container_width=True):
        st.toast("乗艇練習ホワイトボードは現在開発中です！")
with col3:
    # 欠席連絡（URLが用意できたら書き換えてください）
    st.link_button("📝\n\n欠席連絡", "https://docs.google.com/forms/d/e/1FAIpQLSdZWWNO0GpPOpadbspDl_YPgA_jx1Q2i4xUUdH44IinvhGY_w/viewform?usp=dialog", use_container_width=True)

# 【2行目】
col4, col5, col6 = st.columns(3)
with col4:
    if st.button("🚣\n\n測定記録DB", use_container_width=True):
        st.toast("測定記録データベースは現在開発中です！")
with col5:
    if st.button("🧮\n\nAverage計算", use_container_width=True):
        st.toast("Average計算は現在開発中です！")
with col6:
    if st.button("🔧\n\nリギング", use_container_width=True):
        st.toast("リギングサポートは現在開発中です！")

# 【3行目】
col7, col8, col9 = st.columns(3)
with col7:
    if st.button("📦\n\n備品管理", use_container_width=True):
        st.toast("備品管理ツールは現在開発中です！")
with col8:
    if st.button("📊\n\n動画解析", use_container_width=True):
        st.toast("動画解析ツールは現在開発中です！")
with col9:
    # Googleドライブ（URLが用意できたら書き換えてください）
    st.link_button("☁️\n\n共有ドライブ", "https://drive.google.com/drive/folders/...", use_container_width=True)

# スマートフォンで見やすくするための見た目調整CSS
st.markdown("""
<style>
    /* ボタンを正方形に近づけ、文字を中央に配置する */
    div.stButton > button, div.stLinkButton > a {
        min-height: 100px !important;
        white-space: pre-wrap !important;
        font-weight: bold !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
    }
</style>
""", unsafe_allow_html=True)
