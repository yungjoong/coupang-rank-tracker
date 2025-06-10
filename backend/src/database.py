from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLAlchemy 엔진 생성
engine = create_engine(settings.DATABASE_URL)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성
Base = declarative_base()

# 데이터베이스 테이블 생성
def create_tables():
    Base.metadata.create_all(bind=engine)