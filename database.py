# database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# We use SQLite for simplicity. It creates a file named 'router_logs.db'
DATABASE_URL = "sqlite:///./router_logs.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class RequestLog(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    prompt = Column(String)
    complexity = Column(String) # "SIMPLE" or "COMPLEX"
    model_used = Column(String)
    # We will simulate cost based on market rates (e.g., OpenAI prices)
    estimated_cost_saved = Column(Float)

Base.metadata.create_all(bind=engine)