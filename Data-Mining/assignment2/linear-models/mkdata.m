function [X, y, w] = mkdata(N, noisy)
%MKDATA Generate data set.
%
%   INPUT:  N:     number of samples.
%           noisy: if or not add noise to y.
%
%   OUTPUT: X: sample features, P-by-N matrix.
%           y: sample labels, 1-by-N row vector.
%           w: target function parameters, (P+1)-by-1 column vector.
%


range = [-1, 1];
dim = 2;

X = rand(dim, N)*(range(2)-range(1)) + range(1);
while true
  Xsample = [ones(1, dim); rand(dim, dim)*(range(2)-range(1)) + range(1)];
  w = null(Xsample', 'r');
  y = sign(w'*[ones(1, N); X]);
  if all(y)
      break; 
  end
end

if nargin == 2
    if noisy == 'noisy'
        idx = randsample(N,N/10);
        y(idx) = -y(idx);
    end
end

end