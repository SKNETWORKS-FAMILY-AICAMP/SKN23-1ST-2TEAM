import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import pandas as pd
# 하늘색 #e6f0ff
# 연두색 #d9f7f5
# 보라색 #f2ecff


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

# 3. 사이드바 메뉴
menu = st.sidebar.radio("메뉴 선택", ["main", "정비소", "FAQ"])

# 4. main 페이지
if menu == "main":
    st.title("최강 2팀 보여줄게")

    conn = create_connection()
    if conn:
        query = """
        SELECT s.station_name, s.address, s.detail_address,
               s.available_time, s.reg_date,
               r.region AS region_name,
               c.city_name AS city_name
        FROM ev_station s
        LEFT JOIN region r ON s.region_code = r.region_code
        LEFT JOIN city c ON s.city_code = c.city_code
        """
        df = pd.read_sql(query, conn)
        conn.close()

        col1, col2, col3 = st.columns([4, 2, 2])
        address = col1.text_input("위치 검색")

        region_list = ["선택"] + sorted(region_df['region'].tolist())
        selected_region = col2.selectbox("도시", region_list)

        if selected_region == "선택":
            city_list = ["시/군/구"]
        else:
            region_code = region_df.loc[
                region_df['region'] == selected_region, 'region_code'
            ].values[0]

            filtered_city_df = city_df[city_df['region_code'] == region_code]
            city_list = ["시/군/구"] + sorted(filtered_city_df['city_name'].tolist())

        selected_city = col3.selectbox("시/군/구", city_list)

        if selected_region == "선택":
            st.warning("⚠ 도시(Region)를 먼저 선택하세요.")
        elif selected_city == "시/군/구":
            st.warning("⚠ 시/군/구를 선택하세요.")
        else:
            filtered_df = df.copy()

            if address:
                filtered_df = filtered_df[
                    filtered_df['station_name'].str.contains(address, case=False, na=False) |
                    filtered_df['address'].str.contains(address, case=False, na=False) |
                    filtered_df['detail_address'].str.contains(address, case=False, na=False)
                ]

            filtered_df = filtered_df[
                (filtered_df['region_name'] == selected_region) &
                (filtered_df['city_name'] == selected_city)
            ]

            filtered_df = filtered_df.drop(columns=["region_name", "city_name"])

            filtered_df = filtered_df.rename(columns={
                "station_name": "충전소명",
                "address": "주소",
                "detail_address": "상세주소",
                "available_time": "이용시간",
                "reg_date": "등록일"
            })

            st.subheader("충전소 위치")
            st.dataframe(filtered_df, hide_index=True)

# 정비소

elif menu == "정비소":
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

# ================================================================================


