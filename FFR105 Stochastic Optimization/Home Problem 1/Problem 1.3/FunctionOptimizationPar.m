function [maximumFitness] = FunctionOptimizationPar() 
close all
populationSize = 500;
numberOfGenes = 30;
crossOverProbability = 0.8;
mutationProbability = 1/numberOfGenes;
tournamentSelectionParameter = 0.6;
tournamentSize = 2;
nbrOfCopies = 1;
variableRange = 5.0;
numberOfGenerations = 100;
fitness = zeros(populationSize,1);



decodedPopulation = zeros(populationSize, 2);

population = InitializePopulation(populationSize, numberOfGenes);

for iGeneration = 1:numberOfGenerations

    maximumFitness = 0.0; % Assume non-negative fitness values
    xBest = zeros(1,2);
    for i = 1:populationSize
        chromosome = population(i,:);
        x = DecodeChromosome(chromosome, 2, variableRange);
        decodedPopulation(i,:) = x;
        fitness(i) = EvaluateIndividual(x);
        if fitness(i) > maximumFitness
            maximumFitness = fitness(i);
            bestChromosome = population(i,:);
            xBest = x;
        end
    end
  
    
    tempPopulation = population;

    for i = 1:2:populationSize
        i1 = TournamentSelect(fitness, tournamentSelectionParameter, tournamentSize);
        i2 = TournamentSelect(fitness, tournamentSelectionParameter, tournamentSize);
        chromosome1 = population(i1,:);
        chromosome2 = population(i2,:);

        r = rand;
        if rand < crossOverProbability
            newChromosomePair = Cross(chromosome1,chromosome2);
            tempPopulation(i,:) = newChromosomePair(1,:);
            tempPopulation(i+1,:) = newChromosomePair(2,:);
        else
            tempPopulation(i,:) = chromosome1;
            tempPopulation(i+1,:) = chromosome2;
        end
    end % Loop over population

    for i = 1:populationSize
        originalChromosome = tempPopulation(i,:);
        mutatedChromosome = Mutate(originalChromosome, mutationProbability);
        tempPopulation(i,:) = mutatedChromosome;
    end

    population = InsertBestIndividual(tempPopulation, bestChromosome, nbrOfCopies);

end %Loop over genertions