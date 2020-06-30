import numpy as np
import math

def Normal(x, mu, det, inv):
    #x = x.reshape((x.shape[0], 1))
    #mu = mu.reshape((mu.shape[0], 1))
    #print ((x-mu),(x-mu).shape)
    #print ((x-mu).T,(x-mu).T.shape)
    #print (x, x.shape, det, (x-mu).T)
    return 1/(2 * math.pi * abs(det)**0.5) * math.exp(np.matmul(np.matmul((x-mu).T, inv), (x - mu)) * (-0.5))

def gaussian_pos_prob(X, Mu, Sigma, Phi):
    '''
    GAUSSIAN_POS_PROB Posterior probability of GDA.
    Compute the posterior probability of given N data points X
    using Gaussian Discriminant Analysis where the K gaussian distributions
    are specified by Mu, Sigma and Phi.
    Inputs:
        'X'     - M-by-N numpy array, N data points of dimension M.
        'Mu'    - M-by-K numpy array, mean of K Gaussian distributions.
        'Sigma' - M-by-M-by-K  numpy array (yes, a 3D matrix), variance matrix of
                  K Gaussian distributions.
        'Phi'   - K-by-1  numpy array, prior of K Gaussian distributions.
    Outputs:
        'p'     - N-by-K  numpy array, posterior probability of N data points
                with in K Gaussian distribsubplots_adjustutions.
    ''' 
    N = X.shape[1]
    K = Phi.shape[0]
    p = np.zeros((N, K))
    #Your code HERE
    
    det = np.array([np.linalg.det(Sigma[:,:,j]) for j in range(K)])
    inv = np.array([np.linalg.inv(Sigma[:,:,j]) for j in range(K)])

    # begin answer
    
    
    for i in range(N):
        p_x = 0
        p_x_w = []
        for j in range(K):
            p_x_w.append(Normal(X[:,i], Mu[:,j], det[j], inv[j]))
            p_x += Phi[j] * p_x_w[j]
        for j in range(K):
            p[i][j] = p_x_w[j] * Phi[j] / p_x
    
    # end answer
    
    return p
    