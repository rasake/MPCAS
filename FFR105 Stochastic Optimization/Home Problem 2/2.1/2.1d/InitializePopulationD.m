function [ population ] = InitializePopulationD( populationSize, cityLocations)

nbrOfGenes = length(cityLocations);
population = zeros(populationSize, nbrOfGenes);
[path, pathLength] = GetNearestNeighbourPath(cityLocations);
population(1,:) = path;
for i = 2:populationSize;
    [path, pathLength] = GetNearestNeighbourPath(cityLocations);
    mutatedPath = Mutate(path,3/nbrOfGenes);
    population(i,:) = mutatedPath;
end
end
