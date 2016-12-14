function [ L ] = CalulcateLengths( adjacencyMatrix  )
%CALCULATEPATHLENGTHS Summary of this function goesadjacencyMatrix here
%   Detailed explanation goes here
L = zeros(size(adjacencyMatrix));
p=1;
while sum(sum(L==0)) > 0
    Ap = adjacencyMatrix^p;
    deltaL=(((L==0).*Ap)>0)*p;
    L = L+deltaL;
    p = p+1;
end
% Exclude paths that go back to themselves
L(logical(eye(size(L)))) = 0;
end