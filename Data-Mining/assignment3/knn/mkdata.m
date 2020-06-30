function [X, y] = mkdata

N1 = 200; N2 = 200; % Class sizes
X = [randn(2, N1), randn(2, N2) + 2];
y = [repmat(0, 1, N1), repmat(1, 1, N2)];

end