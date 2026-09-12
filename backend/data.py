
import yfinance as yf
import pandas as pd


def get_stock_data(ticker, start_date, end_date):

    data = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=True
    )

    if data.empty:
        raise ValueError("No stock data found.")

    # Handle multi-level columns returned by some yfinance versions
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.reset_index()

    return data


if __name__ == "__main__":

    ticker = "RELIANCE.NS"

    data = get_stock_data(
        ticker,
        "2024-01-01",
        "2026-01-01"
    )

    print(data.head())
    print("\nTotal rows:", len(data))