import yfinance as yf

def score_canslim(ticker):
    score = 0
    stock = yf.Ticker(ticker)
    info = stock.info

    # C: Current earnings (estimation via EPS trend)
    try:
        eps_current = info.get("trailingEps", 0)
        eps_growth = info.get("earningsQuarterlyGrowth", 0)
        if eps_growth and eps_growth > 0.2:
            score += 1
    except: pass

    # A: Annual earnings
    try:
        if info.get("revenueGrowth", 0) > 0.25:
            score += 1
    except: pass

    # N: New highs / products
    try:
        price = info.get("regularMarketPrice", 0)
        high_52 = info.get("fiftyTwoWeekHigh", 0)
        if price >= 0.98 * high_52:
            score += 1
    except: pass

    # S: Supply/Demand (volume + float)
    try:
        float_shares = info.get("floatShares", 1)
        avg_volume = info.get("averageVolume", 0)
        if avg_volume > float_shares * 0.01:
            score += 1
    except: pass

    # L: Leader (momentum)
    try:
        if info.get("beta", 0) > 1.2:
            score += 1
    except: pass

    # I: Institutional Sponsorship
    try:
        inst_pct = info.get("heldPercentInstitutions", 0)
        if inst_pct > 0.4:
            score += 1
    except: pass

    # M: Market Direction (à évaluer ailleurs)
    # Ce critère sera injecté via main.py

    return score