from flask import Flask, request, jsonify, render_template, redirect
import json, os, requests, urllib.parse
import yfinance as yf
from datetime import datetime

app = Flask(__name__)
SECRET_KEY = "KEVIN2025"
IFTTT_KEY = "oTUrNpQHZE4TXt6vn2Q7-N7okwWLo-euWB1Av-iJR7O"
IFTTT_EVENT = "breakout_alert"
IFTTT_URL = f"https://maker.ifttt.com/trigger/{IFTTT_EVENT}/with/key/{IFTTT_KEY}"

WATCHLIST_FILE = "watchlist.json"
ALERT_LOG_FILE = "alerts.log"


def load_watchlist():
    if not os.path.exists(WATCHLIST_FILE):
        return {}
    with open(WATCHLIST_FILE, "r") as f:
        return json.load(f)


def save_watchlist(data):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(data, f, indent=2)


def log_alert(ticker, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(ALERT_LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {ticker}: {message}\n")
    send_ifttt_alert(ticker, message)


def send_ifttt_alert(ticker, message):
    url = IFTTT_URL + "?" + urllib.parse.urlencode({
        "value1": ticker,
        "value2": message
    })
    try:
        requests.get(url)
    except:
        pass  # Ignore push failures silently


def is_market_unstable():
    sp = yf.Ticker("^GSPC").history(period="60d")
    closes, vols = sp["Close"], sp["Volume"]
    mm50 = closes.rolling(50).mean()
    distribution_days = 0
    for i in range(-20, -1):
        if (closes.iloc[i] - closes.iloc[i + 1]
            ) / closes.iloc[i] > 0.002 and vols.iloc[i + 1] > vols.iloc[i]:
            distribution_days += 1
    return closes.iloc[-1] < mm50.iloc[-1] and distribution_days >= 4


def check_breakout(ticker):
    df = yf.Ticker(ticker).history(period="90d")
    high20 = df["Close"].rolling(20).max()
    avg_vol = df["Volume"].rolling(50).mean()
    if df["Close"].iloc[-1] > high20.iloc[-2] and df["Volume"].iloc[
            -1] > 1.3 * avg_vol.iloc[-1]:
        return True, df["Close"].iloc[-1]
    return False, None


def check_sell_rules(ticker, entry):
    df = yf.Ticker(ticker).history(period="60d")
    close = df["Close"]
    alerts = []
    now = close.iloc[-1]
    if now <= entry * 0.93:
        alerts.append("⚠️ Perte > 7% — Règle de vente")
    mm50 = close.rolling(50).mean()
    if now < mm50.iloc[-1]:
        alerts.append("📉 Sous MM50")
    gain = (now - entry) / entry
    if gain >= 0.20 and (close.index[-1] - close.index[-40]).days < 56:
        alerts.append("✅ Gain rapide +20% en <8 sem.")
    return alerts


@app.route("/")
def home():
    watchlist = load_watchlist()
    unstable = is_market_unstable()
    if unstable:
        log_alert("Marché", "⚠️ Marché instable — réduire exposition")
    for ticker, entry in watchlist.items():
        for msg in check_sell_rules(ticker, entry):
            log_alert(ticker, msg)
        breakout, price = check_breakout(ticker)
        if breakout:
            log_alert(ticker, f"🚀 Breakout CAN SLIM détecté à {price:.2f}")
    return render_template("index.html")


@app.route("/watchlist")
def view_watchlist():
    raw = load_watchlist()
    extended = {}
    for ticker, entry in raw.items():
        try:
            df = yf.Ticker(ticker).history(period="2d")
            current_price = df["Close"].iloc[-1]
            change = ((current_price - entry) / entry) * 100
            extended[ticker] = {
                "entry": entry,
                "current": round(current_price, 2),
                "change": round(change, 2)
            }
        except:
            extended[ticker] = {
                "entry": entry,
                "current": None,
                "change": None
            }
    return render_template("watchlist.html", watchlist=extended)


@app.route("/alerts")
def view_alerts():
    if not os.path.exists(ALERT_LOG_FILE):
        return "Aucune alerte pour l’instant."
    with open(ALERT_LOG_FILE) as f:
        lines = f.readlines()[-100:]
    return render_template("alerts.html", alerts=lines)


@app.route("/update", methods=["POST"])
def update_watchlist():
    key = request.form.get("key")
    if key != SECRET_KEY:
        return "Clé invalide", 403
    ticker = request.form["ticker"].upper()
    price = float(request.form["price"])
    data = load_watchlist()
    data[ticker] = price
    save_watchlist(data)
    return redirect("/watchlist")


@app.route("/delete", methods=["POST"])
def delete_watchlist():
    key = request.form.get("key")
    if key != SECRET_KEY:
        return "Clé invalide", 403
    ticker = request.form["ticker"].upper()
    data = load_watchlist()
    if ticker in data:
        del data[ticker]
        save_watchlist(data)
    return redirect("/watchlist")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
