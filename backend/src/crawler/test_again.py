import undetected_chromedriver as uc
from datetime import datetime
import time
import os
import random

def random_sleep():
    """랜덤한 시간 동안 대기"""
    time.sleep(random.uniform(2, 5))

# WSL 환경에서 실행하기 위한 환경 변수 설정
os.environ['DISPLAY'] = ':0'

# Chrome 옵션 설정
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")
options.add_argument("--lang=ko_KR")

# 모바일 환경 설정
options.add_argument("--window-size=360,640")
options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36")

try:
    print("Chrome 드라이버 초기화 중...")
    driver = uc.Chrome(options=options, version_main=129)
    print("Chrome 드라이버 초기화 완료")

    # 쿠팡 모바일 페이지 접속
    print("쿠팡 모바일 페이지 접속 중...")
    driver.get("https://m.coupang.com/")
    random_sleep()

    # 쿠키 수락 버튼 클릭 시도
    try:
        cookie_button = driver.find_element("id", "cookieAcceptButton")
        cookie_button.click()
        print("쿠키 수락 버튼 클릭")
        random_sleep()
    except:
        print("쿠키 수락 버튼을 찾을 수 없거나 이미 수락됨")

    print("현재 페이지 타이틀:", driver.title)

    # 검색 페이지로 이동
    print("검색 페이지로 이동 중...")
    driver.get("https://m.coupang.com/nm/search?q=camping+table")
    random_sleep()

    # 현재 시간을 파일명에 포함
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"coupang_mobile_page_{current_time}.html"

    print(f"페이지 내용을 {filename} 파일로 저장 중...")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f"파일 저장 완료: {filename}")

    # 스크린샷 저장
    screenshot_filename = f"coupang_mobile_screenshot_{current_time}.png"
    driver.save_screenshot(screenshot_filename)
    print(f"스크린샷 저장 완료: {screenshot_filename}")

except Exception as e:
    print(f"오류 발생: {str(e)}")
    print("상세 오류 정보:", e.__class__.__name__)
finally:
    try:
        driver.quit()
    except:
        pass
