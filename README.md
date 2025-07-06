# Coupang Rank Tracker

## 목차
1. 프로젝트 개요
2. 환경설정 및 준비
3. 실행 방법
   - 전체 서비스(docker-compose)
   - 백엔드(API) 단독 실행
   - 프론트엔드 단독 실행
   - 크롤러 단독 실행
4. 주요 기능 및 엔드포인트
5. 디버깅 및 개발 팁
6. 참고 문서

---

## 1. 프로젝트 개요

쿠팡 상품의 검색 랭킹을 자동으로 추적/확인하는 서비스입니다.
- 백엔드: FastAPI + Playwright (크롤러 API)
- 프론트엔드: (별도 폴더, 단일 폼 제공)
- Docker 및 docker-compose 지원

---

## 2. 환경설정 및 준비

### 2-1. Python 가상환경 및 패키지 설치

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2-2. Playwright 브라우저 설치

```bash
python -m playwright install --with-deps
```

### 2-3. 환경변수 파일 설정

```bash
cp backend/.env.example backend/.env
# backend/.env 파일을 본인 환경에 맞게 수정
```

### 2-4. (WSL2 등에서) X 서버 실행
- GUI 브라우저가 필요한 경우 X 서버(VcXsrv, X410 등) 실행 필요
- headless 모드에서는 X 서버 없이도 동작

### 2-5. 프론트엔드 의존성 설치

```bash
cd frontend
yarn install
```

---

## 3. 실행 방법

### 3-1. docker-compose로 전체 서비스 실행

```bash
docker-compose up --build
```
- frontend: http://localhost:9000
- 크롤러 API: http://localhost:8001
- (backend, db, redis 등도 함께 실행)

### 3-2. 백엔드(API) 단독 실행

```bash
uvicorn crawler.api:app --host 0.0.0.0 --port 8001
```

### 3-3. 프론트엔드 단독 실행

```bash
cd frontend
yarn serve
```
- 기본 주소: http://localhost:9000
- 랭킹 체크 페이지: http://localhost:9000/#/rank-check

### 3-4. 크롤러 단독 실행

```bash
python crawler/coupang_rank_crawler.py
```
- 크롬 브라우저가 자동 실행됨
- "브라우저 상태를 확인한 후 Enter를 누르세요..." 메시지에서 Enter 입력
- 각 페이지의 상품 정보가 출력됨
- 디버깅용 HTML은 `/tmp/coupang_debug.html`에 저장

---

## 4. 주요 기능 및 엔드포인트

### 4-1. API 엔드포인트

- `POST /rank`
  - 입력: `{ "search_keyword": "모기장", "product_url": "https://www.coupang.com/vp/products/83004096?itemId=263287724&vendorItemId=3639044886" }`
  - 출력: `{ "rank": 7, "page": 1 }` (없으면 rank/page = null)

### 4-2. 프론트엔드 주요 페이지

- `/rank-check` : 상품 URL과 검색어로 쿠팡 랭킹을 바로 확인할 수 있는 단일 폼 페이지

### 4-3. 크롤러 주요 옵션

- `get_coupang_product_rank` 함수의 `search_keyword`, `product_url`, `max_pages` 값 변경 가능

---

## 5. 디버깅 및 개발 팁

- 오류 발생 시 `/tmp/coupang_debug.html` 파일로 실제 HTML 구조 확인
- 페이지네이션 div의 class명이 바뀌는 경우, selector를 `div[class*="Pagination_pagination"]` 등으로 조정
- driver가 비정상 종료될 경우, driver 접근 시마다 try-except로 감싸서 안전하게 처리
- 프론트엔드에서 API 주소는 `.env` 또는 `src/boot/axios.ts`에서 `http://localhost:8001`로 맞춰야 함

---

## 6. 참고 문서

- [Scrapy Playwright: Complete Tutorial 2025](https://www.zenrows.com/blog/scrapy-playwright#set-up-a-scrapy-project)
- [How to Use Playwright Stealth for Scraping](https://www.zenrows.com/blog/playwright-stealth#what-is)
- [Scrapy Impersonate: Advanced Tutorial for 2025](https://www.zenrows.com/blog/scrapy-impersonate#why-scrapy-impersonate)
- Playwright 브라우저 및 한글 폰트는 Dockerfile에서 자동 설치됨
- 프론트엔드와 연동 시 CORS 설정 필요할 수 있음
