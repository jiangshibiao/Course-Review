import numpy as np

def normal(X):
    return (X - np.average(X, axis = 1).reshape(X.shape[0], 1))

def PCA(data):
    '''
    PCA	Principal Component Analysis

    Input:
      data      - Data numpy array. Each row vector of fea is a data point.
    Output:
      eigvector - Each column is an embedding function, for a new
                  data point (row vector) x,  y = x*eigvector
                  will be the embedding result of x.
      eigvalue  - The sorted eigvalue of PCA eigen-problem.
    '''

    # YOUR CODE HERE
    # Hint: you may need to normalize the data before applying PCA
    # begin answer
    D, N = data.shape
    X = normal(data)
    S = np.matmul(X, X.T) / N
    eigen_val, eigen_vec = np.linalg.eig(S)
    idx = np.argsort(eigen_val)[::-1]
    eigen_val = eigen_val[idx]
    eigen_vec = eigen_vec[:, idx]
    return eigen_vec, eigen_val

    # end answer