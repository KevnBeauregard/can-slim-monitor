import logging
from datetime import datetime
import requests
from .config import ALERT_LOG_FILE, IFTTT_URL

logging.basicConfig(
    filename=ALERT_LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def log_alert(ticker, message):
    logging.info(f"{ticker}: {message}")
    send_ifttt_alert(ticker, message)

def send_ifttt_alert(ticker, message):
    try:
        url = IFTTT_URL
        payload = {"value1": ticker, "value2": message}
        requests.post(url, json=payload)
    except Exception as e:
        logging.error(f"Erreur IFTTT pour {ticker}: {e}")