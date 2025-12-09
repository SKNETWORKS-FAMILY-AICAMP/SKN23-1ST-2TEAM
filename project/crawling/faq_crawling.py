from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import json

driver = webdriver.Chrome()
driver.implicitly_wait(2)
wait = WebDriverWait(driver, 10)

driver.get("https://www.hyundai.com/kr/ko/digital-customer-support/helpdesk/faq")

faq_data = []   # 👉 크롤링 데이터 저장 리스트


def safe_click(el):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    time.sleep(0.15)
    driver.execute_script("arguments[0].click();", el)
    time.sleep(0.15)


def ensure_on(dt_element, timeout=2.0):
    start = time.time()
    if "on" in (dt_element.get_attribute("class") or ""):
        return True

    safe_click(dt_element)

    while time.time() - start < timeout:
        if "on" in (dt_element.get_attribute("class") or ""):
            return True
        time.sleep(0.1)

    try:
        driver.execute_script("""
            var dt = arguments[0];
            dt.classList.add('on');
            var dd = dt.nextElementSibling;
            if(dd) {
                dd.style.display = 'block';
                var exp = dd.querySelector('.exp');
                if(exp) exp.style.display = 'block';
            }
        """, dt_element)
        time.sleep(0.1)
        return "on" in (dt_element.get_attribute("class") or "")
    except:
        return False


def crawl_current_page():
    time.sleep(0.8)

    dls = driver.find_elements(By.CSS_SELECTOR, ".ui_accordion.acc_01 dl")

    for dl in dls:
        try:
            dt = dl.find_element(By.TAG_NAME, "dt")
        except:
            continue

        ensure_on(dt)

        # 제목
        try:
            title = dt.find_element(By.CSS_SELECTOR, ".title").text.strip()
        except:
            title = "제목 없음"

        # 내용
        try:
            dd = dt.find_element(By.XPATH, "following-sibling::dd[1]")
            try:
                content = dd.find_element(By.CSS_SELECTOR, ".exp").text.strip()
            except:
                content = dd.text.strip()
        except:
            content = "내용 없음"

        # 👉 리스트에 저장
        faq_data.append({
            "title": title,
            "content": content
        })

        print(f"수집 완료: {title}")


# -------- 전체 페이지 크롤링 --------
while True:
    crawl_current_page()
    time.sleep(0.6)

    try:
        next_btn = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.navi.next"))
        )
    except:
        print("다음 버튼 없음 → 종료")
        break

    if "disabled" in (next_btn.get_attribute("class") or ""):
        print("마지막 페이지입니다. 종료합니다.")
        break

    safe_click(next_btn)
    time.sleep(1.2)

driver.quit()


# -------- CSV 저장 --------
csv_filename = "faq_output.csv"
with open(csv_filename, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "content"])
    writer.writeheader()
    writer.writerows(faq_data)

print(f"\nCSV 저장 완료: {csv_filename}")


# -------- JSON 저장 --------
json_filename = "faq_output.json"
with open(json_filename, "w", encoding="utf-8-sig") as f:
    json.dump(faq_data, f, ensure_ascii=False, indent=4)

print(f"JSON 저장 완료: {json_filename}")
