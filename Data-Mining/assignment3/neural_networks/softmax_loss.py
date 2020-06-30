import numpy as np

def softmax_loss(in_, label):
    '''
    The softmax loss computing process
      inputs:
          in_     : the output of previous layer, shape: [number of images, number of kinds of labels]
          label   : the ground true of these images, shape: [1, number of images]

      outputs
          loss    : the average loss, scale variable
          accuracy: the accuracy of the classification
          sentivity     : the sentivity for in, shape: [number of images, number of kinds of labels]
    '''
    n, k = in_.shape
    in_ = in_ - np.tile(np.max(in_, axis=1, keepdims=True), (1, k))
    h = np.exp(in_)
    total = np.sum(h, axis=1, keepdims=True)
    probs = h / np.tile(total, k)
    idx = (np.arange(n), label.flatten() - 1)
    loss = -np.sum(np.log(probs[idx])) / n
    max_idx = np.argmax(probs, axis=1)
    
    accuracy = np.sum(max_idx == (label - 1).flatten()) / n
    sensitivity = np.zeros((n, k))
    sensitivity[idx] = -1
    sensitivity = sensitivity + probs

    return loss, accuracy, sensitivity
