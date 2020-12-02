/*
  Create table of artist metadata, including a single genre and list of
    countries in which the artist has had releases
*/


CREATE OR REPLACE TABLE artist_ids_single_genre AS
  SELECT
    uas.artistname,
    dac.countrylist,
    dag.genreid,
    ROW_NUMBER() OVER (ORDER BY uas.artistname) - 1 AS artistnum
  FROM (
    SELECT DISTINCT artistname FROM user_artist_streams_filtered
  ) uas
  JOIN (
    SELECT
      artistname,
      LISTAGG(countryname, ', ') WITHIN GROUP (ORDER BY countryname) AS countrylist
    FROM (
      SELECT
        remove_vowel_accents(TRIM(LOWER(da.artistname))) AS artistname,
        dc.countryname
      FROM FACTS.PROD.DIM_ARTIST da
      JOIN FACTS.PROD.DIM_COUNTRY dc ON dc.countryid = da.countryid
      GROUP BY 1, 2
    )
    GROUP BY 1
  ) dac ON dac.artistname = uas.artistname
  JOIN (
    SELECT
      artistname,
      genreid
    FROM (
      SELECT
        artistname,
        genreid,
        ROW_NUMBER() OVER (PARTITION BY artistname ORDER BY cnt DESC) AS rn
      FROM (
        SELECT
          remove_vowel_accents(TRIM(LOWER(da.artistname))) AS artistname,
          dr.genreid,
          COUNT(*) AS cnt
        FROM FACTS.PROD.DIM_ARTIST da
        JOIN FACTS.PROD.DIM_RELEASE dr ON dr.artistid = da.artistid
        GROUP BY 1, 2
      )
    )
    WHERE rn = 1
  ) dag ON dag.artistname = uas.artistname
