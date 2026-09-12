let priceChart = null;
let portfolioChart = null;


async function runBacktest() {

    const ticker =
        document.getElementById("ticker").value;

    const capital =
        document.getElementById("capital").value;

    const startDate =
        document.getElementById("startDate").value;

    const endDate =
        document.getElementById("endDate").value;

    const shortWindow =
        document.getElementById("shortWindow").value;

    const longWindow =
        document.getElementById("longWindow").value;


    const loading =
        document.getElementById("loading");

    const results =
        document.getElementById("results");


    loading.classList.remove("hidden");

    results.classList.add("hidden");


    try {

        const response = await fetch(
            "http://127.0.0.1:5000/backtest",
            {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    ticker: ticker,

                    start_date: startDate,

                    end_date: endDate,

                    short_window:
                        Number(shortWindow),

                    long_window:
                        Number(longWindow),

                    initial_capital:
                        Number(capital)

                })

            }
        );


        const data = await response.json();

        /*alert("Backend response received!");*/

        console.log("BACKEND RESPONSE:", data);

        if (!data.success) {
           throw new Error(data.error);
         }

        /*alert("Data received successfully!");*/

        console.log(data);

        displayResults(data);
        createCharts(data);


       /* displayResults(data);

        createCharts(data);*/


    }
    catch (error) {

        alert(
            "Error: " + error.message
        );

        console.error(error);

    }
    finally {

        loading.classList.add("hidden");

    }

}
function displayResults(data) {
    const signal = data.signal;

    // Update Market Overview

document.getElementById("marketTicker").textContent =
    data.ticker;

document.getElementById("currentPrice").textContent =
    formatNumber(
        data.chart_data.prices[
            data.chart_data.prices.length - 1
        ]
    );

document.getElementById("marketSignal").textContent =
    signal.decision;

document.getElementById("marketConfidence").textContent =
    signal.confidence + "%";

document.getElementById("signalDecision").textContent =
    signal.decision;

    const signalElement =
    document.getElementById("signalDecision");

signalElement.classList.remove(
    "signal-buy",
    "signal-sell",
    "signal-hold"
);

if (signal.decision === "BUY") {

    signalElement.classList.add("signal-buy");

} else if (signal.decision === "SELL") {

    signalElement.classList.add("signal-sell");

} else {

    signalElement.classList.add("signal-hold");

}

document.getElementById("signalConfidence").textContent =
    signal.confidence + "%";

document.getElementById("signalRSI").textContent =
    signal.rsi;

document.getElementById("signalMACD").textContent =
    signal.macd;

document.getElementById("signalMACDSignal").textContent =
    signal.macd_signal;


const reasonsList =
    document.getElementById("signalReasons");

reasonsList.innerHTML = "";

signal.reasons.forEach(reason => {

    const li =
        document.createElement("li");

    li.textContent = reason;

    reasonsList.appendChild(li);

});

    const backtest =
        data.backtest;

        document.getElementById("initialCapital").textContent =
         formatNumber(backtest.initial_capital);

        document.getElementById("finalValue").textContent =
         formatNumber(backtest.final_value);

        document.getElementById("profit").textContent =
         formatNumber(backtest.profit);

        document.getElementById("returnPercent").textContent =
         Number(backtest.return_percent || 0).toFixed(2) + "%";

    const analytics =
        data.analytics || {};


    document.getElementById("returnPercent").textContent =
    Number(analytics.total_return_percent || 0).toFixed(2) + "%";

document.getElementById("cagr").textContent =
    Number(analytics.cagr_percent || 0).toFixed(2) + "%";

document.getElementById("drawdown").textContent =
    Number(analytics.max_drawdown_percent || 0).toFixed(2) + "%";

document.getElementById("volatility").textContent =
    Number(analytics.volatility_percent || 0).toFixed(2) + "%";

document.getElementById("sharpe").textContent =
    Number(analytics.sharpe_ratio || 0).toFixed(2);

document.getElementById("totalTrades").textContent =
    analytics.number_of_trades || 0;

document.getElementById("winRate").textContent =
    Number(analytics.win_rate_percent || 0).toFixed(2) + "%";

document.getElementById("bestTrade").textContent =
    formatNumber(analytics.best_trade || 0);

document.getElementById("worstTrade").textContent =
    formatNumber(analytics.worst_trade || 0);

document.getElementById("buyHold").textContent =
    Number(
        analytics.buy_and_hold_return_percent || 0
    ).toFixed(2) + "%";

displayTrades(data.trades);

document.getElementById("results").classList.remove("hidden");

}


function displayTrades(trades) {

    const table =
        document.getElementById(
            "tradeTable"
        );


    table.innerHTML = "";


    trades.forEach(trade => {

        const row =
            document.createElement("tr");


        row.innerHTML = `

            <td>
                ${trade.Date}
            </td>

            <td>
                ${trade.Action}
            </td>

            <td>
                ${formatNumber(trade.Price)}
            </td>

            <td>
                ${trade.Quantity}
            </td>

            <td>
                ${formatNumber(
                    trade.Transaction_Cost
                )}
            </td>

        `;


        table.appendChild(row);

    });

}


function createCharts(data) {

    const chartData =
        data.chart_data;

    const trades =
        data.trades;


    createPriceChart(
        chartData,
        trades
    );

    createPortfolioChart(
    data.portfolio_dates,
    data.portfolio_values
    );
    

}


