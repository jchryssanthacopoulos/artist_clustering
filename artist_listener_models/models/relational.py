"""Relational artist model."""

import pandas as pd

from artist_listener_models import config
from artist_listener_models.database import utils as db_utils
from artist_listener_models.models.base import HistoricalArtistModel
from artist_listener_models.models.geo import GeographicArtistModel


class HistoricalArtistRelationalModel(object):
    """Relational artist model for artists in training set."""

    def __init__(self):
        """Graph artist model constructor."""
        self._load_model()

        # make Snowflake connection
        # TODO: put this in a context manager
        self.db_engine = db_utils.connect_to_db()

    def write_similarities_to_snowflake(self, top_n=10):
        """Write artist similarities to Snowflake."""
        similar_artists_df = pd.DataFrame(
            columns=['artist', 'similar_artist', 'similarity'])

        for artist_id in range(self.base_artist_model.num_artists):
            artist_name = self.base_artist_model.get_artist_name(
                artist_id)

            similar_artists = self.base_artist_model.similar_artists_by_id(
                artist_id, top_n=top_n)

            similar_artists_df = similar_artists_df.append(
                pd.DataFrame({
                    'artist': [artist_name] * top_n,
                    'similar_artist': [s['name'] for s in similar_artists],
                    'similarity': [s['similarity'] for s in similar_artists]}))

        similar_artists_df.to_sql(
            config.ARTIST_SIMILARITY_TABLE.lower(),
            self.db_engine,
            if_exists='replace',
            index=False,
            chunksize=20000)

        return self

    def write_geographic_recommendations_to_snowflake(
            self, top_n_artists=10, top_n_geographies=10):
        """Write geographic recommendations to Snowflake."""
        geographic_recs_df = pd.DataFrame(
            columns=[
                'artist', 'territory', 'store', 'actual_streams',
                'modeled_streams'])

        for artist_id in range(self.base_artist_model.num_artists):
            artist_name = self.base_artist_model.get_artist_name(
                artist_id)

            recommendations = self.geographic_model.geographic_recommendations(
                artist_name, top_n_artists=top_n_artists,
                top_n_geographies=top_n_geographies)
            recommendations = recommendations['recommendations']

            for rec in recommendations:
                stores = [
                    store for store in rec['actual_streams'].keys()
                    if store != 'total']

                geographic_recs_df = geographic_recs_df.append(
                    pd.DataFrame({
                        'artist': [artist_name] * len(stores),
                        'territory': [rec['territory']] * len(stores),
                        'store': stores,
                        'actual_streams': [
                            rec['actual_streams'][store] for store in stores],
                        'modeled_streams': [
                            rec['modeled_streams'][store] for store in stores]
                    }))

        geographic_recs_df.to_sql(
            config.ARTIST_GEOGRAPHIC_RECOMMENDATIONS_TABLE.lower(),
            self.db_engine,
            if_exists='replace',
            index=False,
            chunksize=20000)

        return self

    def _load_model(self):
        """Load model."""
        self.base_artist_model = HistoricalArtistModel()
        self.geographic_model = GeographicArtistModel()
