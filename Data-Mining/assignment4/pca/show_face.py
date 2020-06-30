import numpy as np
import matplotlib.pyplot as plt


def show_face(fea):
    '''
    Input: fea -- face image dataset. Each 1x1024 row vector of fea is a data point.
    '''
    faceW = 32
    faceH = 32

    numPerLine = 20
    ShowLine = 2
    fea = fea[:40, :]
    if fea.shape[0] < 40:
        fea = np.concatenate((fea, np.zeros((40 - fea.shape[0], fea.shape[1]))), axis=0)
    Y = np.zeros((faceH * ShowLine, faceW * numPerLine))
    for i in range(ShowLine):
        for j in range(numPerLine):
            Y[i * faceH:(i + 1) * faceH, j * faceW:(j + 1) * faceW]\
                = fea[i * numPerLine + j, :].reshape((faceH, faceW)).transpose()

    plt.figure(figsize=(20, 20))
    plt.axis('off')
    plt.imshow(Y, cmap='gray')
    plt.show()
