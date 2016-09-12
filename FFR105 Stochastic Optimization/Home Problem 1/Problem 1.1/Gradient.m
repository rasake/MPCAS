function [ gradient ] = Gradient( x, mu )
%GRADIENT Summary of this function goes here
%   Detailed explanation goes here

gradientInsideBoundary = [2*(x(1)-1); 4*(x(2)-1)]
penaltyGradient = mu*[2*( norm(x)^2-1 )^2 * 2*x(1); 2*( norm(x)^2-1 )^2 * 2*x(2)]
    
if norm(x) <= 1
    gradient = gradientInsideBoundary;
else
    gradient = gradientInsideBoundary + penaltyGradient;
end

end

