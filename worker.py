import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Fix chemin import core

import time
import threading
import requests
from core.watchlist import load_watchlist
from core.rules import is_valid_breakout
from core.alerts import send_breakout_alert

from flask import Flask

app = Flask(__name__)

@app.route("/")
def ping():
    return "Worker is alive!"

def run_web_server():
    app.run(host="0.0.0.0", port=8080)

def run_worker_loop():
    while True:
        print("🔁 Vérification des actions dans la watchlist...")
        watchlist = load_watchlist()
        for symbol in watchlist:
            print(f"Analyse de {symbol}...")
            try:
                if is_valid_breakout(symbol):
                    send_breakout_alert(symbol)
            except Exception as e:
                print(f"Erreur lors de l'analyse de {symbol}: {e}")
        time.sleep(900)  # 15 minutes

if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    run_worker_loop()
