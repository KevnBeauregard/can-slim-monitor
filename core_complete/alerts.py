import requests

def send_breakout_alert(symbol):
    url = "https://maker.ifttt.com/trigger/breakout_alert/with/key/oTUrNpQHZE4TXt6vn2Q7-N7okwWLo-euWB1Av-iJR7O"
    payload = {"value1": symbol}
    try:
        requests.post(url, json=payload)
        print(f"✅ Alerte envoyée pour {symbol}")
    except Exception as e:
        print(f"❌ Échec de l'alerte pour {symbol}: {e}")
