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

% Training
fully1_weight_inc = zeros(size(weights.fully1_weight)); fully1_bias_inc = zeros(size(weights.fully1_bias));
fully2_weight_inc = zeros(size(weights.fully2_weight)); fully2_bias_inc = zeros(size(weights.fully2_bias));
batch_size = 100;
max_epoch = 10;
momW = 0.9;
wc = 0.0005;
learning_rate = 0.1;

for epoch = 1:max_epoch
    for i = 1:ceil(train_num_cases/batch_size)
        data = train_data((i-1)*batch_size+1:min(i*batch_size, train_num_cases), :, :, :);
        label = train_label(:, (i-1)*batch_size+1:min(i*batch_size, train_num_cases));
        % The feedforward and backpropgation processes.
        [loss, accuracy, gradients] = feedforward_backprop(data, label, weights);
        fprintf('%03d.%02d loss:%0.3e, accuracy:%f\n', epoch, i, loss, accuracy);
        % Updating weights
        fully1_weight_inc = get_new_weight_inc(fully1_weight_inc, weights.fully1_weight, momW, wc, learning_rate, gradients.fully1_weight_grad);
        weights.fully1_weight = weights.fully1_weight + fully1_weight_inc;
        fully1_bias_inc = get_new_weight_inc(fully1_bias_inc, weights.fully1_bias, momW, wc, learning_rate, gradients.fully1_bias_grad);
        weights.fully1_bias = weights.fully1_bias + fully1_bias_inc;
        
        fully2_weight_inc = get_new_weight_inc(fully2_weight_inc, weights.fully2_weight, momW, wc, learning_rate, gradients.fully2_weight_grad);
        weights.fully2_weight = weights.fully2_weight + fully2_weight_inc;
        fully2_bias_inc = get_new_weight_inc(fully2_bias_inc, weights.fully2_bias, momW, wc, learning_rate, gradients.fully2_bias_grad);
        weights.fully2_bias = weights.fully2_bias + fully2_bias_inc;
    end
end

% TODO Testing
[loss, accuracy, ~] = feedforward_backprop(test_data, test_label, weights);
fprintf('loss:%0.3e, accuracy:%f\n', loss, accuracy);