from flask import Flask, render_template, request, redirect
from core.watchlist import load_watchlist, save_watchlist
from core.market import is_market_unstable
from core.rules import check_breakout, check_sell_rules
from core.alerts import log_alert
from core.scoring import score_canslim
import yfinance as yf

app = Flask(__name__)

@app.route("/")
def index():
    data = []
    watchlist = load_watchlist()

    for ticker, entry in watchlist.items():
        try:
            info = yf.Ticker(ticker).info
            score = score_canslim(ticker)

            data.append({
                "ticker": ticker,
                "company": info.get("shortName", ""),
                "price": info.get("regularMarketPrice", 0),
                "score": score,
                "sector": info.get("sector", ""),
                "eps": info.get("trailingEps", "N/A"),
                "volume": info.get("volume", 0),
                "marketCap": info.get("marketCap", 0),
                "buy_price": entry.get("buy_price", ""),
                "graph_url": f"https://quickchart.io/chart?c={{type:'sparkline',data:{{datasets:[{{data:[{','.join(str(p) for p in yf.Ticker(ticker).history(period='14d')['Close'].tolist())}]}}]}}}}"
            })
        except Exception as e:
            print(f"Erreur pour {ticker}: {e}")

    unstable = is_market_unstable()
    return render_template("watchlist.html", data=data, unstable=unstable)

@app.route("/add", methods=["POST"])
def add_stock():
    ticker = request.form.get("ticker").upper()
    price = float(request.form.get("buy_price", 0))
    watchlist = load_watchlist()
    watchlist[ticker] = {"buy_price": price}
    save_watchlist(watchlist)
    return redirect("/")

@app.route("/delete/<ticker>")
def delete_stock(ticker):
    watchlist = load_watchlist()
    if ticker in watchlist:
        del watchlist[ticker]
        save_watchlist(watchlist)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)