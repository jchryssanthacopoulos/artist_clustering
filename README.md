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

Copy `.env.shadow` to `.env` and fill in with your Snowflake and neo4j
connection parameters. The three source tables referenced in `config.py` need to
exist in the Snowflake schema you specified. They can be created using the
SQL files in the `sql` directory. Otherwise, versions of the tables can be
cloned from the `DEV_ENGINEERING.TEST_JAMESC` schema.

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
artist_listener_insights similarity "kelsea ballerini,g herbo"
```

Example output looks like

```
{
  "kelsea ballerini": [
    {
      "name": "waterloo revival",
      "similarity": 0.8724746619981572
    },
    {
      "name": "locash",
      "similarity": 0.8723650858404651
    },
    {
      "name": "taylor acorn",
      "similarity": 0.8719980084142703
    },
    {
      "name": "chris buck band",
      "similarity": 0.8664414011240895
    },
    {
      "name": "michael tyler",
      "similarity": 0.8648188128562296
    },
    {
      "name": "abby anderson",
      "similarity": 0.8612067886941012
    },
    {
      "name": "steve moakler",
      "similarity": 0.8605014044954074
    },
    {
      "name": "david lee murphy",
      "similarity": 0.8601635078631733
    },
    {
      "name": "adam sanders",
      "similarity": 0.8597382393465469
    },
    {
      "name": "levi hummon",
      "similarity": 0.8581953250554374
    }
  ],
  "g herbo": [
    {
      "name": "chief keef",
      "similarity": 0.9528950042946587
    },
    {
      "name": "sd",
      "similarity": 0.9339451879861346
    },
    {
      "name": "yungeen ace",
      "similarity": 0.9123162617820659
    },
    {
      "name": "flipp dinero",
      "similarity": 0.8837287067560998
    },
    {
      "name": "dave east",
      "similarity": 0.8717981051921563
    },
    {
      "name": "chinx",
      "similarity": 0.8526994497773716
    },
    {
      "name": "max b",
      "similarity": 0.8422165316526921
    },
    {
      "name": "tec",
      "similarity": 0.7958956522530052
    },
    {
      "name": "chinx drugz",
      "similarity": 0.7828587936371139
    },
    {
      "name": "lancey foux",
      "similarity": 0.7735180783340619
    }
  ]
}
```

To get geographic recommendations, run

```bash
artist_listener_insights geographic "kelsea ballerini,g herbo"
```

which returns

```
{
  "kelsea ballerini": {
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
      {
        "territory": "Germany",
        "actual_streams": {
          "itunes/apple": 189453,
          "napster": 17073,
          "24/7 entertainment gmbh": 940,
          "spotify": 895416,
          "google play": 6171,
          "amazon unlimited": 40339,
          "deezer": 24840,
          "total": 1174232
        },
        "modeled_streams": {
          "24/7 entertainment gmbh": 17,
          "amazon unlimited": 1630,
          "deezer": 710,
          "google play": 169,
          "itunes/apple": 7264,
          "napster": 271,
          "spotify": 65372,
          "total": 75433
        }
      },
      {
        "territory": "Norway",
        "actual_streams": {
          "google play": 1381,
          "deezer": 373,
          "napster": 5,
          "itunes/apple": 32544,
          "spotify": 954648,
          "total": 988951
        },
        "modeled_streams": {
          "deezer": 6,
          "google play": 43,
          "itunes/apple": 1109,
          "spotify": 66911,
          "napster": null,
          "total": 68069
        }
      },
      {
        "territory": "Sweden",
        "actual_streams": {
          "itunes/apple": 25771,
          "deezer": 1690,
          "spotify": 884904,
          "google play": 535,
          "total": 912900
        },
        "modeled_streams": {
          "deezer": 80,
          "google play": 14,
          "itunes/apple": 927,
          "spotify": 71923,
          "total": 72944
        }
      },
      {
        "territory": "Netherlands",
        "actual_streams": {
          "spotify": 677006,
          "itunes/apple": 44346,
          "napster": 231,
          "deezer": 12523,
          "google play": 2391,
          "total": 736497
        },
        "modeled_streams": {
          "deezer": 323,
          "google play": 11,
          "itunes/apple": 1112,
          "napster": 3,
          "spotify": 29517,
          "total": 30966
        }
      },
      {
        "territory": "Brazil",
        "actual_streams": {
          "deezer": 35166,
          "spotify": 611590,
          "google play": 5562,
          "itunes/apple": 40628,
          "napster": 3099,
          "total": 696045
        },
        "modeled_streams": {
          "deezer": 560,
          "google play": 78,
          "itunes/apple": 941,
          "napster": 35,
          "spotify": 37034,
          "total": 38648
        }
      },
      {
        "territory": "Mexico",
        "actual_streams": {
          "google play": 7981,
          "deezer": 2039,
          "spotify": 507390,
          "napster": 6,
          "itunes/apple": 58027,
          "total": 575443
        },
        "modeled_streams": {
          "deezer": 90,
          "google play": 490,
          "itunes/apple": 2163,
          "spotify": 39861,
          "napster": null,
          "total": 42604
        }
      },
      {
        "territory": "Japan",
        "actual_streams": {
          "itunes/apple": 286561,
          "spotify": 220377,
          "deezer": 51,
          "google play": 9722,
          "total": 516711
        },
        "modeled_streams": {
          "deezer": 1,
          "google play": 120,
          "itunes/apple": 4934,
          "spotify": 11488,
          "total": 16543
        }
      },
      {
        "territory": "Spain",
        "actual_streams": {
          "deezer": 1073,
          "napster": 71,
          "spotify": 312037,
          "itunes/apple": 27166,
          "google play": 502,
          "amazon unlimited": 616,
          "total": 341465
        },
        "modeled_streams": {
          "amazon unlimited": 19,
          "deezer": 31,
          "google play": 17,
          "itunes/apple": 696,
          "spotify": 26852,
          "napster": null,
          "total": 27615
        }
      }
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
      {
        "territory": "New Zealand",
        "actual_streams": {
          "spotify": 8405,
          "google play": 89,
          "amazon unlimited": 1,
          "itunes/apple": 648,
          "total": 9143
        },
        "modeled_streams": {
          "amazon unlimited": 115,
          "google play": 164,
          "itunes/apple": 1382,
          "spotify": 31204,
          "total": 32865
        }
      },
      {
        "territory": "Denmark",
        "actual_streams": {
          "google play": 495,
          "napster": 9,
          "spotify": 254082,
          "deezer": 2090,
          "itunes/apple": 26125,
          "total": 282801
        },
        "modeled_streams": {
          "deezer": 21,
          "google play": 22,
          "itunes/apple": 702,
          "spotify": 21598,
          "napster": null,
          "total": 22343
        }
      },
      {
        "territory": "Taiwan, Province Of China",
        "actual_streams": {
          "itunes/apple": 414,
          "spotify": 2865,
          "total": 3279
        },
        "modeled_streams": {
          "itunes/apple": 1171,
          "spotify": 21118,
          "total": 22289
        }
      },
      {
        "territory": "Switzerland",
        "actual_streams": {
          "google play": 4333,
          "napster": 34,
          "itunes/apple": 48962,
          "deezer": 1418,
          "spotify": 197859,
          "total": 252606
        },
        "modeled_streams": {
          "deezer": 50,
          "google play": 113,
          "itunes/apple": 2262,
          "napster": 0,
          "spotify": 18837,
          "total": 21262
        }
      },
      {
        "territory": "France",
        "actual_streams": {
          "itunes/apple": 42150,
          "google play": 5078,
          "deezer": 47822,
          "spotify": 217604,
          "amazon unlimited": 2775,
          "napster": 17340,
          "total": 332769
        },
        "modeled_streams": {
          "amazon unlimited": 83,
          "deezer": 1291,
          "google play": 185,
          "itunes/apple": 1477,
          "napster": 52,
          "spotify": 16166,
          "total": 19254
        }
      },
      {
        "territory": "Philippines",
        "actual_streams": {
          "itunes/apple": 668,
          "spotify": 9890,
          "deezer": 13,
          "total": 10571
        },
        "modeled_streams": {
          "deezer": 17,
          "itunes/apple": 289,
          "spotify": 15268,
          "total": 15574
        }
      },
      {
        "territory": "Italy",
        "actual_streams": {
          "napster": 91,
          "spotify": 240177,
          "google play": 619,
          "deezer": 871,
          "amazon unlimited": 674,
          "itunes/apple": 22371,
          "total": 264803
        },
        "modeled_streams": {
          "amazon unlimited": 36,
          "deezer": 36,
          "google play": 38,
          "itunes/apple": 626,
          "spotify": 14270,
          "napster": null,
          "total": 15006
        }
      },
      {
        "territory": "Ireland",
        "actual_streams": {
          "spotify": 70166,
          "deezer": 506,
          "google play": 1373,
          "itunes/apple": 13735,
          "total": 85780
        },
        "modeled_streams": {
          "deezer": 10,
          "google play": 103,
          "itunes/apple": 757,
          "spotify": 11233,
          "total": 12103
        }
      }
    ]
  },
  "g herbo": {
    "top_markets": [
      {
        "territory": "USA",
        "actual_streams": {
          "amazon unlimited": 1427521,
          "itunes/apple": 300363758,
          "napster": 784834,
          "spotify": 123188282,
          "google play": 5295399,
          "deezer": 327266,
          "pandora": 5741001,
          "total": 437128061
        },
        "modeled_streams": {
          "amazon unlimited": 94160,
          "deezer": 22765,
          "google play": 357227,
          "itunes/apple": 10304626,
          "napster": 55425,
          "pandora": 312612,
          "spotify": 7343126,
          "total": 18489941
        }
      },
      {
        "territory": "Canada",
        "actual_streams": {
          "deezer": 43641,
          "google play": 278902,
          "itunes/apple": 5538734,
          "napster": 135,
          "spotify": 5092565,
          "total": 10953977
        },
        "modeled_streams": {
          "deezer": 5837,
          "google play": 34153,
          "itunes/apple": 360300,
          "napster": 58,
          "spotify": 632796,
          "total": 1033144
        }
      },
      {
        "territory": "United Kingdom",
        "actual_streams": {
          "napster": 2731,
          "google play": 33520,
          "deezer": 43316,
          "amazon unlimited": 5244,
          "spotify": 1761544,
          "itunes/apple": 1079757,
          "total": 2926112
        },
        "modeled_streams": {
          "amazon unlimited": 2087,
          "deezer": 9850,
          "google play": 7019,
          "itunes/apple": 185232,
          "napster": 601,
          "spotify": 437118,
          "total": 641907
        }
      },
      {
        "territory": "Australia",
        "actual_streams": {
          "amazon unlimited": 61,
          "deezer": 4339,
          "google play": 17734,
          "itunes/apple": 227228,
          "spotify": 837280,
          "total": 1086642
        },
        "modeled_streams": {
          "amazon unlimited": 7,
          "deezer": 767,
          "google play": 3808,
          "itunes/apple": 29521,
          "spotify": 155354,
          "total": 189457
        }
      },
      {
        "territory": "Germany",
        "actual_streams": {
          "itunes/apple": 117046,
          "deezer": 40676,
          "24/7 entertainment gmbh": 827,
          "napster": 10074,
          "google play": 5659,
          "spotify": 711259,
          "amazon unlimited": 3923,
          "total": 889464
        },
        "modeled_streams": {
          "24/7 entertainment gmbh": 58,
          "amazon unlimited": 956,
          "deezer": 6649,
          "google play": 1523,
          "itunes/apple": 25916,
          "napster": 3563,
          "spotify": 188578,
          "total": 227243
        }
      },
      {
        "territory": "Netherlands",
        "actual_streams": {
          "napster": 173,
          "deezer": 38403,
          "spotify": 732074,
          "itunes/apple": 23633,
          "google play": 953,
          "total": 795236
        },
        "modeled_streams": {
          "deezer": 6985,
          "google play": 323,
          "itunes/apple": 3263,
          "napster": 100,
          "spotify": 163479,
          "total": 174150
        }
      },
      {
        "territory": "France",
        "actual_streams": {
          "spotify": 421398,
          "google play": 7387,
          "deezer": 195977,
          "amazon unlimited": 190,
          "napster": 19415,
          "itunes/apple": 114324,
          "total": 758691
        },
        "modeled_streams": {
          "amazon unlimited": 60,
          "deezer": 28736,
          "google play": 1434,
          "itunes/apple": 24163,
          "napster": 7931,
          "spotify": 97005,
          "total": 159329
        }
      },
      {
        "territory": "Sweden",
        "actual_streams": {
          "spotify": 387037,
          "napster": 3,
          "google play": 352,
          "itunes/apple": 10561,
          "deezer": 2238,
          "total": 400191
        },
        "modeled_streams": {
          "deezer": 361,
          "google play": 108,
          "itunes/apple": 2259,
          "napster": 0,
          "spotify": 86545,
          "total": 89273
        }
      },
      {
        "territory": "Brazil",
        "actual_streams": {
          "itunes/apple": 6939,
          "napster": 88,
          "deezer": 56074,
          "google play": 1456,
          "spotify": 247469,
          "total": 312026
        },
        "modeled_streams": {
          "deezer": 5242,
          "google play": 289,
          "itunes/apple": 1561,
          "napster": 49,
          "spotify": 56804,
          "total": 63945
        }
      },
      {
        "territory": "Mexico",
        "actual_streams": {
          "deezer": 3019,
          "itunes/apple": 24290,
          "spotify": 263840,
          "google play": 4392,
          "total": 295541
        },
        "modeled_streams": {
          "deezer": 329,
          "google play": 483,
          "itunes/apple": 3019,
          "spotify": 40380,
          "total": 44211
        }
      }
    ],
    "recommendations": [
      {
        "territory": "Norway",
        "actual_streams": {
          "google play": 120,
          "spotify": 260954,
          "itunes/apple": 9979,
          "deezer": 347,
          "total": 271400
        },
        "modeled_streams": {
          "deezer": 81,
          "google play": 103,
          "itunes/apple": 1591,
          "spotify": 68703,
          "total": 70478
        }
      },
      {
        "territory": "Italy",
        "actual_streams": {
          "spotify": 246124,
          "deezer": 3426,
          "napster": 3,
          "itunes/apple": 17785,
          "amazon unlimited": 29,
          "google play": 1226,
          "total": 268593
        },
        "modeled_streams": {
          "amazon unlimited": 17,
          "deezer": 506,
          "google play": 200,
          "itunes/apple": 2787,
          "napster": 1,
          "spotify": 45212,
          "total": 48723
        }
      },
      {
        "territory": "Denmark",
        "actual_streams": {
          "deezer": 1847,
          "google play": 80,
          "spotify": 135018,
          "itunes/apple": 8952,
          "total": 145897
        },
        "modeled_streams": {
          "deezer": 475,
          "google play": 119,
          "itunes/apple": 2801,
          "spotify": 41518,
          "total": 44913
        }
      },
      {
        "territory": "Switzerland",
        "actual_streams": {
          "24/7 entertainment gmbh": 5,
          "spotify": 123924,
          "deezer": 5039,
          "napster": 18,
          "itunes/apple": 29562,
          "google play": 3540,
          "total": 162088
        },
        "modeled_streams": {
          "deezer": 900,
          "google play": 763,
          "itunes/apple": 8460,
          "napster": 11,
          "spotify": 34743,
          "24/7 entertainment gmbh": null,
          "total": 44877
        }
      },
      {
        "territory": "New Zealand",
        "actual_streams": {
          "spotify": 182048,
          "google play": 976,
          "amazon unlimited": 82,
          "itunes/apple": 21090,
          "deezer": 485,
          "total": 204681
        },
        "modeled_streams": {
          "amazon unlimited": 7,
          "deezer": 108,
          "google play": 202,
          "itunes/apple": 2711,
          "spotify": 41434,
          "total": 44462
        }
      },
      {
        "territory": "Spain",
        "actual_streams": {
          "napster": 8,
          "itunes/apple": 10514,
          "deezer": 2410,
          "spotify": 201415,
          "google play": 885,
          "amazon unlimited": 64,
          "total": 215296
        },
        "modeled_streams": {
          "amazon unlimited": 2,
          "deezer": 335,
          "google play": 177,
          "itunes/apple": 2589,
          "napster": 4,
          "spotify": 35030,
          "total": 38137
        }
      },
      {
        "territory": "Finland",
        "actual_streams": {
          "google play": 118,
          "spotify": 168029,
          "deezer": 2303,
          "itunes/apple": 3916,
          "total": 174366
        },
        "modeled_streams": {
          "deezer": 324,
          "google play": 36,
          "itunes/apple": 802,
          "spotify": 35070,
          "total": 36232
        }
      },
      {
        "territory": "Belgium",
        "actual_streams": {
          "deezer": 7130,
          "itunes/apple": 14022,
          "spotify": 113501,
          "google play": 1598,
          "total": 136251
        },
        "modeled_streams": {
          "deezer": 1214,
          "google play": 388,
          "itunes/apple": 3720,
          "spotify": 28943,
          "total": 34265
        }
      },
      {
        "territory": "Poland",
        "actual_streams": {
          "itunes/apple": 7909,
          "google play": 789,
          "deezer": 1328,
          "spotify": 113894,
          "total": 123920
        },
        "modeled_streams": {
          "deezer": 144,
          "google play": 111,
          "itunes/apple": 942,
          "spotify": 23412,
          "total": 24609
        }
      },
      {
        "territory": "Ireland",
        "actual_streams": {
          "deezer": 1301,
          "spotify": 95337,
          "itunes/apple": 7727,
          "google play": 598,
          "total": 104963
        },
        "modeled_streams": {
          "deezer": 198,
          "google play": 143,
          "itunes/apple": 1510,
          "spotify": 21213,
          "total": 23064
        }
      }
    ]
  }
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
