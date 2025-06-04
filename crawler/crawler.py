import asyncio
from playwright.async_api import async_playwright
import urllib.parse


async def find_product_rank (keyword : str, product_url : str, is_mobile : bool = False):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 페이지 이동
        user_agent_pc = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        user_agent_mobile = "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
        ua = user_agent_mobile if is_mobile else user_agent_pc

        context = browser.new_context(user_agent=ua)
        page = context.new_page()

        search_url = f"https://www.coupang.com/np/search?component=&q={keyword}&channel=user"
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


if __name__ == "__main__":
    keyword = "비타민"
    product_url = "https://www.coupang.com/vp/products/8157279876?itemId=19469999949&vendorItemId=84995750115&q=%EB%B9%84%ED%83%80%EB%AF%BC&searchId=489574363338132"

    find_product_rank(keyword, product_url)