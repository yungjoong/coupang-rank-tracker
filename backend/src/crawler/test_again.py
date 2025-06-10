#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import undetected_chromedriver as uc
from datetime import datetime
import time
import os
import random
from celery import Celery
from ..config import settings  # 상대 경로 수정
import asyncio

def random_sleep():
    """랜덤한 시간 동안 대기"""
    time.sleep(random.uniform(2, 5))

async def find_product_rank(keyword: str, target_product_url: str) -> int:
    """쿠팡에서 특정 키워드로 검색했을 때 상품의 순위를 찾습니다."""
    try:
        print("Chrome 드라이버 초기화 중...")
        # Chrome 옵션 설정
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--lang=ko_KR")
        options.add_argument("--headless=new")  # 새로운 headless 모드

        driver = uc.Chrome(options=options, version_main=129)
        print("Chrome 드라이버 초기화 완료")

        try:
            # 검색 페이지로 이동
            print(f"검색 페이지로 이동 중... 키워드: {keyword}")
            search_url = f"https://m.coupang.com/nm/search?q={keyword}"
            driver.get(search_url)
            random_sleep()

            # 쿠키 수락 버튼 클릭 시도
            try:
                cookie_button = driver.find_element("id", "cookieAcceptButton")
                cookie_button.click()
                print("쿠키 수락 버튼 클릭")
                random_sleep()
            except:
                print("쿠키 수락 버튼을 찾을 수 없거나 이미 수락됨")

            # 상품 목록에서 타겟 URL 검색
            items = driver.find_elements("css selector", "a.search-product-link")

            for index, item in enumerate(items, 1):
                item_url = "https://www.coupang.com" + item.get_attribute("href")
                if item_url == target_product_url:
                    print(f"상품을 찾았습니다! 순위: {index}")
                    return index

            print("상품을 찾지 못했습니다.")
            return None

        finally:
            driver.quit()

    except Exception as e:
        print(f"오류 발생: {str(e)}")
        print("상세 오류 정보:", e.__class__.__name__)
        return None

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

# 기존의 테스트 코드는 if __name__ == "__main__": 블록으로 이동
if __name__ == "__main__":
    # ... 기존 테스트 코드 ...
    pass
