import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'can_slim_worker_final/core'))

from core.config import LOOP_INTERVAL_SECONDS

import time
import threading
import logging
from flask import Flask

# Ajout du dossier parent au path pour les imports locaux
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.watchlist import load_watchlist
from core.rules import is_valid_breakout
from core.alerts import send_breakout_alert
from core.config import LOOP_INTERVAL_SECONDS

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

app = Flask(__name__)

@app.route("/")
def ping():
    return "Worker is alive!"

def run_web_server():
    app.run(host="0.0.0.0", port=8080)

def run_worker_loop():
    while True:
        logging.info("🔁 Vérification des actions dans la watchlist...")
        watchlist = load_watchlist()
        if not watchlist:
            logging.warning("🚫 Watchlist vide ou non chargée.")
            time.sleep(LOOP_INTERVAL_SECONDS)
            continue

        for symbol in watchlist:
            logging.info(f"🔎 Analyse de {symbol}...")
            try:
                if is_valid_breakout(symbol):
                    send_breakout_alert(symbol)
            except Exception as e:
                logging.error(f"❌ Erreur lors de l'analyse de {symbol} : {e}")

        time.sleep(LOOP_INTERVAL_SECONDS)  # Pause entre chaque boucle

if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    run_worker_loop()
