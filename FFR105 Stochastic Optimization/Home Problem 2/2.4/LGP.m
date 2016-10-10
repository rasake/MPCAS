clear all
clc
populationSize = 10;
nbrGenerations = 15;
tournamentSelectionParameter = 0.75;
tournamentSize = 5;
crossOverProbability = 0.2;
mutationProbability = 0.3;
nbrOfCopies = 1;


% Encoding parameters
minChromosomeLength = 3;
maxChromosomeLength = 15;
nbrOperators = 2;
nbrVarRegisters = 3;
constants = [1 -1 -10];


nbrConstRegisters = length(constants);
functionData = LoadFunctionData;


population = InitializePopulation(populationSize,minChromosomeLength, ...
    maxChromosomeLength, nbrOperators, nbrVarRegisters, nbrConstRegisters)
fitness = zeros(1,populationSize);
bestFitnessEver = 0;
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
            [chromosome1, chromosme2] = Cross(chromosome1,chromosome2, 4);
        end
        
        chromosome1 = Mutate(chromosome1, mutationProbability, nbrVarRegisters, nbrConstRegisters);
        chromosome2 = Mutate(chromosome2, mutationProbability, nbrVarRegisters, nbrConstRegisters);
        chromsome1 = LimitLength(chromosome1, maxChromosomeLength);
        chromsome2 = LimitLength(chromosome2, maxChromosomeLength);
        newPopulation(i1).Chromosome = chromosome1;
        newPopulation(i2).Chromosome = chromosome2;
    end
% TODO Elitism
    for i = 1:populationSize
        if fitness(i) > bestFitnessEver
           bestIndividualEver = population(i).Chromosome;
           bestFitnessEver = fitness(i);
        end
    end  
    % Generational replacement
    population = InsertBestIndividual(newPopulation, bestIndividualEver, nbrOfCopies);    
end


jSelected = TournamentSelect( fitness, tournamentSelectionParameter, tournamentSize );
kSelected = TournamentSelect( fitness, tournamentSelectionParameter, tournamentSize );


[ch1,ch2] = Cross(population(jSelected).Chromosome, population(kSelected).Chromosome,4);

