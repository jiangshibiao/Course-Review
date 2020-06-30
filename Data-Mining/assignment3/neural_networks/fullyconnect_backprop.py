import numpy as np

def fullyconnect_backprop(in_sensitivity, in_, weight):
    '''
    The backpropagation process of fullyconnect
      input parameter:
          in_sensitivity  : the sensitivity from the upper layer, shape: 
                          : [number of images, number of outputs in feedforward]
          in_             : the input in feedforward process, shape: 
                          : [number of images, number of inputs in feedforward]
          weight          : the weight matrix of this layer, shape: 
                          : [number of inputs in feedforward, number of outputs in feedforward]

      output parameter:
          weight_grad     : the gradient of the weights, shape: 
                          : [number of inputs in feedforward, number of outputs in feedforward]
          bias_grad       : the gradient of the bias, shape: 
                          : [number of outputs in feedforward, 1]
          out_sensitivity : the sensitivity to the lower layer, shape: 
                          : [number of images, number of inputs in feedforward]

    Note : remember to divide by number of images in the calculation of gradients.
    '''
    input_size, output_size = weight.shape
    image_size = in_.shape[0]
    # begin answer
    bias_grad = np.mean(in_sensitivity, axis = 0).reshape(output_size, 1)
    # out[i][k] = in_[i][j] * w[j][k] + bias[i][k]
    # j,k: in_[i][j] * ans[i][k]
    weight_grad = np.matmul(in_.T, in_sensitivity) / image_size
    out_sensitivity = np.matmul(in_sensitivity, weight.T)
    # end answer

    return weight_grad, bias_grad, out_sensitivity