elif menu == "FAQ":
    st.header("FAQ")

    # ===============================
    # 세션 상태 초기화
    # ===============================
    if "faq_page" not in st.session_state:
        st.session_state.faq_page = 1

    # ===============================
    # CSS 스타일
    # ===============================
    st.markdown("""
        <style>
        /* 테마? */
        .st-bd{
            color: #000;
            border-color: #e6f0ff;
            background-color: #e6f0ff;
            cursor: pointer;
            transition: all .5s;
        }
        .st-bd:hover{
            transform: scale(1.01);
        }
        .st-bo{
            color: #000;        
        }
        .st-bo.st-b8{
             color: #000;   
        }
        
                
        /* 아코디언 스타일 */
        .st-expander {
            background-color: #e6f0ff !important;
            border-radius: 10px !important;
            margin-bottom: 12px !important;
            border: none !important;
        }
        .st-expander summary {
            font-size: 18px !important;
            font-weight: 600 !important;
            color: white !important;
            padding: 16px !important;
        }
        .st-expander p {
            color: #e6e6e6 !important;
            padding: 10px !important;
            font-size: 15px !important;
        }

        /* 페이지네이션 wrapper */
        .pagination-box {
            width: 100%;
            display: flex;
            justify-content: center;
            margin-top: 18px;
        }

        /* 페이지 버튼 */
        .pagination-btn {
            padding: 7px 12px;
            background-color: white;
            border: 1px solid #cdd6e1;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            color: #e6f0ff;
            transition: all .5s;
        }

        .pagination-btn:hover {
            background-color: #e6eef8;
            border-color: #8fb3e2;
            transition: all .5s;
        }

        .pagination-btn.active {
            background-color: #e6f0ff;
            color: white;
            border-color: #e6f0ff;
        }

        div.stButton > button {
            background-color: white;
            border: 1px solid #e6f0ff;
            color: #e6f0ff !important;
            padding: 0px !important;
            border-radius: 6px !important;
            font-size: 13px !important;
            min-height: 28px;
        }

        div.stButton > button:hover {
            background-color: #e6eef8 !important;
            border-color: #8fb3e2 !important;
        }
        .st-emotion-cache-1permvm:has(.st-emotion-cache-10yr2a7){
            justify-content: center;        
        }
                
        .st-emotion-cache-10yr2a7{
            width: 28px !important;
            flex: 0 28px;        
        }
                
        .st-emotion-cache-wfksaw{
            justify-content: center;
            align-items: center;
        }
        
        .st-emotion-cache-zh2fnc{
            width: 100%;
        }
        
        /* disabled 버튼 스타일 */
        div.stButton > button[disabled] {
            opacity: 0.4 !important;
            cursor: not-allowed !important;
        }
                
        .st-emotion-cache-3uj0rx{
            margin-bottom: 0;
        }
                
        .pagination-btn.active{
                font-size: inherit;
                padding: 0;
                text-align: center;
        }
        *:hover{
            transition: all .5s;
        }
        .st-emotion-cache-pxambx{
            transition: all .5s;
        }
        .st-emotion-cache-pxambx:hover{
            color: #000;
            background-color: #e6f0ff;
        }
        .st-emotion-cache-1lsfsc6, .st-emotion-cache-1lsfsc6{
            transition: all .5s;
        }
        .st-emotion-cache-1lsfsc6, .st-emotion-cache-1lsfsc6:hover{
            background-color: #e6f0ff;
            color: #000;
            transition: all .5s;
        }
                
        ul[role="listbox"], ul[role="listbox"] > *, ul[role="listbox"] > * > *{
            background-color: #e6f0ff;
            color: #000;
                transition: all .5s;
        }
                
        
                
        ul[role="listbox"] > * > *:hover{
            background-color: #000;
                color: #e6f0ff;
                transition: all .5s;
        }
        
        ul[role="listbox"] > * > *:hover > span{
            color: #e6f0ff;
        }
        div[data-testid="stMainMenuDivider"]{
            background-color: #000;
        }
                
        div[data-testid="stSidebarContent"]{
            background-color: #e6f0ff;
        }
        div[data-testid="stSidebarContent"] .st-b8{
            color: #000;
        }
                
        label[data-testid="stWidgetLabel"]{
            color: #000;
        }
                
        .st-fa{
            border-color: #000;
        }
                
        .st-emotion-cache-pd6qx2{
            color: #000;
        }

        </style>
    """, unsafe_allow_html=True)

    # ===============================
    # DB에서 FAQ 데이터 불러오기
    # ===============================
    conn = create_connection()
    if conn:
        query = """
        SELECT id, major_category, minor_category, question_text, content
        FROM faq_data
        """
        faq_df = pd.read_sql(query, conn)
        conn.close()

        # ===============================
        # 검색 UI
        # ===============================
        col1, col2 = st.columns([2, 2])

        major_options = ["선택"] + sorted(faq_df['major_category'].dropna().unique())
        selected_major = col1.selectbox("대분류 선택", major_options)

        if selected_major == "선택":
            minor_options = ["선택"]
        else:
            minor_options = ["선택"] + sorted(
                faq_df[faq_df['major_category'] == selected_major]['minor_category'].dropna().unique()
            )

        selected_minor = col2.selectbox("소분류 선택", minor_options)

        # ===============================
        # 필터링
        # ===============================
        filtered_faq = faq_df.copy()

        if selected_major != "선택":
            filtered_faq = filtered_faq[filtered_faq['major_category'] == selected_major]

        if selected_minor != "선택":
            filtered_faq = filtered_faq[filtered_faq['minor_category'] == selected_minor]

        # ===============================
        # 검색 결과 없음
        # ===============================
        if filtered_faq.empty:
            st.warning("검색 결과가 없습니다.")
        else:

            # ===============================
            # 페이지네이션 계산
            # ===============================
            items_per_page = 5
            total_items = len(filtered_faq)
            total_pages = (total_items - 1) // items_per_page + 1

            page = max(1, min(st.session_state.faq_page, total_pages))

            start_idx = (page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            page_data = filtered_faq.iloc[start_idx:end_idx]

            # ===============================
            # 아코디언 출력
            # ===============================
            for _, row in page_data.iterrows():
                with st.expander(f"[{row['major_category']} > {row['minor_category']}] {row['question_text']}"):
                    st.markdown(row['content'], unsafe_allow_html=True)

            # ===============================
            # 페이지네이션 UI (항상 고정 9칸)
            # ===============================
            st.markdown("<div class='pagination-box'>", unsafe_allow_html=True)

            cols = st.columns(9)

            # 0: 처음(⏮)
            cols[0].button(
                "⏮",
                disabled=(page == 1),
                key="first_page",
            )
            if page != 1 and st.session_state.get("first_page"):
                st.session_state.faq_page = 1
                st.rerun()

            # 1: 이전(◀)
            cols[1].button(
                "◀",
                disabled=(page == 1),
                key="prev_page",
            )
            if page != 1 and st.session_state.get("prev_page"):
                st.session_state.faq_page = page - 1
                st.rerun()


            # 2~6 페이지 번호 5칸
            start_p = max(1, page - 2)
            end_p = min(total_pages, start_p + 4)
            pages_to_show = list(range(start_p, end_p + 1))

            # 5칸 유지
            while len(pages_to_show) < 5:
                pages_to_show.append(None)

            for i, p in enumerate(pages_to_show):
                col = cols[i + 2]
                if p is None:
                    col.markdown(" ")
                elif p == page:
                    col.markdown(
                        f"<div class='pagination-btn active'>{p}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    if col.button(str(p), key=f"page_{p}"):
                        st.session_state.faq_page = p
                        st.rerun()


            # 7: 다음(▶)
            cols[7].button(
                "▶",
                disabled=(page == total_pages),
                key="next_page",
            )
            if page != total_pages and st.session_state.get("next_page"):
                st.session_state.faq_page = page + 1
                st.rerun()


            # 8: 마지막(⏭)
            cols[8].button(
                "⏭",
                disabled=(page == total_pages),
                key="last_page",
            )
            if page != total_pages and st.session_state.get("last_page"):
                st.session_state.faq_page = total_pages
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)