function [ xIterations ] = NewtonRaphson( coefficients, startingPoint, tol )
% NewtonRaphson Iterative method to find the minimum of a polynomial
%
% INPUT
% coefficients = [a0 a1 ... an] 
%   specifies input polynomial p(x) = a0 + a1*x + ... an*x^n
%  startingPoint
%   initial guess for the min
%  tol
%   absolute tolerance
%
% OTPUT
% xIterations
%   Array containing all the iterations for the miminum, starting from the
%   initial guess and ending on the final estimate for which the tolerance
%   was achieved

xIterations = startingPoint;
condition = true;
while condition
    xOld = xIterations(end);
    fPrime = Polynomial(xOld, PolynomialDifferentiation(coefficients,1));
    fBis = Polynomial(xOld, PolynomialDifferentiation(coefficients,2));
    xNew = NewtonRaphsonStep( xOld, fPrime, fBis );
    xIterations = [xIterations xNew];
    if abs(xNew) == Inf
        message = ['Newton Raphson iteration aborted at i='...
            num2str(length(xIterations)) ...
            ' due to unbounded growth in the x variable, \n last iteration at x='...
            num2str(xNew) ', next to last iteration at x=' ...
            num2str(xOld) '. \n'];
        fprintf(message)
        break
    end    
    
    condition = abs(xNew - xOld) > tol;

end
end