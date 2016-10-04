function [ population ] = InitializePopulation( populationSize, numberOfGenes )

population = zeros(populationSize, numberOfGenes);
for i = 1:populationSize;
    population(i,:) = randperm(numberOfGenes);
end
end
