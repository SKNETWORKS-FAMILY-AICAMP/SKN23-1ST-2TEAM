# 차종별_용도별_차량_등록대수 db 삽입
import pymysql
from project.api.car_type import fetch_car_type_data


def insert_ev_vehicle_stats_to_db():
    """
    ev_vehicle_stats 테이블에 API로 가져온 데이터 삽입
    """
    # 1) 데이터 가져오기
    df = fetch_car_type_data()

    # 2) MySQL 연결
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        database="sknteam2",
        charset="utf8mb4"
    )
    cursor = conn.cursor()

    # 3) INSERT SQL
    sql = """
        INSERT INTO ev_vehicle_stats (
            region,
            fuel_type,
            usage_type,
            passenger,
            van,
            truck,
            special,
            total
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    inserted = 0

    # 4) DataFrame → SQL insert
    for _, row in df.iterrows():
        values = (
            row.get("시군구별"),
            row.get("연료별"),
            row.get("용도별"),
            row.get("승용"),
            row.get("승합"),
            row.get("화물"),
            row.get("특수"),
            row.get("계"),
        )

        cursor.execute(sql, values)
        inserted += 1

    conn.commit()

    print(f"\n총 {inserted}개의 데이터가 ev_vehicle_stats 테이블에 삽입되었습니다.")

    cursor.close()
    conn.close()


# 단독 실행 테스트용
if __name__ == "__main__":
    insert_ev_vehicle_stats_to_db()


