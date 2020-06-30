import numpy as np

def linear_regression(X, y):
    '''
    LINEAR_REGRESSION Linear Regression.

    INPUT:  X: training sample features, P-by-N matrix.
            y: training sample labels, 1-by-N row vector.

    OUTPUT: w: learned perceptron parameters, (P+1)-by-1 column vector.
    '''
    P, N = X.shape
    w = np.zeros((P + 1, 1))
    # YOUR CODE HERE
    # begin answer
    
    # minimize (X^T * w - y^T)^T * (X^T * w - y^T)
    # partial = 0:  w = (XX^T)^-1 XY^T
    
    
    X = np.concatenate((np.ones((1, N)), np.array(X)), axis = 0)
    inv = np.linalg.inv(np.matmul(X, X.T))
    w = np.matmul(np.matmul(inv, X), y.T)
    # end answer
    return w
