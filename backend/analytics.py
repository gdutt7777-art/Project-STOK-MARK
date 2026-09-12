import pandas as pd
import numpy as np


def calculate_analytics(data, backtest_result):

    initial_capital = backtest_result["initial_capital"]
    final_value = backtest_result["final_value"]
    trades = backtest_result["trades"]
    portfolio_values = backtest_result["portfolio_values"]

    # --------------------------------
    # 1. Total Return
    # --------------------------------

    total_return = (
        (final_value - initial_capital)
        / initial_capital
    ) * 100

    # --------------------------------
    # 2. Number of Trades
    # --------------------------------

    number_of_trades = len(trades)

    # --------------------------------
    # 3. Calculate Trade Profits
    # --------------------------------

    trade_profits = []

    buy_price = None
    buy_quantity = None

    for trade in trades:

        if trade["Action"] == "BUY":

            buy_price = trade["Price"]
            buy_quantity = trade["Quantity"]

        elif trade["Action"] == "SELL" and buy_price is not None:

            sell_price = trade["Price"]

            profit = (
                (sell_price - buy_price)
                * buy_quantity
            )

            trade_profits.append(profit)

            buy_price = None
            buy_quantity = None

    # --------------------------------
    # 4. Winning and Losing Trades
    # --------------------------------

    winning_trades = [
        profit for profit in trade_profits
        if profit > 0
    ]

    losing_trades = [
        profit for profit in trade_profits
        if profit < 0
    ]

    if len(trade_profits) > 0:

        win_rate = (
            len(winning_trades)
            / len(trade_profits)
        ) * 100

    else:

        win_rate = 0

    # --------------------------------
    # 5. Best and Worst Trade
    # --------------------------------

    if trade_profits:

        best_trade = max(trade_profits)
        worst_trade = min(trade_profits)

    else:

        best_trade = 0
        worst_trade = 0

    # --------------------------------
    # 6. Maximum Drawdown
    # --------------------------------

    portfolio_series = pd.Series(
        portfolio_values
    )

    running_max = portfolio_series.cummax()

    drawdown = (
        portfolio_series - running_max
    ) / running_max

    drawdown = drawdown.replace(
        [np.inf, -np.inf],
        np.nan
    ).dropna()

    if len(drawdown) > 0:

        max_drawdown = drawdown.min() * 100

    else:

        max_drawdown = 0

    # --------------------------------
    # 7. Daily Returns
    # --------------------------------

    daily_returns = portfolio_series.pct_change()

    daily_returns = daily_returns.replace(
        [np.inf, -np.inf],
        np.nan
    ).dropna()

    daily_returns = daily_returns[
        np.isfinite(daily_returns)
    ]

    # --------------------------------
    # 8. Volatility
    # --------------------------------

    if len(daily_returns) > 1:

        volatility = (
            daily_returns.std()
            * np.sqrt(252)
            * 100
        )

    else:

        volatility = 0

    # --------------------------------
    # 9. Sharpe Ratio
    # --------------------------------

    if (
        len(daily_returns) > 1
        and daily_returns.std() != 0
    ):

        sharpe_ratio = (
            daily_returns.mean()
            / daily_returns.std()
        ) * np.sqrt(252)

    else:

        sharpe_ratio = 0

    # --------------------------------
    # 10. CAGR
    # --------------------------------

    start_date = pd.to_datetime(
        data["Date"].iloc[0]
    )

    end_date = pd.to_datetime(
        data["Date"].iloc[-1]
    )

    years = (
        end_date - start_date
    ).days / 365.25

    if (
        years > 0
        and final_value > 0
        and initial_capital > 0
    ):

        cagr = (
            (final_value / initial_capital)
            ** (1 / years)
            - 1
        ) * 100

    else:

        cagr = 0

    # --------------------------------
    # 11. Buy & Hold Return
    # --------------------------------

    first_price = float(
        data["Close"].iloc[0]
    )

    last_price = float(
        data["Close"].iloc[-1]
    )

    if first_price > 0:

        buy_hold_return = (
            (last_price - first_price)
            / first_price
        ) * 100

    else:

        buy_hold_return = 0

    # --------------------------------
    # Final NaN / Infinity Protection
    # --------------------------------

    def safe_number(value):

        if pd.isna(value) or not np.isfinite(value):
            return 0

        return float(value)

    # --------------------------------
    # Return All Analytics
    # --------------------------------

    return {

        "total_return_percent":
            safe_number(total_return),

        "cagr_percent":
            safe_number(cagr),

        "max_drawdown_percent":
            safe_number(max_drawdown),

        "volatility_percent":
            safe_number(volatility),

        "sharpe_ratio":
            safe_number(sharpe_ratio),

        "number_of_trades":
            number_of_trades,

        "winning_trades":
            len(winning_trades),

        "losing_trades":
            len(losing_trades),

        "win_rate_percent":
            safe_number(win_rate),

        "best_trade":
            safe_number(best_trade),

        "worst_trade":
            safe_number(worst_trade),

        "buy_and_hold_return_percent":
            safe_number(buy_hold_return)

    }


# --------------------------------
# TESTING
# --------------------------------

if __name__ == "__main__":

    from data import get_stock_data
    from strategy import moving_average_strategy
    from backtest import run_backtest

    data = get_stock_data(
        "RELIANCE.NS",
        "2024-01-01",
        "2026-01-01"
    )

    data = moving_average_strategy(
        data,
        short_window=20,
        long_window=50
    )

    result = run_backtest(
        data,
        initial_capital=100000,
        commission=0.001
    )

    analytics = calculate_analytics(
        data,
        result
    )

    print("\n===== ANALYTICS =====")

    for key, value in analytics.items():

        print(
            key,
            ":",
            round(value, 2)
            if isinstance(value, (int, float))
            else value
        )






if __name__ == "__main__":

    from data import get_stock_data
    from strategy import moving_average_strategy
    from backtest import run_backtest

    data = get_stock_data(
        "RELIANCE.NS",
        "2024-01-01",
        "2026-01-01"
    )

    data = moving_average_strategy(
        data,
        short_window=20,
        long_window=50
    )

    result = run_backtest(
        data,
        initial_capital=100000,
        commission=0.001
    )

    analytics = calculate_analytics(
        data,
        result
    )

    print("\n===== ANALYTICS =====")

    for key, value in analytics.items():

        print(
            key,
            ":",
            round(value, 2)
            if isinstance(value, (int, float))
            else value
        )