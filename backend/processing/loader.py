from database.models import Article, SessionLocal
from datetime import datetime

def load_articles(articles):
    session = SessionLocal()
    loaded = 0
    skipped = 0
    try:
        for a in articles:
            exists = session.query(Article).filter_by(url=a['url']).first()
            if exists:
                skipped += 1
                continue
            try:
                pub_date = datetime.fromisoformat(a['published_at'].replace('Z', '+00:00'))
            except:
                pub_date = datetime.now()
            article = Article(
                title=a['title'],
                source=a['source'],
                url=a['url'],
                country=a['country'] if 'country' in a else 'Unknown',
                industry=a['industry'] if 'industry' in a else 'tech',
                published_at=pub_date,
                content=a['content'],
            )
            session.add(article)
            loaded += 1
        session.commit()
        print(f'Loaded {loaded} articles, skipped {skipped} duplicates')
    except Exception as e:
        session.rollback()
        print(f'Error: {e}')
    finally:
        session.close()