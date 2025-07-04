# Coupang Rank Tracker API (FastAPI + Playwright)

## 실행 방법

### 1. 로컬 개발 서버 실행

```bash
pip install -r requirements.txt
python -m playwright install --with-deps
uvicorn api:app --host 0.0.0.0 --port 8000
```

### 2. Docker로 실행

```bash
docker build -t coupang-rank-api .
docker run -p 8000:8000 coupang-rank-api
```

### 3. docker-compose로 전체 서비스 실행

```bash
cd ..
docker-compose up --build
```
- 크롤러 API: http://localhost:8001
- (frontend, backend, db, redis 등도 함께 실행)

## 주요 엔드포인트

- `POST /rank`
  - 입력: `{ "search_keyword": "모기장", "product_url": "https://www.coupang.com/vp/products/83004096?itemId=263287724&vendorItemId=3639044886" }`
  - 출력: `{ "rank": 7, "page": 1 }` (없으면 rank/page = null)

## 참고
- Playwright 브라우저 및 한글 폰트가 Dockerfile에서 자동 설치됩니다.
- 프론트엔드와 연동 시 CORS 설정이 필요할 수 있습니다.