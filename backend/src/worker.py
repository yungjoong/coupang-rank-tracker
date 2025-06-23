from celery import Celery
from celery.schedules import crontab
from .config import settings
from .crawler.test_again import find_product_rank  # import 경로 수정
import asyncio
from .database import SessionLocal
from . import models

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

# Celery Beat 스케줄 설정
celery.conf.beat_schedule = {
    'check-rankings-daily': {
        'task': 'src.worker.check_all_products_ranks',
        'schedule': crontab(hour=0, minute=0),  # 매일 자정에 실행
    },
}

@celery.task
def crawl_product_rank(keyword: str, product_url: str):
    """상품의 순위를 크롤링하는 Celery 태스크"""
    try:
        # 새로운 이벤트 루프 생성
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # 비동기 함수 실행
        rank = loop.run_until_complete(find_product_rank(keyword, product_url))

        # 이벤트 루프 종료
        loop.close()

        return {
            "rank": rank,
            "keyword": keyword,
            "url": product_url,
            "status": "success" if rank is not None else "not_found"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "keyword": keyword,
            "url": product_url
        }

@celery.task
def check_all_products_ranks():
    """모든 상품의 순위를 체크하는 태스크"""
    db = SessionLocal()
    try:
        products = db.query(models.Product).all()
        for product in products:
            for keyword in product.keywords:
                crawl_product_rank.delay(
                    keyword=keyword.keyword,
                    product_url=product.url
                )
    finally:
        db.close()