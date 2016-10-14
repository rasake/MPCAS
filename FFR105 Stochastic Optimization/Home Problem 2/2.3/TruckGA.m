clear all
clc
global TRUCKMASS MAX_T AMBIENT_T TAU Ch Cb STEP_SIZE MAX_SPEED MAX_ALPHA
global START_SPEED START_GEAR START_T
global NBR_HIDDEN_NEURONS BETA

TRUCKMASS = 20000; %kg
MAX_T = 750; %Kelvin
AMBIENT_T = 283; %Kelvin
TAU = 30; %seconds
Ch = 40; %K/s
Cb = 3000; %N
MAX_SPEED = 25; %m/s
MAX_ALPHA = 10; %degrees
START_SPEED = 20; %m/s
START_GEAR = 7;
START_T = 500; %K

STEP_SIZE = 0.1;

NBR_HIDDEN_NEURONS = 3;
BETA = 0.2;

populationSize = 30;
nbrGenerations = 20;
nbrGenes = 6*NBR_HIDDEN_NEURONS+2;
crossOverProbability = 0.3;
mutationProbability = 1/nbrGenes;
creepRate=0.1;
tournamentSelectionParameter = 0.7;
tournamentSize = 2;
nbrOfCopies = 2;


population = InitializePopulation(populationSize, nbrGenes);


%Evaluation
fitness = zeros(populationSize,1);
bestFitnessEver = 0;
validationFitness = 0;
for k=1:nbrGenerations
    %Evaluation
    for i = 1:populationSize
        fitness(i) = EvaluateChromosome(population(i,:), 1);
        tmp = EvaluateChromosome(population(i,:), 2);
        validationFitness(i) = mean(tmp);
    end

    %Reproduction
    newPopulation = population;
    for i = 1:2:populationSize
        i1 = TournamentSelect(fitness, tournamentSelectionParameter, tournamentSize);
        i2 = TournamentSelect(fitness, tournamentSelectionParameter, tournamentSize);
        chromosome1 = population(i1,:);
        chromosome2 = population(i2,:);
        
        if rand < crossOverProbability
            [chromosome1, chromosome2] = Cross(chromosome1,chromosome2);
        end
        
        newPopulation(i,:) = CreepMutate(chromosome1, mutationProbability, creepRate);
        newPopulation(2*i,:) = CreepMutate(chromosome2, mutationProbability, creepRate);
    end

    %Elitism
    for i = 1:populationSize
        if fitness(i) > bestFitnessEver
            bestIndividualEver = population(i,:);
            bestFitnessEver = fitness(i);
%             disp('New best individual found')
%             %disp(bestIndividualEver)
%             disp('with fitness')
%             disp(bestFitnessEver)
        end
    end
    % Generational replacement
    population = InsertBestIndividual(newPopulation, bestIndividualEver, nbrOfCopies);
    
    % Hold out validation
    if i > 50
        oldAverage = mean(validationFitness(-25,10));
        newAverage = mean(validationFitness(-15:end));
        if newAverage > oldAverage % validation eror is going up
            tapOut = true;
        end
    else
        tapOut = false;
    end
    if tapOut
        break
    end
end



disp('Best individual found')
disp(num2str(bestIndividualEver))
disp('with fitness')
disp(bestFitnessEver)




