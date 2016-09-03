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
    if abs(xNew) == Inf
        message = ['Newton Raphson iteration aborted at i='  num2str(length(xIterations)) ' due to unbounded growth in the x variable, \n last iteration at x=' num2str(xNew) ', next to last iteration at x=' num2str(xOld) '. \n'];
        fprintf(message)
        break
    end    
    
    condition = abs(xNew - xOld) > tol;

end
end