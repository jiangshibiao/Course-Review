import numpy as np
import matplotlib.pyplot as plt

import knn


def knn_plot(x, y, k):

    plt.figure(figsize=(10, 10))

    color = ['red', 'blue']

    for label in np.unique(y):
        p = x[y == label]
        plt.scatter(p[:, 0], p[:, 1], s=3, c=color[label])

    xmin = np.min(x[:, 0])
    xmax = np.max(x[:, 0])
    ymin = np.min(x[:, 1])
    ymax = np.max(x[:, 1])
    step = 0.05
    mesh = np.meshgrid(np.arange(xmin, xmax + step, step), np.arange(ymin, ymax + step, step))
    mesh_f = np.vstack((mesh[0].flatten(), mesh[1].flatten())).T

    classes = knn.knn(mesh_f, x, y, k).reshape(mesh[0].shape)
    plt.contour(mesh[0], mesh[1], classes, levels=2)
    ti = 'K = {}'.format(k)
    plt.title(ti)
