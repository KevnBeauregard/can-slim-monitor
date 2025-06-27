import time
import json
import requests
from core.watchlist import load_watchlist
from core.fetch import get_price
from core.rules import check_breakout_canslim
from core.alerts import send_ifttt_alert
from core.config import CHECK_INTERVAL

def check_alerts():
    watchlist = load_watchlist()
    triggered = []

    for stock in watchlist:
        current_price = get_price(stock["ticker"])
        buy_price = stock.get("buy_price")

        if not current_price or not buy_price:
            continue

        # Détection breakout CAN SLIM
        triggered_breakout, info = check_breakout_canslim(stock["ticker"])
        if triggered_breakout:
            triggered.append(f"{stock['ticker']} breakout confirmé : {info}")

        # Signaux de vente
        if current_price > buy_price * 1.01:
            triggered.append(f"{stock['ticker']} a dépassé le prix d'achat ({current_price:.2f} > {buy_price:.2f})")
        elif current_price < buy_price * 0.92:
            triggered.append(f"{stock['ticker']} a chuté de plus de 8% ({current_price:.2f} < {buy_price:.2f})")

    if triggered:
        message = "📈 Alerte CAN SLIM :\n\n" + "\n".join(triggered)
        send_ifttt_alert(message)

if __name__ == "__main__":
    print("Worker CAN SLIM lancé.")
    while True:
        try:
            check_alerts()
        except Exception as e:
            print(f"Erreur dans le worker : {e}")
        time.sleep(CHECK_INTERVAL)