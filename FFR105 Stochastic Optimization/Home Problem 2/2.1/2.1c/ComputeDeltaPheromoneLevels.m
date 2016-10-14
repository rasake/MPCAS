function [ deltaPheromone ] = ComputeDeltaPheromoneLevels(pathCollection,pathLengthCollection)
%COMPUTEDELTAPHEROMONELEVELS Summary of this function goes here
%   Detailed explanation goes here

nbrOfNodes = size(pathCollection,2);
nbrOfAnts =  size(pathCollection,1);
deltaPheromone = zeros(nbrOfNodes,nbrOfNodes);

for k=1:nbrOfAnts
   kPathLength = pathLengthCollection(k);
   kRoute = [pathCollection(k,:) pathCollection(k,1)]; %Route including return to original node
   for l = 1:nbrOfNodes
       lStart = kRoute(l);
       lDestination = kRoute(l+1);
       deltaPheromone(lDestination,lStart) = deltaPheromone(lDestination,lStart) ...
           + 1/kPathLength;
   end
end

end

