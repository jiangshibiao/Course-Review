import numpy as np
import matplotlib.pyplot as plt


def kmeans_plot(x, idx, ctrs, iter_ctrs):
    """
    Input:  x - data point features, n-by-p maxtirx.
            idx  - cluster label
            ctrs - cluster centers, K-by-p matrix.
            iter_ctrs - cluster centers of each iteration, (iter, k, p)
                        3D matrix.
    """
    plt.figure(figsize=(10, 10))

    color = ['red', 'blue']
    fmt = ['rs-', 'bo-']
    for label in np.unique(idx):
        plt.scatter(x[idx == label, 0], x[idx == label, 1], s=3, c=color[label])
        plt.plot(iter_ctrs[:, label, 0], iter_ctrs[:, label, 1],
                 fmt[label], linewidth=2, markersize=5)
