function [ modifiedPopulation ] = InsertBestIndividual( population, bestIndividual, nbrOfCopies )

modifiedPopulation = population;

for i = 1:nbrOfCopies
    modifiedPopulation(i,:) = bestIndividual;
end



end

