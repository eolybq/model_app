import yfinance as yf
import pandas as pd

def fetch_save_ticker(ticker):
    """
    Fetch and save historical stock data from Yahoo Finance to csv.

    Parameters:
    - ticker (str): Stock ticker symbol (e.g., "TSLA").

    Returns:
    - pd.DataFrame: DataFrame containing historical stock data.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period='max', interval='1d')

    data["date"] = pd.to_datetime(data["date"]).dt.strftime('%Y-%m-%d')
    data.to_csv(f"data/{ticker}.csv")

    return data


def load_user_data(ticker, period, interval):
    """
    Takes
    - ticker (str): Stock ticker symbol (e.g., "TSLA").
    - period (str): Data period ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max").
    - interval (str): Data interval ("1d", "1wk", "1mo", etc.).
    """

# TODO: mozna neco z tohoto?:
'''
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