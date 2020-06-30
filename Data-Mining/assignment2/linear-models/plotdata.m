function plotdata(X, y, wf, wg, desc)
%PLOTDATA Plot data set.
%
%   INPUT:  X: sample features, P-by-N matrix.
%           y: sample labels, 1-by-N row vector.
%           wf: true target function parameters, (P+1)-by-1 column vector.
%           wg: learnt target function parameters, (P+1)-by-1 column vector.
%           desc: title of figure.
%

figure;

if size(X, 1) ~= 2
    disp('WTF');
    return;
end

plot(X(1, y == 1), X(2, y == 1), 'o', 'MarkerFaceColor', 'r', ...
                                      'MarkerSize', 10);
hold on;

plot(X(1, y == -1), X(2, y == -1), 'o', 'MarkerFaceColor', 'g', ...
                                        'MarkerSize', 10);
hold on;

f = ezplot(@(x) (-wf(2)/wf(3))*x-wf(1)/wf(3), [-1 1 -1 1]);
set(f, 'Color', 'b', 'LineWidth', 2, 'LineStyle', '-');
hold on;

g = ezplot(@(x) (-wg(2)/wg(3))*x-wg(1)/wg(3), [-1 1 -1 1]);
set(g, 'Color', 'b', 'LineWidth', 2, 'LineStyle', '--');
title(desc);
hold off;
end