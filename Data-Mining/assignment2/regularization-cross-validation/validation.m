%% Ridge Regression
load('digit_train', 'X', 'y');

% Do feature normalization
% ...

% Do LOOCV
lambdas = [1e-3, 1e-2, 1e-1, 0, 1, 1e1, 1e2, 1e3];
lambda = 0

for i = 1:length(lambdas)
    E_val = 0
    for j = 1:size(X, 2)
        X_ = ___; y_ = ___; % take point j out of X
        w = ridge(X_, y_, lambdas(i));
        E_val = Eval + ___;
    end
    % Update lambda according validation error
end

% Compute training error

load('digit_test', 'X_test', 'y_test');
% Do feature normalization
% ...
% Compute test error

%% Logistic

