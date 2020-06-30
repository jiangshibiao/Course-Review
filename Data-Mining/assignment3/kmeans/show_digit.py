import numpy as np
import matplotlib.pyplot as plt

def show_digit(x):
    """
    Inputs:
        x: cluster center matrix (k, p), returned by kmeans.
    """

    w = 20
    h = 20
    col = 10
    row = (x.shape[0] + col - 1) // col
    plt.figure(figsize=(10, 10))
    padding = row * col - x.shape[0]
    if padding:
        print(x.shape, padding)
        x = np.vstack((x, np.zeros((padding, x.shape[1]))))
    x = x.reshape(row, col, w, h).transpose(0, 3, 1, 2).reshape(row * h, col * w )
    plt.imshow(x, cmap='gray')
