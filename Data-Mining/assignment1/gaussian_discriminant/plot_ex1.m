function plot_ex1(mu0, Sigma0, mu1, Sigma1, phi, fig_title, pos)

if mod(pos-1, 4) == 0
    figure;
end

N = 100;

% generate data
X0 = mvnrnd(mu0, Sigma0, round((1-phi) * N))';
X1 = mvnrnd(mu1, Sigma1, round(phi * N))';

% visualize
blue = [0 0 1];
red = [1 0 0];

x0 = X0(1,:);
y0 = X0(2,:);
x1 = X1(1,:);
y1 = X1(2,:);

subplot(1, 4, mod(pos-1, 4)+1);


xmin = min(min(x0), min(x1));
xmax = max(max(x0), max(x1));
ymin = min(min(y0), min(y1));
ymax = max(max(y0), max(y1));

step = 0.1; % TODO
[xs, ys] = meshgrid(xmin:step:xmax, ymin:step:ymax);

xy = [xs(:) ys(:)];

Sigma = zeros(2,2,2);
Sigma(:,:,1) = Sigma0;
Sigma(:,:,2) = Sigma1;
pos_prob = gaussian_pos_prob(xy', [mu0, mu1], Sigma, [1-phi, phi]);
pos_prob = pos_prob(:,1);
image_size = size(xs);
decisionmap = reshape((pos_prob > 0.5) + 1, image_size);
imagesc([xmin,xmax],[ymin,ymax],decisionmap);
hold on;
set(gca,'ydir','normal');
 
% colormap for the classes:
% class 1 = light red, 2 = light green, 3 = light blue
cmap = [1 0.8 0.8; 0.95 1 0.95; 0.9 0.9 1];
colormap(cmap);
alpha(0.8);

diff = abs(pos_prob-0.5);
diff_sorted = sort(diff);
threshold = diff_sorted(int32(length(diff_sorted)/500));

bb = xy(diff < threshold,:);


plot(x0, y0, '.', 'Color', blue);  % dark
hold on;
plot(x1, y1, '.', 'Color', red);

plot(bb(:,1), bb(:,2), '.', 'Color', 'k', 'MarkerSize', 6);

title(fig_title);

set(gcf, 'renderer', 'painters');

argn = [ ...
    xmin - 0.1 * (xmax - xmin), xmax + 0.1 * (xmax - xmin), ...
    ymin - 0.1 * (ymax - ymin), ymax + 0.1 * (ymax - ymin) ];

axis(argn);

axis equal;
axis tight;
end
