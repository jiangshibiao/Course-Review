function kmeans_plot(X, idx, ctrs, iter_ctrs)
%KMEANS K-Means clustering algorithm
%
%   Input: X - data point features, n-by-p maxtirx. 
%          idx  - cluster label
%          ctrs - cluster centers, K-by-p matrix.
%          iter_ctrs - cluster centers of each iteration, K-by-p-by-iter
%                       3D matrix.


plot(X(idx==1,1),X(idx==1,2),'r.','MarkerSize',12)
hold on
plot(X(idx==2,1),X(idx==2,2),'b.','MarkerSize',12)

t = size(iter_ctrs, 3);
x1 = reshape(iter_ctrs(1,1,:), 1, t);
y1 = reshape(iter_ctrs(1,2,:), 1, t);
x2 = reshape(iter_ctrs(2,1,:), 1, t);
y2 = reshape(iter_ctrs(2,2,:), 1, t);


plot(x1, y1,'-rs',...
     'MarkerSize',12,'LineWidth',2);
plot(x2, y2,'-bo',...
     'MarkerSize',12,'LineWidth',2);
 
legend('Cluster 1','Cluster 2',...
       'Location','NW')

end

