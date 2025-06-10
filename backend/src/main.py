from fastapi import FastAPI, BackgroundTasks
from .worker import crawl_product_rank
from .models import ProductSearch

app = FastAPI()

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