from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .worker import crawl_product_rank
from . import models, schemas
from .database import SessionLocal, engine, create_tables

# 데이터베이스 테이블 생성
create_tables()

app = FastAPI()

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9000"],  # 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/search/")
async def search_product_rank(product: schemas.ProductSearch):
    # Celery task 실행
    task = crawl_product_rank.delay(
        keyword=product.keyword,
        product_url=product.url
    )
    return {"task_id": task.id}

@app.get("/tasks/{task_id}")
async def get_task_result(task_id: str):
    task = crawl_product_rank.AsyncResult(task_id)
    if task.ready():
        return {"status": task.status, "result": task.get()}
    return {"status": task.status}

@app.post("/products/", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(
        url=product.url,
        name=product.name,
        created_at=datetime.utcnow()
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.post("/products/{product_id}/keywords/", response_model=schemas.Keyword)
def add_keyword(product_id: int, keyword: schemas.KeywordCreate, db: Session = Depends(get_db)):
    db_keyword = models.Keyword(
        keyword=keyword.keyword,
        product_id=product_id,
        created_at=datetime.utcnow()
    )
    db.add(db_keyword)
    db.commit()
    db.refresh(db_keyword)
    return db_keyword

@app.get("/products/", response_model=List[schemas.ProductWithKeywords])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

# requirements.txt에 추가된 패키지
# fastapi[all]
# uvicorn[standard]
# sqlalchemy
# asyncpg
# python-dotenv
# undetected-chromedriver
# celery
# redis
# flower
# pydantic-settings