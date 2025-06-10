from celery import Celery
from .config import settings
from .crawler.test_again import find_product_rank  # import 경로 수정
import asyncio

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