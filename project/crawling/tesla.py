from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pymysql

# 1) Selenium 기본 세팅
path = './chromedriver'
service = webdriver.chrome.service.Service(path)
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)

driver.get('https://www.tesla.com/ko_KR/findus/list/services/South+Korea')
time.sleep(1)

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
CREATE TABLE IF NOT EXISTS repair_shop (
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

time.sleep(1)

# 데이터 수집
body = driver.find_element(By.TAG_NAME, "body")       # BODY 태그 선택
rows = driver.find_elements(By.CSS_SELECTOR, ".subregions_page_locations > div")

for row in rows:
    try:
        body.send_keys(Keys.END)
        name = row.find_element(By.CSS_SELECTOR, ".subregion_location_title p").text
        category = 'NULL'
        location = row.find_element(By.CSS_SELECTOR, '.subregion_location_addressLine1').text
        tel = row.find_element(By.CSS_SELECTOR, '.styles_listContactContainer__LhUad .tds-link').text
        company_name = '테슬라'

        print(name, "|", category, "|", location, "|", tel, "|", company_name)

        insert_sql = """
            INSERT INTO repair_shop (name, category, location, tel, company_name)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (name, category, location, tel, company_name))
    except:
        pass
db.commit()  # 페이지마다 저장

driver.quit()
db.close()