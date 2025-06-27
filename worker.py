import time
from datetime import datetime
from main import load_watchlist, is_market_unstable, check_breakout, check_sell_rules, log_alert

def check_stocks_daily():
    print(f"[{datetime.now()}] Vérification des actions en cours...")
    watchlist = load_watchlist()

    if is_market_unstable():
        log_alert("Marché", "⚠️ Marché instable — réduire exposition")

    for ticker, entry in watchlist.items():
        # Vérifie les règles de vente
        for msg in check_sell_rules(ticker, entry):
            log_alert(ticker, msg)

        # Vérifie les breakouts
        breakout, price = check_breakout(ticker)
        if breakout:
            log_alert(ticker, f"🚀 Breakout CAN SLIM détecté à {price:.2f}")

if __name__ == "__main__":
    while True:
        check_stocks_daily()
        time.sleep(15 * 60)  # toutes les 15 minutes
