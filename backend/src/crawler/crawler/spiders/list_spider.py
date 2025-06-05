import scrapy
from urllib.parse import urlencode

# 코드 출처 : https://velog.io/@2hannah/%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%97%94%EC%A7%80%EB%8B%88%EC%96%B4%EB%A7%81-Scrapy%EB%A1%9C-%EC%BF%A0%ED%8C%A1-%EC%83%81%ED%92%88-%EB%AA%A9%EB%A1%9D-%ED%81%AC%EB%A1%A4%EB%A7%81-%ED%95%B4%EC%98%A4%EA%B8%B0
# 동작 확인 @ 25.06.05 (for categories)
SCRAPEOPS_API_KEY = "a1173785-8edc-4f47-8444-40915d4cbf6b"

headers = {
    "authority": "weblog.coupang.com",
    "scheme": "https",
    # "origin": "https://www.coupang.com",
    "Sec-Ch-Ua-Mobile": "?1",
    "Sec-Ch-Ua-Platform": "Android",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-encoding" : "gzip, deflate, br, zstd",
    "Accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-control": "no-cache",
    "Cookie": "PCID=15651274385971747379966; MARKETID=15651274385971747379966; delivery_toggle=false; cto_bundle=Jb0R0V8yVHpBUThwWCUyQmkwWU9xTXppTktVaWVmQzh1RWs4ZDN2eU15JTJGRUlpSFlJUWNHN0RPd2picmtBWXd4YXlhOEFSU3BpYVBLdzFEYzgwMVBCY1hpUjkwcCUyRktuVzJ3UGN4NyUyRmtGVVpvSGdBZGhSaTE2aG82ZWxMc1VVckNTTTRiM0NQVCUyRmt4a2xVUnhlaWlWMzlVWG1lS21RJTNEJTNE; trac_src=1042016; trac_spec=10304903; trac_addtag=900; trac_ctag=HOME; trac_lptag=%EC%BF%A0%ED%8C%A1; trac_itime=20250604130941; x-coupang-accept-language=ko-KR; x-coupang-target-market=KR; sid=833af7b210bd44549f46d70331c7833dd4010499; web-session-id=5a0a41d8-7846-4c48-9321-c56526a78bd5; ak_bmsc=17F0A2DAE92E073D7390DBA9FEB1B95E~000000000000000000000000000000~YAAQRrxBF1rsLTyXAQAAZ5y6PRweXIBcK63x2jDujTWTbgIyjfDIRk5OCWBLcYDdjzcLcUunjk7y1TR2a0g9hYejIRJRVEXzD/VhOzO6G0dMOayoCbTKKOc1w6F0AdRhhdQ/G5W+JhE1XnastBcxl4Ix56IjBi6XaFOBGnkgqZHDa4DZHdQBoaF9X7hTcShUgbbcVFvC8q7On74cwxFkXthn+PrlBth0E6YBwuKskeJAXXVRSturbaXGOYh4HOpgqbrroN1JW+SfVPRfJUywoqjGMtx0s6Wt6yi9qEWeCkxAgRdj1CJ2cjGhyCkMF4YKi5B6mKA2TISCg2ComeEzhS0FLPG5ako0eyrozjpSLcX1rjBHPVoKBQkDcwftxII/notFUR1Oeku9A4hUZIOekdz/C6q1WpyibRVLw4pgQJJys2b62eM2OwWRixT/2xPU; searchKeyword=%EB%B9%84%ED%83%80%EB%AF%BC|%EC%BA%A0%ED%95%91%20%ED%85%8C%EC%9D%B4%EB%B8%94|camping%20table; searchKeywordType={%22%EB%B9%84%ED%83%80%EB%AF%BC%22:0}|{%22%EC%BA%A0%ED%95%91%20%ED%85%8C%EC%9D%B4%EB%B8%94%22:0}|{%22camping%20table%22:0}; overrideAbTestGroup=%5B%5D; bm_so=4A75204D00C9D3E996D79F790D34DDDBF64151B0E68E0D20920F119A57BEFFF9~YAAQn0g7FxUIhi+XAQAA69njPQM8Pz/+LCTvZxyvnvoJYDKNr25+S2D7xItajKyDxSWtbfF2qEuqBoHlDP7Hkr8WLkKvpgLK8xdWWiyGMeLe14p7Qzxc7vsdsZtky1NjAHdALW9Ga+3HfMzziyAErwHZwXIUiXNNRkDMgFsOQAT2bxKhZ4An61f6UdfAHzPozRoIRMb+naya9/jzlLCiLREhJPjdg94ksMi7RwV8+roD0lln5JDrzJByLIcsBM+S6qPpbXhbWdV9vqyFLxBso6WuuY7hHTyPEmB9zMaG6KiCUXioHOgS+pIHGrUQx4e5pnCdmvLN1fiUeQERZupjwkgJIZQaIGeeQ0ipnKO/NqeWJj/qagYf1GwknhySfFYRgx/goNVCHzM2H8YUJLmpMxSg/MNd96yiFrcHwQ0BNoF++GVLkOy/uFpJ6rO7NDXtoFVKUBSUGBKP5TJNrYzhlA==; bm_sz=E1F4B1D5A4B6DF851165EDBA462258BD~YAAQn0g7FxcIhi+XAQAA7NnjPRzScFOmU/3OGo0XM76ag6X9eUgiPPwdI+XnIB3GlDARXHotz8cAgBbDUQ2raeuePz/CXviI7/RWsRrWc40I2/j5n2mZ/kqWeBEvXYcJUBbj6R4/g29LUy50xOyVbluP+BiUFT/RTv6bC/d3r1RM6y4gFp9zfOBG7dEJUNhgVFmugSnCtYapmGC0rpkx3/oP4oOpGJxoEM/LWTadaY23sdUJzybCUN20n3c/0B0SWXhHJmX8o3sd9SNIXioFr1krV88o/H98SQBsJgcRTy9d7ZpDUYHrR4YCakftxveM82MVgy1Kob3zwLGvZQHStdwTQQu07Q2Bic0WPtRmmRZ8GRmq1JtaUyR9MEjo1H21qHSt6zh/vMWb7N+x9CgA97tNOwFBtgkGHC5XxDOzeOOeic4noiU+X/PhxGOHdQI9ODDg3LMcelxuwwZNO3bEcZgfgwDmWxivHWHoiCt8sT6GOPthBJDs0vPG4C02~4273207~4408368; _abck=1B50FFDB4C14C00831399E519B7910EC~0~YAAQn0g7F0oIhi+XAQAAbdvjPQ4+KoT3dLV1855H9xvsmjvGv3K33ifXipyHxqravoQgFQH0gEzu2BosfWilvbHr8ehGskKSY3cNGiev8p4iUktxmyDQg6rV38qjidhFo4Sd/B9e7ygHk0QZwUWqRSKeL6gs74l3rhk2D5mxyYHKINY7JPJiK0faMQG6Xsfo10GrD7aNWeHOnwNFF+OE4CP0/v+KW1PZQf+3opDVqtYX4tTsJy5U9vBkKigjFZVXZQAsjnR9o6loLgWeTadF53oUxkcqgXmYuz6N0blTCT449KkUwV5Q11Y245prFuTzVBuO0RzpHft+t7HolZQfgRJkuLrfaHWUBNzQbpQM5ZkJvOv1O0EhriRvDjjrbmJUR2fx7ESpSW1M0wkjKDU+W457Z1DC6LmlDxu6x9ge85jv0jPt1Jzs8Nr39dcPFpcmbClIAkPwk/p9gyPIqr9CRndIpEhoDgMwcHDlUZWW3dkrAOI1zNhFa1MmxJpcA+t2wI9vsGfWUisOpG2e85K8doXnidD7j1oC86HB+PQuU78AUzQvpZMklxirdHng/KSq2eyGc64pdOTfa7n7F800lXgx+XeFrraZZ8vZCBHuYi8z5J5NucMe+Guu+fxIM9o/oSHFUVq2yAtHhN4CN7aiuvkvjs7AYS8D6Isb3VD3RYgENndFP6pNUhWKv7H/M7CIEquUyh3R9keWKds4oFFlCAXkNuFzt7kYxNYlL4kdMDGdksq3KXILPrOBSjdbYgo=~-1~-1~-1; bm_lso=4A75204D00C9D3E996D79F790D34DDDBF64151B0E68E0D20920F119A57BEFFF9~YAAQn0g7FxUIhi+XAQAA69njPQM8Pz/+LCTvZxyvnvoJYDKNr25+S2D7xItajKyDxSWtbfF2qEuqBoHlDP7Hkr8WLkKvpgLK8xdWWiyGMeLe14p7Qzxc7vsdsZtky1NjAHdALW9Ga+3HfMzziyAErwHZwXIUiXNNRkDMgFsOQAT2bxKhZ4An61f6UdfAHzPozRoIRMb+naya9/jzlLCiLREhJPjdg94ksMi7RwV8+roD0lln5JDrzJByLIcsBM+S6qPpbXhbWdV9vqyFLxBso6WuuY7hHTyPEmB9zMaG6KiCUXioHOgS+pIHGrUQx4e5pnCdmvLN1fiUeQERZupjwkgJIZQaIGeeQ0ipnKO/NqeWJj/qagYf1GwknhySfFYRgx/goNVCHzM2H8YUJLmpMxSg/MNd96yiFrcHwQ0BNoF++GVLkOy/uFpJ6rO7NDXtoFVKUBSUGBKP5TJNrYzhlA==^1749090034599; redirect_app_organic_traffic_target=N; bottom_sheet_nudge_banner_ids=CRM-157469_web_1st%2CCRM-157469_web_2nd; bm_sv=E263286DFE6764EE50849DA6C2373548~YAAQn0g7F9sLhi+XAQAAuPjjPRyFR2npNMpf6zNkJUanAThCyrHjdMZH+vds/NRPhkbT7Q64KkhTzQt1SmE42aKZzyZNbBSVT8tr91VFiTpb7KVEhm/gLFfG1IBku3BQSKnNtf4TWtTy1zxsWD0xxAVxrkDO+kLQ4UzX8mFwXQZ8mgrPFUkO0Da3sGugFfdEYXZGahCZfVMRJDelMdV4RE5ZjNiu9GYlFKVxNI1wth7nBLPuJT+CaeTBygKJgZ76l3M=~1; bm_s=YAAQn0g7F/wMhi+XAQAAKwDkPQPXGVNh2x0gKvAb9sWAfQ/OCpEHT7h3ijgS5qvcppelCKXMtsad3x8SjACtRTsllVwNa2dSAVmeJ9vVKDVEVwxxKXCnNK3MJukTZC/ObMkccDb2O46JeRR/1iDigbZ2N9Qp5dldgfFR8IRXxR5zI+KHq5bjMSfnPTYNwCE0rEp94tBkgXIt3nLhzllQarGR46j9tTqWTOkXy78yPVg3jknCYzIXvgp84UXUhegjzcLJt50KoZRAubqgAd4SQg59WcsKgkz+toOxb9QW2B/bUXoskMi7S7oeilSrEzxgCysmok7cueia9+b9OvzA3/VMOWwticYtSIUTX6yQfeZfm6hZm6iFa5o6uLdtJ1BKNwuD46lPwZkOgvc6esAjcEPbAe6ib2QkPr8UyAPm3fEaBjIa9gMUSmO+Dd6IGQb4b3os4gGzOmPJTHw6vQoE2m7lhp2cJOPSxiuK26h5QLfSmI+yIMjPylMPxzCw9w655jooiSlCtSKVG7haaVrRtS8Sqq2DfEmYO0D3mFqiUpz8qJu5z6ZvXUSa95hHXMOLI+ClR/DqbWxUemxAiQjL; __cf_bm=lyS.ojyk7ZQ6suz126Gtj7a5cBy4w7LtOjZDay4vY8Q-1749090045-1.0.1.1-qPIETex0IoIkOVJg7NEBzRD3EGTny9NVndgqHnaW1T6DOLuEy9oNGwtl9dTByc9qoVA7kDN1FZf9pwAXbhcrFR3UoxbXbrcHfLHyWf9SxGA",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Whale/3.20.182.14 Safari/537.36",
}

class CoupangSpider(scrapy.Spider):
    name = "coupang"
    allowed_domains = ["coupang.com", "proxy.scrapeops.io"]
    # start_urls = ["https://coupang.com"]

    def get_scrapeops_url(self, url : str):
        """
        Generate a ScrapeOps proxy URL for the given URL.
        """
        cookies = '_fbp=fb.1.1709172148924.2042270649; gd1=Y; delivery_toggle=false; srp_delivery_toggle=true; MARKETID=17272706554699560993959; x-coupang-accept-language=ko-KR;'
        payload = { 'api_key' : SCRAPEOPS_API_KEY, 'url' : url, 'custome_cookies' : cookies }
        proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
        return proxy_url

    def start_requests(self):
        urls = [
            # "https://www.coupang.com/np/categories/498704/",
            "https://www.coupang.com",
            # "https://www.coupang.com/np/search?component=&q=camping+table&channel=user"
        ]
        for url in urls:
            yield scrapy.Request(url=self.get_scrapeops_url(url), callback=self.parse)

    def parse(self, response):
        print(response.text)
        # for product in response.css(".baby-product"):  # 상품 리스트 선택
        #     yield {
        #         "name": product.css(".name::text").get(),
        #         "price": product.css(".price-value::text").get()
        #     }