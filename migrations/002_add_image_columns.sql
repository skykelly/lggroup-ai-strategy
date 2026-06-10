-- 콘셉트/위키 페이지 대표 이미지 (출처 페이지의 og:image에서 추출)
ALTER TABLE concepts ADD COLUMN IF NOT EXISTS image_url text;
ALTER TABLE concepts ADD COLUMN IF NOT EXISTS image_source_url text;

ALTER TABLE pages ADD COLUMN IF NOT EXISTS image_url text;
ALTER TABLE pages ADD COLUMN IF NOT EXISTS image_source_url text;
