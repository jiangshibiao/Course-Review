load digit_data
[~, num_cases] = size(X);
train_num_cases = num_cases / 5 * 4;
X = reshape(X, [400, num_cases]);
X = permute(X, [2, 1]);
% X has the shape of [number of samples, number of pixels]
train_data = X(1:train_num_cases, :, :, :);
train_label = y(:, 1:train_num_cases);
test_data = X(train_num_cases+1:num_cases, :, :, :);
test_label = y(:, train_num_cases+1:num_cases);
weights.fully1_weight = randn([400, 25]) ./ 400; weights.fully1_bias = rand([25, 1]);
weights.fully2_weight = randn([25, 10]) ./ 25; weights.fully2_bias = rand([10, 1]);

data = train_data(1:100, :, :, :);
label = train_label(:, 1:100);

EPSILON = 0.00010;
[loss, ~, grads] = feedforward_backprop(data, label, weights);

% check correctness of fully1_bias's gradient
for c = 1:size(weights.fully1_bias, 1)
    weights.fully1_bias(c, 1) = weights.fully1_bias(c, 1) + EPSILON;
    [loss_2, ~, grads_2] = feedforward_backprop(data, label, weights);
    fprintf('%.2e, %.2e, %.2e\n', (loss_2 - loss) / EPSILON, grads.fully1_bias_grad(c, 1), grads_2.fully1_bias_grad(c, 1));
    weights.fully1_bias(c, 1) = weights.fully1_bias(c, 1) - EPSILON;
end