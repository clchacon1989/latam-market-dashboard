from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc
from database.models import Article, MarketSummary, SessionLocal
from typing import Optional
import uvicorn

app = FastAPI(title='LATAM Market Intelligence API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/health')
def health():
    return {'status': 'ok', 'message': 'LATAM API is running'}

@app.get('/api/articles')
def get_articles(country: Optional[str] = None, industry: Optional[str] = None):
    session = SessionLocal()
    q = session.query(Article).order_by(desc(Article.published_at))
    if country:
        q = q.filter(Article.country == country)
    if industry:
        q = q.filter(Article.industry == industry)
    results = q.limit(100).all()
    session.close()
    return [{'id': r.id, 'title': r.title, 'source': r.source,
             'country': r.country, 'industry': r.industry,
             'published_at': str(r.published_at), 'url': r.url} for r in results]

@app.get('/api/summaries')
def get_summaries(country: Optional[str] = None, industry: Optional[str] = None):
    session = SessionLocal()
    q = session.query(MarketSummary).order_by(desc(MarketSummary.generated_at))
    if country:
        q = q.filter(MarketSummary.country == country)
    if industry:
        q = q.filter(MarketSummary.industry == industry)
    results = q.limit(20).all()
    session.close()
    return [{'id': r.id, 'country': r.country, 'industry': r.industry,
             'summary': r.summary, 'generated_at': str(r.generated_at),
             'period_start': str(r.period_start), 'period_end': str(r.period_end)} for r in results]

@app.get('/api/stats')
def get_stats():
    session = SessionLocal()
    countries = ['Chile', 'Colombia', 'Peru', 'Ecuador', 'Mexico',
                 'Brazil', 'Argentina', 'Unknown']
    stats = []
    for country in countries:
        count = session.query(Article).filter(Article.country == country).count()
        if count > 0:
            stats.append({'country': country, 'article_count': count})
    session.close()
    return stats

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)