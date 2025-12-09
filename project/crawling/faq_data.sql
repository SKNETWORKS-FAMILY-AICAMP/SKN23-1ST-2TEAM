USE sknteam2;

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
