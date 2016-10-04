function [ pheromoneLevels ] = InitializePheromoneLevels(numberOfCities, tau0)
%INITIALIZEPHEROMONELEVELS Returns square matrix with pheromone levels set
%to tau0 for all edges
pheromoneLevels = ones(numberOfCities,numberOfCities) * tau0;

end

