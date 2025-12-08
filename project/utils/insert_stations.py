# 충전소 데이터 db 삽입
import pymysql
from project.api.station import fetch_ev_station_data


def insert_ev_stations_to_db():
    """
    ev_station 테이블에 API로 가져온 데이터 삽입
    """
    # 1) 데이터 가져오기
    df = fetch_ev_station_data()

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
        INSERT INTO ev_station (
            station_id,
            station_name,
            address,
            detail_address,
            lat,
            lon,
            available_time,
            contact,
            reg_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    inserted = 0

    # 4) DataFrame → SQL insert
    for _, row in df.iterrows():
        values = (
            row.get("충전소아이디"),
            row.get("충전소명"),
            row.get("충전소주소"),
            row.get("상세주소"),
            row.get("위도"),
            row.get("경도"),
            row.get("이용가능시간"),
            row.get("연락처"),
            row.get("등록일자"),
        )

        cursor.execute(sql, values)
        inserted += 1

    conn.commit()

    print(f"\n총 {inserted}개의 데이터가 ev_station 테이블에 삽입되었습니다.")

    cursor.close()
    conn.close()


# 단독 실행 테스트용
if __name__ == "__main__":
    insert_ev_stations_to_db()


