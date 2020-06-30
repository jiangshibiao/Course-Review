import numpy as np
from numpy.linalg import svd

def nullspace(A, atol=1e-13, rtol=0):
    A = np.atleast_2d(A)
    u, s, vh = svd(A)
    tol = max(atol, rtol * s[0])
    nnz = (s >= tol).sum()
    ns = vh[nnz:].conj().T
    return ns

def mkdata(N, noisy=None):
    '''
    MKDATA Generate data set.
    INPUT:  N:     number of samples.
            noisy: if or not add noise to y.
    
    OUTPUT: X: sample features, P-by-N matrix.
            y: sample labels, 1-by-N row vector.
            w: target function parameters, (P+1)-by-1 column vector.
    '''
    data_range = np.array([-1, 1])
    dim = 2

    X = np.random.random((dim, N)) * (data_range[1] - data_range[0]) + data_range[0]
    while True:
        Xsample = np.vstack((np.ones((1, dim)), np.random.random((dim, dim)) * (data_range[1]-data_range[0]) + data_range[0]))
        w = nullspace(Xsample.T)
        a =  np.vstack((np.ones((1, N)), X))
        y = np.sign(np.matmul(w.T, np.vstack((np.ones((1, N)), X))))
        if np.all(y) and np.unique(y).shape[0] > 1:
            break
    if noisy:
        idx = np.random.choice(N, N//10)
        y[0, idx] = -y[0, idx]

    return X, y, w

