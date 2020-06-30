import numpy as np

import knn
import show_image
import extract_image

def hack(img_name):
    '''
    HACK Recognize a CAPTCHA image
      Inputs:
          img_name: filename of image
      Outputs:
          digits: 1x5 matrix, 5 digits in the input CAPTCHA image.
    '''
    data = np.load('hack_data.npz')
    x = extract_image.extract_image(img_name)

    # YOUR CODE HERE (you can delete the following code as you wish)
    x_train = data['x_train']
    y_train = data['y_train']
    number = len(x_train)

    # begin answer
    x_train, x_valid = x_train[ : number // 2], x_train[number // 2:]
    y_train, y_valid = y_train[ : number // 2], y_train[number // 2:]
    
    best_acc, best_k = 0.0, 1
    for k in range(1, 101):
        y = knn.knn(x_valid, x_train, y_train, k)
        acc = np.sum(y == y_valid) / len(y)
        print ("K =", k, " ACC =", acc)
        if acc > best_acc:
            best_acc = acc
            best_k = k
    print ("Choose", best_k, "as K.")
    digits = knn.knn(x, x_train, y_train, best_k)
    # end answer
    return digits
