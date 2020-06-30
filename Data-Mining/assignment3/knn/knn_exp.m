[X, y] = mkdata;

K = [1 10 100];
for i = 1:length(K)
    knn_plot(X, y, K(i));
end