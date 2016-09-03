function [ xOut ] = NewtonRaphsonStep( xIn, fPrime, fBis )
% NewtonRaphsonStep Performs a step from the point xIn according to the 
%
% INPUT
% xIn
%   point to step from
% fPrime
%   first order derivative at xIn
% fBis
%   second order derivative at xIn
%
% OTPUT
% xOut
%   next x generated with Newton-Raphson

xOut = xIn - fPrime/fBis;

end

