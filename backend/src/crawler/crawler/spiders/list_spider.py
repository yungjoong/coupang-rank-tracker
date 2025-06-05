import scrapy
from urllib.parse import urlencode

# 코드 출처 : https://velog.io/@2hannah/%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%97%94%EC%A7%80%EB%8B%88%EC%96%B4%EB%A7%81-Scrapy%EB%A1%9C-%EC%BF%A0%ED%8C%A1-%EC%83%81%ED%92%88-%EB%AA%A9%EB%A1%9D-%ED%81%AC%EB%A1%A4%EB%A7%81-%ED%95%B4%EC%98%A4%EA%B8%B0
# 동작 확인 @ 25.06.05 (for categories)
SCRAPEOPS_API_KEY = "a1173785-8edc-4f47-8444-40915d4cbf6b"

# 동작하는 CURL
"""
curl 'https://m.coupang.com/nm/search?component=&q=%EB%AA%A8%EA%B8%B0%EC%9E%A5&channel=user' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'cache-control: no-cache' \
  -b 'web-session-id=229eae01-af5a-4087-a2ac-3a5dabdb89ed; bm_ss=ab8e18ef4e; x-coupang-target-market=KR; x-coupang-accept-language=ko-KR; PCID=17490972502962738236778; searchKeyword=%EB%AA%A8%EA%B8%B0%EC%9E%A5; searchKeywordType={%22%EB%AA%A8%EA%B8%B0%EC%9E%A5%22:0}; sid=1dce6407f0774794a1e2e1f1cc3e0364d3588a84; MARKETID=17490972502962738236778; helloCoupang=Y; _fbp=fb.1.1749097387662.801372350355765444; bm_mi=E3AF71501D5EB7E9C7CF21A01EE34BC2~YAAQNrxBFwfpdDyXAQAAQ8ZUPhyfCOzhcgGBRirgy0BQznxVrdd3auiVue4BnmmszRBwI6B62FPpw2A6jkWckWGNxOBHLTo+TOLz8ypMBV7wQys05r51kvy5E0Mvv4QEDR06m/SeE4FNGAWkMHXXKTICimQD6nfBnhtHAoJQ4Bmkc7an7RMu+OTpCUoinhmsMBa3L7JY1dSRzXQHOfk3+2+Z89NvySh+pGK8Zc4abgY+upm3ks8MJRahFqUWq7SeAxwVa/zyXX55EhyUsISRXBoJp6OtWldigTxv7JB88QveFF7pMGGmsse9yajKA8HyVWM/smuK3KboQa7g2qyw22Q=~1; ak_bmsc=CBE2858024C0D44BDC74B2E9362C2036~000000000000000000000000000000~YAAQNrxBF+DwdDyXAQAAstRUPhxA6VYOXs3B1Uq5ZPa8nlbz7R3vTrib+gHZmm5uPpfEM34iwO2G1c/ntTwHf45jXfCn8z1aARCECy9wPPmrGOtgRxtKCsarVW9WZAxAlNIaNJDMAlldYHrvxoBwIei/Wbpd8uXX1o2DRxJbc9vFQOOy5JACz/3TmHrVQoxd8ZYhJ2UdvE8M0AUHApUzVU/sdg/zOSBZInDlgF/zV2Rg8azwL+scze7F2HegmT2IzbG/d2MMgXxtKulG1lT4hXIws8tXeVU09D7F8WwUx4EP0SdDeTI+8ZDYvwrpE1ZkNli4IEOs6+QEpJj8XcMakJnOaXuE2/nj5brwSMu/5JxGp9t2G++xdQ1v+EbvA1vaqp6u2kHcFl31QIlMWlAR5ICSmM/TjgC3LscwhYlCLyxeK2awoZRaFgUzDWqfXgiZQ1kD0aGadtieUQ+FOyuOTXjwS3Fy2dXYmhfVqZAedncncpLMT44JC/9LadnA5MxEv2RzTa6AWTuy+81UauIL+VbkXPtR+ZZ6Og==; bm_lso=02E514E6CF0A232C0770F402E81B921B699F61B124CAC04762D9CD1AE12F03CF~YAAQNrxBF3kXdTyXAQAAWyFVPgPPO6lUaSwDOXFDY3ctbDcuw4mWq0Hnqp1gTJLb85aVdzxGEjSvSd05hwoDhxyJjrPtr0OMahaWlIo92MTbzuUrfCXXnBQTQe7N06teHOM5dCmhZTAmxA63kewinc3iCsdLkfIXX/AWRhnAcDrWLsntwLUTBv/OGsA1AViBfysvAx0TOmkX/R8+AK3WyvkmUSr8XeYDvoXEhKcf6QP5fmiqh4hOtrt7bUqhs0tIvdg7AzPDUaT/OtycQ2O19rAGk82oYoxkNeoWmWs7SaXHk2VHxY0u38UF+6ud6NBrOInUc1//D/2a2aRbtlx3tTyxo8SosBuw4rI6DG32EoC45Udvp90q28KexRLKiCb5mAU9BpO9HGxfDG4tZ+vogJ2b8gCGjEqT/+42hrh6R9GB9o1dAw0oFjEL5s9rBd7TJET3RVuV4ryTlxBuGrhvcw==^1749097461500; cto_bundle=dB9Y3F9wNEhUd2wlMkZsaVlUVjMlMkZ2dHVqeVNZWWFMdlBFd0FMUXVyeW5ncHdSNTdLMElSSnVrS0VQeW9ob3Bid3pKYXpEZzZiRkgxa0lvQnlJMDFObXA1c2xZWDh5WFhxSjAlMkZicWNmTEFrQk90UFlWOWFNZ1dtZiUyQm50NEduaFo2Z2tIVXcyNzlWSmN5cG5xTXRTYnpIYjk1MDVVUSUzRCUzRA; baby-isWide=wide; bm_so=EEF4DBE253804B188CE6998088E643305FE14FA09001A04CC6742FA268D2EE70~YAAQbUg7F49o8TCXAQAAQ9qCPgOcinYbJ7r+qvlW/9vBcik/43CkGZMbtVdn/mhnt3kMqQb8+xbRHRVgqvEb+geMmzQ3mnPa7HBixz/f6wXE/3V9rcsMLkCjo3penft/+wyW5XEaz5y5oiDSJurhOfODaoFacCtEpXMVdZLlODZsXrjRpgQtYvV2a+F/9W2OoS9tWXsFryGavDo4yp7jwRtjYY7LaLOgP6Nmur6rUbZkeJelHaf83zllTlz2S2YiQHSwMtu8uI9MbhnW7PyZval8ZddH1KUX5OKjCQ9rYt66MK6wk+tLDonus2zqgaidV01xw8bT413XfuDO8ZFBH2lye+pVFS6QT99OmTJn7pX6XXpe8c0iENKbiA28X5YH3UPuY947ArXXuQxpzqIaZwzPMJJ/K0O3kHj+OfmcPez9gQJ+qacDKJoyCkkF5sRY0i+3/nQQaML7mcPLiDCbtw==; overrideAbTestGroup=%5B%5D; bm_sc=4~1~880806574~YAAQhEg7F7c4cDCXAQAAbiWDPgS71dOfCGaovyRnFV9FEo3ZVjiXvj78hTF4iMbBV5rWlFPA1rB5egbZl2dRt8CaGdn4EmVET0lKF9HwCCrHuss34aiYtuc+jZWPuTR3j6ZBCR1tSxhFQgG3NwJtHvupLlbxzEzZ7dsn/ZNTZNXIQFiGe7K6kJNlVG09rjQgtJc0cJ8jmNK0CzoY9L5K/rO58/9+Jskd5DKTcVJAl0jD7YUK4I9wzNiC8qNu1cHsm9OTEx6qk9LoCZPPk2w3eADCwYaE/TEC/uAJ975Yt2859L9PNnSonRo3+7D8RQNvdkN/NonO+j1U2j/+Ht8qNVxIsjgls6e4+bGqMx5PSs0DL6SzqetHjc5wLh85Tljl5YHESbPtUwbfsaj4bjAmUBbe+u0XEo+ahFofEWzlIuBDIh5SgrsrFByPrzl7FvmDyon4kp/j2IYirRrkW0wIGSPrjeRSStW19fcpBfOY7XSMZdiw+DPG3FBkEuFFXNSIb0p01HH39d2iJcQA; bm_sv=FFB7206A003D2F32245626CDE323BDAB~YAAQhEg7F7g4cDCXAQAAbiWDPhwIhGyiErtiFtIuFf1eij95o31X2J1AnqMoJtv9nZJrTMcYr3zCuPSkV8KeByYO3rK8DP1bVrAZz797XggOTJyy5mq7x+I57PL+p7yobO2Lj6dCM05zYQFH+zb1xqsuXnavYf5HOINFG/0tLh1Q2XCFyP8c7z9yFlXyZ+qSw46ihfPieigCOBLPoE9OjT8lLzKDu3nWbZvKu2Os5tKr3R3VGgfH9lex60KW6diblok=~1; _abck=78338E473AB83633FCC48DD005450690~-1~YAAQhEg7F5o8cDCXAQAAgz2DPg6bkmbyPsAY2YlHNhdhDmaBpOORkfT8PoA3x452i0X67cVQ8+UeoRLg+SMPYU1/0fAE2Nv3SP+oi0HtNhBEj8uyuRi4GsixqWy21ZywbhIw/q5ypSaDxUbDYMs7F0PDWFrwWB4vYatBbx+XAtO1pv+LLSepi7Ku5b0S97qdjyvjf+5r3/FyZ8wbcgpks2R7NwWmV1Xxwt4MebQ5oymMuXhOHLmHqoW5qDd7Lwnqv45DzJhmwrprQxJyJ648Wvz14cFr7xoVZoGTp7PeH/zujxZaFeDV81mLClFmDidUvwOMNYEqaGwRNvMd0Okx2LQz+eHBvWVYJtpz1uIjpgbx9spkMZtBGKonUe8rJMdbwvQhXEBUKCwQqL4+e1dA2mId1LgDDWhW9BrBV9aUOxv1dGR0z6FMXvvzuFk8fl34o97HkVtwjj3J/JdX0CbQzRag1uYbSDjo1apaMSS4cT7qrRgBulXANp2Q+bWpBm1Yu4AcpTClKr/2gKhVbK4nzgaAYaXtRAkBT/nIVQZM+UF3I+nrN/do0fxRM++yY2Aj0DvLCA6eTw2o6d2vvd70xjaTzqlq094U3apCOxG2YHZ7xqN91ZlER+V1NhcOd8lp9rVUgD9Zg4sc7d959PFI7uReCQWBgRsDMpDE6vd4DfajsiIMVQ3CJn3L8ibzIVga2f4PNpoGpQ==~-1~||0||~-1; bm_s=YAAQhUg7F5Gr6zCXAQAAdj6DPgOWF+KZW5I/CKLIPKvzXZQ+6J9Ta5rx1517utjcM4OKL96NLSCFUvEK/UqOZaM3mPU7H55md65aG/rf/idXRV8Alsq9EmfFsPdZomqyF5dY9Swdof4Q9SE4QBTacwKT64JSMN/PSjH8bspwkFe4AKEhY11aDexGra1X+3xJsjktGGDj33FNudpCZLogW/6YHqwOlFra9eXx4pahHcpYLSrOnr5AA5LvtO9B7lReK/68+eXsCfXwFzcqBCuetJ8aIU1TBqEQrWPC3dEH6B7avmA5NuJxRaMrUs6cmf0fdHFY2iK36ylOnd4ymiT8Xrr7TJnRNhMmewJ57D7OPNzP4JgQvi/YPHs0uf4cUvOPEHTkwkjgRCX72pErbBhL+YqVQMektpAU9FHX491gTe5hnKf4j3WmOfnD2Z3zBXNl6UmYK24X2JHgyXYWJ1PxJa1ObdFE0m0DStiR4v6CONi/yifG09Ekgijm8W1MdVAxEAeIbAESyw55acweWalqg9mdY4JHplQ4YANqywSMapWu7Nc8t8D6D1kCVf3fWk7mEj/He3saNcZHGiYs5cE92WcDMQ==; bm_sz=62540C00B84C7A1F3176FFB8475471C1~YAAQhUg7F5Kr6zCXAQAAdj6DPhzPETuNtBXl7cz9w+1pU3K7T/nXjb/F5u/EJeASDXuH4+obugFq32NlZXMCJcQ+EejIwLxWUYvauDGfNnbdFun3iEEwDpWCtrGs9ILXV1NBDmkHP6FvYSY7jPP/kXssnxa7009i99V/CoAW9ZhXsl5lHCQptoZPPKhqn3SXpDlZTYQROP6B4QV91Lbf28yBTK0VJo90+Gst6jbjOEEbnZVreA4+/bk1+MFSwNaKKK1vIJjbVQrqpkU0S+wJrL8LvbHY5M5jVu8buSVlfmGmtsM3QvNMwZJHZFqVTav+47ZhG3uZ6/XcyAdx8TwOvTKI8KTFltlFLBvbYD53w8aJyY+9oUfmnkbhHaYDUHqdb7vXz2mXFitIbs3KLp0KyKpsFrSrNvhA4UAHuJ7VyUhShfKmM+/ykXAO/psTrwsoCcWtfxe8DRmO74L8Z/Putd4yr46Rao5pKbXChnwKkz1RG7yA~3552051~3424568' \
  -H 'pragma: no-cache' \
  -H 'priority: u=0, i' \
  -H 'sec-ch-ua: "Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?1' \
  -H 'sec-ch-ua-platform: "Android"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: none' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36'
"""

