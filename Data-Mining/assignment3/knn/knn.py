import numpy as np
import scipy.stats

def distance(x, y):
    return np.sum((x - y) ** 2)


def knn(x, x_train, y_train, k):
    '''
    KNN k-Nearest Neighbors Algorithm.

        INPUT:  x:         testing sample features, (N_test, P) matrix.
                x_train:   training sample features, (N, P) matrix.
                y_train:   training sample labels, (N, ) column vector.
                k:         the k in k-Nearest Neighbors

        OUTPUT: y    : predicted labels, (N_test, ) column vector.
    '''

    # Warning: uint8 matrix multiply uint8 matrix may cause overflow, take care
    # Hint: You may find numpy.argsort & scipy.stats.mode helpful

    # YOUR CODE HERE
    # begin answer
    '''ret = []
    for x_ask in x:
        neighbors = np.argsort([distance(x, x_train_example) for x_train_example in x_train])[:k]
        label_dict = {}
        for nei in neighbors:
            label_dict[y_train[nei]] = label_dict.get(y_train[nei], 0) + 1
        ret.append(max(label_dict, key = label_dict.get))'''
    # The above solution is too slow
    
    xy = np.matmul(x, x_train.T)
    xx = np.tile(np.sum(x ** 2, axis = 1), (x_train.shape[0], 1)).T
    yy = np.tile(np.sum(x_train ** 2, axis = 1), (x.shape[0], 1))
    #print (xy.shape, x.shape, xx.shape, x_train.shape, yy.shape)
    dxy = xx + yy - 2 * xy
    
    lbs = y_train[np.argsort(dxy, axis = 1)[:, :k]]
    ret = scipy.stats.mode(lbs, axis = 1)[0].flatten()
    # end answer

    return ret
