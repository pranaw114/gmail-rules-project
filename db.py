import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

with open('config.json', 'r') as f:
    cfg = json.load(f)

engine = create_engine(cfg.get('database_url', 'sqlite:///emails.db'), future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
