def run_backtest(data, initial_capital=100000, commission=0.001):

    data = data.copy()

    cash = initial_capital
    shares = 0

    trades = []
    portfolio_values = []

    for i in range(len(data)):

        price = float(data.loc[i, "Close"])
        signal = data.loc[i, "Position"]

        # BUY
        if signal > 0 and shares == 0:

            quantity = int(cash / price)

            if quantity > 0:

                cost = quantity * price
                transaction_cost = cost * commission

                cash -= cost + transaction_cost
                shares = quantity

                trades.append({
                    "Date": data.loc[i, "Date"],
                    "Action": "BUY",
                    "Price": price,
                    "Quantity": quantity,
                    "Transaction_Cost": transaction_cost
                })

        # SELL
        elif signal < 0 and shares > 0:

            revenue = shares * price
            transaction_cost = revenue * commission

            cash += revenue - transaction_cost

            trades.append({
                "Date": data.loc[i, "Date"],
                "Action": "SELL",
                "Price": price,
                "Quantity": shares,
                "Transaction_Cost": transaction_cost
            })

            shares = 0

        # Calculate portfolio value
        portfolio_value = cash + (shares * price)

        portfolio_values.append(portfolio_value)

    # Final portfolio value
    final_price = float(data.iloc[-1]["Close"])

    final_value = cash + (shares * final_price)

    return {
        "initial_capital": initial_capital,
        "final_value": final_value,
        "profit": final_value - initial_capital,
        "return_percent": (
            (final_value - initial_capital)
            / initial_capital
        ) * 100,
        "trades": trades,
        "portfolio_values": portfolio_values
    }


if __name__ == "__main__":

    from data import get_stock_data
    from strategy import moving_average_strategy

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

    print("\n===== BACKTEST RESULTS =====")

    print(
        "Initial Capital:",
        result["initial_capital"]
    )

    print(
        "Final Portfolio Value:",
        round(result["final_value"], 2)
    )

    print(
        "Profit:",
        round(result["profit"], 2)
    )

    print(
        "Return:",
        round(result["return_percent"], 2),
        "%"
    )

    print("\n===== TRADES =====")

    for trade in result["trades"]:
        print(trade)