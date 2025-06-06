import scrapy
from urllib.parse import urlencode

# 코드 출처 : https://velog.io/@2hannah/%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%97%94%EC%A7%80%EB%8B%88%EC%96%B4%EB%A7%81-Scrapy%EB%A1%9C-%EC%BF%A0%ED%8C%A1-%EC%83%81%ED%92%88-%EB%AA%A9%EB%A1%9D-%ED%81%AC%EB%A1%A4%EB%A7%81-%ED%95%B4%EC%98%A4%EA%B8%B0
# 동작 확인 @ 25.06.05 (for categories)
SCRAPEOPS_API_KEY = "a1173785-8edc-4f47-8444-40915d4cbf6b"

class ImpersonateSpider(scrapy.Spider):
    name = "impersonate_spider"
    custom_settings = {
        "USER_AGENT": None,
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_impersonate.ImpersonateDownloadHandler",
            "https": "scrapy_impersonate.ImpersonateDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }

    def start_requests(self):
        yield scrapy.Request(
            "https://tls.browserleaks.com/json",
            dont_filter=True,
            meta={"impersonate": "chrome110"},
        )

    def parse(self, response):
        # ja3_hash: 773906b0efdefa24a7f2b8eb6985bf37
        # ja3_hash: cd08e31494f9531f560d64c695473da9
        # ja3_hash: 2fe1311860bc318fc7f9196556a2a6b9
        yield {"ja3_hash": response.json()["ja3_hash"]}

class CoupangSpider(scrapy.Spider):
    name = "coupang"
    allowed_domains = ["coupang.com", "proxy.scrapeops.io"]

    custom_settings = {
        'DOWNLOAD_HANDLERS': {
            "http": "scrapy_impersonate.ImpersonateDownloadHandler",
            "https": "scrapy_impersonate.ImpersonateDownloadHandler",
        },
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'scrapy_impersonate.ImpersonateMiddleware': 725,
        # },
        'IMPERSONATE': {
            'browser': {
                'custom': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36',
            },
            'mobile': True,
            'viewport': {
                'width': 360,
                'height': 640,
            },
        }
    }

    def get_scrapeops_url(self, url : str):
        """
        Generate a ScrapeOps proxy URL for the given URL.
        """
        payload = { 'api_key' : SCRAPEOPS_API_KEY, 'url' : url }
        proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
        return proxy_url

    def start_requests(self):
        urls = [
            "https://www.coupang.com/np/search?q=camping+table&channel=user"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield {
            'html': response.text
        }

        # for product in response.css(".baby-product"):  # 상품 리스트 선택
        #     yield {
        #         "name": product.css(".name::text").get(),
        #         "price": product.css(".price-value::text").get()
        #     }