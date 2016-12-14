function [ adjacancyMatrix ] = adjSmallWorld( n0, p, c )

adjacancyMatrix = zeros(n0,n0);
for i=1:c/2
    tmp = ones(n0-i,1);
    adjacancyMatrix = adjacancyMatrix + diag(tmp,i);
    tmp = ones(i,1);
    adjacancyMatrix = adjacancyMatrix + diag(tmp,n0-i);
end
adjacancyMatrix = adjacancyMatrix + adjacancyMatrix';
nbrEdges = sum(sum(adjacancyMatrix));
for i = 1:nbrEdges
    if rand < p
        startNode = randi(n0);
        tmp = 1:n0;
        tmp = [tmp(1:startNode-1) tmp(startNode+1:end)];
        stopNode = tmp(randi(n0-1));
        adjacancyMatrix(startNode,stopNode) = 1;
        adjacancyMatrix(stopNode,startNode) = 1;
    end
end
end

