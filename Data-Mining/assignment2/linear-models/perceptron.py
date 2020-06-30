import numpy as np

def perceptron(X, y):
    '''
    PERCEPTRON Perceptron Learning Algorithm.

       INPUT:  X: training sample features, P-by-N matrix.
               y: training sample labels, 1-by-N row vector.

       OUTPUT: w:    learned perceptron parameters, (P+1)-by-1 column vector.
               iter: number of iterations

    '''
    P, N = X.shape
    w = np.zeros((P + 1, 1))
    iters = 0
    # YOUR CODE HERE
    
    # begin answer
    learning_rate = 0.01
    while True:
        iters += 1
        ok_edges = 0
        for i in range(N):
            newx = np.concatenate(([1], X[:, i]))
            res = y[0][i] * np.matmul(newx, w)[0]
            if res > 0:
                ok_edges += 1
            else:
                w[:, 0] = w[:, 0] + learning_rate * y[0][i] * newx
        if ok_edges == N:
            break
        #print (ok_edges)
    # end answer
    
    return w, iters