-- CREATE USER 'sknteam2'@'localhost' IDENTIFIED BY '1234';
-- GRANT ALL PRIVILEGES ON sknteam2.* TO 'sknteam2'@'localhost';
-- FLUSH PRIVILEGES;
-- 
-- SELECT user, host FROM mysql.user;

create database sknteam2;

use sknteam2;

CREATE table if not exists ev_station (
    station_id VARCHAR(100) COMMENT '충전소 ID',
    station_name VARCHAR(200) COMMENT '충전소명',
    address VARCHAR(300) COMMENT '충전소 주소',
    detail_address VARCHAR(300) COMMENT '상세 주소',
    lat DOUBLE COMMENT '위도',
    lon DOUBLE COMMENT '경도',
    available_time VARCHAR(200) COMMENT '이용 시간',
    contact VARCHAR(100) COMMENT '연락처',
    reg_date VARCHAR(50) COMMENT '등록일자'
);

select * from ev_station
order by station_id;

select count(*) from ev_station;


CREATE TABLE IF NOT EXISTS ev_vehicle_stats (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '고유 ID',
    region VARCHAR(100) COMMENT '시군구 지역명',
    fuel_type VARCHAR(50) COMMENT '연료 종류 (전기, 수소 등)',
    usage_type VARCHAR(50) COMMENT '차량 용도 (개인, 업무, 공공 등)',
    passenger INT COMMENT '승용 차량 수',
    van INT COMMENT '승합 차량 수',
    truck INT COMMENT '화물 차량 수',
    special INT COMMENT '특수 차량 수',
    total INT COMMENT '전체 차량 수 합계'
) COMMENT='지역별 전기차/친환경차 통계 테이블';


CREATE TABLE IF NOT EXISTS ev_regional_status (
    ev_region_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ev_region_id',
    base_date DATE COMMENT '기준일',
    seoul INT COMMENT '서울',
    incheon INT COMMENT '인천',
    gyeonggi INT COMMENT '경기',
    gangwon INT COMMENT '강원',
    chungbuk INT COMMENT '충북',
    chungnam INT COMMENT '충남',
    daejeon INT COMMENT '대전',
    sejong INT COMMENT '세종',
    gyeongbuk INT COMMENT '경북',
    daegu INT COMMENT '대구',
    jeonbuk INT COMMENT '전북',
    jeonnam INT COMMENT '전남',
    gwangju INT COMMENT '광주',
    gyeongnam INT COMMENT '경남',
    busan INT COMMENT '부산',
    ulsan INT COMMENT '울산',
    jeju INT COMMENT '제주'
) COMMENT='지역별 전기차 현황 테이블';

select * from ev_vehicle_stats;
select * from ev_regional_status;



CREATE TABLE IF NOT EXISTS faq_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT,
    content TEXT
);


SELECT
    title,
    SUBSTRING(
        title,
        LOCATE('[', title) + 1,
        LOCATE(']', title) - LOCATE('[', title) - 1
    ) AS category,
    LTRIM(SUBSTRING_INDEX(title, ']', -1)) AS question_text
FROM faq_data;

ALTER TABLE faq_data
ADD COLUMN category VARCHAR(255),
ADD COLUMN question_text TEXT;

UPDATE faq_data
SET 
    category = SUBSTRING(
        title,
        LOCATE('[', title) + 1,
        LOCATE(']', title) - LOCATE('[', title) - 1
    ),
    question_text = LTRIM(SUBSTRING_INDEX(title, ']', -1));

ALTER TABLE faq_data
DROP COLUMN title;

ALTER TABLE faq_data
MODIFY COLUMN content text AFTER question_text;

ALTER TABLE faq_data
ADD COLUMN major_category VARCHAR(100),
ADD COLUMN minor_category VARCHAR(100);

UPDATE faq_data
SET major_category = TRIM(SUBSTRING_INDEX(category, '>', 1)),
    minor_category = TRIM(SUBSTRING_INDEX(category, '>', -1));

ALTER TABLE faq_data
DROP COLUMN category;

ALTER TABLE faq_data
MODIFY COLUMN id int not null FIRST;

ALTER TABLE faq_data
MODIFY COLUMN content text AFTER question_text;

ALTER TABLE faq_data
ADD COLUMN major_category VARCHAR(100),
ADD COLUMN minor_category VARCHAR(100);

UPDATE faq_data
SET major_category = TRIM(SUBSTRING_INDEX(category, '>', 1)),
    minor_category = TRIM(SUBSTRING_INDEX(category, '>', -1));

ALTER TABLE faq_data
DROP COLUMN category;

ALTER TABLE faq_data
MODIFY COLUMN id int not null FIRST;
