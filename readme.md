# 👋 SKN23-1st-Team2 Mini Project 👋

지역별 전기차 충전소 & 지역별 정비소 & FAQ 통합 정보 서비스
- 팀원 : 유헌상 김민정 김다빈
- 역할 : 
  - 유헌상 - 팀장, 데이터 총괄 및 streamlit 메인페이지 구현
  - 김민정 - Mysql 데이터 정제 및 streamlit 정비소 페이지 구현 
  - 김다빈 - 현대 faq, 웹사이트 크롤링 담당, streamlit faq페이지 구현
- 프로젝트 기간 : 2024.12.10 ~ 2024.12.11

1. 프로젝트 개요 및 소개

현시점 전 세계에서는 지구 온난화등 환경 문제로 인하여 전기차 수요가 급격히 증가하고 있습니다.   
그래서 저희 팀에서는 전기차 운전자 및 전기차 예비 구매자를 대상으로 하여 현재위치, 선택지역을 기준으로 가까운 충전소들을 추천할 수 있는 서비스를 제공합니다.

전국 EV 충전소 검색
시/도 → 시/군/구 기반 위치 조회
주소 기반 상세 검색
자주 묻는 질문(FAQ) 조회 기능

Streamlit 기반 인터렉티브 UI

2. Tech Stack
- Data
- Python
- Pandas
- MySQL

- Selenium (일부 데이터 크롤링)
- UI
- Streamlit
- CSS(custom style)
- SessionState

- Co-Work Tools
- Git / GitHub
- Notion

3. ERD
이미지 추가

5. 결과 화면
이미지/영상 추가

6. 디렉토리 구조
```
sknteam2
├─ project
│   └─ api
├─      └─ 
├─ faq_output.json
├─      └─ 
├─ create_table_grant.sql
├─ requirements.txt
├─ sample.py
├─ streamlit.py
└─ README.md
(추후 수정)
```
7. 실행 방법
파이썬먼저 까세요~

8. 향후 개선 사항
- FAQ CRUD 기능 추가
- 사용자 로그인 기능
- 반응형 UI
- 관리자 페이지 구축
- API 기반 실시간 충전소 정보 연동

9. 한줄 회고
- 유헌상
- 김민정
- 김다빈
