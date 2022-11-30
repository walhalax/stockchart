import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('米国株価可視化アプリ')

# サイドバーに表示する文言を登録
st.sidebar.write("""
# GAFA株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定してください。
""")

st.sidebar.write("""
## 表示日数選択
""")

# 表j日数変更のためのスライダーを追加
# 作成済みのコードに合わせるために日数を'days'で定義
days = st.sidebar.slider('日数', 1, 50 ,20)

# メイン画面の表示文言を登録
# 日数は可変されるので日数部分にfstringsメソッドを置く
st.write(f"""
### 過去 **{days}日間**のGAFAの株価
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


