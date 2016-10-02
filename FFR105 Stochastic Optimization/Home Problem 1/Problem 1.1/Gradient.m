function [ gradient ] = Gradient( x1, x2, mu )
%GRADIENT Summary of this function goes here
%   Detailed explanation goes here

gradientInsideBoundary = [2*(x1-1); 4*(x2-2)];

penaltyGradient = mu*[2*(x1^2+x2^2-1)* 2*x1; 2*(x1^2+x2^2-1) * 2*x2];
if penaltyGradient == Inf
    x1,x2
    penaltyGradient
end
if x1^2 + x2^2 - 1 <= 0
    gradient = gradientInsideBoundary;
else
    gradient = gradientInsideBoundary + penaltyGradient;
end

end

