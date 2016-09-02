function [ coeff_out ] = PolynomialDifferentiation( coeff_in, diff_order )
%UNTITLED6 Summary of this function goes here
%   Detailed explanation goes here

% TODO zero order drivative?

polynomial_order = length(coeff_in)-1;
coeff_out = zeros(polynomial_order-1);
for power_i = 1:1:polynomial_order
    coeff_out(end-(power_i-1)) = coeff_in(end-(power_i))*factorial(power_i)/factorial(diff_order);

end

