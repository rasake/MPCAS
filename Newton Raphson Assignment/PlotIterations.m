function [] = PlotIterations(coefficients,iterationValues)
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here
x = linspace(min(iterationValues)-3, max(iterationValues)+3);
plot(x, Polynomial(x,coefficients))
hold on
plot(iterationValues, Polynomial(iterationValues,coefficients), 'o')

end

