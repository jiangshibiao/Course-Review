import matplotlib.pyplot as plt


def show_image(x):
    """
    Inputs:
        x: (N, 144) matrix, N digits in an image, each digit is a (144, ) column vector.
    """
    num = x.shape[0]
    x = x.reshape(num, 12, 12).transpose(1, 0, 2).reshape(12, num * 12)
    plt.imshow(x, cmap='gray')
