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