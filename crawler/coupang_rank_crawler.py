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
        options.add_argument('--window-size=1280,800')
        options.add_argument('--auto-open-devtools-for-tabs')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        options.headless = False  # uc 내부 버그 우회
        driver = uc.Chrome(options=options, headless=False)
        driver.get("https://www.coupang.com/")
        time.sleep(4)
        print("현재 URL:", driver.current_url)
        input("브라우저 상태를 확인한 후 Enter를 누르세요...")
        search_box = None
        for selector in ["input[name='q']", "input#searchKeyword", "input[type='search']"]:
            try:
                search_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if search_box:
                    break
            except Exception:
                continue
        if not search_box:
            raise Exception("검색창을 찾을 수 없습니다.")
        search_box.clear()
        search_box.send_keys(search_keyword)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)
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
            try:
                products = driver.find_elements(By.CSS_SELECTOR, "ul#product-list > li")
            except Exception as e:
                print(f"[오류] driver 접근 실패(아마 브라우저가 닫힘): {e}")
                break
            for prod in products:
                try:
                    a_tag = prod.find_element(By.TAG_NAME, "a")
                    link = a_tag.get_attribute("href")
                    try:
                        name = prod.find_element(By.XPATH, ".//div[contains(@class, 'productName')]").text
                    except:
                        name = ""
                    try:
                        price = prod.find_element(By.XPATH, ".//strong[contains(@class, 'price')]").text
                    except:
                        price = ""
                    try:
                        img = prod.find_element(By.TAG_NAME, "img").get_attribute("src")
                    except:
                        img = ""
                    # 상품 정보 출력
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
            if page < max_pages:
                print("next_page")
                try:
                    # 1. 오버레이가 사라질 때까지 대기
                    WebDriverWait(driver, 10).until(
                        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fw-absolute"))
                    )
                    # 2. 버튼 찾기
                    next_page_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, f'a[data-page="{page+1}"]'))
                    )
                    # 3. 버튼을 화면 중앙에 위치
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_page_btn)
                    time.sleep(0.5)
                    # 4. 클릭 시도 (예외 발생 시 재시도)
                    for _ in range(3):
                        try:
                            next_page_btn.click()
                            break
                        except Exception as e:
                            print(f"[재시도] 클릭 실패: {e}")
                            time.sleep(1)
                    # 5. 페이지 전환 대기
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, f'a[data-page="{page+1}"].Pagination_selected__r1eiC'))
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


if __name__ == "__main__":
    # 테스트용 예시
    search_keyword = "모기장"
    product_url = "https://www.coupang.com/vp/products/22907705?itemId=245504923&vendorItemId=3603606470"
    product_name = "알뜨리 야광 원터치 모기장, 화이트"
    result = get_coupang_product_rank(search_keyword, product_url, max_pages=3)
    print("크롤러 결과:", result)