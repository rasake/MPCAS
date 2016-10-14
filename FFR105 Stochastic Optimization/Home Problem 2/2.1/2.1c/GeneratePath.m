function [ path ] = GeneratePath(pheromoneLevels, visibility, alpha, beta)
%GENERATEPATH Summary of this function goes here
%   Detailed explanation goes here

nbrOfNodes = size(pheromoneLevels,1);
path = zeros(1,nbrOfNodes);
startingNode = randi(nbrOfNodes);
path(1) = startingNode;

for j = 1:nbrOfNodes-1
    jNode = path(j);
    jProbMatrix = zeros(50-length(path),2);
    k = 1;
    for iNode = 1:nbrOfNodes
        if ~any(path==iNode)
            ijProb = pheromoneLevels(iNode,jNode)^alpha*visibility(iNode,jNode)^beta;
            jProbMatrix(k,1) = ijProb;
            jProbMatrix(k,2) = iNode;
            k = k+1;
        end
    end
    % Normalize and sort probabilities
    jProbMatrix(:,1) = jProbMatrix(:,1)/sum(jProbMatrix(:,1));
    jProbMatrix = sortrows(jProbMatrix,1);
    % Transorm to cumlative prob. distribution
    jProbMatrix(:,1) = cumsum(jProbMatrix(:,1));
    
    
    % Choose destination with RWS
    r = rand;
    [value, index] = max(jProbMatrix(:,1)>=r);
    jDestinationNode = jProbMatrix(index,2);
    path(j+1) = jDestinationNode;    
end
end

