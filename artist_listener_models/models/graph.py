"""Graph artist model."""

import numpy as np

from artist_listener_models.database import utils as db_utils
from artist_listener_models.models.base import HistoricalArtistModel


class HistoricalArtistGraphModel(object):
    """Graph artist model for artists in training set."""

    def __init__(self):
        """Graph artist model constructor."""
        self._load_model()

        # make graph connection
        # TODO: put this in a context manager
        self.graph = db_utils.connect_to_graph_db()

    def write_to_neo4j(self):
        """Write model of artists, clusters, and similarities to neo4j."""
        for cluster in range(self.num_clusters):
            # create cluster node
            self._create_cluster_node(cluster)

            # add artist nodes
            self._add_artist_nodes(cluster)

            # add similarity relationships
            self._add_similarity_relationships(cluster)

    @property
    def num_clusters(self):
        """Get number of clusters."""
        return self.base_artist_model.num_clusters

    @property
    def clusters(self):
        """Get clusters."""
        return self.base_artist_model.clusters

    @property
    def artist_metadata(self):
        """Get artist metadata."""
        return self.base_artist_model.artist_metadata

    def _load_model(self):
        """Load model."""
        self.base_artist_model = HistoricalArtistModel()

    def _add_artist_nodes(self, cluster_id):
        """Add artist nodes for cluster to graph."""
        artist_ids = np.nonzero(self.clusters == cluster_id)[0]

        for artist_id in artist_ids:
            artist = self.artist_metadata.loc[artist_id]
            self._create_artist_node(
                cluster_id, artist_id, artist.genreid,
                artist.artistname, artist.countrylist)

    def _add_similarity_relationships(self, cluster_id):
        """Add similarity relationships for cluster to graph."""
        artist_ids = np.nonzero(self.clusters == cluster_id)[0]

        for artist_id in artist_ids:
            artist = self.artist_metadata.loc[artist_id]

            similar_artists = self.base_artist_model.similar_artists_by_id(
                artist_id)
            similar_artist_ids = [s['id'] for s in similar_artists]

            for similar_artist_id in similar_artist_ids:
                similar_artist = self.artist_metadata.loc[
                    similar_artist_id]
                self._create_similarity_edge(
                    artist_id, artist.genreid, similar_artist_id,
                    similar_artist.genreid)

    def _create_cluster_node(self, cluster_id):
        """Create cluster node in graph."""
        self.graph.run(
            'CREATE (:Cluster {{id: {}}})'.format(cluster_id))

    def _create_artist_node(
            self, cluster_id, artist_id, genre_id, name, countries):
        """Create artist node in graph."""
        query = """
            MATCH (cl:Cluster) WHERE cl.id = {}
            CREATE (ar:ArtistGenre{} {{
                id: {},
                name: "{}",
                countries: "{}"
            }}),
            (ar)-[:IN]->(cl)
        """

        query = query.format(
            cluster_id, genre_id, artist_id,
            *(self._replace_double_quotes(s) for s in [name, countries]))
        self.graph.run(query)

    def _create_similarity_edge(
            self, artist_id1, genre_id1, artist_id2, genre_id2):
        """Create similarity edge in graph."""
        query = """
            MATCH (ar1:ArtistGenre{}) WHERE ar1.id = {}
            MATCH (ar2:ArtistGenre{}) WHERE ar2.id = {}
            MERGE (ar1)-[:SIMILAR_TO]->(ar2)
        """

        query = query.format(
            genre_id1, artist_id1, genre_id2, artist_id2)
        self.graph.run(query)

    def _replace_double_quotes(self, string):
        """Replace double with single quotes."""
        return string.replace('"', '\'')
