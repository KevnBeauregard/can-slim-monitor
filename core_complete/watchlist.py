import json

def load_watchlist(filename="watchlist.json"):
    with open(filename, "r") as f:
        return json.load(f)