"""js
fetch("https://m.coupang.com/nm/search?component=&q=%EB%AA%A8%EA%B8%B0%EC%9E%A5&channel=user", {
  "headers": {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
  },
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
});
"""


"""
curl 'https://www.coupang.com/np/search?component=&q=%EB%AA%A8%EA%B8%B0%EC%9E%A5&channel=user' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'cache-control: no-cache' \
  -b 'PCID=15651274385971747379966; MARKETID=15651274385971747379966; delivery_toggle=false; cto_bundle=Jb0R0V8yVHpBUThwWCUyQmkwWU9xTXppTktVaWVmQzh1RWs4ZDN2eU15JTJGRUlpSFlJUWNHN0RPd2picmtBWXd4YXlhOEFSU3BpYVBLdzFEYzgwMVBCY1hpUjkwcCUyRktuVzJ3UGN4NyUyRmtGVVpvSGdBZGhSaTE2aG82ZWxMc1VVckNTTTRiM0NQVCUyRmt4a2xVUnhlaWlWMzlVWG1lS21RJTNEJTNE; trac_src=1042016; trac_spec=10304903; trac_addtag=900; trac_ctag=HOME; trac_lptag=%EC%BF%A0%ED%8C%A1; trac_itime=20250604130941; x-coupang-accept-language=ko-KR; x-coupang-target-market=KR; sid=833af7b210bd44549f46d70331c7833dd4010499; web-session-id=5a0a41d8-7846-4c48-9321-c56526a78bd5; searchKeyword=%EB%B9%84%ED%83%80%EB%AF%BC|%EC%BA%A0%ED%95%91%20%ED%85%8C%EC%9D%B4%EB%B8%94|camping%20table; searchKeywordType={%22%EB%B9%84%ED%83%80%EB%AF%BC%22:0}|{%22%EC%BA%A0%ED%95%91%20%ED%85%8C%EC%9D%B4%EB%B8%94%22:0}|{%22camping%20table%22:0}; bottom_sheet_nudge_banner_ids=CRM-157469_web_1st%2CCRM-157469_web_2nd; bm_ss=ab8e18ef4e; bm_so=0E1B9F735C9F3A0E61F3205DAF37EA0CB4D25BBEB26D5B36C48F5E0B23212909~YAAQPLxBF4PG1jeXAQAA8lkPPgO+lUiHht/pThb3n1RRwmE9eTAnjwMMBQmkvxvcbPz9b7FmktUt6qUhVwA+lYEYmWw9BkeaUGv1EHVBjSc3o7gLon60aKe4bj78vjibzE/gmVW6S4n9L78irraLAd2U3U6wgjgmeoLBY2Xj+4iHMOZvDVe4u4UFecV4TZpCAzgBOi0Qn0QRem6Tv8yVrARmxEIUHIgW61QimSrSu6t1Pr8Ey73VVQbCcKCWLyawybhnoVsHHIPwmPocXTdm/Lzdwl2Q1m4VTrf8Ob0GcQnOIf1A/965jdyztX9YFzG1cvSVXH04fmE2hgfmp949LnhTeQjGBgopQ3cRPed55+nwPwmxTjPB9T4eEURXo6IrK1OtrNEkQoPZPamdRMhJQojruSbeyklBvoBaBkK5Z9p91HJZpE9L3CoBr9sF6Zj/uDurB+oQWWq6P+T8sqcAxA==; bm_sz=E1F4B1D5A4B6DF851165EDBA462258BD~YAAQPLxBF4XG1jeXAQAA8lkPPhzH9QTFEBmcQK7yO0Hh3l/ONE0V+mgnEXr16hMBsBZBRQPB/HwB74IU/Se/TlHBFELwpXxLDiFxcWToCXKY4tSeE9LgmMzTywf2PPNeUjxyH1P0SVkC7q2SYyJkGOhUTMT6m0+ouZCr5dy6cdS0S4i+Xx++PKq4m5fgzImluMK1P/G7oK3NWrNVz9UHRq/N9H/sGzf/t47qBOGgSNbzN+ZVYyRxk2MDKOHtjwnwD2oz9D8tBrB3mbdloVyBVdJFWT2zuYDxoPo5vtTlkNYB3uU8ZHUomdH2dFeTuosJRe6ZWg9qP3nTcLfPbbWXaq31MC1eYmyN67OuHajvYgoz0n7PIopghHqaw0F5a8lEveSS7wwt/GK5pYRuyYLkcC+FUbd+B6PC+cfSyWhad1Va9gwfwACgvnyTtZ6AvPZI7kxHxPMj9Qv9fg+rohaH/F1ztEuqUL57ij/J2panLC+wRigbE0amZLKz6Dbo+soizypN/6cQ14pCK8Nf3fNUoi8ZQOQhUNHMfQ==~4273207~4408368; bm_lso=0E1B9F735C9F3A0E61F3205DAF37EA0CB4D25BBEB26D5B36C48F5E0B23212909~YAAQPLxBF4PG1jeXAQAA8lkPPgO+lUiHht/pThb3n1RRwmE9eTAnjwMMBQmkvxvcbPz9b7FmktUt6qUhVwA+lYEYmWw9BkeaUGv1EHVBjSc3o7gLon60aKe4bj78vjibzE/gmVW6S4n9L78irraLAd2U3U6wgjgmeoLBY2Xj+4iHMOZvDVe4u4UFecV4TZpCAzgBOi0Qn0QRem6Tv8yVrARmxEIUHIgW61QimSrSu6t1Pr8Ey73VVQbCcKCWLyawybhnoVsHHIPwmPocXTdm/Lzdwl2Q1m4VTrf8Ob0GcQnOIf1A/965jdyztX9YFzG1cvSVXH04fmE2hgfmp949LnhTeQjGBgopQ3cRPed55+nwPwmxTjPB9T4eEURXo6IrK1OtrNEkQoPZPamdRMhJQojruSbeyklBvoBaBkK5Z9p91HJZpE9L3CoBr9sF6Zj/uDurB+oQWWq6P+T8sqcAxA==^1749092886225; redirect_app_organic_traffic_target=N; bm_s=YAAQPLxBF/km1zeXAQAAmPYPPgMBsCAuWoe3X1fEyVnj6qeT3zUddy8Tv749K+yryUHQdCgDf7DXLkkEcSqOvlxnkFzcTLGv29Faooh4WaxHmdu4pikRMgPxlpcavHdZECrPonAyCdWTt17M89+XtmjzrJSXgHQB4UuBe6wZII3KcVsMjIAZWRKla+m0T5ASBrvzMnm+FpLvRf849djHvaUyNeFcmf9EKrSs91iuas3t1xCaCK0TpeKhsFG3Sni2tJWQAlRTOPBfVS5pKrPUNoTLFYY277EETw0oNZ1r8u6gpvMJamewyy1M0Oofxr9+l6u9f/TiT/zvPsLL9YLipuK7kISeAbznIpl5gu2Ytl130ffU7j63ZwP/8s1OJHrH0oFqrIiuzU/OvY4cXWg4dBOPtsRToXmuYSOhJncFEB5oppVWVc00xfI6zGqyGn8onhT5Fh+7gQ3u4P04W91r5X/8aaoQ8ISEJ5L/UtxdPwqA3nPAvrnLvXkWJczNd79nO8+i51TUrSeEQsEBtYUFTG5ADVfe1DxqWxIrCEompIqaP3LaVbkdkHwFiXSgjKmaoeyHhzhgbRgDQloicmTu; ak_bmsc=32E5D48874DE77C13129AF7D3451C567~000000000000000000000000000000~YAAQjkg7F2vnWiaXAQAAlcYpPhxrQeFoSVD4RCaueak9ovWZQCQzegcMIgyJnOMt+UfBFIR/YxGHE71P/r8kEkBPqydDQCmbaOWlhl52fPN3b64GItAZnfpRNNIuk4u8hF3IR4pRegux3llBxQrR3WrMcNiXWbNOjL/B0UReA7YHUQXyrBp0X3cckl4kCeHDDRjegQ5I385qqeqArjdry4tMBb33Rq7k8RZHn8YEYVqU7S88+t5C8LY008NzORa0s8YgRsT9r5CfaJgkPLbL/1IFvsuF4lxv1WJ+npsrMY/IusowpE3u4AFbR+rGn+7hedzqBAZ5x8na07O2oPi3AIvZ4uCvK3meFRMqhl4=; _abck=1B50FFDB4C14C00831399E519B7910EC~-1~YAAQhkg7F+gorjiXAQAAY9QpPg4SWWgb4QBfb3hW3q+jc6errjTanXWrzcfwj4zWT/lc3cEjrNXKo96RNcZ+JuEBw/P55DhxbGpc5dv9o5wdp51orXjUw/BZpUkc5tUbAruOxQ63ecSQWjtcutZNbgeE/Tw7Wwa4BQXUfcGCdkH8L+YIO6fMlFSvopB3ZnxjbwZ5sgYTSKzzHhQrTH4aHwmF63TIejDggNWnK+UzKjBdVJCparj19bSOPQc6rGZ8GSyKNmUiT3/ZCfzeAlCWUqDQ2SnzDD7bEENAipgYcIcXcGmIIkueXkV0KG8LyA349ElRz479H9Ezbciul8N5x+rEjb9jNpWWvAR/ypsSfkPNKKX29/1FQa643+L4e64mYDlzeApJxYWgm1gk/RRwjIuwTIjMVcns1Kq+PMt+EAk/sKPOB81+7HOBeKoXa4lJbezyxMloXN+RhDovXhdlM9O8ejFscEwM6/z5QW71GE7c2kaZExjEofdTqAuReUWVr923mOHjh5XoLzagRSADSYzmrZWVl4NUnYomM4IC0Ufp0ay/vCaMb+D65hnkg+3aLDx9nGSaRm/8036LELw9WYtbu/iiJxxdko6RxUpE/TArKBzF1O4EZ/Ls9qdP9EfuFYoZw1w68h5Jm/PdDnLSTMNNBG8VzuaTRV1GtEFSqXKdVNKkcmU0NC7wpDd0WVZLQTXPALoummPla8gJXjdCaMnkcqd5Lv6D+LdZLPopkxg+jUFG6PIn0KLVpTK18lBc2A2R9qlxRk+9lIcOdQSYZ2NbPAxbycz5o2SwzZw=~-1~||0||~-1; bm_sv=12FA0405DA8FD6FDA728984B3319F19C~YAAQhkg7F5cwrjiXAQAA4g8qPhzfc9J/8zV5wKGeYHbL3IQ01uqJyJbK8S49nWCPcRHo9v36oIkiFQvV+WmoTKxWx/0CsLYQOvgUDQidbnamgsrbsRuw33bqtu3aHpbPFCLnKxAGTJZIK3F2xSBJ9nAnDRjQrzHtCRkQtZd3YpTgn1MaqzrXAYxT4KNMJpJqPhtkKQeht192ntYWwQiIRI2ZX6arF6rG7qLC+mI14p4sTXTIEJQdzfLfgxh87M0SiA==~1' \
  -H 'pragma: no-cache' \
  -H 'priority: u=0, i' \
  -H 'referer: https://www.coupang.com/np/search?component=&q=%EB%AA%A8%EA%B8%B0%EC%9E%A5&channel=user' \
  -H 'sec-ch-ua: "Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?1' \
  -H 'sec-ch-ua-platform: "Android"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: same-origin' \
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