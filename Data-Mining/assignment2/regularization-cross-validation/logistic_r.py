import numpy as np

def h(theta, x):
    return 1.0 / (1 + np.exp(-np.squeeze(np.matmul(theta.T, x))))

def logistic_r(X, y, lmbda):
    '''
    LR Logistic Regression.

      INPUT:  X:   training sample features, P-by-N matrix.
              y:   training sample labels, 1-by-N row vector.
              lmbda: regularization parameter.

      OUTPUT: w    : learned parameters, (P+1)-by-1 column vector.
    '''
    P, N = X.shape
    w = np.zeros((P + 1, 1))
    X = np.concatenate((np.ones((1, N)), X), axis = 0)
    y = np.array(y == 1, dtype = np.float).reshape(N)
    # YOUR CODE HERE
    # begin answer
    step = 0
    maxstep = 100
    learning_rate = 0.001
    smaller = 1
    while step < maxstep:
        regular = w * lmbda
        regular[0] = 0
        grad = np.matmul(X, (h(w, X) - y).reshape((N, 1))) + regular
        learning_rate *= smaller
        #print (learning_rate, np.linalg.norm(w), np.linalg.norm(grad))
        w = w - learning_rate * grad
        
        step += 1
    # end answer
    return w
