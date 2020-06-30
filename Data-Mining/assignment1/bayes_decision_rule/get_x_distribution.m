function distribution = get_x_distribution(x1, x2, range)
%GET_X_DISTRIBUTION get the number of occurance of each feature in two classes
%
%   INPUT:  x1, features of first class, 1-By-N1 vector
%           x2, features of second class, 1-By-N2 vector
%           range,  contains smallest feature and biggest feature, 1-By-2 vector
%           N1 is the number of class 1's samples, and N2 is the number of class 2's samples.
%
%   OUTPUT: distribution,   the number of occurance of each feature(from smallest feature to biggest feature) in two classes

distribution = zeros(2, range(2) - range(1) + 1);
distribution(1, min(x1) - range(1) + 1: max(x1) - range(1) + 1) = hist(x1, max(x1) - min(x1) + 1);
distribution(2, min(x2) - range(1) + 1: max(x2) - range(1) + 1) = hist(x2, max(x2) - min(x2) + 1);

end
