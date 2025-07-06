# 현재 진행상황

1. 배너 삭제, 클릭을 통한 페이지 이동 시도
   => 배너가 완벽하게 사라지지 않음. => 대기시간을 10 -> 15초로 늘림. => 소용없음
   => 클릭이 안되는 오류가 발생함.

# Coupang Rank Tracker - 윈도우 환경 배포 가이드

## 1. 사전 준비
- Windows 10/11 PC 또는 서버
- [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop) 설치 (WSL2 백엔드 권장)
- [Git for Windows](https://git-scm.com/download/win) 설치

## 2. 프로젝트 다운로드
```sh
git clone https://github.com/yungjoong/coupang-rank-tracker.git
cd coupang-rank-tracker
```

## 3. 환경 파일(.env) 준비
- `.env.example` 파일이 있다면 복사해서 `.env`로 만들고, 필요한 값을 채워주세요.

## 4. 서비스 실행
```sh
docker-compose up -d --build
```
- 최초 실행 시 이미지 빌드 및 의존성 설치로 시간이 다소 걸릴 수 있습니다.

## 5. 서비스 접속
- 웹사이트: http://localhost:9000
- (서버라면 방화벽/포트포워딩 필요)

## 6. 기타 명령어
- 서비스 중지: `docker-compose down`
- 로그 확인: `docker-compose logs`
- 컨테이너 상태 확인: `docker ps`

## 7. 윈도우 환경에서 자주 발생하는 문제/FAQ
- **WSL2가 설치되어 있지 않으면 Docker Desktop이 동작하지 않음**
  → 설치 과정에서 WSL2 설치 안내가 나오면 반드시 따라야 함
- **포트 충돌**
  → 이미 9000, 8000, 5432, 6379 등 포트를 쓰는 서비스가 있으면 docker-compose.yml에서 포트 변경 필요
- **공유 드라이브 권한 문제**
  → Docker Desktop에서 "Settings > Resources > File Sharing"에서 프로젝트 폴더 드라이브(C: 등)를 공유해야 함
- **방화벽/네트워크**
  → 외부에서 접속하려면 방화벽/포트포워딩 설정 필요

---

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
