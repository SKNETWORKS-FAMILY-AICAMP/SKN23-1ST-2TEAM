import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PUBLIC_DATA_API_KEY")
BASE_URL = os.getenv("PUBLIC_STATION_BASE_URL")


def fetch_ev_station_data():
    """
    전기차 충전소 API 호출 후 pandas DataFrame으로 반환
    """
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

        rows = data.get("data", [])

        if not rows:
            break

        all_rows.extend(rows)
        print(f"{page} 페이지 로드 완료 (rows: {len(rows)})")

        page += 1

    df = pd.DataFrame(all_rows)
    print("총 데이터 수:", len(df))

    return df


# 단독 실행 테스트용
if __name__ == "__main__":
    df = fetch_ev_station_data()
    print(df.head())