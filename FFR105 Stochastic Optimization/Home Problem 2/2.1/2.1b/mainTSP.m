clear all
close all
populationSize = 50;
mutationProbability = 1/50;
tournamentSelectionParameter = 0.8;
tournamentSize = 2;
nbrOfCopies = 1;
numberOfGenerations = 200;


% Load City Locations
cityLocations = LoadCityLocations();
numberOfGenes = length(cityLocations);

% Each row is a chromosome
population = InitializePopulation(populationSize, numberOfGenes);

% Vizualize starting point of algorithm
fitness = zeros(populationSize,1);
    for i = 1:populationSize
        fitness(i) = EvaluateIndividual(population(i,:), cityLocations);
    end
[bestFitnessEver, iBestEver] = max(fitness);
bestIndividualEver = population(iBestEver,:);
disp('Shortest path length in initalization')
disp(1/bestFitnessEver)
tspFigure = InitializeTspPlot(cityLocations,[0 20 0 20]); 
connections = InitializeConnections(cityLocations); 
PlotPath(connections,cityLocations,bestIndividualEver);     


for iGeneration = 1:numberOfGenerations
    % Evaluation
    fitness = zeros(populationSize,1);
    for i = 1:populationSize
        fitness(i) = EvaluateIndividual(population(i,:), cityLocations);
    end
    % Reproduction
    newPopulation = CreateNextGeneration( population, fitness, tournamentSize, ...
        tournamentSelectionParameter, mutationProbability);
    % Elitism
    for i = 1:populationSize
        if fitness(i) > bestFitnessEver
           bestIndividualEver = population(i,:);
           bestFitnessEver = fitness(i);
           PlotPath(connections,cityLocations,bestIndividualEver);     
        end
    end  
    % Generational replacement
    population = InsertBestIndividual(newPopulation, bestIndividualEver, nbrOfCopies);     
end

disp('Shortest path length')
disp(1/bestFitnessEver)