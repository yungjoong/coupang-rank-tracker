import scrapy
from urllib.parse import urlencode

# 코드 출처 : https://velog.io/@2hannah/%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%97%94%EC%A7%80%EB%8B%88%EC%96%B4%EB%A7%81-Scrapy%EB%A1%9C-%EC%BF%A0%ED%8C%A1-%EC%83%81%ED%92%88-%EB%AA%A9%EB%A1%9D-%ED%81%AC%EB%A1%A4%EB%A7%81-%ED%95%B4%EC%98%A4%EA%B8%B0
# 동작 확인 @ 25.06.05 (for categories)
SCRAPEOPS_API_KEY = "a1173785-8edc-4f47-8444-40915d4cbf6b"

# 동작하는 CURL
"""
curl 'https://www.coupang.com/np/search?q=camping%20table&channel=recent' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'cache-control: no-cache' \
  -b 'PCID=15651274385971747379966; MARKETID=15651274385971747379966; delivery_toggle=false; cto_bundle=Jb0R0V8yVHpBUThwWCUyQmkwWU9xTXppTktVaWVmQzh1RWs4ZDN2eU15JTJGRUlpSFlJUWNHN0RPd2picmtBWXd4YXlhOEFSU3BpYVBLdzFEYzgwMVBCY1hpUjkwcCUyRktuVzJ3UGN4NyUyRmtGVVpvSGdBZGhSaTE2aG82ZWxMc1VVckNTTTRiM0NQVCUyRmt4a2xVUnhlaWlWMzlVWG1lS21RJTNEJTNE; trac_src=1042016; trac_spec=10304903; trac_addtag=900; trac_ctag=HOME; trac_lptag=%EC%BF%A0%ED%8C%A1; trac_itime=20250604130941; x-coupang-accept-language=ko-KR; x-coupang-target-market=KR; sid=833af7b210bd44549f46d70331c7833dd4010499; web-session-id=5a0a41d8-7846-4c48-9321-c56526a78bd5; searchKeyword=%EB%B9%84%ED%83%80%EB%AF%BC|%EC%BA%A0%ED%95%91%20%ED%85%8C%EC%9D%B4%EB%B8%94|camping%20table; searchKeywordType={%22%EB%B9%84%ED%83%80%EB%AF%BC%22:0}|{%22%EC%BA%A0%ED%95%91%20%ED%85%8C%EC%9D%B4%EB%B8%94%22:0}|{%22camping%20table%22:0}; bottom_sheet_nudge_banner_ids=CRM-157469_web_1st%2CCRM-157469_web_2nd; bm_ss=ab8e18ef4e; bm_so=0E1B9F735C9F3A0E61F3205DAF37EA0CB4D25BBEB26D5B36C48F5E0B23212909~YAAQPLxBF4PG1jeXAQAA8lkPPgO+lUiHht/pThb3n1RRwmE9eTAnjwMMBQmkvxvcbPz9b7FmktUt6qUhVwA+lYEYmWw9BkeaUGv1EHVBjSc3o7gLon60aKe4bj78vjibzE/gmVW6S4n9L78irraLAd2U3U6wgjgmeoLBY2Xj+4iHMOZvDVe4u4UFecV4TZpCAzgBOi0Qn0QRem6Tv8yVrARmxEIUHIgW61QimSrSu6t1Pr8Ey73VVQbCcKCWLyawybhnoVsHHIPwmPocXTdm/Lzdwl2Q1m4VTrf8Ob0GcQnOIf1A/965jdyztX9YFzG1cvSVXH04fmE2hgfmp949LnhTeQjGBgopQ3cRPed55+nwPwmxTjPB9T4eEURXo6IrK1OtrNEkQoPZPamdRMhJQojruSbeyklBvoBaBkK5Z9p91HJZpE9L3CoBr9sF6Zj/uDurB+oQWWq6P+T8sqcAxA==; bm_sz=E1F4B1D5A4B6DF851165EDBA462258BD~YAAQPLxBF4XG1jeXAQAA8lkPPhzH9QTFEBmcQK7yO0Hh3l/ONE0V+mgnEXr16hMBsBZBRQPB/HwB74IU/Se/TlHBFELwpXxLDiFxcWToCXKY4tSeE9LgmMzTywf2PPNeUjxyH1P0SVkC7q2SYyJkGOhUTMT6m0+ouZCr5dy6cdS0S4i+Xx++PKq4m5fgzImluMK1P/G7oK3NWrNVz9UHRq/N9H/sGzf/t47qBOGgSNbzN+ZVYyRxk2MDKOHtjwnwD2oz9D8tBrB3mbdloVyBVdJFWT2zuYDxoPo5vtTlkNYB3uU8ZHUomdH2dFeTuosJRe6ZWg9qP3nTcLfPbbWXaq31MC1eYmyN67OuHajvYgoz0n7PIopghHqaw0F5a8lEveSS7wwt/GK5pYRuyYLkcC+FUbd+B6PC+cfSyWhad1Va9gwfwACgvnyTtZ6AvPZI7kxHxPMj9Qv9fg+rohaH/F1ztEuqUL57ij/J2panLC+wRigbE0amZLKz6Dbo+soizypN/6cQ14pCK8Nf3fNUoi8ZQOQhUNHMfQ==~4273207~4408368; bm_lso=0E1B9F735C9F3A0E61F3205DAF37EA0CB4D25BBEB26D5B36C48F5E0B23212909~YAAQPLxBF4PG1jeXAQAA8lkPPgO+lUiHht/pThb3n1RRwmE9eTAnjwMMBQmkvxvcbPz9b7FmktUt6qUhVwA+lYEYmWw9BkeaUGv1EHVBjSc3o7gLon60aKe4bj78vjibzE/gmVW6S4n9L78irraLAd2U3U6wgjgmeoLBY2Xj+4iHMOZvDVe4u4UFecV4TZpCAzgBOi0Qn0QRem6Tv8yVrARmxEIUHIgW61QimSrSu6t1Pr8Ey73VVQbCcKCWLyawybhnoVsHHIPwmPocXTdm/Lzdwl2Q1m4VTrf8Ob0GcQnOIf1A/965jdyztX9YFzG1cvSVXH04fmE2hgfmp949LnhTeQjGBgopQ3cRPed55+nwPwmxTjPB9T4eEURXo6IrK1OtrNEkQoPZPamdRMhJQojruSbeyklBvoBaBkK5Z9p91HJZpE9L3CoBr9sF6Zj/uDurB+oQWWq6P+T8sqcAxA==^1749092886225; redirect_app_organic_traffic_target=N; bm_s=YAAQPLxBF/km1zeXAQAAmPYPPgMBsCAuWoe3X1fEyVnj6qeT3zUddy8Tv749K+yryUHQdCgDf7DXLkkEcSqOvlxnkFzcTLGv29Faooh4WaxHmdu4pikRMgPxlpcavHdZECrPonAyCdWTt17M89+XtmjzrJSXgHQB4UuBe6wZII3KcVsMjIAZWRKla+m0T5ASBrvzMnm+FpLvRf849djHvaUyNeFcmf9EKrSs91iuas3t1xCaCK0TpeKhsFG3Sni2tJWQAlRTOPBfVS5pKrPUNoTLFYY277EETw0oNZ1r8u6gpvMJamewyy1M0Oofxr9+l6u9f/TiT/zvPsLL9YLipuK7kISeAbznIpl5gu2Ytl130ffU7j63ZwP/8s1OJHrH0oFqrIiuzU/OvY4cXWg4dBOPtsRToXmuYSOhJncFEB5oppVWVc00xfI6zGqyGn8onhT5Fh+7gQ3u4P04W91r5X/8aaoQ8ISEJ5L/UtxdPwqA3nPAvrnLvXkWJczNd79nO8+i51TUrSeEQsEBtYUFTG5ADVfe1DxqWxIrCEompIqaP3LaVbkdkHwFiXSgjKmaoeyHhzhgbRgDQloicmTu; ak_bmsc=32E5D48874DE77C13129AF7D3451C567~000000000000000000000000000000~YAAQjkg7F2vnWiaXAQAAlcYpPhxrQeFoSVD4RCaueak9ovWZQCQzegcMIgyJnOMt+UfBFIR/YxGHE71P/r8kEkBPqydDQCmbaOWlhl52fPN3b64GItAZnfpRNNIuk4u8hF3IR4pRegux3llBxQrR3WrMcNiXWbNOjL/B0UReA7YHUQXyrBp0X3cckl4kCeHDDRjegQ5I385qqeqArjdry4tMBb33Rq7k8RZHn8YEYVqU7S88+t5C8LY008NzORa0s8YgRsT9r5CfaJgkPLbL/1IFvsuF4lxv1WJ+npsrMY/IusowpE3u4AFbR+rGn+7hedzqBAZ5x8na07O2oPi3AIvZ4uCvK3meFRMqhl4=; _abck=1B50FFDB4C14C00831399E519B7910EC~-1~YAAQhkg7F+gorjiXAQAAY9QpPg4SWWgb4QBfb3hW3q+jc6errjTanXWrzcfwj4zWT/lc3cEjrNXKo96RNcZ+JuEBw/P55DhxbGpc5dv9o5wdp51orXjUw/BZpUkc5tUbAruOxQ63ecSQWjtcutZNbgeE/Tw7Wwa4BQXUfcGCdkH8L+YIO6fMlFSvopB3ZnxjbwZ5sgYTSKzzHhQrTH4aHwmF63TIejDggNWnK+UzKjBdVJCparj19bSOPQc6rGZ8GSyKNmUiT3/ZCfzeAlCWUqDQ2SnzDD7bEENAipgYcIcXcGmIIkueXkV0KG8LyA349ElRz479H9Ezbciul8N5x+rEjb9jNpWWvAR/ypsSfkPNKKX29/1FQa643+L4e64mYDlzeApJxYWgm1gk/RRwjIuwTIjMVcns1Kq+PMt+EAk/sKPOB81+7HOBeKoXa4lJbezyxMloXN+RhDovXhdlM9O8ejFscEwM6/z5QW71GE7c2kaZExjEofdTqAuReUWVr923mOHjh5XoLzagRSADSYzmrZWVl4NUnYomM4IC0Ufp0ay/vCaMb+D65hnkg+3aLDx9nGSaRm/8036LELw9WYtbu/iiJxxdko6RxUpE/TArKBzF1O4EZ/Ls9qdP9EfuFYoZw1w68h5Jm/PdDnLSTMNNBG8VzuaTRV1GtEFSqXKdVNKkcmU0NC7wpDd0WVZLQTXPALoummPla8gJXjdCaMnkcqd5Lv6D+LdZLPopkxg+jUFG6PIn0KLVpTK18lBc2A2R9qlxRk+9lIcOdQSYZ2NbPAxbycz5o2SwzZw=~-1~||0||~-1; bm_sv=12FA0405DA8FD6FDA728984B3319F19C~YAAQhkg7F5cwrjiXAQAA4g8qPhzfc9J/8zV5wKGeYHbL3IQ01uqJyJbK8S49nWCPcRHo9v36oIkiFQvV+WmoTKxWx/0CsLYQOvgUDQidbnamgsrbsRuw33bqtu3aHpbPFCLnKxAGTJZIK3F2xSBJ9nAnDRjQrzHtCRkQtZd3YpTgn1MaqzrXAYxT4KNMJpJqPhtkKQeht192ntYWwQiIRI2ZX6arF6rG7qLC+mI14p4sTXTIEJQdzfLfgxh87M0SiA==~1' \
  -H 'pragma: no-cache' \
  -H 'priority: u=0, i' \
  -H 'referer: https://www.coupang.com/np/search?q=%EC%BA%A0%ED%95%91+%ED%85%8C%EC%9D%B4%EB%B8%94&channel=auto&page=2' \
  -H 'sec-ch-ua: "Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?1' \
  -H 'sec-ch-ua-platform: "Android"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36'
"""

