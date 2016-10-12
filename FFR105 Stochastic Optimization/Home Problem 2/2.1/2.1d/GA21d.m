clear all
close all
populationSize = 100;
mutationProbability = 1/50;
tournamentSelectionParameter = 0.8;
tournamentSize = 3;
nbrOfCopies = 1;
numberOfGenerations = 500;


% Load City Locations
cityLocations = LoadCityLocations();
numberOfGenes = length(cityLocations);

% Each row is a chromosome
population = InitializePopulationD(populationSize, cityLocations);

% Set up plotting
tspFigure = InitializeTspPlot(cityLocations,[0 20 0 20]); 
connections = InitializeConnections(cityLocations); 

% Assume positive fitness values
bestFitnessEver = 0;

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
           bestGen = iGeneration;
        end
    end  
    % Generational replacement
    population = InsertBestIndividual(newPopulation, bestIndividualEver, nbrOfCopies);     
end

disp('Shortest path length')
disp(1/bestFitnessEver)
disp('Found in genereation')
disp(bestGen)