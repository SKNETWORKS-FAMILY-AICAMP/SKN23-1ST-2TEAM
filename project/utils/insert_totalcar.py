# 충전소 데이터 db 삽입
import pymysql
from project.api.total_car import fetch_ev_regional_status_data


def insert_ev_regional_status_data():
    """
    ev_regional_status 테이블에 API로 가져온 데이터 삽입
    """
    # 1) 데이터 가져오기
    df = fetch_ev_regional_status_data()

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
        INSERT INTO ev_regional_status (
            base_date,
            seoul,
            incheon,
            gyeonggi,
            gangwon,
            chungbuk,
            chungnam,
            daejeon,
            sejong,
            gyeongbuk,
            daegu,
            jeonbuk,
            jeonnam,
            gwangju,
            gyeongnam,
            busan,
            ulsan,
            jeju
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    inserted = 0

    # 4) DataFrame → SQL insert
    for _, row in df.iterrows():
        values = (
            row.get("기준일"),
            row.get("서울"),
            row.get("인천"),
            row.get("경기"),
            row.get("강원"),
            row.get("충북"),
            row.get("충남"),
            row.get("대전"),
            row.get("세종"),
            row.get("경북"),
            row.get("대구"),
            row.get("전북"),
            row.get("전남"),
            row.get("광주"),
            row.get("경남"),
            row.get("부산"),
            row.get("울산"),
            row.get("제주")
        )

        cursor.execute(sql, values)
        inserted += 1

    conn.commit()

    print(f"\n총 {inserted}개의 데이터가 ev_regional_status 테이블에 삽입되었습니다.")

    cursor.close()
    conn.close()


# 단독 실행 테스트용
if __name__ == "__main__":
    insert_ev_regional_status_data()


