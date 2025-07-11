import logging
logging.basicConfig(level=logging.INFO, force=True)

import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
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
        # 안정성 향상을 위한 옵션 추가
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--window-size=360,800')  # Galaxy S22 해상도
        options.add_argument('--user-agent=Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36')
        # 추가 옵션
        # options.add_argument('--disable-software-rasterizer')
        # options.add_argument('--single-process')
        # options.add_argument('--headless=new')
        # headless 모드 해제 (headless=True는 쿠팡에서 막힐 수 있음)
        options.headless = False
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

        # driver.delete_all_cookies()
        # # driver.set_window_size(360, 800)  # 모바일 해상도 설정
        # # 모바일 쿠팡 메인 페이지로 이동
        # driver.get("https://www.coupang.com/")

        # # 페이지 로딩 완료 대기
        # WebDriverWait(driver, 10).until(
        #     lambda driver: driver.execute_script("return document.readyState") == "complete"
        # )

        # wait_and_remove_banners(driver)

        # input("확인")

        # 검색어로 바로 검색 결과 페이지로 이동
        search_url = f"https://m.coupang.com/nm/search?q={search_keyword}"
        driver.delete_all_cookies()
        driver.get(search_url)
        # print("드라이버 타이틀:", driver.title)
        WebDriverWait(driver, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        # 주요 상품 리스트 등장 대기(모바일 쿠팡 상품 리스트)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul#productList"))
            )
        except Exception as e:
            print("상품 리스트 로딩 대기 실패:", e)
        # with open("/tmp/coupang_close_banner_begin.html", "w", encoding="utf-8") as f:
        #     f.write(driver.page_source)
        # print("/tmp/coupang_close_banner_begin.html (close_bottom_banners_new 결과)")
        # 반드시 상품 리스트 등장 후 배너 제거 시도
        close_bottom_banners_new(driver)
        # 배너 제거 후 상태 저장
        # with open("/tmp/coupang_close_banner_end.html", "w", encoding="utf-8") as f:
        #     f.write(driver.page_source)
        # print("/tmp/coupang_close_banner_end.html (close_bottom_banners_new 결과)")
        # 배너 제거 후 스크린샷 저장
        # driver.save_screenshot("/tmp/coupang_close_banner_end.png")
        # print("/tmp/coupang_close_banner_end.png (close_bottom_banners_new 결과)")


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
            close_bottom_banners_new(driver)

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
                    # close_bottom_banners_new(driver)
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
                    # JS로 강제 클릭
                    driver.execute_script("arguments[0].click();", next_page_btn)
                    print(f"페이지 {page+1}로 이동 클릭 완료 (JS 강제 클릭)")
                    # close_bottom_banners_new(driver)
                    # 상품 리스트가 갱신될 때까지 대기 (첫 번째 상품의 링크가 바뀔 때까지)
                    # URL 변화 체크
                    print("클릭 후 URL:", driver.current_url)
                    # 상품 리스트 갱신 대기
                    WebDriverWait(driver, 10).until(
                        EC.staleness_of(products[0])
                    )
                    time.sleep(2)
                except Exception as e:
                    # 오류 발생 시 스크린샷 저장

                    with open(f"/tmp/coupang_error_page{page+1}.html", "w", encoding="utf-8") as f:
                        f.write(driver.page_source)
                    error_screenshot_path = f"/tmp/coupang_error_page{page+1}.png"
                    driver.save_screenshot(error_screenshot_path)
                    print(f"[오류] 다음 페이지 이동 실패: {e}")
                    print(f"[디버깅] 오류 시점 스크린샷 저장 : {error_screenshot_path}")
                    # input("다음 페이지 이동에 실패했습니다. 브라우저에서 직접 조작 후 Enter를 눌러주세요...")
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


def wait_and_remove_banners(driver, timeout=30):
    """배너가 나타날 때까지 기다린 후 제거"""

    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            # 배너 컨테이너가 나타날 때까지 대기
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#wa-banners"))
            )

            # 컨테이너 제거
            driver.execute_script("document.querySelector('#wa-banners').remove();")
            print("배너 컨테이너 제거 완료")
            return True

        except Exception:
            # 0.5초 대기 후 재시도
            time.sleep(0.5)
            continue

    print("타임아웃: 배너 제거 실패")
    return False

def close_bottom_banners_new(driver):
    """
    begin.html을 참고하여, banner로 추정되는 모든 요소를 한 번에 제거하는 함수
    """
    selectors = [
        '#bottom-sheet-nudge',
        '.bottom-sheet-nudge-container',
        '.bottom-sheet-nudge-dimmed',
        '#BottomAppBanner',
        '.bottom-sheet-nudge-container__header',
        '.bottom-sheet-nudge-container__content',
        '#fullBanner',
        '#coupang-banner',
        '.banner',
        # 아래 3개는 너무 광범위하므로 제거
        # '[class*="banner"]',
        # '[id*="banner"]',
        # '[class*="nudge"]',
        # '[id*="nudge"]',
    ]
    removed = False
    for selector in selectors:
        try:
            driver.execute_script(f"document.querySelectorAll('{selector}').forEach(e => e.remove());")
            removed = True
            print(f"배너/팝업 제거: {selector}")
        except Exception as e:
            print(f"배너/팝업 제거 실패: {selector}", e)
    if removed:
        print("close_bottom_banners_new: 배너 관련 요소 일괄 제거 완료")
    else:
        print("close_bottom_banners_new: 제거할 배너 요소 없음")

# if __name__ == "__main__":
#     # 테스트용 예시 (1page)
#     # search_keyword = "모기장"
#     # product_url = "https://www.coupang.com/vp/products/22907705?itemId=245504923&vendorItemId=3603606470"
#     # product_name = "알뜨리 야광 원터치 모기장, 화이트"
#     # result = get_coupang_product_rank(search_keyword, product_url, max_pages=3)
#     # print("크롤러 결과:", result)

#     # 테스트용 예시 (2page)
#     search_keyword = "냉면"
#     product_url = "https://www.coupang.com/vp/products/2439939?itemId=18171088581&vendorItemId=85320458323"
#     product_name = "둥지냉면 동치미 물냉면 161g, 8개"
#     result = get_coupang_product_rank(search_keyword, product_url, max_pages=3)
#     print("크롤러 결과:", result)

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import messagebox

    def run_crawler():
        keyword = entry_keyword.get()
        url = entry_url.get()
        try:
            max_pages = int(entry_pages.get())
        except ValueError:
            max_pages = 3
        btn_run.config(state="disabled")
        root.update()
        try:
            result = get_coupang_product_rank(keyword, url, max_pages=max_pages)
            messagebox.showinfo("결과", f"랭크: {result.get('rank')}\n페이지: {result.get('page')}")
        except Exception as e:
            messagebox.showerror("오류", str(e))
        btn_run.config(state="normal")

    root = tk.Tk()
    root.title("쿠팡 랭킹 크롤러")

    tk.Label(root, text="검색어:").pack()
    entry_keyword = tk.Entry(root)
    entry_keyword.pack()

    tk.Label(root, text="상품 URL:").pack()
    entry_url = tk.Entry(root)
    entry_url.pack()

    tk.Label(root, text="최대 페이지:").pack()
    entry_pages = tk.Entry(root)
    entry_pages.insert(0, "3")
    entry_pages.pack()

    btn_run = tk.Button(root, text="실행", command=run_crawler)
    btn_run.pack()

    root.mainloop()
