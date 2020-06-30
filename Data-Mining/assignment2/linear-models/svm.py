import numpy as np
from scipy.optimize import minimize


def svm(X, y):
    '''
    SVM Support vector machine.

    INPUT:  X: training sample features, P-by-N matrix.
            y: training sample labels, 1-by-N row vector.

    OUTPUT: w: learned perceptron parameters, (P+1)-by-1 column vector.
            num: number of support vectors

    '''
    P, N = X.shape
    w = np.zeros((P + 1, 1))
    num = 0

    # YOUR CODE HERE
    # Please implement SVM with scipy.optimize. You should be able to implement
    # it within 20 lines of code. The optimization should converge wtih any method
    # that support constrain.
    X = np.concatenate((np.ones((1, N)), X), axis = 0)
    constains = []
    for i in range(N):
        dic = {'type': 'ineq', 'fun': lambda g, x = X[:, i].reshape(P+1, 1), y = y[0][i]: np.matmul(g.T, x)[0] * y - 1}
        constains.append(dic)
    
    while True:
        answer = minimize(lambda x: x[1:].T * x[1:], np.random.normal(0, 10, 3), method = 'COBYLA', constraints = constains)
        #print (answer)
        if answer.success: break
    w = answer.x
    return w, np.sum([np.abs(np.matmul(w.T, X[:, i].reshape((P+1, 1))) - y[0][i]) <= 1e-4 for i in range(N)])

