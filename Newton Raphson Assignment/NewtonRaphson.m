function [ xIterations ] = NewtonRaphson( coefficients, startingPoint, tol )
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here

xIterations = startingPoint;
condition = true;
while condition
    xOld = xIterations(end);
    fPrime = Polynomial(xOld, PolynomialDifferentiation(coefficients,1));
    fBis = Polynomial(xOld, PolynomialDifferentiation(coefficients,2));
    xNew = NewtonRaphsonStep( xOld, fPrime, fBis );
    xIterations = [xIterations xNew];
    condition = abs(xNew - xOld) > tol;
end
end