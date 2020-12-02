"""Base artist model."""

import pickle

import numpy as np

from artist_listener_models import config
from artist_listener_models.database.utils import load_table


class HistoricalArtistModel(object):
    """Artist model for artists in training set."""

    def __init__(self):
        """Artist model constructor."""
        self._load_model()

    def similar_artists(self, artist_name, top_n=10):
        """Get similar artists.

        The artist must be in the training set.

        Args:
            artist_name (str): Artist name in all lowercase
            top_n (int || 10): Number of similar artists to retrieve

        Returns:
            Dictionary with keys artist_names, artist_ids,
            and artist_similarities.

        """
        return self.similar_artists_by_id(
            self.get_artist_id(artist_name))

    def similar_artists_by_id(self, artist_id, top_n=10):
        """Get similar artists by ID.

        The artist must be in the training set.

        Args:
            artist_id (int): Zero-based artist ID
            top_n (int || 10): Number of similar artists to retrieve

        Returns:
            Dictionary with keys artist_names, artist_ids,
            and artist_similarities.

        """
        # get other artists in same cluster, excluding current artist
        artist_ids_in_cluster = np.nonzero(
            self.clusters == self.clusters[artist_id])[0]
        artist_ids_in_cluster = artist_ids_in_cluster[
            artist_ids_in_cluster != artist_id]

        # get similarity
        similarity = self._get_similarity(
            self.user_features[artist_id],
            self.user_features[artist_ids_in_cluster])

        # get top artists
        top_artists_in_cluster = (-similarity).argsort()[:top_n]
        top_artist_ids = artist_ids_in_cluster[top_artists_in_cluster]

        # get top similarities
        top_artist_similarity = similarity[top_artists_in_cluster]

        return [{
            'name': self.get_artist_name(aid),
            'id': int(aid),
            'similarity': similarity
        } for aid, similarity in zip(top_artist_ids, top_artist_similarity)]

    def get_artist_id(self, artist_name):
        """Get zero-based artist ID from name."""
        return self.artist_metadata[
            self.artist_metadata.artistname == artist_name].index[0]

    def get_artist_name(self, artist_id):
        """Get artist name from ID."""
        return self.artist_metadata.loc[artist_id].artistname

    @property
    def num_artists(self):
        """Get number of artists."""
        return len(self.artist_metadata)

    @property
    def num_clusters(self):
        """Get number of clusters."""
        return self.clusters.max() - self.clusters.min() + 1

    def _load_model(self):
        """Load model."""
        model_data = pickle.load(open(config.OUTPUT_FILE, 'rb'))
        self.user_features = model_data['normalized']
        self.clusters = model_data['clusters']

        self.artist_metadata = load_table(
            config.ARTIST_METADATA_TABLE, index_col='artistnum')

    def _get_similarity(self, artist_features, group_artist_features):
        """Get similarity using specified method."""
        if config.SIMILARITY_METRIC == 'cosine':
            # this assumes features are normalized
            similarity = group_artist_features.dot(artist_features)
            return 0.5 * (similarity + 1)  # transform to range [0, 1]
        elif config.SIMILARITY_METRIC == 'euclidean':
            return 1 / np.linalg.norm(
                group_artist_features - artist_features, axis=1)
        else:
            raise Exception('Unrecognized similarity metric')
