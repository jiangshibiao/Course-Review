import numpy as np

def h(theta, x):
    return 1.0 / (1 + np.exp(-np.squeeze(np.matmul(theta.T, x))))


def logistic(X, y):
    '''
    LR Logistic Regression.

    INPUT:  X: training sample features, P-by-N matrix.
            y: training sample labels, 1-by-N row vector.

    OUTPUT: w: learned parameters, (P+1)-by-1 column vector.
    '''
    P, N = X.shape
    w = np.zeros((P + 1, 1))
    X = np.concatenate((np.ones((1, N)), X), axis = 0)
    y = np.array(y == 1, dtype = np.float).reshape(N)
    # YOUR CODE HERE
    # begin answer
    step = 0
    maxstep = 100
    learning_rate = 1
    smaller = 0.99
    while step < maxstep:
        loss = - sum(np.log(h(w, X[:, y == 1]))) - sum(np.log(1 - h(w, X[:, y == 0])))
        grad = np.matmul(X, (h(w, X) - y).reshape((N, 1)))
        learning_rate *= smaller
        w = w - learning_rate * grad
        step += 1
    # end answer
    
    return w, loss
