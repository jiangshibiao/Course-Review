import numpy as np
import imageio
def extract_image(image_file_name):
    '''
    EXTRACT_IMAGE Extract features from image
      Inputs:
          image_file_name: filename of image
      Outputs:
          x: 4x144 matrix, 4 digits in an image, each digit is a (144, 1) column vector.
    '''
    # m = imread(image_file_name)
    m = imageio.imread(image_file_name, pilmode='L')
    d1 = m[0:12, 0:12].reshape(144)
    d2 = m[0:12, 12:24].reshape(144)
    d3 = m[0:12, 24:36].reshape(144)
    d4 = m[0:12, 36:48].reshape(144)
    x = np.vstack((d1, d2, d3, d4))
    return x
