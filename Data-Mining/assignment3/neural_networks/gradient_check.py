import scipy.io as sio
import numpy as np
from feedforward_backprop import feedforward_backprop

digit_data = sio.loadmat('digit_data.mat')
X = digit_data['X']
y = digit_data['y']
_, num_cases = X.shape
train_num_cases = num_cases * 4 // 5
X = X.reshape((400, num_cases))
X = X.reshape((num_cases, 400))
# X has the shape of (number of samples, number of pixels)
train_data = X[:train_num_cases,:]
train_label = y[:, :train_num_cases]
test_data = X[train_num_cases:num_cases, :]
test_label = y[:,train_num_cases:]
weights = {}
weights['fully1_weight'] = np.random.randn(400, 25) / 400
weights['fully1_bias'] = np.random.rand(25, 1) 
weights['fully2_weight'] = np.random.randn(25, 10) / 25
weights['fully2_bias'] = np.random.rand(10, 1)

data = train_data[:100, :]
label = train_label[:, :100]

EPSILON = 0.00010
loss, _, grads = feedforward_backprop(data, label, weights)

print (grads['fully1_bias_grad'].shape)

# check correctness of fully1_bias's gradient
for c in range(weights['fully1_bias'].shape[0]):
    weights['fully1_bias'][c, 0] = weights['fully1_bias'][c, 0] + EPSILON
    loss_2, _, grads_2 = feedforward_backprop(data, label, weights)
    print('{:.2}, {:.2}, {:.2}'.format((loss_2 - loss) / EPSILON, grads['fully1_bias_grad'][c, 0], grads_2['fully1_bias_grad'][c, 0]))
    weights['fully1_bias'][c, 0] = weights['fully1_bias'][c, 0] - EPSILON

