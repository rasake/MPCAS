function [ y ] = Polynomial( x, polynomialCoefficients )
% Polynomial Evaluates a polynomial at x
%
% INPUT
% x
%   where to evaluate the polynomial
% polynomialCoefficients = [a0 a1 ... an] 
%   specifies input polynomial p(x) = a0 + a1*x + ... an*x^n
%
% OTPUT
% y
%   value of polynomial at x
y = 0;
for iPower = 0:1:length(polynomialCoefficients)-1
     y = y + polynomialCoefficients(iPower+1)*x.^(iPower);
end

