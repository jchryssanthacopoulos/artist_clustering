/*
  Create table of user IDs
*/


CREATE OR REPLACE TABLE user_ids AS
  SELECT
    userid,
    ROW_NUMBER() OVER (ORDER BY userid) - 1 AS usernum
  FROM (
    SELECT DISTINCT userid from user_artist_streams_filtered
  )
