from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from .worker import crawl_product_rank
from . import models, schemas
from .database import SessionLocal, engine

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/search/")
async def search_product_rank(product: ProductSearch):
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

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(url=product.url, name=product.name)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.post("/products/{product_id}/keywords/", response_model=schemas.Keyword)
def add_keyword(product_id: int, keyword: schemas.KeywordCreate, db: Session = Depends(get_db)):
    db_keyword = models.Keyword(keyword=keyword.keyword, product_id=product_id)
    db.add(db_keyword)
    db.commit()
    db.refresh(db_keyword)
    return db_keyword

@app.get("/products/", response_model=List[schemas.ProductWithKeywords])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()