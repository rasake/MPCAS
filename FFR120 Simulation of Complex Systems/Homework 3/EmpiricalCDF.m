function [ x,f ] = EmpiricalCDF( data )
%EMPIRICAL Summary of this function goes here
%   Detailed explanation goes here

x = sort(data, 'descend');
nDataPoints = length(x);
f = (1:nDataPoints)/nDataPoints;
end

