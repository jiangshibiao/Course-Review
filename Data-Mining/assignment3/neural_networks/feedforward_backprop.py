from fullyconnect_feedforward import fullyconnect_feedforward
from fullyconnect_backprop import fullyconnect_backprop
from relu_feedforward import relu_feedforward
from relu_backprop import relu_backprop
from softmax_loss import softmax_loss

def feedforward_backprop(data, label, weights):


    # feedforward hidden layer and relu
    fully1_out = fullyconnect_feedforward(data, weights['fully1_weight'], weights['fully1_bias']);
    relu1_out = relu_feedforward(fully1_out)

    # softmax loss (probs = e^(w*x+b) / sum(e^(w*x+b))) is implemented in two parts for convenience.
    # first part: y = w * x + b is a fullyconnect.
    fully2_out = fullyconnect_feedforward(relu1_out, weights['fully2_weight'], weights['fully2_bias'])
    # second part: probs = e^y / sum(e^y) is the so-called softmax_loss here.
    loss, accuracy, fully2_sensitivity = softmax_loss(fully2_out, label)
    gradients = {}
    gradients['fully2_weight_grad'], gradients['fully2_bias_grad'], relu1_sensitivity = fullyconnect_backprop(fully2_sensitivity, relu1_out, weights['fully2_weight'])
    # backprop of relu and then hidden layer 
    fully1_sensitivity = relu_backprop(relu1_sensitivity, fully1_out)
    gradients['fully1_weight_grad'], gradients['fully1_bias_grad'], _ = fullyconnect_backprop(fully1_sensitivity, data, weights['fully1_weight'])

    return loss, accuracy, gradients