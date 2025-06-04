import asyncio
import random
from playwright.async_api import async_playwright
import urllib.parse
import time

class CoupangRankChecker:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None

    async def init_browser(self):
        """
        개인화 요소를 제거한 깨끗한 브라우저 환경 초기화
        """
        playwright = await async_playwright().start()

        # 브라우저 시작 (매번 새로운 인스턴스)
        self.browser = await playwright.chromium.launch(
            headless=False,  # 디버깅을 위해 headless 모드 비활성화
            args=[
                "--no-first-run",
                "--disable-blink-features=AutomationControlled",  # 자동화 감지 방지
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor",
                "--incognito",  # 개인화 요소 제거
            ]
        )
        self.context = await self.browser.new_context(
            user_agent=self.get_random_user_agent(),
            ignore_https_errors=True,
        )

    def get_random_user_agent(self):
        """랜덤 User-Agent 생성"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
            "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
        ]
        return random.choice(user_agents)

    async def cleanup(self):
        """
        브라우저 및 컨텍스트 종료
        """
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()

async def find_product_rank(keyword: str, product_url: str, is_mobile: bool = False):
    """
    쿠팡에서 상품 순위를 찾는 함수

    Args:
        keyword (str): 검색 키워드
        product_url (str): 찾을 상품의 URL
        is_mobile (bool): 모바일 검색 여부

    Returns:
        int: 상품 순위 (찾지 못한 경우 -1)
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        # User-Agent 설정
        user_agent_pc = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        user_agent_mobile = "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
        ua = user_agent_mobile if is_mobile else user_agent_pc

        context = await browser.new_context(user_agent=ua)
        page = await context.new_page()

        try:
            # URL에서 상품 ID 추출
            product_id = product_url.split('products/')[1].split('?')[0]

            # 검색 URL 생성
            encoded_keyword = urllib.parse.quote(keyword)
            search_url = f"https://www.coupang.com/np/search?q={encoded_keyword}&channel=user"

            # 검색 페이지로 이동
            await page.goto(search_url)
            await page.wait_for_timeout(3000)  # 페이지 로딩 대기

            rank = 1
            page_num = 1
            max_pages = 3  # 최대 3페이지까지 검색

            while page_num <= max_pages:
                # 상품 목록 가져오기
                items = await page.query_selector_all('#productList > li')

                for item in items:
                    try:
                        # 상품 링크 가져오기
                        link_element = await item.query_selector('a')
                        if not link_element:
                            continue

                        link = await link_element.get_attribute('href')
                        if not link:
                            continue

                        # 상품 ID 추출 및 비교
                        if product_id in link:
                            print(f"\n상품을 찾았습니다!")
                            print(f"키워드: {keyword}")
                            print(f"순위: {rank}위")
                            print(f"페이지: {page_num}페이지")
                            return rank

                        rank += 1
                    except Exception as e:
                        print(f"상품 처리 중 오류 발생: {str(e)}")
                        continue

                # 다음 페이지로 이동
                page_num += 1
                if page_num <= max_pages:
                    next_page_url = f"https://www.coupang.com/np/search?q={encoded_keyword}&channel=user&page={page_num}"
                    await page.goto(next_page_url)
                    await page.wait_for_timeout(3000)

            print(f"\n상품을 찾지 못했습니다.")
            print(f"검색된 키워드: {keyword}")
            print(f"검색한 페이지 수: {max_pages}")
            print(f"상위 {rank-1}개 상품 중에 해당 상품이 없습니다.")
            return -1

        except Exception as e:
            print(f"오류 발생: {str(e)}")
            return -1

        finally:
            await browser.close()

async def main():
    checker = CoupangRankChecker()
    try:
        await checker.init_browser()
    finally:
        await checker.cleanup()

if __name__ == "__main__":
    keyword = "비타민"
    product_url = "https://www.coupang.com/vp/products/8157279876?itemId=19469999949&vendorItemId=84995750115&q=%EB%B9%84%ED%83%80%EB%AF%BC&searchId=489574363338132"

    asyncio.run(find_product_rank(keyword, product_url, is_mobile=False))