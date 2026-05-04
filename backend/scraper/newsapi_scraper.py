import httpx, os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

COUNTRY_KEYWORDS = {
    # North America
    'Mexico':             ['Mexico', 'Mexican', 'Ciudad de Mexico', 'CDMX', 'Monterrey', 'Guadalajara'],
 
    # Central America
    'Guatemala':          ['Guatemala', 'Guatemalan', 'Guatemala City'],
    'Belize':             ['Belize', 'Belizean', 'Belmopan', 'Belize City'],
    'Honduras':           ['Honduras', 'Honduran', 'Tegucigalpa', 'San Pedro Sula'],
    'El Salvador':        ['El Salvador', 'Salvadoran', 'San Salvador'],
    'Nicaragua':          ['Nicaragua', 'Nicaraguan', 'Managua'],
    'Costa Rica':         ['Costa Rica', 'Costa Rican', 'San Jose'],
    'Panama':             ['Panama', 'Panamanian', 'Panama City'],
 
    # Caribbean
    'Cuba':               ['Cuba', 'Cuban', 'Havana'],
    'Dominican Republic': ['Dominican Republic', 'Dominican', 'Santo Domingo', 'Santiago DR'],
    'Puerto Rico':        ['Puerto Rico', 'Puerto Rican', 'San Juan'],
    'Jamaica':            ['Jamaica', 'Jamaican', 'Kingston'],
    'Trinidad':           ['Trinidad', 'Tobago', 'Trinidadian', 'Port of Spain'],
    'Haiti':              ['Haiti', 'Haitian', 'Port-au-Prince'],
 
    # South America
    'Colombia':           ['Colombia', 'Colombian', 'Bogota', 'Medellin', 'Cali', 'Barranquilla'],
    'Venezuela':          ['Venezuela', 'Venezuelan', 'Caracas', 'Maracaibo'],
    'Ecuador':            ['Ecuador', 'Ecuadorian', 'Quito', 'Guayaquil', 'Cuenca'],
    'Peru':               ['Peru', 'Peruvian', 'Lima', 'Arequipa', 'Cusco'],
    'Bolivia':            ['Bolivia', 'Bolivian', 'La Paz', 'Santa Cruz', 'Cochabamba'],
    'Brazil':             ['Brazil', 'Brazilian', 'Sao Paulo', 'Rio de Janeiro', 'Brasilia', 'Belo Horizonte'],
    'Chile':              ['Chile', 'Chilean', 'Santiago', 'Valparaiso', 'Concepcion'],
    'Argentina':          ['Argentina', 'Argentine', 'Buenos Aires', 'Cordoba', 'Rosario'],
    'Uruguay':            ['Uruguay', 'Uruguayan', 'Montevideo'],
    'Paraguay':           ['Paraguay', 'Paraguayan', 'Asuncion'],
    'Guyana':             ['Guyana', 'Guyanese', 'Georgetown'],
    'Suriname':           ['Suriname', 'Surinamese', 'Paramaribo'],
}
INDUSTRY_KEYWORDS = {
    # Tech & Digital
    'fintech':       ['fintech', 'payment', 'neobank', 'digital bank', 'banking', 'crypto',
                      'lending', 'insurtech', 'remittance', 'wealthtech', 'regtech',
                      'financial inclusion', 'open banking', 'wallet', 'blockchain'],
 
    'e-commerce':    ['ecommerce', 'e-commerce', 'marketplace', 'retail tech', 'delivery',
                      'last mile', 'logistics tech', 'dropshipping', 'D2C',
                      'social commerce', 'quick commerce', 'fulfillment'],
 
    'saas':          ['SaaS', 'software as a service', 'B2B software', 'cloud software',
                      'enterprise software', 'vertical SaaS', 'no-code', 'low-code',
                      'workflow automation', 'CRM', 'ERP', 'HRM'],
 
    'ai-ml':         ['artificial intelligence', 'machine learning', 'AI', 'deep learning',
                      'computer vision', 'NLP', 'natural language', 'generative AI',
                      'LLM', 'automation', 'predictive analytics', 'data science'],
 
    'cybersecurity': ['cybersecurity', 'infosec', 'data privacy', 'identity management',
                      'fraud prevention', 'zero trust', 'endpoint security', 'compliance tech'],
 
    # Health & Life Sciences
    'healthtech':    ['healthtech', 'health tech', 'telemedicine', 'telehealth', 'healthcare',
                      'medtech', 'digital health', 'mental health tech', 'femtech',
                      'genomics', 'pharmatech', 'hospital tech', 'medical device'],
 
    'biotech':       ['biotech', 'biotechnology', 'life sciences', 'drug discovery',
                      'clinical trials', 'bioinformatics', 'synthetic biology', 'diagnostics'],
 
    # Food & Agriculture
    'agtech':        ['agtech', 'ag tech', 'agriculture tech', 'farming tech', 'precision agriculture',
                      'crop management', 'smart farming', 'vertical farming', 'agribusiness',
                      'livestock tech', 'irrigation tech'],
 
    'foodtech':      ['foodtech', 'food tech', 'alternative protein', 'plant-based', 'food delivery',
                      'restaurant tech', 'ghost kitchen', 'food supply chain', 'food safety'],
 
    # Education
    'edtech':        ['edtech', 'ed tech', 'education tech', 'e-learning', 'online learning',
                      'upskilling', 'reskilling', 'corporate training', 'LMS',
                      'tutoring platform', 'bootcamp', 'MOOCs'],
 
    # Energy & Environment
    'cleantech':     ['cleantech', 'renewable energy', 'solar', 'wind energy',
                      'energy storage', 'smart grid', 'carbon credits', 'sustainability tech',
                      'green tech', 'ESG tech', 'climate tech', 'EV charging'],
 
    # Mobility & Infrastructure
    'mobility':      ['mobility', 'ride hailing', 'rideshare', 'micromobility', 'electric vehicle',
                      'EV', 'autonomous vehicle', 'fleet management', 'urban mobility'],
 
    'logistics':     ['logistics', 'supply chain', 'freight tech', 'trucking tech', 'warehousing',
                      'inventory management', 'shipping tech', 'customs tech', 'cold chain'],
 
    # Real Estate & Construction
    'proptech':      ['proptech', 'real estate tech', 'property tech', 'smart building',
                      'construction tech', 'contech', 'facility management', 'mortgage tech'],
 
    # Media & Creator Economy
    'mediatech':     ['media tech', 'streaming', 'content platform', 'creator economy',
                      'influencer', 'gaming', 'esports', 'OTT', 'podcast tech', 'sports tech'],
 
    # HR & Future of Work
    'hrtech':        ['HR tech', 'human resources tech', 'recruiting tech', 'talent management',
                      'payroll tech', 'workforce management', 'gig economy', 'remote work tech'],
 
    # Government & Social Impact
    'govtech':       ['govtech', 'government tech', 'civic tech', 'public sector tech',
                      'smart city', 'legaltech', 'legal tech', 'e-government'],
 
    'impact':        ['social impact', 'impact investing', 'financial inclusion', 'microfinance',
                      'social enterprise', 'nonprofit tech', 'humanitarian tech', 'SDGs'],
 
    # Hardware & Deep Tech
    'hardware':      ['hardware', 'IoT', 'internet of things', 'robotics', 'drone',
                      'semiconductor', 'wearable', 'smart device', 'Industry 4.0'],
}
def detect_country(text):
    text = text.lower()
    for country, keywords in COUNTRY_KEYWORDS.items():
        if any(kw.lower() in text for kw in keywords):
            return country
    return 'Unknown'

def detect_industry(text):
    text = text.lower()
    for industry, keywords in INDUSTRY_KEYWORDS.items():
        if any(kw.lower() in text for kw in keywords):
            return industry
    return 'tech'

def fetch_latam_news(days_back=7):
    api_key = os.getenv('NEWSAPI_KEY')
    from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

    query = '(Chile OR Colombia OR Peru OR Ecuador OR Mexico) AND (startup OR fintech OR tech OR funding)'

    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 100,
        'apiKey': api_key
    }

    response = httpx.get(url, params=params)
    data = response.json()

    articles = []
    for item in data.get('articles', []):
        text = f"{item.get('title', '')} {item.get('description', '')}"
        articles.append({
            'title': item.get('title', '')[:500],
            'source': item.get('source', {}).get('name', ''),
            'url': item.get('url', ''),
            'published_at': item.get('publishedAt', ''),
            'content': item.get('description', '') or '',
            'country': detect_country(text),
            'industry': detect_industry(text),
        })

    print(f'Fetched {len(articles)} articles')
    return articles

if __name__ == '__main__':
    articles = fetch_latam_news()
    for a in articles[:3]:
        print(f"{a['country']} | {a['industry']} | {a['title'][:60]}")
