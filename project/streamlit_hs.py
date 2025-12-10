import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import pandas as pd
import streamlit.components.v1 as components
import json

# AgGrid imports
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# -------------------------------
# 1) 환경변수 로드
# -------------------------------
load_dotenv()
PASSWORD = os.getenv('PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_NAME = os.getenv('DB_NAME', 'sknteam2')
KAKAO_API_KEY = os.getenv("KAKAO_MAP_API_KEY")

st.set_page_config(layout="wide", page_title="충전소 지도 (AgGrid 통합)")

# -------------------------------
# 2) DB 연결 함수
# -------------------------------
def create_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=PASSWORD,
            database=DB_NAME,
            charset='utf8'
        )
        return conn
    except Error as e:
        st.error(f"DB 연결 오류: {e}")
        return None

# -------------------------------
# 3) 지역/도시 캐싱 로드
# -------------------------------
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

# -------------------------------
# 4) 사이드바 메뉴
# -------------------------------
menu = st.sidebar.radio("메뉴 선택", ["main", "정비소", "FAQ"])

# -------------------------------
# 5) MAIN 화면
# -------------------------------
if menu == "main":

    st.title("최강 2팀 충전소 지도")

    conn = create_connection()
    if conn is None:
        st.stop()

    query = """
    SELECT 
        s.station_name, s.address, s.detail_address,
        s.available_time, s.reg_date, s.lat, s.lon,
        r.region AS region_name,
        c.city_name AS city_name
    FROM ev_station s
    LEFT JOIN region r ON s.region_code = r.region_code
    LEFT JOIN city c ON s.city_code = c.city_code
    """
    df = pd.read_sql(query, conn)
    conn.close()

    # -------------------------------
    # 검색 UI
    # -------------------------------
    col1, col2, col3 = st.columns([2, 2, 4])
    address = col3.text_input("충전소 이름/주소 검색 (선택)")

    region_list = ["선택"] + sorted(region_df['region'].tolist())
    selected_region = col1.selectbox("도시 선택", region_list)

    if selected_region == "선택":
        city_list = ["시/군/구"]
    else:
        region_code = region_df.loc[region_df['region'] == selected_region, 'region_code'].values[0]
        filtered_city_df = city_df[city_df['region_code'] == region_code]
        city_list = ["시/군/구"] + sorted(filtered_city_df['city_name'].tolist())

    selected_city = col2.selectbox("시/군/구 선택", city_list)

    # -------------------------------
    # 필터 적용
    # -------------------------------
    filtered_df = df.copy()

    if selected_region != "선택" and selected_city != "시/군/구":
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
    else:
        filtered_df = pd.DataFrame(columns=df.columns)

    # -------------------------------
    # AgGrid 설정
    # -------------------------------
    st.subheader("충전소 목록")

    selected_row = None

    if not filtered_df.empty:
        grid_df = filtered_df.copy()
        grid_df = grid_df.rename(columns={
            "station_name": "충전소명",
            "address": "주소",
            "detail_address": "상세주소",
            "available_time": "이용시간",
            "reg_date": "등록일",
            "lat": "lat",
            "lon": "lon"
        })

        gb = GridOptionsBuilder.from_dataframe(grid_df)
        gb.configure_column("lat", hide=True)
        gb.configure_column("lon", hide=True)
        if "region_name" in grid_df.columns:
            gb.configure_column("region_name", hide=True)
        if "city_name" in grid_df.columns:
            gb.configure_column("city_name", hide=True)

        gb.configure_selection(selection_mode="single", use_checkbox=False)
        grid_options = gb.build()

        grid_response = AgGrid(
            grid_df,
            gridOptions=grid_options,
            height=160,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            allow_unsafe_jscode=True,
            fit_columns_on_grid_load=True,
        )

        selected_rows = grid_response.get("selected_rows", [])
        if isinstance(selected_rows, pd.DataFrame):
            selected_rows = selected_rows.to_dict(orient="records")
        if selected_rows is None or not isinstance(selected_rows, list):
            selected_rows = []

        if len(selected_rows) > 0:
            sel = selected_rows[0]
            selected_row = {
                "lat": float(sel["lat"]),
                "lon": float(sel["lon"]),
                "station_name": sel["충전소명"]
            }
    else:
        st.info("검색 조건을 선택하세요.")

    # -------------------------------
    # 지도 마커 및 Kakao 길찾기 URL 생성
    # -------------------------------
    if isinstance(selected_row, dict) and selected_row:
        coords = [selected_row]
        mode = "single"
    else:
        if not filtered_df.empty:
            coords = filtered_df[['lat', 'lon', 'station_name']].dropna().to_dict(orient="records")
            mode = "all"
        else:
            coords = []
            mode = "init"

    coords_json = json.dumps(coords, ensure_ascii=False)

    # -------------------------------
    # Kakao Map HTML/JS
    # -------------------------------
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8" />
      <style>
        html, body, #map {{
          width:100%;
          height:600px;
          margin:0;
          padding:0;
        }}
        .info-window {{
          padding:6px 8px;
          font-size:14px;
        }}
        #kakao-link {{
          margin-top:10px;
        }}
      </style>
    </head>
    <body>
      <div id="map"></div>
      <div id="kakao-link"></div>

      <script src="https://dapi.kakao.com/v2/maps/sdk.js?appkey={KAKAO_API_KEY}&autoload=false"></script>
      <script>
        var serverCoords = {coords_json};
        var mode = "{mode}";
        var map;
        var markers = [];

        function clearMarkers() {{
          markers.forEach(m => m.setMap(null));
          markers = [];
        }}

        function addMarker(lat, lon, title) {{
          var pos = new kakao.maps.LatLng(lat, lon);
          var marker = new kakao.maps.Marker({{position: pos, map: map}});
          markers.push(marker);

          var iw = new kakao.maps.InfoWindow({{
            content: '<div class="info-window">' + (title||'') + '</div>'
          }});
          kakao.maps.event.addListener(marker, 'click', function() {{
            iw.open(map, marker);
          }});
        }}

        function fitBounds(coords) {{
          if (!coords || coords.length === 0) return;
          var bounds = new kakao.maps.LatLngBounds();
          coords.forEach(c => bounds.extend(new kakao.maps.LatLng(c.lat, c.lon)));
          map.setBounds(bounds);
        }}

        function initMap(lat, lon) {{
          kakao.maps.load(function() {{
            map = new kakao.maps.Map(document.getElementById('map'), {{
              center: new kakao.maps.LatLng(lat, lon),
              level: 6
            }});

            if (mode === "all") {{
              clearMarkers();
              serverCoords.forEach(c => addMarker(c.lat, c.lon, c.station_name));
              fitBounds(serverCoords);
            }} else if (mode === "single") {{
              if (navigator.geolocation) {{
                navigator.geolocation.getCurrentPosition(function(position) {{
                  var myLat = position.coords.latitude;
                  var myLon = position.coords.longitude;

                  clearMarkers();
                  addMarker(myLat, myLon, "내 위치");

                  var c = serverCoords[0];
                  addMarker(c.lat, c.lon, c.station_name);

                  fitBounds([
                    {{lat: myLat, lon: myLon}},
                    {{lat: c.lat, lon: c.lon}}
                  ]);

                  // Kakao 길찾기 버튼 생성
                  var kakaoLinkDiv = document.getElementById("kakao-link");
                  var kakaoUrl = "https://map.kakao.com/link/by/car/"
                      + "내위치," + myLat + "," + myLon + "/"
                      + c.station_name + "," + c.lat + "," + c.lon;
                  kakaoLinkDiv.innerHTML = '<a href="' + kakaoUrl + '" target="_blank" style="font-size:16px;"> 카카오 길찾기 열기</a>';

                }}, function() {{
                  var c = serverCoords[0];
                  clearMarkers();
                  addMarker(c.lat, c.lon, c.station_name);
                  map.setCenter(new kakao.maps.LatLng(c.lat, c.lon));
                }});
              }}
            }} else if (mode === "init") {{
              if (navigator.geolocation) {{
                navigator.geolocation.getCurrentPosition(function(p) {{
                  clearMarkers();
                  addMarker(p.coords.latitude, p.coords.longitude, "내 위치");
                  map.setCenter(new kakao.maps.LatLng(p.coords.latitude, p.coords.longitude));
                }});
              }} else {{
                  map.setCenter(new kakao.maps.LatLng(37.5665,126.9780));
              }}
            }}
          }});
        }}

        var defaultLat = 37.5665;
        var defaultLon = 126.9780;
        if (serverCoords.length > 0) {{
          defaultLat = serverCoords[0].lat;
          defaultLon = serverCoords[0].lon;
        }}
        initMap(defaultLat, defaultLon);
      </script>
    </body>
    </html>
    """

    components.html(html_code, height=700, scrolling=True)

# -------------------------------
# 기타 메뉴
# -------------------------------
elif menu == "정비소":
    st.header("정비소 페이지")
    st.info("정비소 정보를 입력하세요.")

elif menu == "FAQ":
    st.header("FAQ")
    st.info("FAQ를 입력하세요.")