import yfinance as yf

def fetch_stock_data(ticker, start_date, end_date, interval="1d"):
    """
    Fetch historical stock data from Yahoo Finance.

    Parameters:
    - ticker (str): Stock ticker symbol (e.g., "TSLA").
    - start_date (str): Start date in "YYYY-MM-DD" format.
    - end_date (str): End date in "YYYY-MM-DD" format.
    - interval (str): Data interval ("1d", "1wk", "1mo", etc.).

    Returns:
    - pd.DataFrame: DataFrame containing historical stock data.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date, interval=interval)
    return data


# TODO: mozna neco z tohoto?:
'''
# 2. Info o firmě
tsla = yf.Ticker("TSLA")
print(tsla.info)  # slovník s fundamenty, sektorem, P/E, tržní kapitalizací...

Volitelné parametry:
auto_adjust=True (přepočítá ceny o splity a dividendy)

# 6. Finanční výkazy
print(tsla.financials)        # výkaz zisku a ztráty
print(tsla.balance_sheet)     # rozvaha
print(tsla.cashflow)          # cashflow
'''