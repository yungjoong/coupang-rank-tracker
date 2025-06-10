from celery import Celery
from .config import settings

celery = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Seoul',
    enable_utc=True,
)

@celery.task
async def crawl_product_rank(keyword: str, product_url: str):
    from .crawler.test_again import find_product_rank
    return await find_product_rank(keyword, product_url)