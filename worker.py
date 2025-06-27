import time
from datetime import datetime
from core.watchlist import load_watchlist
from core.market import is_market_unstable
from core.rules import check_breakout, check_sell_rules
from core.alerts import log_alert

def check_stocks():
    print(f"[{datetime.now()}] Vérification des actions...")
    watchlist = load_watchlist()

    if is_market_unstable():
        log_alert("MARCHÉ", "⚠️ Le marché est instable. Prudence.")

    for ticker, entry in watchlist.items():
        for msg in check_sell_rules(ticker, entry):
            log_alert(ticker, msg)

        breakout, price = check_breakout(ticker)
        if breakout:
            log_alert(ticker, f"🚀 Breakout détecté à {price:.2f}")

if __name__ == "__main__":
    while True:
        start = time.time()
        check_stocks()
        elapsed = time.time() - start
        time.sleep(max(0, 15 * 60 - elapsed))