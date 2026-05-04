import feedparser
from datetime import datetime

LATAM_FUNDING_QUERIES = [
    "Chile startup funding round",
    "Colombia fintech funding",
    "Peru startup investment",
    "Ecuador startup funding",
    "Mexico startup venture capital",
    "Brazil startup funding",
    "Argentina startup investment",
    "LATAM startup funding",
    "Latin America venture capital",
]

def fetch_funding_news_google():
    """Pull funding news from Google News RSS -- no API key needed"""
    results = []
    for query in LATAM_FUNDING_QUERIES:
        url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en"
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            results.append({
                'title': entry.get('title', ''),
                'url': entry.get('link', ''),
                'published_at': str(datetime.now()),
                'source': 'Google News',
                'content': entry.get('summary', ''),
            })
    print(f"Google News: {len(results)} funding headlines")
    return results

def fetch_techcrunch_latam():
    """Pull LATAM mentions from TechCrunch RSS -- no key needed"""
    feed = feedparser.parse("https://techcrunch.com/feed/")
    keywords = ["chile", "colombia", "peru", "ecuador", "mexico",
                "brazil", "argentina", "latam", "latin america"]
    results = []
    for entry in feed.entries:
        text = (entry.get('title', '') + entry.get('summary', '')).lower()
        if any(kw in text for kw in keywords):
            results.append({
                'title': entry.get('title', ''),
                'url': entry.get('link', ''),
                'published_at': str(datetime.now()),
                'source': 'TechCrunch',
                'content': entry.get('summary', ''),
            })
    print(f"TechCrunch: {len(results)} LATAM articles")
    return results

def fetch_all_funding_signals():
    """Combine all working sources"""
    return fetch_funding_news_google() + fetch_techcrunch_latam()

if __name__ == '__main__':
    items = fetch_all_funding_signals()
    print(f"\nTotal: {len(items)} articles")
    for item in items[:5]:
        print(f"{item['source']} | {item['title'][:60]}")