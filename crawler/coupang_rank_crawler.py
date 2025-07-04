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


def get_coupang_product_rank(search_keyword, product_url, max_pages=3):
    """
    쿠팡에서 검색어로 검색 후, 상품 URL이 몇 번째에 노출되는지 반환합니다.
    Args:
        search_keyword (str): 검색어
        product_url (str): 찾고자 하는 상품의 URL
        max_pages (int): 검색 결과 몇 페이지까지 확인할지
    Returns:
        dict: {'rank': int or None, 'page': int or None, 'links': list or None, 'screenshots': list}
    """
    logging.info(f"[쿠팡] get_coupang_product_rank 진입: search_keyword={search_keyword}, product_url={product_url}, max_pages={max_pages}")
    try:
        product_id = extract_product_id(product_url)
        if not product_id:
            logging.warning(f"[쿠팡] 잘못된 상품 URL: {product_url}")
            return {"rank": None, "page": None, "links": [], "screenshots": [], "all_links_page1": []}
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
        # driver.get("https://www.naver.com/")
        time.sleep(4)
        print("현재 URL:", driver.current_url)
        input("브라우저 상태를 확인한 후 Enter를 누르세요...")
        # 검색창 여러 셀렉터 중 하나라도 있으면 사용
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
        # 1페이지의 모든 상품 링크, 상품명, 가격, 이미지 수집 및 출력 (클래스명 일부 일치로 견고하게)
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
                    # print(f"상품명: {name} | 가격: {price} | 링크: {link} | 이미지: {img}")
                except Exception as e:
                    print(f"[오류] 상품 정보 추출 실패: {e}")
            if page < max_pages:
                print("next_page")
                # try:
                #     pagination = WebDriverWait(driver, 10).until(
                #         EC.presence_of_element_located((By.CSS_SELECTOR, "div.Pagination_pagination__eHDDy"))
                #     )
                #     next_page_btn = pagination.find_element(By.CSS_SELECTOR, f'a[data-page="{page+1}"]')
                #     driver.execute_script("arguments[0].scrollIntoView();", next_page_btn)
                #     next_page_btn.click()
                #     WebDriverWait(driver, 10).until(
                #         EC.text_to_be_present_in_element(
                #             (By.CSS_SELECTOR, "a.Pagination_selected__r1eiC"), str(page+1)
                #         )
                #     )
                #     time.sleep(2)
                # except Exception as e:
                #     print(f"[오류] 다음 페이지 이동 실패: {e}")
                #     break
    except Exception as e:
        import traceback
        logging.error(f"[쿠팡] 크롤러 예외 발생: {e}\n{traceback.format_exc()}")
        return {"rank": None, "page": None, "links": [], "screenshots": [], "all_links_page1": [], "error": str(e)}
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
    product_url = "https://www.coupang.com/vp/products/83004096?itemId=263287724&vendorItemId=3639044886"
    result = get_coupang_product_rank(search_keyword, product_url, max_pages=3)
    print("크롤러 결과:", result)