import pandas as pd


def calculate_rsi(data, period=14):

    delta = data["Close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    average_gain = gain.rolling(
        window=period
    ).mean()

    average_loss = loss.rolling(
        window=period
    ).mean()

    relative_strength = (
        average_gain / average_loss
    )

    rsi = 100 - (
        100 / (1 + relative_strength)
    )

    return rsi


def calculate_macd(data):

    short_ema = data["Close"].ewm(
        span=12,
        adjust=False
    ).mean()

    long_ema = data["Close"].ewm(
        span=26,
        adjust=False
    ).mean()

    macd = short_ema - long_ema

    signal = macd.ewm(
        span=9,
        adjust=False
    ).mean()

    return macd, signal


def generate_signal(data):

    data = data.copy()

    # RSI
    data["RSI"] = calculate_rsi(data)

    # MACD
    data["MACD"], data["MACD_Signal"] = \
        calculate_macd(data)

    # Latest row
    latest = data.iloc[-1]

    score = 0
    reasons = []

    # -----------------------------
    # Moving Average Signal
    # -----------------------------

    if latest["Short_MA"] > latest["Long_MA"]:

        score += 1

        reasons.append(
            "Short moving average is above long moving average."
        )

    elif latest["Short_MA"] < latest["Long_MA"]:

        score -= 1

        reasons.append(
            "Short moving average is below long moving average."
        )

    # -----------------------------
    # RSI Signal
    # -----------------------------

    rsi = latest["RSI"]

    if pd.isna(rsi):
       rsi = 50

    if rsi < 30:

        score += 1

        reasons.append(
            "RSI indicates potentially oversold conditions."
        )

    elif rsi > 70:

        score -= 1

        reasons.append(
            "RSI indicates potentially overbought conditions."
        )

    else:

        reasons.append(
            "RSI is in a neutral range."
        )

    # -----------------------------
    # MACD Signal
    # -----------------------------

    if latest["MACD"] > latest["MACD_Signal"]:

        score += 1

        reasons.append(
            "MACD is above its signal line."
        )

    else:

        score -= 1

        reasons.append(
            "MACD is below its signal line."
        )

    # -----------------------------
    # Final Decision
    # -----------------------------

    if score >= 2:

        decision = "BUY"

    elif score <= -2:

        decision = "SELL"

    else:

        decision = "HOLD"

    # -----------------------------
    # Confidence
    # -----------------------------

    confidence = (
        abs(score) / 3
    ) * 100

    return {

        "decision": decision,

        "confidence": round(
            confidence,
            2
        ),

        "score": score,

        "rsi": round(
            float(rsi),
            2
        ),

        "macd": round(
            float(latest["MACD"]),
            4
        ),

        "macd_signal": round(
            float(latest["MACD_Signal"]),
            4
        ),

        "reasons": reasons
    }