function createPriceChart(chartData, trades) {

    const canvas =
        document.getElementById(
            "priceChart"
        );


    if (priceChart !== null) {

        priceChart.destroy();

    }


    const dates =
        chartData.dates;


    const prices =
        chartData.prices;


    const shortMA =
        chartData.short_ma;


    const longMA =
        chartData.long_ma;


    /*
     * Create BUY points
     */

    const buyPoints =
        trades
            .filter(
                trade =>
                    trade.Action === "BUY"
            )
            .map(trade => {

                const index =
                    dates.indexOf(
                        trade.Date
                    );

                if (index === -1) {
                    return null;
                }

                return {
                    x: dates[index],
                    y: prices[index]
                };

            })
            .filter(
                point => point !== null
            );


    /*
     * Create SELL points
     */

    const sellPoints =
        trades
            .filter(
                trade =>
                    trade.Action === "SELL"
            )
            .map(trade => {

                const index =
                    dates.indexOf(
                        trade.Date
                    );

                if (index === -1) {
                    return null;
                }

                return {
                    x: dates[index],
                    y: prices[index]
                };

            })
            .filter(
                point => point !== null
            );


    priceChart =
        new Chart(
            canvas,
            {

                type: "line",

                data: {

                    labels: dates,

                    datasets: [

                        {

                            label:
                                "Stock Price",

                            data: prices,

                            borderWidth: 2,

                            pointRadius: 0,

                            tension: 0.1

                        },


                        {

                            label:
                                "Short Moving Average",

                            data: shortMA,

                            borderWidth: 2,

                            pointRadius: 0,

                            tension: 0.1

                        },


                        {

                            label:
                                "Long Moving Average",

                            data: longMA,

                            borderWidth: 2,

                            pointRadius: 0,

                            tension: 0.1

                        },


                        {

                            label: "BUY",

                            data: buyPoints,

                            type: "scatter",

                            pointRadius: 7,

                            pointHoverRadius: 9

                        },


                        {

                            label: "SELL",

                            data: sellPoints,

                            type: "scatter",

                            pointRadius: 7,

                            pointHoverRadius: 9

                        }

                    ]

                },

                options: {

                    responsive: true,

                    interaction: {

                        intersect: false,

                        mode: "index"

                    },

                    scales: {

                        x: {

                            title: {

                                display: true,

                                text: "Date"

                            }

                        },

                        y: {

                            title: {

                                display: true,

                                text:
                                    "Stock Price"

                            }

                        }

                    }

                }

            }
        );

}


function formatNumber(number) {

    return Number(number).toLocaleString(
        "en-IN",
        {
            maximumFractionDigits: 2
        }
    );

}


function createPortfolioChart(dates, values) {

    const canvas =
        document.getElementById("portfolioChart");

    if (portfolioChart !== null) {
        portfolioChart.destroy();
    }

    portfolioChart = new Chart(
        canvas,
        {
            type: "line",

            data: {
                labels: dates,

                datasets: [
                    {
                        label: "Portfolio Value",

                        data: values,

                        borderWidth: 2,

                        pointRadius: 0,

                        tension: 0.2
                    }
                ]
            },

            options: {

                responsive: true,

                interaction: {
                    intersect: false,
                    mode: "index"
                },

                scales: {

                    x: {
                        title: {
                            display: true,
                            text: "Date"
                        }
                    },

                    y: {
                        title: {
                            display: true,
                            text: "Portfolio Value"
                        }
                    }
                }
            }
        }
    );
}

/* =========================================
   WATCHLIST
   ========================================= */

async function analyzeWatchlistStock(ticker) {

    const today = new Date();

    const endDate =
        today.toISOString().split("T")[0];

    const start = new Date();

    start.setFullYear(
        start.getFullYear() - 1
    );

    const startDate =
        start.toISOString().split("T")[0];


    try {

        const response = await fetch(
            "http://127.0.0.1:5000/backtest",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    ticker: ticker,

                    start_date: startDate,

                    end_date: endDate,

                    short_window: 20,

                    long_window: 50,

                    initial_capital: 100000

                })
            }
        );


        const data =
            await response.json();


        if (!data.success) {

            throw new Error(
                data.error
            );

        }


        updateWatchlistCard(
            ticker,
            data
        );


    } catch (error) {

        console.error(
            "Watchlist error:",
            error
        );

    }

}


function updateWatchlistCard(
    ticker,
    data
) {

    const cards =
        document.querySelectorAll(
            ".watchlist-card"
        );


    cards.forEach(card => {

        const tickerElement =
            card.querySelector(
                ".stock-top span"
            );


        if (
            tickerElement &&
            tickerElement.textContent === ticker
        ) {

            const price =
                data.chart_data.prices[
                    data.chart_data.prices.length - 1
                ];


            const signal =
                data.signal;


            const priceElement =
                card.querySelector(
                    ".stock-price span"
                );


            const signalElement =
                card.querySelector(
                    ".watch-signal"
                );


            const infoElements =
                card.querySelectorAll(
                    ".stock-info strong"
                );


            priceElement.textContent =
                formatNumber(price);


            signalElement.textContent =
                signal.decision;


            infoElements[1].textContent =
                signal.confidence + "%";


            signalElement.classList.remove(
                "watch-buy",
                "watch-sell",
                "watch-hold"
            );


            if (
                signal.decision === "BUY"
            ) {

                signalElement.classList.add(
                    "watch-buy"
                );

            }

            else if (
                signal.decision === "SELL"
            ) {

                signalElement.classList.add(
                    "watch-sell"
                );

            }

            else {

                signalElement.classList.add(
                    "watch-hold"
                );

            }

        }

    });

}