"""Train the model."""

import pickle

import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.mixture import BayesianGaussianMixture
from sklearn.preprocessing import Normalizer

from artist_listener_models import config
from artist_listener_models import utils
from artist_listener_models.database.utils import load_table


def main():
    """Train model."""
    artist_user_streams = load_table(config.ARTIST_USER_STREAMS_TABLE)

    # take log of streams
    artist_user_streams['log_total_streams'] = np.log(
        artist_user_streams['total_streams'])

    # cast to sparse matrix
    sparse_mat = utils.cast_to_sparse_matrix(
        artist_user_streams, var='log_total_streams')

    # project to lower-dimensional space
    svd = TruncatedSVD(
        n_components=config.NUM_FEATURES, random_state=config.RANDOM_STATE)
    lower_dim_data = svd.fit_transform(sparse_mat)

    # normalize using L2
    artist_user_features = Normalizer().transform(lower_dim_data)

    # cluster
    gmm = BayesianGaussianMixture(
        n_components=config.NUM_CLUSTERS, random_state=config.RANDOM_STATE)
    clusters = gmm.fit_predict(artist_user_features)

    # save data products
    pickle.dump({
        'projected': lower_dim_data,
        'normalized': artist_user_features,
        'clusters': clusters},
        open(config.OUTPUT_FILE, 'wb'))
