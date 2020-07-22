import numpy as np
from sklearn import cluster, datasets
from sklearn.preprocessing import StandardScaler


def dendrogram_permutation(algorithm):
    """
    Calculate permutation of data points for dendrogram
    """
    sorting_permutation = np.argsort(algorithm.labels_)
    return sorting_permutation
