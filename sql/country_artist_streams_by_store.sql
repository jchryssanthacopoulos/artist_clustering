/*
  Create table of artist streams by country and store
*/


CREATE OR REPLACE TABLE country_artist_streams_by_store AS
  SELECT
    ai.artistnum,
    ai.artistname,
    dc.countryname,
    LOWER(ds.storename) AS storename,
    SUM(fa.units) AS total_streams
  FROM FACTS.PROD.FACT_ANALYTICS fa
  JOIN FACTS.PROD.DIM_ARTIST da ON da.artistid = fa.artistid
  JOIN artist_ids_single_genre ai ON ai.artistname = remove_vowel_accents(TRIM(LOWER(da.artistname)))
  JOIN FACTS.PROD.DIM_COUNTRY dc ON dc.countryid = fa.countryid
  JOIN FACTS.PROD.DIM_STORE ds ON ds.storeid = fa.storeid
  WHERE fa.transactiontypeid IN (1, 10, 48)
    AND fa.dayid BETWEEN 6942 and 7306  --all of 2018
  GROUP BY 1, 2, 3, 4
