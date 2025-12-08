import os
import requests
import pandas as pd
from dotenv import load_dotenv
import pymysql

load_dotenv()

# 환경변수 불러오기
API_KEY = os.getenv("PUBLIC_DATA_API_KEY")
BASE_URL = os.getenv("PUBLIC_STATION_BASE_URL")

url = f"https://{BASE_URL}"

all_rows = []
page = 1
per_page = 100

while True:
    params = {
        "page": page,
        "perPage": per_page,
        "serviceKey": API_KEY
    }

    res = requests.get(url, params=params)
    res.raise_for_status()

    data = res.json()

    # 데이터 추출
    rows = data.get("data", [])

    # 데이터가 더 이상 없으면 중단
    if not rows:
        break

    all_rows.extend(rows)
    print(f"{page} 페이지 로드 완료 (rows: {len(rows)})")

    page += 1

# pandas DataFrame 변환
df = pd.DataFrame(all_rows)
print("총 데이터 수:", len(df))
print(df.head())