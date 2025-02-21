# backend/app.py
import requests
import os

# Make sure you have your NewsAPI key stored securely.
# You can either set it as an environment variable or paste it here directly.
NEWS_API_KEY = 'fc37cdb2bbae4dd89f6dcaca589ef8ac'

def fetch_latest_news(query=None):
    """
    Fetch the latest news articles using NewsAPI.org.
    If a query is provided, it searches for that topic; otherwise, it uses a default query.
    """
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": 10,  # Limit the number of articles
        "country": "us"  # Focus on US news (adjust as needed)
    }
    # Default query: Focus on tech companies, AI, US politics, etc.
    if query:
        params["q"] = query
    else:
        params["q"] = "tech OR AI OR 'US politics' OR technology"

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()  # Contains an 'articles' key
    else:
        print("[NEWS] Error fetching news:", response.status_code, response.text)
        return {"articles": []}
