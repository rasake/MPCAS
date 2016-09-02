function [ xOut ] = NewtonRaphsonStep( xIn, fPrime, fBis )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

xOut = xIn - fPrime/fBis;

end

