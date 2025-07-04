FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성 및 한글 폰트 설치
RUN apt-get update && \
    apt-get install -y wget curl unzip fonts-nanum fonts-noto-cjk chromium && \
    rm -rf /var/lib/apt/lists/*

# requirements.txt 복사 및 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Playwright 브라우저 설치
RUN python -m playwright install --with-deps

# 앱 코드 복사
COPY . .

# 기본 실행: FastAPI 서버 (코드가 /app/crawler에 있으므로 경로 반영)
CMD ["uvicorn", "crawler.api:app", "--host", "0.0.0.0", "--port", "8000"]