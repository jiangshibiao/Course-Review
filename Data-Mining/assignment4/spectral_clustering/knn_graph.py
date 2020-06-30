import numpy as np

def knn_graph(X, k, threshold):
    '''
    KNN_GRAPH Construct W using KNN graph

        Input:
            X - data point features, n-by-p maxtirx.
            k - number of nn.
            threshold - distance threshold.

        Output:
            W - adjacency matrix, n-by-n matrix.
    '''

    # YOUR CODE HERE
    n, p = X.shape
    # begin answer
    xx = np.tile(np.sum(X ** 2, axis = 1), (n, 1)).T
    #print (X, xx)
    yy = xx.T
    xy = np.matmul(X, X.T)
    #print (xx.shape, xy.shape, yy.shape)
    
    
    dist = xx + yy - 2 * xy
    #print (xx[0][0], xy[0][0])
    #print (dist[0][0])
    #print (dist[0][1], np.sum((X[0]-X[1])**2))
    distid = np.argsort(dist)[:, 1:k+1]
    
    W = np.zeros((n, n))
    for i in range(n):
        small_index = dist[i][distid[i]] <= threshold
        W[i][distid[i][small_index]] = 1
    
    return W
    # end answer
