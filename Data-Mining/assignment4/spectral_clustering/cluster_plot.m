function cluster_plot(X, idx)
%CLUSTER_PLOT show clustering results
%
%   Input: X   - data point features, n-by-p maxtirx.
%          idx - data point cluster labels, n-by-1 vector.


plot(X(idx==1,1),X(idx==1,2),'r.','MarkerSize',12)
hold on
plot(X(idx==2,1),X(idx==2,2),'b.','MarkerSize',12)

legend('Cluster 1','Cluster 2')
axis equal
end