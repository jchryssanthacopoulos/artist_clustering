"""Upload artist data to database."""

import sys

from artist_listener_models.models.graph import HistoricalArtistGraphModel
from artist_listener_models.models.relational import (
    HistoricalArtistRelationalModel)


def main(*args):
    """Upload artist insights."""
    args = sys.argv[1:]

    if args[0] == 'neo4j':
        HistoricalArtistGraphModel().write_to_neo4j()
    elif args[0] == 'snowflake':
        HistoricalArtistRelationalModel().\
            write_similarities_to_snowflake().\
            write_geographic_recommendations_to_snowflake()
    else:
        print('Unrecognized option', args[0])
        print(
            'Syntax is artist_listener_upload [neo4j,snowflake]')
