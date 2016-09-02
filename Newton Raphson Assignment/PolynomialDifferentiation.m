function [ coeffOut ] = PolynomialDifferentiation( coeffIn, diffOrder )
%UNTITLED6 Summary of this function goes here
%   coeff_in = [a0 a1 ... an] 
%       specifies input polynomial p(x) = a0 + a1*x + ... an*x^n
%   diff_order
%       the order of the differentiation to be pergormed on the input
%       polynomial
%   coeff_out = [b0 b1 ... bn] 
%       specifies the output polynomial p(x) = b0 + b1*x + ... bn*x^n

% TODO zero order derivative?
% TODO assert input formatting


if diffOrder > 1 % Recursive call if higher order derivative
    coeffIn = PolynomialDifferentiation(coeffIn, diffOrder-1);
end
if length(coeffIn) < 2
    coeffOut = [];
elseif diffOrder == 0
    coeffOut = coeffIn;
else
    polynomialOrder = length(coeffIn)-1;
    coeffOut = zeros(1,polynomialOrder);
    for iPower = 1:1:polynomialOrder
        coeffOut(iPower) = coeffIn(iPower+1)*iPower;
    end
end
