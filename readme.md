👋 SKN07-1st-Team2 Mini Project 👋

전기차 충전소 & FAQ 통합 정보 서비스
팀원 : (팀원 정보 입력 가능)
프로젝트 기간 : 2024.11.13 ~ 2024.11.14

1. 프로젝트 개요 및 소개

전기차 보급은 빠르게 증가하고 있으며, 국내 전기차 등록 대수는 매년 크게 증가하고 있습니다.
하지만 전기차 이용자의 불만 1~2위는 충전 인프라 부족, 충전소 정보 부족 등 충전에 대한 불편함이 압도적입니다.

이에 따라 본 프로젝트는 아래 기능을 제공하는 전기차 관련 통합 정보 웹 서비스를 제공합니다.

전국 EV 충전소 검색

시/도 → 시/군/구 기반 위치 조회

주소 기반 상세 검색

충전소 이용시간/주소/등록일 조회

자주 묻는 질문(FAQ) 조회 기능

대분류/소분류 필터 + 아코디언 UI

페이지네이션 기능(5개씩 표시)

Streamlit 기반 인터렉티브 UI

2. Tech Stack
🧱 Data Pipeline

Python

Pandas

MySQL

Selenium (일부 데이터 크롤링)

🖥️ UI

Streamlit

HTML/CSS(Custom)

SessionState 기반 페이지 관리

🤝 Co-Work Tools

Git / GitHub

Notion

Slack

3. Flow Chart

(원하시면 실제 Flow Chart 이미지 삽입 가능합니다.)

4. ER(Entity Relation) 다이어그램

(요청 시 실제 ERD 생성하여 이미지 추가 가능)

5. 결과 화면
🔌 지역별 충전소 검색 UI

(이미지 삽입 가능)

🔎 지역별 충전소 조회 결과

(이미지 삽입 가능)

📄 FAQ 페이지

대분류/소분류 필터

아코디언 구조

페이지네이션
(이미지 삽입 가능)

6. 디렉토리 구조

요청하신 형식에 맞춰 현재 리포지토리 기준으로 재작성했습니다.

SKN07-1st-2Team
├─ project
│   └─ (작업 중인 프로젝트 파일)
├─ faq_output.csv
├─ faq_output.json
├─ create_table_grant.sql
├─ requirements.txt
├─ sample.py
├─ streamlit.py
└─ README.md

7. 실행 방법
pip install -r requirements.txt
streamlit run streamlit.py


DB 설정은 create_table_grant.sql 실행 후 .env 파일에 DB 정보를 추가하면 됩니다.

8. 향후 개선 사항

FAQ CRUD 기능 추가

사용자 로그인 기능

반응형 UI

관리자 페이지 구축

API 기반 실시간 충전소 정보 연동