import anthropic, os
from dotenv import load_dotenv
from datetime import datetime, timedelta, date
from database.models import Article, FundingRound, MarketSummary, SessionLocal

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))

SUMMARY_PROMPT = '''
You are a LATAM tech market analyst. Based on the data below, write a 1-page
executive summary for a SaaS company considering entering this market.

Country: {country}
Industry: {industry}
Period: Last 7 days

Recent news articles:
{articles_text}

Recent funding activity:
{funding_text}

Write a clear, conversational summary that covers:
1. What is the overall market mood right now?
2. What are the top 2-3 notable events or companies?
3. What should a SaaS founder entering this market know?
4. Is sentiment positive, cautious, or mixed?

Write as if explaining to a smart executive who has 3 minutes to read this.
Start with: Here is what is happening in {country} {industry} right now.
'''

def generate_summary(country, industry):
    session = SessionLocal()
    try:
        cutoff = datetime.now() - timedelta(days=7)
        articles = session.query(Article).filter(
            Article.country == country,
            Article.industry == industry,
            Article.published_at >= cutoff
        ).limit(10).all()

        funding = session.query(FundingRound).filter(
            FundingRound.country == country,
            FundingRound.industry == industry,
        ).limit(10).all()

        if not articles and not funding:
            print(f'  Skipping {country}/{industry} — no data')
            return None

        articles_text = chr(10).join([
            f'- {a.title}: {a.content[:200]}'
            for a in articles
        ]) or 'No recent articles found.'

        funding_text = chr(10).join([
            f'- {f.company_name}: ${f.amount_usd}M {f.round_type}'
            for f in funding
        ]) or 'No recent funding data found.'

        response = client.messages.create(
            model='claude-opus-4-6',
            max_tokens=1000,
            messages=[{
                'role': 'user',
                'content': SUMMARY_PROMPT.format(
                    country=country,
                    industry=industry,
                    articles_text=articles_text,
                    funding_text=funding_text,
                )
            }]
        )

        summary_text = response.content[0].text

        summary = MarketSummary(
            country=country,
            industry=industry,
            period_start=date.today() - timedelta(days=7),
            period_end=date.today(),
            summary=summary_text,
        )
        session.add(summary)
        session.commit()
        print(f'  Generated summary for {country}/{industry}')
        return summary_text

    except Exception as e:
        print(f'  Error for {country}/{industry}: {e}')
        session.rollback()
        return None
    finally:
        session.close()

def generate_all_summaries():
    countries  = ['Chile', 'Colombia', 'Peru', 'Ecuador', 'Mexico']
    industries = ['fintech', 'e-commerce', 'healthtech']
    print(f'Generating summaries for {len(countries)} countries x {len(industries)} industries...')
    for country in countries:
        for industry in industries:
            generate_summary(country, industry)

if __name__ == '__main__':
    print('Testing Claude summary for Colombia fintech...')
    result = generate_summary('Mexico', 'fintech')
    if result:
        print('SUCCESS! Summary:')
        print(result[:300] + '...')

