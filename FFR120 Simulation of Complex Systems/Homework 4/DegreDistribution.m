function [ degreeDist ] = DegreDistribution( adjacencyMatrix )
degreeDist=sum(adjacencyMatrix,1);
end

