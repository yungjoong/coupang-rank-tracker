import scrapy


class CoupangSpider(scrapy.Spider):
    name = "coupang"
    allowed_domains = ["coupang.com"]
    start_urls = ["https://coupang.com"]

    def start_requests(self):
        urls = [
            "https://www.coupang.com/np/categories/498704/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for product in response.css(".baby-product"):  # 상품 리스트 선택
            yield {
                "name": product.css(".name::text").get(),
                "price": product.css(".price-value::text").get()
            }