import yfinance as yf

def check_breakout(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="15d")
        recent_high = hist["Close"][-10:-1].max()
        current_price = hist["Close"].iloc[-1]
        breakout = current_price > recent_high * 1.03
        return breakout, current_price
    except Exception:
        return False, None

def check_sell_rules(ticker, entry):
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")["Close"].iloc[-1]
        alerts = []
        if "buy_price" in entry and price < entry["buy_price"] * 0.93:
            alerts.append("🔻 -7% stop loss déclenché")
        return alerts
    except Exception:
        return []