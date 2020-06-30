import numpy as np


def kmeans(x, k):
    '''
    A Fast implementation of K-Means clustering algorithm

        Input:  x - data point features, n-by-p maxtirx.
                k - the number of clusters

        OUTPUT: idx  - cluster label
    '''

    x = x.astype(float)
    n = x.shape[0]
    ctrs = x[np.random.permutation(x.shape[0])[:k]]
    iter_ctrs = [ctrs]
    idx = np.ones(n)
    x_square = np.expand_dims(np.sum(np.multiply(x, x), axis=1), 1)

    while True:
        distance = -2 * np.matmul(x, ctrs.T)
        distance += x_square
        distance += np.expand_dims(np.sum(ctrs * ctrs, axis=1), 0)
        new_idx = distance.argmin(axis=1)
        if (new_idx == idx).all():
            break
        idx = new_idx
        ctrs = np.zeros(ctrs.shape)
        for i in range(k):
            ctrs[i] = np.average(x[idx == i], axis=0)
        iter_ctrs.append(ctrs)
    iter_ctrs = np.array(iter_ctrs)

    return idx
