import numpy as np

def get_new_weight_inc(weight_inc, weight, momW, wc, lr, weight_grad):
    '''
    Get new increment weight, the update weight policy.
      inputs:
              weight_inc:     old increment weights
              weight:         old weights
              momW:           weight momentum
              wc:             weight decay
              lr:             learning rate
              weight_grad:    weight gradient

      outputs:
              weight_inc:   new increment weights
    '''
    weight_inc = momW * weight_inc - wc * lr * weight - lr * weight_grad

    return weight_inc

