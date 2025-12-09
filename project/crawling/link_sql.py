import csv
import json
import pymysql

# ------------------------------
# 🔧 MySQL 연결 정보 수정
# ------------------------------
conn = pymysql.connect(
    host="localhost",       # 예: 127.0.0.1
    user="root",            # 사용자명
    password="1234",     # 비밀번호
    db="sknteam2",            # 사용할 DB 이름
    charset="utf8mb4"
)

cursor = conn.cursor()

# ------------------------------
# 1) 테이블 생성
# ------------------------------
create_table_sql = """
CREATE TABLE IF NOT EXISTS faq_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT,
    content TEXT
);
"""
cursor.execute(create_table_sql)
conn.commit()
print("테이블 생성 완료 or 이미 존재합니다.")


# ------------------------------
# 2) CSV 파일 삽입
# ------------------------------
def insert_csv(csv_path):
    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            sql = "INSERT INTO faq_data (title, content) VALUES (%s, %s)"
            cursor.execute(sql, (row["title"], row["content"]))

    conn.commit()
    print("CSV 삽입 완료:", csv_path)


# ------------------------------
# 3) JSON 파일 삽입
# ------------------------------
def insert_json(json_path):
    with open(json_path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

        for item in data:
            sql = "INSERT INTO faq_data (title, content) VALUES (%s, %s)"
            cursor.execute(sql, (item["title"], item["content"]))

    conn.commit()
    print("JSON 삽입 완료:", json_path)


# ------------------------------
# 실행 (원하는 파일 선택)
# ------------------------------
insert_csv("faq_output.csv")     # CSV → MySQL
insert_json("faq_output.json")   # JSON → MySQL


# ------------------------------
# 종료
# ------------------------------
cursor.close()
conn.close()
print("MySQL 저장 완료 및 연결 종료")
