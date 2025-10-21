import yfinance as yf
import pandas as pd
import numpy as np


# fetch a ulozeni z yahoo finance
def fetch_save_ticker(ticker):
    # TODO: osetrit pokud ticker neexistuje
    ticker = ticker.upper()
    stock = yf.Ticker(ticker)
    data = stock.history(period='max', interval='1d')

    # odstraneni timezone
    data.index = data.index.tz_localize(None)

    data.columns = data.columns.str.lower()
    data = data.drop(columns=['dividends', 'stock splits'], axis=1)
    data["log_return"] = np.log(data["close"] / data["close"].shift(1))
    data = data.dropna()

    # presun date z indexu do sloupce a vytvoreni ciselneho indexu -> lepsi manipulace s daty
    # NOTE: musi se opravit index aby zacinal od 0 kvuli odhozenemu prvnimu radku NA
    data = data.reset_index(names='date')
    data['date'] = pd.to_datetime(data['date'])



    data.to_csv(f"data/{ticker}.csv", index=False)
    return data


# nahrani dat z csv, orezani dle start a end, prevod na zvoleny interval
def load_user_data(ticker, start, end, interval="1d"):
    ticker = ticker.upper()
    df = pd.read_csv(f"data/{ticker}.csv")
    df['date'] = pd.to_datetime(df['date'])

    start = start
    end = end

    df = df[(df["date"] >= start) & (df["date"] <= end)]

    if interval == "1week":
        # Weekly OHLCV s obchodní den nastaveno na realny posledni obchodni den v tydnu
        df = df.groupby(pd.Grouper(key='date', freq='W-FRI'), as_index = False).agg({
            "date": "last",
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum"
            
        })

    if interval == "1month":
        # Monthly OHLCV s obchodní den realny posledni obchodni den v mesici
        df = df.groupby(pd.Grouper(key='date', freq='M'), as_index = False).agg({
            "date": "last",
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum"
        })

    if interval == "3month":
        # Monthly OHLCV s obchodní den realny posledni obchodni den v mesici
        df = df.groupby(pd.Grouper(key='date', freq='3M'), as_index = False).agg({
            "date": "last",
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum"
        })

    return df



'''
TODO: mozna neco z tohoto?:
# 2. Info o firmě
Volitelné parametry:
auto_adjust=True (přepočítá ceny o splity a dividendy)

tsla = yf.Ticker("TSLA")
print(tsla.info)  # slovník s fundamenty, sektorem, P/E, tržní kapitalizací...

# 6. Finanční výkazy
print(tsla.financials)        # výkaz zisku a ztráty
print(tsla.balance_sheet)     # rozvaha
print(tsla.cashflow)          # cashflow
'''