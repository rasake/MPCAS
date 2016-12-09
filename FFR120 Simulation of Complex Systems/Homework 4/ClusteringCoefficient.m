function [ clusteringCoeff ] = ClusteringCoefficient( adjacencyMatrix )
nbrTriangles = trace(adjacencyMatrix^3) / 6;
D = sum(adjacencyMatrix);
nbrTriplets = sum((D).*(D-1)/2);
clusteringCoeff = 3*nbrTriangles/nbrTriplets;
end

