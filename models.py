from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class ParsedListing(Base):
    __tablename__ = 'parsed_listings'
    id = Column(Integer, primary_key=True)
    raw_text = Column(Text, nullable=False)
    parsed_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
