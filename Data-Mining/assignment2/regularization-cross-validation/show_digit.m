function show_digit(fea)
%SHOW_DIGIT show digits in X

idx = randperm(size(fea, 2));
fea = fea(:, idx(1:100));
fea = fea';

faceW = 28;
faceH = 28;
numPerLine = 20;
ShowLine = 4;

Y = zeros(faceH*ShowLine,faceW*numPerLine);
for i=0:ShowLine-1
   for j=0:numPerLine-1
     Y(i*faceH+1:(i+1)*faceH,j*faceW+1:(j+1)*faceW) = reshape(fea(i*numPerLine+j+1,:),[faceH,faceW])';
   end
end

imagesc(Y);colormap(gray); axis image;

end