function [] = PlotIterations(coefficients,iterationValues)

x = linspace(min(iterationValues)-3, max(iterationValues)+3);
plot(x, Polynomial(x,coefficients))
hold on
plot(iterationValues, Polynomial(iterationValues,coefficients), 'bo')

end