import numpy as np

def bestMap(L1,L2):
    '''
    bestmap: permute labels of L2 to match L1 as good as possible

        INPUT:  
            L1: labels of L1, shape of (N,) vector
            L2: labels of L2, shape of (N,) vector

        OUTPUT:
            new_L2: best matched permuted L2, shape of (N,) vector
    version 1.0 --December/2018
    Modified from bestMap.m (written by Deng Cai)
    '''

    if L1.shape[0] != L2.shape[0] or len(L1.shape) > 1 or len(L2.shape) > 1: 
        raise Exception('L1 shape must equal L2 shape')
        return 

    Label1 = np.unique(L1)
    nClass1 = Label1.shape[0]
    Label2 = np.unique(L2)
    nClass2 = Label2.shape[0]
    nClass = max(nClass1,nClass2)
    G = np.zeros((nClass, nClass))
    for i in range(nClass1):
        for j in range(nClass2):
            G[j,i] = np.sum((np.logical_and(L1 == Label1[i], L2 == Label2[j])).astype(np.int64))
    from scipy.optimize import linear_sum_assignment
    c,t = linear_sum_assignment(-G)
    newL2 = np.zeros(L2.shape)
    for i in range(nClass2):
        newL2[L2 == Label2[i]] = Label1[t[i]]
    return newL2