headers = {
  'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
  'Cache-Control' : 'no-cache',
  'Pragma' : 'no-cache',
  'Priority' : 'u=0, i',
  'Referer' : 'https://www.coupang.com/np/search?q=%EC%BA%A0%ED%95%91+%ED%85%8C%EC%9D%B4%EB%B8%94&channel=auto&page=2',
  'Sec-Ch-Ua' : '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
  'Sec-Ch-Ua-Mobile' : '?1',
  'Sec-Ch-Ua-Platform' : '"Android"',
  'Sec-Fetch-Dest' : 'document',
  'Sec-Fetch-Mode' : 'navigate',
  'Sec-Fetch-Site' : 'same-origin',
  'Sec-Fetch-User' : '?1',
  'Upgrade-Insecure-Requests' : '1',
  'User-Agent' : 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36'
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
        payload = { 'api_key' : SCRAPEOPS_API_KEY, 'url' : url, 'custom_cookies' : cookies }
        proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
        return proxy_url

    def start_requests(self):
        cookies = {
            'PCID' : '15651274385971747379966',
            'MARKETID' : '15651274385971747379966',
            'delivery_toggle' : 'false',
            'cto_bundle' : 'Jb0R0V8yVHpBUThwWCUyQmkwWU9xTXppTktVaWVmQzh1RWs4ZDN2eU15JTJGRUlpSFlJUWNHN0RPd2picmtBWXd4YXlhOEFSU3BpYVBLdzFEYzgwMVBCY1hpUjkwcCUyRktuVzJ3UGN4NyUyRmtGVVpvSGdBZGhSaTE2aG82ZWxMc1VVckNTTTRiM0NQVCUyRmt4a2xVUnhlaWlWMzlVWG1lS21RJTNEJTNE',
            'trac_src' : '1042016',
            'trac_spec' : '10304903',
            'trac_addtag' : '900',
            'trac_ctag' : 'HOME',
            'trac_lptag' : '%EC%BF%A0%ED%8C%A1',
            'trac_itime' : '20250604130941',
            'x-coupang-accept-language' : 'ko-KR',
            'x-coupang-target-market' : 'KR',
            'sid' : '833af7b210bd44549f46d70331c7833dd4010499',
            'web-session-id' : '5a0a41d8-7846-4c48-9321-c56526a78bd5',
            'searchKeyword' : '%EB%B9%84%ED%83%80%EB%AF%BC|%EC%BA%A0%ED%95%91%20%ED%85%8C%EC%9D%B4%EB%B8%94|camping%20table',
            'searchKeywordType' : '{%22%EB%B9%84%ED%83%80%EB%AF%BC%22:0}|{%22%EC%BA%A0%ED%95%91%20%ED%85%8C%EC%9D%B4%EB%B8%94%22:0}|{%22camping%20table%22:0}',
            'bottom_sheet_nudge_banner_ids' : 'CRM-157469_web_1st%2CCRM-157469_web_2nd',
            'bm_ss' : 'ab8e18ef4e',
            'bm_so' : '0E1B9F735C9F3A0E61F3205DAF37EA0CB4D25BBEB26D5B36C48F5E0B23212909~YAAQPLxBF4PG1jeXAQAA8lkPPgO+lUiHht/pThb3n1RRwmE9eTAnjwMMBQmkvxvcbPz9b7FmktUt6qUhVwA+lYEYmWw9BkeaUGv1EHVBjSc3o7gLon60aKe4bj78vjibzE/gmVW6S4n9L78irraLAd2U3U6wgjgmeoLBY2Xj+4iHMOZvDVe4u4UFecV4TZpCAzgBOi0Qn0QRem6Tv8yVrARmxEIUHIgW61QimSrSu6t1Pr8Ey73VVQbCcKCWLyawybhnoVsHHIPwmPocXTdm/Lzdwl2Q1m4VTrf8Ob0GcQnOIf1A/965jdyztX9YFzG1cvSVXH04fmE2hgfmp949LnhTeQjGBgopQ3cRPed55+nwPwmxTjPB9T4eEURXo6IrK1OtrNEkQoPZPamdRMhJQojruSbeyklBvoBaBkK5Z9p91HJZpE9L3CoBr9sF6Zj/uDurB+oQWWq6P+T8sqcAxA==',
            'bm_sz' : 'E1F4B1D5A4B6DF851165EDBA462258BD~YAAQPLxBF4XG1jeXAQAA8lkPPhzH9QTFEBmcQK7yO0Hh3l/ONE0V+mgnEXr16hMBsBZBRQPB/HwB74IU/Se/TlHBFELwpXxLDiFxcWToCXKY4tSeE9LgmMzTywf2PPNeUjxyH1P0SVkC7q2SYyJkGOhUTMT6m0+ouZCr5dy6cdS0S4i+Xx++PKq4m5fgzImluMK1P/G7oK3NWrNVz9UHRq/N9H/sGzf/t47qBOGgSNbzN+ZVYyRxk2MDKOHtjwnwD2oz9D8tBrB3mbdloVyBVdJFWT2zuYDxoPo5vtTlkNYB3uU8ZHUomdH2dFeTuosJRe6ZWg9qP3nTcLfPbbWXaq31MC1eYmyN67OuHajvYgoz0n7PIopghHqaw0F5a8lEveSS7wwt/GK5pYRuyYLkcC+FUbd+B6PC+cfSyWhad1Va9gwfwACgvnyTtZ6AvPZI7kxHxPMj9Qv9fg+rohaH/F1ztEuqUL57ij/J2panLC+wRigbE0amZLKz6Dbo+soizypN/6cQ14pCK8Nf3fNUoi8ZQOQhUNHMfQ==~4273207~4408368',
            'bm_lso' : '0E1B9F735C9F3A0E61F3205DAF37EA0CB4D25BBEB26D5B36C48F5E0B23212909~YAAQPLxBF4PG1jeXAQAA8lkPPgO+lUiHht/pThb3n1RRwmE9eTAnjwMMBQmkvxvcbPz9b7FmktUt6qUhVwA+lYEYmWw9BkeaUGv1EHVBjSc3o7gLon60aKe4bj78vjibzE/gmVW6S4n9L78irraLAd2U3U6wgjgmeoLBY2Xj+4iHMOZvDVe4u4UFecV4TZpCAzgBOi0Qn0QRem6Tv8yVrARmxEIUHIgW61QimSrSu6t1Pr8Ey73VVQbCcKCWLyawybhnoVsHHIPwmPocXTdm/Lzdwl2Q1m4VTrf8Ob0GcQnOIf1A/965jdyztX9YFzG1cvSVXH04fmE2hgfmp949LnhTeQjGBgopQ3cRPed55+nwPwmxTjPB9T4eEURXo6IrK1OtrNEkQoPZPamdRMhJQojruSbeyklBvoBaBkK5Z9p91HJZpE9L3CoBr9sF6Zj/uDurB+oQWWq6P+T8sqcAxA==^1749092886225',
            'redirect_app_organic_traffic_target' : 'N',
            'bm_s' : 'YAAQPLxBF/km1zeXAQAAmPYPPgMBsCAuWoe3X1fEyVnj6qeT3zUddy8Tv749K+yryUHQdCgDf7DXLkkEcSqOvlxnkFzcTLGv29Faooh4WaxHmdu4pikRMgPxlpcavHdZECrPonAyCdWTt17M89+XtmjzrJSXgHQB4UuBe6wZII3KcVsMjIAZWRKla+m0T5ASBrvzMnm+FpLvRf849djHvaUyNeFcmf9EKrSs91iuas3t1xCaCK0TpeKhsFG3Sni2tJWQAlRTOPBfVS5pKrPUNoTLFYY277EETw0oNZ1r8u6gpvMJamewyy1M0Oofxr9+l6u9f/TiT/zvPsLL9YLipuK7kISeAbznIpl5gu2Ytl130ffU7j63ZwP/8s1OJHrH0oFqrIiuzU/OvY4cXWg4dBOPtsRToXmuYSOhJncFEB5oppVWVc00xfI6zGqyGn8onhT5Fh+7gQ3u4P04W91r5X/8aaoQ8ISEJ5L/UtxdPwqA3nPAvrnLvXkWJczNd79nO8+i51TUrSeEQsEBtYUFTG5ADVfe1DxqWxIrCEompIqaP3LaVbkdkHwFiXSgjKmaoeyHhzhgbRgDQloicmTu',
            'ak_bmsc' : '32E5D48874DE77C13129AF7D3451C567~000000000000000000000000000000~YAAQjkg7F2vnWiaXAQAAlcYpPhxrQeFoSVD4RCaueak9ovWZQCQzegcMIgyJnOMt+UfBFIR/YxGHE71P/r8kEkBPqydDQCmbaOWlhl52fPN3b64GItAZnfpRNNIuk4u8hF3IR4pRegux3llBxQrR3WrMcNiXWbNOjL/B0UReA7YHUQXyrBp0X3cckl4kCeHDDRjegQ5I385qqeqArjdry4tMBb33Rq7k8RZHn8YEYVqU7S88+t5C8LY008NzORa0s8YgRsT9r5CfaJgkPLbL/1IFvsuF4lxv1WJ+npsrMY/IusowpE3u4AFbR+rGn+7hedzqBAZ5x8na07O2oPi3AIvZ4uCvK3meFRMqhl4=',
             '_abck' : '1B50FFDB4C14C00831399E519B7910EC~-1~YAAQhkg7F+gorjiXAQAAY9QpPg4SWWgb4QBfb3hW3q+jc6errjTanXWrzcfwj4zWT/lc3cEjrNXKo96RNcZ+JuEBw/P55DhxbGpc5dv9o5wdp51orXjUw/BZpUkc5tUbAruOxQ63ecSQWjtcutZNbgeE/Tw7Wwa4BQXUfcGCdkH8L+YIO6fMlFSvopB3ZnxjbwZ5sgYTSKzzHhQrTH4aHwmF63TIejDggNWnK+UzKjBdVJCparj19bSOPQc6rGZ8GSyKNmUiT3/ZCfzeAlCWUqDQ2SnzDD7bEENAipgYcIcXcGmIIkueXkV0KG8LyA349ElRz479H9Ezbciul8N5x+rEjb9jNpWWvAR/ypsSfkPNKKX29/1FQa643+L4e64mYDlzeApJxYWgm1gk/RRwjIuwTIjMVcns1Kq+PMt+EAk/sKPOB81+7HOBeKoXa4lJbezyxMloXN+RhDovXhdlM9O8ejFscEwM6/z5QW71GE7c2kaZExjEofdTqAuReUWVr923mOHjh5XoLzagRSADSYzmrZWVl4NUnYomM4IC0Ufp0ay/vCaMb+D65hnkg+3aLDx9nGSaRm/8036LELw9WYtbu/iiJxxdko6RxUpE/TArKBzF1O4EZ/Ls9qdP9EfuFYoZw1w68h5Jm/PdDnLSTMNNBG8VzuaTRV1GtEFSqXKdVNKkcmU0NC7wpDd0WVZLQTXPALoummPla8gJXjdCaMnkcqd5Lv6D+LdZLPopkxg+jUFG6PIn0KLVpTK18lBc2A2R9qlxRk+9lIcOdQSYZ2NbPAxbycz5o2SwzZw=~-1~||0||~-1',
             'bm_sv' : '12FA0405DA8FD6FDA728984B3319F19C~YAAQhkg7F5cwrjiXAQAA4g8qPhzfc9J/8zV5wKGeYHbL3IQ01uqJyJbK8S49nWCPcRHo9v36oIkiFQvV+WmoTKxWx/0CsLYQOvgUDQidbnamgsrbsRuw33bqtu3aHpbPFCLnKxAGTJZIK3F2xSBJ9nAnDRjQrzHtCRkQtZd3YpTgn1MaqzrXAYxT4KNMJpJqPhtkKQeht192ntYWwQiIRI2ZX6arF6rG7qLC+mI14p4sTXTIEJQdzfLfgxh87M0SiA==~1'
        }
        urls = [
            # "https://www.coupang.com/np/categories/498704/",
            # "https://www.coupang.com",
            # "https://www.coupang.com/vp/product/reviews?productId=8599565520&page=1&size=5&sortBy=ORDER_SCORE_ASC&ratings=&q=&viRoleCode=3&ratingSummary=true"
            # "https://www.coupang.com/np/search?component=&q={}&channel=user"
            # "https://www.coupang.com/np/search?q=%EC%BA%A0%ED%95%91+%ED%85%8C%EC%9D%B4%EB%B8%94&channel=auto"
            "https://www.coupang.com/np/search?q=camping+table&channel=recent"
        ]
        for url in urls:
            yield scrapy.Request(url=url, cookies=cookies, callback=self.parse)

    def parse(self, response):
        print(response.text)
        # for product in response.css(".baby-product"):  # 상품 리스트 선택
        #     yield {
        #         "name": product.css(".name::text").get(),
        #         "price": product.css(".price-value::text").get()
        #     }