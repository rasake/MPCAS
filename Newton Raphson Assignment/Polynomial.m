function [ y ] = Polynomial( x, coefficients )
%UNTITLED5 Summary of this function goes here
%   Detailed explanation goes here

% Better name for output variable
y = 0;
for iPower = 0:1:length(coefficients)-1
     y = y + coefficients(iPower+1)*x.^(iPower);
end

