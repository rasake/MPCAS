clear all
clc

nbrNodes = 10;
p = 0.2;
c=4;

%%
subplot(1,2,1)

adjacancyMatrix = zeros(nbrNodes,nbrNodes);
for i=1:c/2
    tmp = ones(nbrNodes-i,1);
    adjacancyMatrix = adjacancyMatrix + diag(tmp,i);
    tmp = ones(i,1);
    adjacancyMatrix = adjacancyMatrix + diag(tmp,nbrNodes-i);
end
adjacancyMatrix = adjacancyMatrix + adjacancyMatrix';
G1 = graph(adjacancyMatrix);
plot(G1,'NodeLabel',{})
title('Small world model before adding short-cuts')

%%

subplot(1,2,2)

nbrEdges = sum(sum(adjacancyMatrix));
for i = 1:nbrEdges
    if rand < p
        startNode = randi(nbrNodes);
        tmp = 1:nbrNodes;
        tmp = [tmp(1:startNode-1) tmp(startNode+1:end)];
        stopNode = tmp(randi(nbrNodes-1));
        adjacancyMatrix(startNode,stopNode) = 1;
        adjacancyMatrix(stopNode,startNode) = 1;
    end
end
G1 = graph(adjacancyMatrix);
plot(G1)
title('Small world model after adding short-cuts')