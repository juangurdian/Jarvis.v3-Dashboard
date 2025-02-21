import requests

def fetch_trending_crypto():
    url = "https://api.dexscreener.com/latest/dex/trending"
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/105.0.0.0 Safari/537.36")
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        print("[CRYPTO] Fetched data:", data)
        return data
    except Exception as e:
        print("[CRYPTO] Error fetching trending crypto:", e)
        return {"pairs": []}
