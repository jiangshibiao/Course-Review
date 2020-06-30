import numpy as np

def get_x_distribution(x1, x2, data_range):
    '''
    GET_X_DISTRIBUTION get the number of occurance of each feature in two classes
    INPUT:  x1, features of first class, 1-By-N1 numpy array
            x2, features of second class, 1-By-N2 numpy array
            data_range, contains smallest feature and biggest feature, 1-By-2 numpy array
            N1 is the number of class 1's samples, and N2 is the number of class 2's samples.

    OUTPUT: distribution, the number of occurance of each feature(from smallest feature to biggest feature) in two classes    
    '''
    distribution = np.zeros((2, data_range[1] - data_range[0] + 1))
    distribution[0, np.min(x1) - data_range[0]: np.max(x1) - data_range[0] + 1], _ = np.histogram(x1, np.max(x1) - np.min(x1) + 1)
    distribution[1, np.min(x2) - data_range[0]: np.max(x2) - data_range[0] + 1], _ = np.histogram(x2, np.max(x2) - np.min(x2) + 1)
    return distribution