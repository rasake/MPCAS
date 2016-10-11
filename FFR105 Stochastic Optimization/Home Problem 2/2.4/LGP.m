function [bestIndividualEver, bestFitnessEver] = LGP

populationSize = 50;
nbrGenerations = 100;
tournamentSelectionParameter = 0.75;
tournamentSize = 5;
crossOverProbability = 0.2;
minMutationProbability = 0.05;
maxMutationProbability = 0.2;
alpha = 1.1;
minDiversity = 0.3;
nbrOfCopies = 1;


% Encoding parameters
minChromosomeLength = 12;
maxChromosomeLength = 40;
nbrOperators = 4;
nbrVarRegisters = 4;
constants = [1 -1];


nbrConstRegisters = length(constants);
functionData = LoadFunctionData;


population = InitializePopulation(populationSize,minChromosomeLength, ...
    maxChromosomeLength, nbrOperators, nbrVarRegisters, nbrConstRegisters);
fitness = zeros(1,populationSize);
bestFitnessEver = 0;
mutationProbability = minMutationProbability;
for k=1:nbrGenerations
    %Evaluation
    for i=1:populationSize
        chromosome = population(i).Chromosome;
        fitness(i) = evaluateChromosome(chromosome, functionData, nbrVarRegisters, constants);
    end
    %Reproduction
    newPopulation = population;
    for i = 1:2:populationSize
        i1 = TournamentSelect(fitness, tournamentSelectionParameter, tournamentSize);
        i2 = TournamentSelect(fitness, tournamentSelectionParameter, tournamentSize);
        chromosome1 = population(i1).Chromosome;
        chromosome2 = population(i2).Chromosome;
        
        if rand < crossOverProbability
            [chromosome1, chromosome2] = Cross(chromosome1,chromosome2, 4);
        end
        
        chromosome1 = Mutate(chromosome1, mutationProbability, nbrVarRegisters, nbrConstRegisters);
        chromosome2 = Mutate(chromosome2, mutationProbability, nbrVarRegisters, nbrConstRegisters);
        newPopulation(i1).Chromosome = LimitLength(chromosome1, maxChromosomeLength);
        newPopulation(i2).Chromosome = LimitLength(chromosome2, maxChromosomeLength);
    end
    %Adjust mutation rate
    diversity = CalculateDiversity(newPopulation, populationSize);
    if diversity < minDiversity
        mutationProbability = mutationProbability*alpha;
    else
        mutationProbability = mutationProbability/alpha;
    end
    mutationProbability = max(mutationProbability, minMutationProbability);
    mutationProbability = min(mutationProbability, maxMutationProbability);
    
    %Elitism
    for i = 1:populationSize
        if fitness(i) > bestFitnessEver
            bestIndividualEver = population(i).Chromosome;
            bestFitnessEver = fitness(i);
            disp('New best individual found')
            disp(bestIndividualEver)
            disp('with fitness')
            disp(bestFitnessEver)
        end
    end
    % Generational replacement
    population = InsertBestIndividual(newPopulation, bestIndividualEver, nbrOfCopies);
end

end
