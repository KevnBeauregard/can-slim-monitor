import requests
from core.config import IFTTT_WEBHOOK_URL

def send_ifttt_alert(message):
    data = {"value1": message}
    try:
        response = requests.post(IFTTT_WEBHOOK_URL, json=data)
        response.raise_for_status()
        print("Alerte IFTTT envoyée :", message)
    except Exception as e:
        print("Erreur lors de l'envoi IFTTT :", e)