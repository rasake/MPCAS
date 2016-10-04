function [ newPopulation ] = CreateNextGeneration( population, fitness, tournamentSize, ...
        tournamentSelectionParameter, mutationProbability )
%CREATENEXTGENERATION Create the next generation through selection and
%mutation

newPopulation = population;
for k = 1:length(population)
   iSelected = TournamentSelect(fitness, tournamentSelectionParameter, tournamentSize);
   chromosome = population(iSelected,:);
   mutatedChromosome = Mutate(chromosome, mutationProbability);
   newPopulation(k,:) = mutatedChromosome; 
end

end

