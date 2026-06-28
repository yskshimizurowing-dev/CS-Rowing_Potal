import pandas as pd

if data:
    # 1. 取得したリストデータをDataFrameに変換
    df = pd.DataFrame(data)

    # 2. データの整理 (元のスプレッドシートの構成に合わせて抽出)
    # B列（インデックス1）に値があるものを抽出する例
    sheet_date = str(df.iloc[0, 1])  # B1: 日付
    location = str(df.iloc[1, 1])    # B2: 場所
    am_menu = df.iloc[2, 1]          # B3: AMメニュー
    pm_menu = df.iloc[3, 1]          # B4: PMメニュー
    
    # クルー編成（6行目/インデックス5以降）
    # 元のコードに合わせてスライスしてください
    crew_rows = df.iloc[5:].values.tolist()

    # 3. 元のUIの表示を開始
    st.title(f"🚣‍♂️ {sheet_date}")
    
    st.markdown(f"""
        <div class="menu-box">
          <div class="menu-title">📢 本日の練習メニュー</div>
          <div class="menu-item"><b>【場所】</b>{location}</div>
          <div class="menu-item"><b>【AM】</b>{am_menu}</div>
          <div class="menu-item"><b>【PM】</b>{pm_menu}</div>
        </div>
    """, unsafe_allow_html=True)

    # クルー編成のカード表示
    for row in crew_rows:
        # row[2]が艇名、row[3:8]がメンバー名として以前のコードを再利用
        boat_name = row[2]
        members = [str(m) for m in row[3:8] if m]
        if boat_name:
            st.markdown(f"""
                <div class="boat-card">
                    <div class="boat-name">{boat_name}</div>
                    <div class="member-list">{', '.join(members)}</div>
                </div>
            """, unsafe_allow_html=True)
