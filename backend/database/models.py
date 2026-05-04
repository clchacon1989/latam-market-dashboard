from sqlalchemy import Column, String, Float, DateTime, Date, Text, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os, uuid
from datetime import datetime

load_dotenv()
Base = declarative_base()
engine = create_engine(os.getenv('DATABASE_URL').replace("postgresql://", "postgresql+psycopg://"))
SessionLocal = sessionmaker(bind=engine)

class Article(Base):
    __tablename__ = 'articles'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(500))
    source = Column(String(100))
    url = Column(Text, unique=True)
    country = Column(String(50))
    industry = Column(String(100))
    published_at = Column(DateTime)
    content = Column(Text)
    sentiment = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.now)

class FundingRound(Base):
    __tablename__ = 'funding_rounds'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_name = Column(String(300))
    country = Column(String(50))
    industry = Column(String(100))
    amount_usd = Column(Numeric(15, 2))
    round_type = Column(String(50))
    announced_date = Column(Date)
    created_at = Column(DateTime, default=datetime.now)

class MarketSummary(Base):
    __tablename__ = 'market_summaries'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    country = Column(String(50))
    industry = Column(String(100))
    period_start = Column(Date)
    period_end = Column(Date)
    summary = Column(Text)
    generated_at = Column(DateTime, default=datetime.now)

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    create_tables()
    print('Tables created successfully!')