from flask import Flask, request, jsonify
from flask_cors import CORS

from data import get_stock_data
from strategy import moving_average_strategy
from backtest import run_backtest
from analytics import calculate_analytics
from signal_engine import generate_signal


app = Flask(__name__)

CORS(app)


@app.route("/")
def home():

    return jsonify({
        "message": "Algorithmic Trading Simulator API is running!"
    })


@app.route("/backtest", methods=["POST"])
def backtest():

    try:

        # Get data sent by frontend
        request_data = request.get_json()

        if not request_data:
         raise ValueError("No input data received.")

        ticker = request_data.get(
            "ticker",
            "RELIANCE.NS"
        )

        if not ticker:
         raise ValueError("Ticker symbol is required.")

        start_date = request_data.get(
            "start_date",
            "2024-01-01"
        )

        end_date = request_data.get(
            "end_date",
            "2026-01-01"
        )

        short_window = int(
            request_data.get(
                "short_window",
                20
            )
        )

        long_window = int(
            request_data.get(
                "long_window",
                50
            )
        )

        if short_window <= 0 or long_window <= 0:
         raise ValueError(
        "Moving average windows must be greater than 0."
        )

        if short_window >= long_window:
         raise ValueError(
        "Short MA must be smaller than Long MA."
        )

        initial_capital = float(
            request_data.get(
                "initial_capital",
                100000
            )
        )

        if initial_capital <= 0:
         raise ValueError(
        "Initial capital must be greater than 0."
        )
        
        if start_date >= end_date:
          raise ValueError(
            "Start Date must be before end date."
    )

        # --------------------------------
        # Get historical stock data
        # --------------------------------

        data = get_stock_data(
            ticker,
            start_date,
            end_date
        )

        # --------------------------------
        # Apply trading strategy
        # --------------------------------

        data = moving_average_strategy(
            data,
            short_window,
            long_window
        )

        # --------------------------------
        # Run backtest
        # --------------------------------

        result = run_backtest(
            data,
            initial_capital=initial_capital,
            commission=0.001
        )

        # --------------------------------
        # Calculate analytics
        # --------------------------------

        analytics = calculate_analytics(
            data,
            result
        )

        if analytics is None:
         analytics = {}

        signal = generate_signal(data)

        # --------------------------------
        # Send response
        # --------------------------------

        return jsonify({

    "success": True,

    "ticker": ticker,

    "signal": signal,

    "backtest": {

        "initial_capital":
            result["initial_capital"],

        "final_value":
            result["final_value"],

        "profit":
            result["profit"],

        "return_percent":
            result["return_percent"]

    },

    "analytics": analytics,

    "trades": result["trades"],

    "portfolio_dates":
    data["Date"].dt.strftime(
        "%Y-%m-%d"
    ).tolist(),

    "portfolio_values":
     result["portfolio_values"],

    "chart_data": {

        "dates":
            data["Date"].dt.strftime(
                "%Y-%m-%d"
            ).tolist(),

        "prices":
            data["Close"].astype(float).tolist(),

        "short_ma":
            data["Short_MA"]
            .fillna(0)
            .astype(float)
            .tolist(),

        "long_ma":
            data["Long_MA"]
            .fillna(0)
            .astype(float)
            .tolist()

    }

})


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )