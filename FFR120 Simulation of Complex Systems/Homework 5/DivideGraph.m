function [ Q, communities ] = DivideGraph( A )
%DIVIDEGRAPH Summary of this function goes here
%   Detailed explanation goes here
m = sum(sum(A))/2;
nodes = 1:length(A);
B = ModularityMatrix(A,m);
communities = cell(0);
[Q, communities] = modularityRec(B,0,m,nodes,communities);


function [Q, communities] = modularityRec(B,Q,m,nodes,communities)
    [deltaQ,s] = modularity(B,m);
    if deltaQ > 1e-8
        Q = Q+deltaQ;
        [Bneg, Bpos] = divB(B,s);
        nodesNeg = nodes(s<0);
        [Q, communities] = modularityRec(Bneg,Q,m,nodesNeg,communities);
        nodesPos = nodes(s>0);
        [Q, communities] = modularityRec(Bpos,Q,m,nodesPos,communities);
    else
        %community found! Add it to cell array
        communities{end+1} = nodes;
    end
end
end

