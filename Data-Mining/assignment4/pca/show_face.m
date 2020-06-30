function show_face(fea)
% Input: fea -- face image dataset. Each 1x1024 row vector of fea is a data point.

faceW = 32;
faceH = 32;

numPerLine = 20;
ShowLine = 2;

Y = zeros(faceH*ShowLine,faceW*numPerLine);
size(Y)
for i=0:ShowLine-1
   for j=0:numPerLine-1
     Y(i*faceH+1:(i+1)*faceH,j*faceW+1:(j+1)*faceW) = reshape(fea(i*numPerLine+j+1,:),[faceH,faceW]);
   end
end

imagesc(Y);colormap(gray);axis image; axis off;
end