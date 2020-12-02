"""Configuration parameters."""

import os


# Snowflake connection parameters
SNOWFLAKE_USER = os.environ.get('SNOWFLAKE_USER')
SNOWFLAKE_PASSWORD = os.environ.get('SNOWFLAKE_PASSWORD')
SNOWFLAKE_ACCOUNT = os.environ.get('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_DATABASE = os.environ.get('SNOWFLAKE_DATABASE')
SNOWFLAKE_SCHEMA = os.environ.get('SNOWFLAKE_SCHEMA')
SNOWFLAKE_ROLE = os.environ.get('SNOWFLAKE_ROLE')
SNOWFLAKE_WAREHOUSE = os.environ.get('SNOWFLAKE_WAREHOUSE')

# neo4j connection parameters
NEO4J_URI = os.environ.get('NEO4J_URI')
NEO4J_USER = os.environ.get('NEO4J_USER')
NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD')

# table of artist streams by user and associated metadata
ARTIST_USER_STREAMS_TABLE = 'USER_ARTIST_STREAMS_FILTERED_WITH_IDS'
ARTIST_METADATA_TABLE = 'ARTIST_IDS_SINGLE_GENRE'

# table of artist streams by country and store
ARTIST_COUNTRY_STREAMS_TABLE = 'COUNTRY_ARTIST_STREAMS_BY_STORE'

# number of user features to create
NUM_FEATURES = 1000

# number of artist clusters to create
NUM_CLUSTERS = 10

# state for random number generator
RANDOM_STATE = 0

# output file to save
OUTPUT_FILE = 'features_clusters.p'

# table of artist similarities
ARTIST_SIMILARITY_TABLE = 'ARTIST_SIMILARITY'

# table of artist geographic recommendations
ARTIST_GEOGRAPHIC_RECOMMENDATIONS_TABLE = 'ARTIST_GEOGRAPHIC_RECOMMENDATIONS'

# similarity metric to use (i.e., euclidean or cosine)
SIMILARITY_METRIC = 'cosine'
