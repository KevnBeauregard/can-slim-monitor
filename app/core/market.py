import yfinance as yf

def is_market_unstable():
    try:
        qqq = yf.Ticker("QQQ")
        hist = qqq.history(period="5d")
        drop_count = sum(hist["Close"].pct_change().dropna() < -0.01)
        return drop_count >= 3
    except Exception:
        return False