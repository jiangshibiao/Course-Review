import numpy as np
from kmeans import kmeans

def spectral(W, k):
    '''
    SPECTRUAL spectral clustering

        Input:
            W: Adjacency matrix, N-by-N matrix
            k: number of clusters

        Output:
            idx: data point cluster labels, n-by-1 vector.
    '''
    # YOUR CODE HERE
    # begin answer
    n = W.shape[0]
    D = np.zeros((n, n))
    for i in range(n):
        D[i][i] = np.sum(W[i])
    eigen, vec = np.linalg.eig(D-W)
    choose = vec[:, np.argsort(eigen)[:k]]
    return kmeans(choose, k)
    # end answer
