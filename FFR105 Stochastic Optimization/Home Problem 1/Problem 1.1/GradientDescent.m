function [ minimum ] = GradientDescent( x0, mu, eta, T )
%GRADIENTDESCENT Summary of this function goes here
%   Detailed explanation goes here

jX = x0
while norm(Gradient(jX,mu)) >= T
    jX = jX - eta*Gradient(jX,mu)
end
minimum = jX;
end
