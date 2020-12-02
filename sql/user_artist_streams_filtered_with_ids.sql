/*
  Create table of user streams by artist with associated IDs
*/


CREATE OR REPLACE TABLE user_artist_streams_filtered_with_ids AS
  SELECT
    uas.artistname,
    ai.artistnum,
    uas.userid,
    ui.usernum,
    uas.total_streams
  FROM user_artist_streams_filtered uas
  JOIN artist_ids_single_genre ai ON ai.artistname = uas.artistname
  JOIN user_ids ui ON ui.userid = uas.userid
