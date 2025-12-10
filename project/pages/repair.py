import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import pandas as pd

st.set_page_config(layout="wide")   # 화면 넓게

# 1. 환경변수 & DB 연결
load_dotenv()
PASSWORD = os.getenv('PASSWORD')

def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=PASSWORD,
            database="sknteam2",
            charset='utf8'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        st.error(f"DB 연결 오류: {e}")
        return None


# 2. DB에서 region / city 데이터 불러오기

@st.cache_data
def load_regions_and_cities():
    conn = create_connection()
    if conn:
        region_df = pd.read_sql("SELECT * FROM region", conn)
        city_df = pd.read_sql("SELECT * FROM city", conn)
        conn.close()
        return region_df, city_df
    return pd.DataFrame(), pd.DataFrame()

region_df, city_df = load_regions_and_cities()

st.subheader("정비소 페이지")
# st.info("정비소 데이터를 여기에 작성하세요.")

# --- SQL 데이터 조회 ---    
conn = create_connection()
if conn:
    query = """
        SELECT s.name, s.location, s.company_name,
                r.region AS region_name,
                c.city_name AS city_name, 
                s.tel, s.category
        FROM repair_shop s
        LEFT JOIN region r ON s.region_code = r.region_code
        LEFT JOIN city c ON s.city_code = c.city_code;
    """
    df = pd.read_sql(query, conn)
    conn.close()

# 검색 UI
col1, col2, col3 = st.columns([2, 2, 2])

region_list = ["선택"] + sorted(region_df['region'].tolist())
selected_region = col1.selectbox("도시", region_list)

company_list = ["선택"] + sorted(df['company_name'].unique().tolist()) 
selected_company = col3.selectbox("회사", company_list)


# 선택한 region → city 목록

if selected_region == "선택":
    city_list = ["시/군/구"]
else:
    region_code = region_df.loc[
        region_df['region'] == selected_region, 'region_code'
    ].values[0]

    filtered_city_df = city_df[city_df['region_code'] == region_code]
    city_list = ["시/군/구"] + sorted(filtered_city_df['city_name'].tolist())

selected_city = col2.selectbox("시/군/구", city_list)

# 조건 만족 여부 확인

if selected_region == "선택":
    st.warning("⚠ 도시(Region)를 먼저 선택하세요.")
elif selected_city == "시/군/구":
    st.warning("⚠ 시/군/구를 선택하세요.")
else:
    # 필터링

    filtered_df = df.copy()

    # 지역 필터링
    filtered_df = filtered_df[
        (filtered_df['region_name'] == selected_region) &
        (filtered_df['city_name'] == selected_city)
    ]

    # 회사명 필터링
    if selected_company != "선택":
        filtered_df = filtered_df[filtered_df['company_name'] == selected_company]
    
    # region_name, city_name 제거

    filtered_df = filtered_df.drop(columns=["region_name", "city_name"])

    # 컬럼명 한글로 변경

    filtered_df = filtered_df.rename(columns={
        "name": "정비소명",
        "location": "주소",
        "tel": "전화번호",
        "category": "카테고리",
        "company_name" : '회사'
    })

    # 결과 출력

    st.subheader("정비소 검색 결과")

    # 정비소가 없을 경우
    if filtered_df.empty:
        st.warning(f"'{selected_city}' 지역에 정비소가 없습니다.")
    else:
        st.dataframe(filtered_df, hide_index=True)