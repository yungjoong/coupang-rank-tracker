from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    keywords = relationship("Keyword", back_populates="product")

class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String)
    product_id = Column(Integer, ForeignKey("products.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    product = relationship("Product", back_populates="keywords")
    rankings = relationship("Ranking", back_populates="keyword")

class Ranking(Base):
    __tablename__ = "rankings"

    id = Column(Integer, primary_key=True, index=True)
    keyword_id = Column(Integer, ForeignKey("keywords.id"))
    rank = Column(Integer, nullable=True)
    checked_at = Column(DateTime, default=datetime.utcnow)
    keyword = relationship("Keyword", back_populates="rankings")

class ProductSearch(BaseModel):
    keyword: str
    url: str