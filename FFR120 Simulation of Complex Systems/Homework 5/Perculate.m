function [ Aperc ] = Perculate( A, p ) %Remove edges with prob p
nbrNodes = length(A);
tmp = triu(A.*(rand(nbrNodes,nbrNodes)>p));
Aperc = tmp + tmp';
end

