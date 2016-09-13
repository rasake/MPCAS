clear all
clc
mu = [1 10 100 1000 10000 100000]; %penalty -factor
eta = 0.000001; %steplength
T = 1e-8; %threshold
x0 = [1;2]; %starting point

nbrOfIteraions = length(mu);
minima = zeros(nbrOfIteraions,2);
for i = 1: nbrOfIteraions
    minima(i,:) = GradientDescent(x0, mu(i), eta, T)';
end

results_str = num2str([mu' minima], '%.3f');
header = '      mu      x1      x2';
disp(header)
disp(results_str)