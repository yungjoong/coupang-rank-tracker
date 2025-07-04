## 환경설정 확인

```bash
git config --get pull.rebase
git config --global --get pull.rebase

# False 가 나와야 함. 아니라면

git config --global pull.rebase false
git config pull.rebase false
```

## 참고한 문서들
* [Scrapy Playwright: Complete Tutorial 2025](https://www.zenrows.com/blog/scrapy-playwright#set-up-a-scrapy-project)
* [How to Use Playwright Stealth for Scraping](https://www.zenrows.com/blog/playwright-stealth#what-is)
* [Scrapy Impersonate: Advanced Tutorial for 2025](https://www.zenrows.com/blog/scrapy-impersonate#why-scrapy-impersonate)

## 환경변수 설정

1. Copy the example environment file:
```bash
cp backend/.env.example backend/.env
```

2. Update the environment variables in `.env` with your values
```

# Coupang Rank Tracker

## 오늘(25.7.5)  작업한 내용

- 쿠팡 상품 검색 결과에서 여러 페이지(1~N페이지) 상품 정보를 크롤링하는 기능 구현
- 페이지네이션(다음 페이지 이동) 시 동적으로 변하는 class명을 견고하게 처리하는 방법 논의
- Selenium/undetected_chromedriver 환경에서 driver가 비정상 종료될 때의 예외 처리 및 안전성 강화
- driver 접근 시마다 try-except로 감싸서 크롤러가 중단되지 않도록 개선
- 페이지네이션 div의 class명이 동적으로 바뀌는 문제로 selector를 개선하는 방법 실험
- 디버깅을 위해 HTML을 저장하는 코드 추가 및 실제 구조 확인 방법 논의

---

## 로컬에서 실행하는 방법

1. **Python 가상환경 생성 및 패키지 설치**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. **(필요시) undetected_chromedriver, selenium 등 추가 설치**

```bash
pip install undetected-chromedriver selenium
```

3. **X 서버(WSL2 등에서 GUI 브라우저 사용 시) 실행**
- WSL2 환경에서는 X 서버(VcXsrv, X410 등)가 실행 중이어야 GUI 브라우저가 뜹니다.
- headless 모드로 실행하면 X 서버 없이도 동작합니다.

---

## coupang_rank_crawler.py 실행 방법

1. **실행 전 환경 준비**
   - `.venv` 가상환경 활성화
   - 필요한 패키지 설치 완료

2. **실행**

```bash
python crawler/coupang_rank_crawler.py
```

3. **실행 시 동작**
   - 크롬 브라우저가 자동으로 실행됨
   - "브라우저 상태를 확인한 후 Enter를 누르세요..." 메시지가 나오면 브라우저를 닫지 말고 Enter만 입력
   - 각 페이지의 상품 정보가 출력됨
   - 디버깅용 HTML은 `/tmp/coupang_debug.html`에 저장됨

4. **실행 옵션/테스트**
   - `get_coupang_product_rank` 함수의 `search_keyword`, `product_url`, `max_pages` 값을 변경하여 테스트 가능

---

## 디버깅 팁
- 오류 발생 시 `/tmp/coupang_debug.html` 파일을 열어 실제 HTML 구조를 확인할 수 있음
- 페이지네이션 div의 class명이 바뀌는 경우, selector를 `div[class*="Pagination_pagination"]` 등으로 조정
- driver가 비정상 종료될 경우, driver 접근 시마다 try-except로 감싸서 안전하게 처리

---

다음 작업 시에는 README의 안내에 따라 환경을 세팅하고, `crawler/coupang_rank_crawler.py`를 실행하면 이어서 디버깅 및 개발을 진행할 수 있습니다.
