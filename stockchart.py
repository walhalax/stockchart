import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('米国株価可視化アプリ')

st.write('モバイルの場合は画面左上の">"からサイドバーを表示してください')


# サイドバーに表示する文言を登録
st.sidebar.write("""
スライダーで表示範囲を指定してください。
""")

st.sidebar.write("""
## 表示日数
""")

# 表j日数変更のためのスライダーを追加
# 作成済みのコードに合わせるために日数を'days'で定義
days = st.sidebar.slider('表示したい日数の範囲を指定してください。', 1, 720 ,30)

# メイン画面の表示文言を登録
# 日数は可変されるので日数部分にfstringsメソッドを置く
st.write(f"""
### 過去 **{days}日間**の米国の株価
""")

@st.cache                                             # データ保持にキャッシュを使用する
def get_data(days, tickers):
    df = pd.DataFrame()                               # dfで空のデータを用意
    for company in tickers.keys():                    #
        tkr = yf.Ticker(tickers[company])             # ティッカーを'tkr'と定義
        hist = tkr.history(period=f'{days}d')         # データ変更を容易にするためにfstringsを使って入れ子構造に
        hist.index = hist.index.strftime('%d %B %Y')  # 年月日→日月年へと変更
        hist = hist[['Close']]                        # 株価の終値のみを表示し、その箇所に社名を表示
        hist.columns = [company]                      # カラムに各社を呼び出すために'company'を指定
        hist = hist.T                                 # 行と列を転置する
        hist.index.name = 'Name'                      # indexに会社名を表示
        df = pd.concat([df, hist])                    # 'concat'で'df'に'hist'を追加
    return df


# エラー時の対処のため"try"の中に入れ子にする
try:
    st.sidebar.write("""
    ## 株価(ドル)
    """)
    ymin, ymax = st.sidebar.slider(
        '表示したいグラフ上の株価の範囲を指定してください。',
        0.0, 300.0, (0.0, 400.0)
    )

    tickers = {                                       # ティッカーを用いて会社名の辞書リストを作成
        'google': 'GOOGL',
        'apple': 'AAPL',
        'meta': 'META',
        'amazon': 'AMZN',
        'microsoft': 'MSFT',
        'netflix': 'NFLX',
        'tesla': 'TSLA',
        'nvidia': 'NVDA',
        'square': 'SQ',
        'visa': 'V',
        'cocacola': 'KO',
        'mcdonald': 'MCD',
        'moderna': 'MRNA',
        'pfizer': 'PFE',
    }
    # 取得したデータを'df’に格納する
    df = get_data(days, tickers)

    # 会社名選択セクションの作成
    companies = st.multiselect(
        '表示したい会社名を選択してください。',
        list(df.index),    # df の Index から会社名を取得
        ['google', 'amazon', 'meta', 'apple', 'microsoft', 'tesla', 'nvidia', 'square', 'visa', 'cocacola', 'mcdonald', 'moderna', 'pfizer',]
    )
    # 選択がなかった場合のエラーと、選択された場合の処理を追加
    if not companies:
        st.error('少なくとも一社は選択してください。')
    else:
        data = df.loc[companies]
        st.write("### 株価(USD)", data.sort_index()) # 株価リストを表示
        data = data.T.reset_index()                 # データ転置
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(USD)'}  # 'Value'カラム名を株価の表示にする
        )

    # チャート表示部分の実装
        st.write("### 株価チャート")
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None),
                color='Name:N'
        )
    )

    st.altair_chart(chart, use_container_width=True)
# エラーメッセージの実装
except:
    st.error(
        "おっと！何かエラーが起きているようです。"
    )

