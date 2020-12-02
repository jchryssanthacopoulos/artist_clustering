/*
  Create table of user streams by artist for Spotify 2018
*/


CREATE OR REPLACE FUNCTION remove_vowel_accents(s VARCHAR)
  RETURNS VARCHAR
  AS $$REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(s, 'ó', 'o'), 'é', 'e'), 'á', 'a'), 'í', 'i'), 'ú', 'u')$$;


CREATE OR REPLACE TABLE user_artist_streams_all_artists
  (artistname, userid, total_streams) AS
    SELECT
      remove_vowel_accents(TRIM(LOWER(da.artistname))),
      sos.user_id,
      COUNT(*) AS total_streams
    FROM FACTS.PROD.STAGING_SOS sos
    JOIN FACTS.PROD.DIM_ARTIST da ON da.artistid = sos.artistid
    WHERE sos.download_activity_date BETWEEN '2018-01-01' AND '2018-12-31'
      AND sos.storeid = 286
      AND LOWER(da.artistname) NOT LIKE '%various%'  --exclude various forms of "various artists"
      AND LOWER(da.artistname) NOT LIKE '%varios%'
      AND LOWER(da.artistname) NOT LIKE '%vários%'
    GROUP BY 1, 2
