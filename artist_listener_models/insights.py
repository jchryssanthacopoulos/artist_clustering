"""Get artist insights based on similar artists."""

import json
import sys

from artist_listener_models.models.base import HistoricalArtistModel
from artist_listener_models.models.geo import GeographicArtistModel


def get_similar_artists(artist_names):
    """Get similar artists."""
    artist_model = HistoricalArtistModel()

    similar_artists = {}
    for artist in artist_names:
        similar_artists_response = artist_model.similar_artists(
            artist)

        # remove artist ID from response
        for similar_artist in similar_artists_response:
            del similar_artist['id']

        similar_artists[artist] = similar_artists_response

    _display_results(similar_artists)


def get_geographic_recommendations(artist_names):
    """Get geographic recommendations."""
    geographic_model = GeographicArtistModel()

    geographic_recs = {}
    for artist in artist_names:
        geographic_recs[artist] = (
            geographic_model.geographic_recommendations(artist))

    _display_results(geographic_recs)


def _display_results(results):
    """Display results."""
    print(json.dumps(results, indent=2, ensure_ascii=False))


def main(*args):
    """Get artist insights."""
    args = sys.argv[1:]

    if args[0] == 'similarity':
        artist_names = args[1].split(',')
        get_similar_artists(artist_names)
    elif args[0] == 'geographic':
        artist_names = args[1].split(',')
        get_geographic_recommendations(artist_names)
    else:
        print('Unrecognized option', args[0])
        print(
            'Syntax is artist_listener_insights '
            '[similarity,geographic] artist[,artist2[,...]]')
