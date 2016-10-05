function [ newPheromoneLevel ] = UpdatePheromoneLevels(pheromoneLevel,deltaPheromoneLevel,rho)

newPheromoneLevel = (1-rho)*pheromoneLevel + deltaPheromoneLevel;

end

