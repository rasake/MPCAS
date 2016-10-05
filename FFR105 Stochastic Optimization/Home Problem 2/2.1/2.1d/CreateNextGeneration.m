function [ newPopulation ] = CreateNextGeneration( population, fitness, tournamentSize, ...
        tournamentSelectionParameter, mutationProbability )
%CREATENEXTGENERATION Create the next generation through selection and
%mutation

newPopulation = population;
for k = 1:length(population)
   iSelected = TournamentSelect(fitness, tournamentSelectionParameter, tournamentSize);
   kChromosome = population(iSelected,:);
   kMutatedChromosome = Mutate(kChromosome, mutationProbability);
   newPopulation(k,:) = kMutatedChromosome; 
end

end

