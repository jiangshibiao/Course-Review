import numpy as np
from likelihood import likelihood

def posterior(x):
    '''
    POSTERIOR Two Class Posterior Using Bayes Formula
    INPUT:  x, features of different class, C-By-N vector
            C is the number of classes, N is the number of different feature
    OUTPUT: p,  posterior of each class given by each feature, C-By-N matrix
    '''

    C, N = x.shape
    l = likelihood(x)
    total = np.sum(x)
    p = np.zeros((C, N))
    #TODO

    # begin answer
    for j in range(N):
        P_x = np.sum(x[:, j]) / total
        for i in range(C):
            P_i = np.sum(x[i, :]) / total
            p[i][j] = l[i][j] * P_i / P_x
    # end answer
    
    return p
