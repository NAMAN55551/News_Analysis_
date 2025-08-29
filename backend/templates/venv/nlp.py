import requests
import json

NEWS_API_KEY = "add your api"
BASE_URL_TOP = "https://newsapi.org/v2/top-headlines"
BASE_URL_EVERYTHING = "https://newsapi.org/v2/everything"

def fetch_news(query=None, country=None, sources=None, page_size=50, use_everything=False):
    if use_everything:
        url = BASE_URL_EVERYTHING
        params = {
            "apiKey": NEWS_API_KEY,
            "q": query or "",
            "pageSize": page_size
        }
        if sources:
            params["sources"] = sources
    else:
        url = BASE_URL_TOP
        params = {"apiKey": NEWS_API_KEY, "pageSize": page_size}
        if sources:
            params["sources"] = sources
        elif country:
            params["country"] = country
        if query:
            params["q"] = query

    resp = requests.get(url, params=params)
    print("DEBUG URL:", resp.url)
    if resp.status_code == 200:
        data = resp.json()
        return data.get("articles", [])
    else:
        raise Exception(f"Error fetching news: {resp.status_code} {resp.text}")

def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    categories = {
        "politics": {"query": "politics", "use_everything": True},
        "sports": {"country": "us", "use_everything": False},
        "entertainment": {"country": "us", "use_everything": False},
        "economics": {"query": "economics", "use_everything": True},
        "environment": {"query": "environment", "use_everything": True}
    }

    all_news = {}

    for cat, params in categories.items():
        print(f"Fetching {cat} news...")
        try:
            articles = fetch_news(
                query=params.get("query"),
                country=params.get("country"),
                page_size=50,
                use_everything=params.get("use_everything", False)
            )
            all_news[cat] = articles
            print(f"Fetched {len(articles)} articles for {cat}")
        except Exception as e:
            print(f"Failed to fetch {cat} news: {e}")

    save_to_json(all_news, "all_news.json")
    print("All news saved to all_news.json")
