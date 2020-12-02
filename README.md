# Structure in Artist-Listener Data

This repository contains code to train a model that returns listener
features for artists. It can be used as a base model for creating more
complex models to generate artist insights (e.g., geographic or demographic
recommendations).

## Install

Ensure you're using Python 3.6. Then simply pull down the code and run

```bash
python -m venv env
source env/bin/activate
pip install .
```

## Run

This software assumes you are using Snowflake as your data warehouse. It can always be reworked to use another data source, as long as you have the tables described below.

Copy `.env.shadow` to `.env` and fill in with your Snowflake and neo4j
connection parameters. The three source tables referenced in `config.py` need to
exist in the Snowflake schema you specified. These are:

1. `USER_ARTIST_STREAMS_FILTERED_WITH_IDS`: A table with columns `artistname`, `artistnum`, `userid`, `usernum`, and `total_streams`. Each row represents the total times a given listener streamed a given artist.
2. `ARTIST_IDS_SINGLE_GENRE`: A table with columns `artistname`, `countrylist`, and `genreid`. This represents the countries an artist has been played in, as well as their genre. `countrylist` is a comma-separated list of country names.
3. `COUNTRY_ARTIST_STREAMS_BY_STORE`: A table with columns `artistnum`, `artistname`, `countryname`, `storename`, and `total_streams`. Each row is the total number of streams an artist received in a given country and "store" (e.g., Spotify, iTunes).

### Train

To train the model, simply run

```bash
artist_listener_train
```

This will save the features and artist clusters in `features_clusters.p`
by default.

### Inference

You can use the model to infer similar artists or generate geographic
recommendations.

```bash
artist_listener_insights similarity "<artist_name_1,artist_name_2,...>"
```

Example output looks like

```
{
  "artist_name_1": [
    {
      "name": "similar_artist_name_1",
      "similarity": 0.8724746619981572
    },
    {
      "name": "similar_artist_name_2",
      "similarity": 0.8723650858404651
    },
    ...
  ],
  "artist_name_2": [
    {
      "name": "similar_artist_name_1",
      "similarity": 0.9528950042946587
    },
    {
      "name": "similar_artist_name_2",
      "similarity": 0.9339451879861346
    },
    ...
  ]
}
```

To get geographic recommendations, run

```bash
artist_listener_insights geographic "<artist_name_1,artist_name_2,...>"
```

which returns

```
{
  "aritst_name_1": {
    "top_markets": [
      {
        "territory": "USA",
        "actual_streams": {
          "itunes/apple": 65034529,
          "pandora": 11254721,
          "spotify": 108156780,
          "google play": 5427456,
          "amazon unlimited": 24978311,
          "napster": 928452,
          "deezer": 99110,
          "total": 215879359
        },
        "modeled_streams": {
          "amazon unlimited": 1058597,
          "deezer": 6532,
          "google play": 364509,
          "itunes/apple": 3434108,
          "napster": 39947,
          "pandora": 710965,
          "spotify": 8630254,
          "total": 14244912
        }
      },
      {
        "territory": "Canada",
        "actual_streams": {
          "google play": 1093796,
          "deezer": 39841,
          "spotify": 9839118,
          "itunes/apple": 7106304,
          "napster": 2568,
          "total": 18081627
        },
        "modeled_streams": {
          "deezer": 1843,
          "google play": 98414,
          "itunes/apple": 604035,
          "napster": 122,
          "spotify": 1132072,
          "total": 1836486
        }
      },
      ...
    ],
    "recommendations": [
      {
        "territory": "Australia",
        "actual_streams": {
          "itunes/apple": 27266,
          "deezer": 476,
          "spotify": 65721,
          "amazon unlimited": 10,
          "google play": 2794,
          "total": 96267
        },
        "modeled_streams": {
          "amazon unlimited": 227,
          "deezer": 118,
          "google play": 3219,
          "itunes/apple": 34395,
          "spotify": 241024,
          "total": 278983
        }
      },
      {
        "territory": "United Kingdom",
        "actual_streams": {
          "napster": 68,
          "google play": 344,
          "deezer": 342,
          "amazon unlimited": 108,
          "itunes/apple": 917,
          "spotify": 14662,
          "total": 16441
        },
        "modeled_streams": {
          "amazon unlimited": 1849,
          "deezer": 845,
          "google play": 2272,
          "itunes/apple": 28737,
          "napster": 116,
          "spotify": 169733,
          "total": 203552
        }
      },
      ...
    ]
  },
  ...
}
```

### Upload to Databases

To load similarity and geographic insights data for all artists
in the training set into Snowflake, run

```
artist_listener_upload snowflake
```

To upload a graph of artist nodes, clusters, and similarities to neo4j, run

```
artist_listener_upload neo4j
```

This requires being connected to a graph through the neo4j browser, which
can be used to visualize the model.
