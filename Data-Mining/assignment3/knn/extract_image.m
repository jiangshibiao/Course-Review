function X = extract_image(image_file_name)
%EXTRACT_IMAGE Extract features from image
%   Inputs:
%       image_file_name: filename of image
%   Outputs:
%       X: 144x4 matrix, 4 digits in an image, each digit is a 144x1 vector.

m = imread(image_file_name);
d1 = reshape(m(1:12, 1:12), 144, 1);
d2 = reshape(m(1:12, 13:24), 144, 1);
d3 = reshape(m(1:12, 25:36), 144, 1);
d4 = reshape(m(1:12, 37:48), 144, 1);
X = [d1, d2, d3, d4];

end
