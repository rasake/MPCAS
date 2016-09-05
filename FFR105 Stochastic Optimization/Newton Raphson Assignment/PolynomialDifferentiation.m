function [ coeffOut ] = PolynomialDifferentiation( coeffIn, diffOrder )
% PolynomialDifferentiation Differentiates the polynomial with coefficients 
% coeffIn to the diffOrder
%
% INPUT
% coeff_in = [a0 a1 ... an] 
%   specifies input polynomial p(x) = a0 + a1*x + ... an*x^n
%  diff_order
%   the order of the differentiation to be pergormed
%
% OTPUT
% coeff_out = [b0 b1 ... bn] 
%   specifies the output polynomial p(x) = b0 + b1*x + ... bn*x^n

if diffOrder > 1 % Recursive call if higher order derivative
    coeffIn = PolynomialDifferentiation(coeffIn, diffOrder-1);
end
if length(coeffIn) < 2 % The derivative of a constant is zero
    coeffOut = [];
elseif diffOrder == 0
    coeffOut = coeffIn;
else
    polynomialOrder = length(coeffIn)-1;
    coeffOut = zeros(1,polynomialOrder); % Pre-allocate
    for iPower = 1:1:polynomialOrder
        coeffOut(iPower) = coeffIn(iPower+1)*iPower;
    end
end
