"""Geographic artist model."""

from artist_listener_models import config
from artist_listener_models.database.utils import load_table
from artist_listener_models.models.base import HistoricalArtistModel


class GeographicArtistModel(object):
    """Artist model for producing geographic insights."""

    def __init__(self):
        """Geographic model constructor."""
        self._load_model()

    def geographic_recommendations(
            self, artist_name, top_n_artists=10, top_n_geographies=10):
        """Get geographic recommendations.

        The artist must be in the training set.

        Args:
            artist_name (str): Artist name in all lowercase
            top_n_artists (int || 10): Number of similar artists to use
            top_n_geographies (int || 10): Number of geographies to retrieve

        Returns:
            Dictionary with keys top_markets and recommendations.

        """
        artist_streams = self._get_artist_streams(artist_name)
        artist_country_streams = self._agg_sort_country_streams(
            artist_streams)

        # get expected streams
        expected_streams = self._get_expected_streams(
            artist_name, top_n=top_n_artists)
        expected_country_streams = self._agg_sort_country_streams(
            expected_streams)

        # get top markets
        top_markets = []
        for country in artist_country_streams.index[:top_n_geographies]:
            actual_streams = artist_streams.loc[country][
                'total_streams'].to_dict()

            modeled_streams = {}
            if country in expected_streams.index:
                modeled_streams = expected_streams.loc[country][
                    'total_streams'].to_dict()
                expected_country_streams.drop(country, inplace=True)

            self._harmonize_stores(actual_streams, modeled_streams)
            self._add_total_streams(actual_streams)
            self._add_total_streams(modeled_streams)

            top_markets.append({
                'territory': country,
                'actual_streams': actual_streams,
                'modeled_streams': modeled_streams})

        # get recommendations
        recommendations = []
        for country in expected_country_streams.index[:top_n_geographies]:
            modeled_streams = expected_streams.loc[country][
                'total_streams'].to_dict()

            actual_streams = {}
            if country in artist_streams.index:
                actual_streams = artist_streams.loc[country][
                    'total_streams'].to_dict()

            self._harmonize_stores(actual_streams, modeled_streams)
            self._add_total_streams(actual_streams)
            self._add_total_streams(modeled_streams)

            recommendations.append({
                'territory': country,
                'actual_streams': actual_streams,
                'modeled_streams': modeled_streams})

        return {
            'top_markets': top_markets,
            'recommendations': recommendations}

    @property
    def num_countries(self):
        """Get number of countries."""
        return len(self.country_metadata)

    def _load_model(self):
        """Load model."""
        self.base_artist_model = HistoricalArtistModel()
        self.artist_country_streams = load_table(
            config.ARTIST_COUNTRY_STREAMS_TABLE, index_col='artistnum')

    def _get_expected_streams(self, artist_name, top_n=10):
        """Get expected streams for artist based on similar artists."""
        similar_artists = self.base_artist_model.similar_artists(
            artist_name, top_n=top_n)

        # average streams over similar artists
        sum_similarity = 0
        for i in range(top_n):
            artist_id = similar_artists[i]['id']
            artist_similarity = similar_artists[i]['similarity']

            similar_artist_streams = self._get_artist_streams_by_id(
                artist_id)
            similar_artist_streams['total_streams'] *= artist_similarity

            if i == 0:
                expected_country_streams = similar_artist_streams
            else:
                expected_country_streams = expected_country_streams.add(
                    similar_artist_streams, fill_value=0)

            sum_similarity += artist_similarity

        expected_country_streams['total_streams'] /= sum_similarity
        expected_country_streams['total_streams'] = \
            expected_country_streams['total_streams'].apply(int)

        return expected_country_streams

    def _get_artist_streams(self, artist_name):
        """Get artist streams."""
        artist_id = self.base_artist_model.get_artist_id(artist_name)
        return self._get_artist_streams_by_id(artist_id)

    def _get_artist_streams_by_id(self, artist_id):
        """Get artist streams by ID."""
        return self.artist_country_streams.loc[artist_id].drop(
            'artistname', axis=1).set_index(['countryname', 'storename'])

    def _agg_sort_country_streams(self, streams_df):
        """Aggregate streams by country and sort in descending order."""
        return streams_df.sum(level='countryname').sort_values(
            'total_streams', ascending=False)

    def _harmonize_stores(self, actual_streams, modeled_steams):
        """Harmonize stores between actual and modeled streams."""
        for key in list(modeled_steams.keys()):
            if key not in actual_streams:
                del modeled_steams[key]
        for key in actual_streams:
            if key not in modeled_steams:
                modeled_steams[key] = None

    def _add_total_streams(self, streams_dict):
        """Add key-value pair for total streams."""
        streams_dict['total'] = sum(
            v for v in streams_dict.values() if v is not None)
