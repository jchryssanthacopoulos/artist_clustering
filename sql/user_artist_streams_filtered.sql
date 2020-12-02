/*
  Create filtered version of user streams table by artist
  where infrequent listeners and unpopular artists are
  iteratively filtered out to reduce dataset size
*/


CREATE OR REPLACE TABLE user_artist_streams_filtered AS (
  WITH user_artist_streams AS (
    SELECT
      *
    FROM user_artist_streams_all_artists
    WHERE total_streams >= 100  --filter out users
  ), popular_artists AS (
    SELECT
      artistname
    FROM user_artist_streams
    GROUP BY 1
    HAVING COUNT(*) >= 1000  --filter out artists
  )
  SELECT
    a.artistname,
    a.userid,
    a.total_streams
  FROM user_artist_streams a
  JOIN (
    SELECT
      userid
    FROM user_artist_streams uas
    JOIN popular_artists pa ON pa.artistname = uas.artistname
    GROUP BY 1
    HAVING COUNT(*) >= 10  --filter out users
  ) fl ON fl.userid = a.userid
  JOIN popular_artists pa on pa.artistname = a.artistname
)
