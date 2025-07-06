import logging
logging.basicConfig(level=logging.INFO, force=True)

import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import os
import random
from selenium.common.exceptions import NoAlertPresentException


def extract_product_id(url: str) -> str | None:
    """
    /vp/products/숫자 패턴을 추출
    """
    m = re.search(r"(/vp/products/\d+)", url)
    return m.group(1) if m else None


def get_coupang_product_rank(search_keyword, product_url, max_pages=3, DEBUG=False):
    """
    쿠팡에서 검색어로 검색 후, 상품 URL이 몇 번째에 노출되는지 반환합니다.
    Args:
        search_keyword (str): 검색어
        product_url (str): 찾고자 하는 상품의 URL
        max_pages (int): 검색 결과 몇 페이지까지 확인할지
        DEBUG (bool): 디버깅용 전체 링크 반환 여부
    Returns:
        dict: {'rank': int or None, 'page': int or None, 'links': list or None, 'screenshots': list, 'products': list, 'all_links_all_pages': list (옵션)}
    """
    logging.info(f"[쿠팡] get_coupang_product_rank 진입: search_keyword={search_keyword}, product_url={product_url}, max_pages={max_pages}, DEBUG={DEBUG}")
    try:
        product_id = extract_product_id(product_url)
        if not product_id:
            logging.warning(f"[쿠팡] 잘못된 상품 URL: {product_url}")
            return {"rank": None, "page": None, "links": [], "screenshots": [], "products": []}
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--window-size=360,800')  # Galaxy S22 해상도
        options.add_argument('--auto-open-devtools-for-tabs')
        options.add_argument('--user-agent=Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36')
        options.headless = False  # headless 모드 해제
        driver = uc.Chrome(options=options, headless=False)
        try:
            # 모바일 디바이스 에뮬레이션 적용 (Galaxy S22)
            device_metrics = {
                "width": 360,
                "height": 800,
                "deviceScaleFactor": 3.0,
                "mobile": True
            }
            driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", device_metrics)
            driver.execute_cdp_cmd("Emulation.setUserAgentOverride", {
                "userAgent": "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
            })
            driver.execute_cdp_cmd("Emulation.setTouchEmulationEnabled", {
                "enabled": True,
                "configuration": "mobile"
            })
        except Exception as e:
            print("[모바일 에뮬레이션 오류]", e)
        # 모바일 쿠팡 메인 페이지로 이동
        # driver.get("https://m.coupang.com/")

        # 검색어로 바로 검색 결과 페이지로 이동
        time.sleep(3)
        search_url = f"https://m.coupang.com/nm/search?q={search_keyword}"
        driver.get(search_url)
        close_bottom_banners(driver)

        # [배너 닫기] close-banner-icon-button 클릭 시도
        # try:
        #     close_btn = WebDriverWait(driver, 5).until(
        #         EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close-banner-icon-button"))
        #     )
        #     close_btn.click()
        #     print("앱 설치 배너 닫기 완료")
        #     time.sleep(1)
        # except Exception as e:
        #     print("앱 설치 배너 없음 또는 닫기 실패:", e)
        # [앱 하단 배너 닫기] BottomAppBanner의 닫기 버튼 클릭 시도
        # input("브라우저 상태를 확인한 후 Enter를 누르세요...")

        # [앱 하단 배너 닫기] BottomAppBanner의 닫기 버튼 클릭 시도
        try:
            close_app_banner = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#BottomAppBanner a.close-banner"))
            )
            close_app_banner.click()
            print("앱 하단 배너 닫기 완료")
            time.sleep(1)
        except Exception as e:
            print("앱 하단 배너 없음 또는 닫기 실패:", e)

        # [하단 로그인 유도 배너 닫기]
        try:
            bottom_sheet_close = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#bottomSheetBudgeCloseButton"))
            )
            bottom_sheet_close.click()
            print("하단 로그인 유도 배너 닫기 완료")
            time.sleep(1)
        except Exception as e:
            print("하단 로그인 유도 배너 없음 또는 닫기 실패:", e)

        # [앱 하단 배너 닫기] BottomAppBanner의 닫기 버튼 클릭 시도
        try:
            close_app_banner = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#BottomAppBanner a.close-banner"))
            )
            close_app_banner.click()
            print("앱 하단 배너 닫기 완료")
            time.sleep(1)
        except Exception as e:
            print("앱 하단 배너 없음 또는 닫기 실패:", e)

        # input("브라우저 상태를 확인한 후 Enter를 누르세요...")

        all_products = []
        global_rank = 1
        screenshots = []
        vendor_id_to_find = None
        all_links_all_pages = []
        found_rank = None
        found_page = None
        m = re.search(r'vendorItemId=(\d+)', product_url)
        if m:
            vendor_id_to_find = m.group(1)
        else:
            logging.warning(f"[쿠팡] 상품 URL에서 vendorItemId를 찾을 수 없습니다: {product_url}")

        for page in range(1, max_pages+1):
            print(page)
            print("현재 URL:", driver.current_url)
            # [디버깅] 각 페이지 HTML과 스크린샷 저장
            with open(f"/tmp/coupang_search_page{page}.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            screenshot_path = f"/tmp/coupang_search_page{page}.png"
            driver.save_screenshot(screenshot_path)
            print(f"페이지 {page} HTML과 스크린샷 저장 완료: {screenshot_path}")

            # 모바일 상품 리스트 추출
            products = driver.find_elements(By.CSS_SELECTOR, "ul#productList > li.plp-default__item")
            for prod in products:
                try:
                    a_tag = prod.find_element(By.TAG_NAME, "a")
                    link = a_tag.get_attribute("href")
                    if link and link.startswith("/"):
                        link = "https://m.coupang.com" + link
                    img = prod.find_element(By.CSS_SELECTOR, "span.thumbnail img").get_attribute("src")
                    name = prod.find_element(By.CSS_SELECTOR, "strong.title").text
                    try:
                        price = prod.find_element(By.CSS_SELECTOR, "div.discount-price strong").text
                    except:
                        price = prod.find_element(By.CSS_SELECTOR, "strong.price").text
                    print(f"상품명: {name} | 가격: {price} | 링크: {link} | 이미지: {img}")
                    all_products.append({
                        "name": name,
                        "price": price,
                        "link": link,
                        "img": img,
                        "page": page,
                        "rank": global_rank
                    })
                    global_rank += 1
                    if DEBUG:
                        all_links_all_pages.append(link)
                    # vendorItemId 비교
                    if vendor_id_to_find and not found_rank:
                        m2 = re.search(r'vendorItemId=(\d+)', link or "")
                        if m2 and m2.group(1) == vendor_id_to_find:
                            found_rank = global_rank
                            found_page = page
                            # 1. 해당 상품 위치로 스크롤
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", prod)
                            time.sleep(0.5)  # 스크롤 후 약간 대기
                            # 2. 스크린샷 저장
                            screenshot_path = f"/tmp/coupang_product_page{page}_rank{global_rank}.png"
                            driver.save_screenshot(screenshot_path)
                            screenshots.append(screenshot_path)
                except Exception as e:
                    print(f"[오류] 상품 정보 추출 실패: {e}")
            # 상품을 찾았다면 더 이상 다음 페이지로 넘어가지 않음
            if found_rank and found_page:
                print(f"상품을 찾았으므로 {page}페이지에서 루프 종료")
                break
            if page < max_pages:
                try:
                    next_page_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, f'span.page[data-page="{page+1}"]'))
                    )
                    # 하단 메뉴/배너 숨기기
                    try:
                        driver.execute_script("document.querySelectorAll('.footer-gotop, #bottomMenu').forEach(e => e.style.display='none');")
                    except Exception:
                        pass
                    # 페이지네이션 버튼을 화면 중앙으로 스크롤
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_page_btn)
                    time.sleep(0.5)
                    next_page_btn.click()
                    print(f"페이지 {page+1}로 이동 클릭 완료")
                    close_bottom_banners(driver)
                    # 상품 리스트가 갱신될 때까지 대기 (첫 번째 상품의 링크가 바뀔 때까지)
                    WebDriverWait(driver, 10).until(
                        EC.staleness_of(products[0])
                    )
                    time.sleep(2)
                except Exception as e:
                    print(f"[오류] 다음 페이지 이동 실패: {e}")
                    break
        result = {
            "products": all_products,
            "rank": found_rank,
            "page": found_page,
            "screenshots": screenshots
        }
        if DEBUG:
            result["all_links_all_pages"] = all_links_all_pages
        return result
    except Exception as e:
        import traceback
        logging.error(f"[쿠팡] 크롤러 예외 발생: {e}\n{traceback.format_exc()}")
        return {"rank": None, "page": None, "links": [], "screenshots": [], "products": [], "all_links_all_pages": [], "error": str(e)}
    finally:
        try:
            if 'driver' in locals() and hasattr(driver, 'page_source') and getattr(driver, 'session_id', None):
                with open("/tmp/coupang_debug.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
        except Exception as fe:
            logging.error(f"[쿠팡] HTML 저장 실패: {fe}")
        try:
            if 'driver' in locals() and getattr(driver, 'session_id', None):
                driver.quit()
        except Exception:
            pass


def close_bottom_banners(driver, max_wait=10):
    import time
    start = time.time()
    while time.time() - start < max_wait:
        closed = False
        # 1. 하단 로그인 유도 배너 닫기 (항상 먼저 시도)
        try:
            bottom_sheet_close = driver.find_element(By.CSS_SELECTOR, "#bottomSheetBudgeCloseButton")
            if bottom_sheet_close.is_displayed():
                bottom_sheet_close.click()
                print("하단 로그인 유도 배너 닫기 완료")
                closed = True
                # 배너가 사라질 때까지 대기
                WebDriverWait(driver, 5).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "#bottomSheetBudgeCloseButton"))
                )
                time.sleep(0.2)
        except Exception:
            pass
        # 2. 앱 하단 배너 닫기 (로그인 유도 배너가 사라진 후 시도)
        try:
            close_app_banner = driver.find_element(By.CSS_SELECTOR, "#BottomAppBanner a.close-banner")
            if close_app_banner.is_displayed():
                close_app_banner.click()
                print("앱 하단 배너 닫기 완료")
                closed = True
                WebDriverWait(driver, 5).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "#BottomAppBanner"))
                )
                time.sleep(0.2)
        except Exception:
            pass
        # 둘 다 안 보이면 종료
        if not closed:
            break
        time.sleep(0.2)


if __name__ == "__main__":
    # 테스트용 예시
    search_keyword = "모기장"
    product_url = "https://www.coupang.com/vp/products/22907705?itemId=245504923&vendorItemId=3603606470"
    product_name = "알뜨리 야광 원터치 모기장, 화이트"
    result = get_coupang_product_rank(search_keyword, product_url, max_pages=3)
    print("크롤러 결과:", result)
