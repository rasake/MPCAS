function [ y ] = gPrime(localField, beta )
y = beta*(1-tanh(beta*localField).^2);
end