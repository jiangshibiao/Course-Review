import numpy as np
import matplotlib.pyplot as plt
from pca import PCA

def hack_pca(filename):
    '''
    Input: filename -- input image file name/path
    Output: img -- image without rotation
    '''
    img_r = (plt.imread(filename)).astype(np.float64) # 4 channels: R,G,B,A
    img_gray = img_r[:,:,0] * 0.3 + img_r[:,:,1] * 0.59 + img_r[:,:,2] * 0.11
    
    X_int = np.array(np.where(img_gray > 0))
    X = X_int.astype(np.float64)
    D, N = X.shape

    eigen_vec, eigen_val = PCA(X)
    print (eigen_vec, eigen_val)
    Y = np.matmul(X.T, eigen_vec).T
    
    Y_int = Y.astype(np.int32)
    dmin = np.min(Y_int, axis = 1).reshape(D, 1)
    Y_int = Y_int - dmin
    bound = np.max(Y_int, axis = 1) + 1
    new_img = np.zeros(bound)
    for t in range(Y_int.shape[1]):
        new_img[tuple(Y_int[:, t])] = img_gray[tuple(X_int[:, t])]
    new_img = new_img.T[::-1, ::-1]
    
    return new_img