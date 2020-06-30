from gaussian_pos_prob import gaussian_pos_prob
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

figure, subfigs = plt.subplots(2, 4, figsize=(16, 8), tight_layout=True, dpi=100,
                               subplot_kw=dict(aspect='auto'))

def plot_ex1(mu0, Sigma0, mu1, Sigma1, phi, fig_title, pos):
    fig = subfigs[(pos - 1) // 4][(pos - 1) % 4]
    fig.cla()
    N = 1000

    # generate data
    X0 = np.random.multivariate_normal(mu0.flatten(), Sigma0, round((1 - phi) * N)).T
    X1 = np.random.multivariate_normal(mu1.flatten(), Sigma1, round(phi * N)).T

    x0 = X0[0, :]
    y0 = X0[1, :]
    x1 = X1[0, :]
    y1 = X1[1, :]

    xmin = min(np.min(x0), np.min(x1))
    xmax = max(np.max(x0), np.max(x1))
    ymin = min(np.min(y0), np.min(y1))
    ymax = max(np.max(y0), np.max(y1))

    step = 0.01  # TODO
    xs, ys = np.meshgrid(np.arange(xmin, xmax + step, step), np.arange(ymin, ymax + step, step))

    xy = np.vstack((xs.flatten(), ys.flatten())).T
    Sigma = np.zeros((2, 2, 2))
    Sigma[:, :, 0] = Sigma0
    Sigma[:, :, 1] = Sigma1
    pos_prob = gaussian_pos_prob(xy.T, np.hstack((mu0, mu1)), Sigma, np.array([1 - phi, phi]))
    pos_prob = pos_prob[:, 0]
    image_size = xs.shape
    decisionmap = ((np.array(pos_prob > 0.5, dtype=float) + 1) * 100).reshape(image_size)
    # class 1 = light red, 2 = light green, 3 = light blue
    cmap = matplotlib.colors.ListedColormap([(1, 0.8, 0.8), (0.95, 1, 0.95), (0.9, 0.9, 1)])
    if np.unique(decisionmap).shape == (1,): # GREEN HACK
        cmap = matplotlib.colors.ListedColormap([(0.95, 1, 0.95)])    
    
    fig.pcolormesh(xs, ys, decisionmap, cmap=cmap, alpha=0.8)

    diff = abs(pos_prob - 0.5)
    diff_sorted = sorted(diff)
    threshold = diff_sorted[len(diff_sorted) // 500]
    bb = xy[diff < threshold, :]
    fig.plot(x0, y0, '.', color='blue', markersize=5)
    fig.plot(x1, y1, '.', color='red', markersize=5)
    fig.plot(bb[:, 0], bb[:, 1], '.', color='black', markersize=5)
    fig.set_title(fig_title)
    fig.set_aspect('equal', adjustable='box')

    