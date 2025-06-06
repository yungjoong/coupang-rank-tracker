import scrapy
from scrapy_playwright.page import PageMethod
from playwright_stealth import stealth_sync
from playwright.sync_api import sync_playwright

class PlaywrightStealthSpider(scrapy.Spider):
    name = "playwright_stealth"
    allowed_domains = ["coupang.com"]

    custom_settings = {
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.PlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.PlaywrightDownloadHandler",
        },
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_playwright.middleware.PlaywrightMiddleware": 800,
        },
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": True,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--disable-features=IsolateOrigins,site-per-process",
            ],
        },
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 30000,
    }

    def start_requests(self):
        urls = [
            "https://www.coupang.com/np/search?q=camping+table&channel=user"
        ]
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod("wait_for_selector", ".baby-product"),
                    ],
                ),
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]

        # Playwright Stealth 적용
        await stealth_sync(page)

        # 페이지 내용 가져오기
        content = await page.content()

        # 상품 정보 추출
        products = await page.query_selector_all(".baby-product")
        for product in products:
            name = await product.query_selector(".name")
            price = await product.query_selector(".price-value")

            yield {
                "name": await name.text_content() if name else None,
                "price": await price.text_content() if price else None,
            }

        await page.close()