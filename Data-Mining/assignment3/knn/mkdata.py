import numpy as np


def mkdata():
    n1 = 200
    n2 = 200  # Class sizes
    x = np.vstack((np.random.randn(n1, 2), np.random.randn(n2, 2) + 2))
    y = np.hstack((np.array([0] * n1), np.array([1] * n2)))
    return x, y

