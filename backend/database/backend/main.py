from scraper.newsapi_scraper import fetch_latam_news
from scraper.funding_scraper import fetch_all_funding_signals
from processing.loader import load_articles
from database.models import create_tables

def run_pipeline():
    print('--- LATAM Data Pipeline Starting ---')

    # Step 1: Fetch news articles (NewsAPI)
    print('Fetching news articles...')
    articles = fetch_latam_news(days_back=7)
    load_articles(articles)

    # Step 2: Fetch funding signals (Google News + TechCrunch)
    print('Fetching funding signals...')
    funding_articles = fetch_all_funding_signals()
    load_articles(funding_articles)

    print('--- Pipeline Complete ---')

if __name__ == '__main__':
    create_tables()
    run_pipeline()