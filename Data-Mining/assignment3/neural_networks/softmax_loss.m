function [loss, accuracy, sensitivity] = softmax_loss(in, label)
%The softmax loss computing process
%   inputs:
%       in      : the output of previous layer, shape: [number of images, number of kinds of labels]
%       label   : the ground true of these images, shape: [1, number of images]
%
%   outputs
%       loss    : the average loss, scale variable
%       accuracy: the accuracy of the classification
%       sentivity     : the sentivity for in, shape: [number of images, number of kinds of labels]

[n, k] = size(in);
in = in - repmat(max(in, [],  2), [1, k]);
h = exp(in);
total = sum(h, 2);
probs = h ./ repmat(total, [1, k]);
idx = sub2ind(size(probs), 1:n, label);
loss = -sum(log(probs(idx))) / n;

[~, max_idx] = sort(probs, 2, 'descend');
max_idx = max_idx(:, 1)';
accuracy = sum(max_idx == label) / n;

sensitivity = zeros(n, k);
sensitivity(idx) = -1;
sensitivity = sensitivity + probs;

end

