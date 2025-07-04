# Coupang Rank Tracker Frontend

## 실행 방법

### 1. 개발 서버 실행 (로컬)

```bash
cd frontend
yarn install
yarn dev
```

- 기본 주소: http://localhost:9000
- 랭킹 체크 페이지: http://localhost:9000/#/rank-check

### 2. Docker로 실행

```bash
cd frontend
docker build -t coupang-rank-frontend .
docker run -p 9000:9000 coupang-rank-frontend
```

### 3. docker-compose로 전체 서비스 실행

```bash
docker-compose up --build
```
- frontend: http://localhost:9000
- 크롤러 API: http://localhost:8001
- (기존 backend, db, redis 등도 함께 실행)

## 주요 페이지

- `/rank-check` : 상품 URL과 검색어로 쿠팡 랭킹을 바로 확인할 수 있는 단일 폼 페이지

## 백엔드 연동
- `.env` 또는 `src/boot/axios.ts`에서 API 주소를 크롤러 서버(`http://localhost:8001`)로 맞춰주세요.
