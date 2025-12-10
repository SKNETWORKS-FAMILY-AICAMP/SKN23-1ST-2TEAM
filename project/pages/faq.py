from utils.load_css import load_css
load_css("styles/faq.css")
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

st.header("FAQ")

# ===============================
# 세션 상태 초기화
# ===============================
if "faq_page" not in st.session_state:
    st.session_state.faq_page = 1

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