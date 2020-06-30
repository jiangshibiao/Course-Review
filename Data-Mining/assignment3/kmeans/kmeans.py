import numpy as np


def kmeans(x, k):
    '''
    KMEANS K-Means clustering algorithm

        Input:  x - data point features, n-by-p maxtirx.
                k - the number of clusters

        OUTPUT: idx  - cluster label
                ctrs - cluster centers, K-by-p matrix.
                iter_ctrs - cluster centers of each iteration, (iter, k, p)
                        3D matrix.
    '''
    # YOUR CODE HERE
    N = x.shape[0]
    p = x.shape[1]

    # begin answer
    iter_max = 10
    iter_ctrs = np.zeros((iter_max, k, p))
    ctrs = x[np.random.choice(np.arange(0, N), k, replace = False)]
    iter_ctrs[0] = ctrs
    last_idx = np.zeros(N)
    xx = np.tile(np.sum(x ** 2, axis = 1), (k, 1)).T
    #print (xx[np.isnan(xx)], ctrs[np.isnan(ctrs)])
    for i in range(1, iter_max):
        xy = np.matmul(x, ctrs.T)
        yy = np.tile(np.sum(ctrs ** 2, axis = 1), (N, 1))
        #print (xx[np.isnan(xx)], yy[np.isnan(yy)])
        dxy =  xx + yy - 2 * xy
        
        idx = np.argmin(dxy, axis = 1)
        #print (dxy[np.isnan(dxy)], idx[np.isnan(idx)])
        if (idx == last_idx).all():
            iter_ctrs = iter_ctrs[0: i]
            break
        last_idx = idx
        for j in range(k):
            if np.sum(idx == j) > 0:
                ctrs[j] = np.mean(x[idx == j], axis = 0)
        #print (ctrs)
        iter_ctrs[i] = ctrs
    # end answer

    #print (idx.shape, ctrs.shape, iter_ctrs.shape)
    return idx, ctrs, iter_ctrs
