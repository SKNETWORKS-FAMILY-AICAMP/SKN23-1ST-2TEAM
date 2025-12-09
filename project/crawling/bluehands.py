from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pymysql

# 1. Chrome 브라우저 실행
path = './chromedriver'
service = webdriver.chrome.service.Service(path)
driver = webdriver.Chrome(service=service)

wait = WebDriverWait(driver, 10)

# 2) MySQL 연결
db = pymysql.connect(
    host='localhost',    # 필요 시 본인 설정
    user='root',
    password='rlaekqls23',     # 본인 MySQL 비밀번호 입력
    database='sknteam2',   # 저장할 DB명
    charset='utf8mb4'
)
cursor = db.cursor()

# ==========================
# 3) 테이블 자동 생성
# ==========================
create_table_sql = """
CREATE TABLE IF NOT EXISTS repair_shop(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    category VARCHAR(255),
    location VARCHAR(255),
    tel VARCHAR(100),
    company_name varchar(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
cursor.execute(create_table_sql)
db.commit()

# 2. 사이트 접속
driver.get('https://www.hyundai.com/kr/ko/service-membership/service-network/service-reservation-search')
time.sleep(1)

# 2-1 팝업 닫기
modal_btn = driver.find_element(By.CSS_SELECTOR, '.hmc_modal_base.layer_popup .layer_btns button')
modal_btn.click()

# 2-2 첫번째 셀렉트 박스 전체 선택
Select(driver.find_element(By.ID, "snGubunList")).select_by_visible_text("전체")

# 2-3 두번째 셀렉트 박스 전체 선택
Select(driver.find_element(By.ID, "selectBoxCity")).select_by_index(0)

time.sleep(0.5)

# 2-4 세번째 셀렉트 박스 전체 선택
Select(driver.find_element(By.ID, "selectBoxTownShip")).select_by_index(0)

# 2-5 검색 클릭
driver.find_element(By.CSS_SELECTOR, ".wrap-btns .btn_md_primary.search_btn").click()

#   모든 페이지 끝까지 반복 크롤링
while True:
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#listView tr")))
    time.sleep(1)

    # 데이터 수집
    rows = driver.find_elements(By.CSS_SELECTOR, "#listView tr")

    for row in rows:
        try:
            name = row.find_element(By.CSS_SELECTOR, ".link_line").text
            category = row.find_element(By.CSS_SELECTOR, '.wrap-word').text
            location = row.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text
            tel = row.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text
            company_name = '현대'


            print(name, "|", category, "|", location, "|", tel, "|", company_name)
            insert_sql = """
                INSERT INTO repair_shop(name, category, location, tel, company_name)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_sql, (name, category, location, tel, company_name))
        except:
            pass
    db.commit()  # 페이지마다 저장
    # next 버튼 찾기
    try:
        next_btn = driver.find_element(By.CSS_SELECTOR, ".navi.next")
    except:
        break

    # next_btn에 disabled 클래스가 있는지 확인
    if "disabled" in next_btn.get_attribute("class"):
        break

    # next 클릭
    next_btn.click()

driver.quit()
db.close()