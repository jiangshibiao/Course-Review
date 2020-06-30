function show_digit(X)
%SHOW_IMAGE Show a clustering centers image
%   Inputs:
%       X: cluster center matrix, returned by kmeans.

W = 20;
H = 20;
ShowLine = size(X, 1)/10;
numPerLine = 10;

Y = zeros(H,W);
for i=0:ShowLine-1
for j=0:numPerLine-1
    Y(i*H+1:(i+1)*H,j*W+1:(j+1)*W) = reshape(X(i*numPerLine+j+1,:),[H,W]);
end
end

imagesc(Y);colormap(gray);axis image;
end