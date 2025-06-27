import yfinance as yf

def check_breakout_canslim(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="60d")
    if hist.empty or len(hist) < 20:
        return False, None

    # 1. Détection de la base plate (zone de consolidation)
    base = hist[-20:-5]  # 15 derniers jours sauf la dernière semaine
    resistance = base['Close'].max()

    today = hist.iloc[-1]
    prev = hist.iloc[-2]

    # 2. Nouveau sommet annuel ou proche (≥ 98% du plus haut 52 semaines)
    high_52 = hist['Close'].rolling(252, min_periods=1).max().iloc[-1]
    near_52 = today['Close'] >= 0.98 * high_52

    # 3. Volume élevé (≥ 140% moyenne 50 jours)
    avg_vol = hist['Volume'].rolling(50).mean().iloc[-1]
    vol_break = today['Volume'] >= 1.4 * avg_vol

    # 4. Cassure de résistance + clôture forte ou gap-up
    price_break = today['Close'] > resistance
    close_strong = today['Close'] >= today['High']
    gap_up = today['Open'] > prev['High']

    triggered = near_52 and vol_break and price_break and (close_strong or gap_up)

    return bool(triggered), {
        "price": round(today['Close'], 2),
        "resistance": round(resistance, 2),
        "vol": int(today['Volume']),
        "avg_vol": int(avg_vol),
        "high_52": round(high_52, 2)
    }