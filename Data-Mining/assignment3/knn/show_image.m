function show_image(X)
%SHOW_IMAGE Show a CAPTCHA image
%   Inputs:
%       X: 144x4 matrix, 4 digits in an image, each digit is a 144x1 vector.

num = size(X, 2);
X = reshape(X, 12, 12 * num);
imagesc(X); colormap(gray); axis image;
end