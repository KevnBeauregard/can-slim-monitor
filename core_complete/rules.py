import yfinance as yf

def is_valid_breakout(symbol):
    data = yf.download(symbol, period="6mo", interval="1d", progress=False)
    if data.empty or len(data) < 30:
        return False

    last_close = data["Close"].iloc[-1]
    prev_highs = data["Close"].iloc[-30:-1]
    recent_volume = data["Volume"].iloc[-1]
    avg_volume = data["Volume"].iloc[-30:-1].mean()

    breakout = last_close > prev_highs.max() and recent_volume > avg_volume * 1.5
    return breakout
