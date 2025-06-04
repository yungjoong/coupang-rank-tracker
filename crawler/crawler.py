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
                # "--no-sandbox",
                # "--disable-setuid-sandbox",
                # "--disable-features=IsolateOrigins,site-per-process",
            ]
        )
        self.context = await self.browser.new_context(
            # 랜덤 User-Agent (봇 탐지 방지)
            user_agent=self.get_random_user_agent(),

            # 쿠키 및 스토리지 무시
            ignore_https_errors=True,
        )

    def get_random_user_agent(self):
        """랜덤 User-Agent 생성"""
        user_agents = [

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

async def find_product_rank (keyword : str, product_url : str, is_mobile : bool = False):
    with async_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 페이지 이동
        user_agent_pc = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        user_agent_mobile = "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
        ua = user_agent_mobile if is_mobile else user_agent_pc

        context = browser.new_context(user_agent=ua)
        page = context.new_page()

        search_url = f"https://www.coupang.com/np/search?&q={keyword}&channel=user"
        next_page = f"https://www.coupang.com/np/search?q={keyword}&channel=user&page=5"
        page.goto(search_url)
        page.wait_for_timeout(5000)

        rank = 1
        found_rank = False
        items = page.query_selector_all('#product-list > li')
        for item in items :
            link = ""

        f"/vp/products/6409464601?itemId=1087020209&vendorItemId=90419565452&q=비타민&searchId=16cdad842266734&sourceType=search&itemsCount=36&searchRank=33&rank=33"

        # 브라우저 종료
        browser.close()


async def main():
    checker = CoupangRankChecker()

    try:
        # 브라우저 초기화
        await checker.init_browser()

    finally:
        await checker.cleanup()

if __name__ == "__main__":
    keyword = "비타민"
    product_url = "https://www.coupang.com/vp/products/8157279876?itemId=19469999949&vendorItemId=84995750115&q=%EB%B9%84%ED%83%80%EB%AF%BC&searchId=489574363338132"

    asyncio.run(find_product_rank(keyword, product_url, is_mobile=False))