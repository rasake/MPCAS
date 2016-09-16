%%
points = []
fitnesses = []

for i = 1:50
    FunctionOptimization;
    points= [points; xBest];
    fitnesses = [fitnesses; maximumFitness];
end

mean(fitnesses);
[maxFit, index] = max(fitnesses);
xBest = points(index,:);
disp('///////////////////////')
disp(['Average Best Fitness: ' num2str(mean(fitnesses)) ])
disp(['STD Best Fitness: ' num2str(std(fitnesses)) ])
disp(['Max Best Fitness: ' num2str(maxFit) ])
disp(['Best x found: ' num2str(xBest)])
disp('///////////////////////')



% R
%///////////////////////
% Average Best Fitness: 0.13547
% STD Best Fitness: 0.13892
% Max Best Fitness: 0.33333
% Best x found: 0.0002   -0.9999
% //////////////////
% populationSize = 30;
% numberOfGenes = 30;
% crossOverProbability = 0.8;
% mutationProbability = 0.025;
% tournamentSelectionParameter = 0.75;
% tournamentSize = 2;
% nbrOfCopies = 1;
% variableRange = 5.0;
% numberOfGenerations = 100;
% fitness = zeros(populationSize,1);



% H
% ///////////////////////
% Average Best Fitness: 0.11071
% STD Best Fitness: 0.13602
% Max Best Fitness: 0.33333
% Best x found: 0.00015259    -0.99994
% ///////////////////////
% populationSize = 30;
% numberOfGenes = 30;
% crossoverProbability = 0.8;
% mutationProbability = 0.025;
% tournamentSelectionParameter = 0.75;
% tournamentSize = 2;
% variableRange = 5.0;
% numberOfVariables = 2;
% numberOfGenerations = 100;
% fitness = zeros(populationSize,1);
% nbrBestIndividualsToInsert = 1;


% R
% ///////////////////////
% Average Best Fitness: 0.20309
% STD Best Fitness: 0.15375
% Max Best Fitness: 0.33333
% Best x found: 0.00015259    -0.99994
% ///////////////////////
% populationSize = 30;
% numberOfGenes = 30;
% crossOverProbability = 0.8;
% mutationProbability = 0.1;
% tournamentSelectionParameter = 0.75;
% tournamentSize = 2;
% nbrOfCopies = 1;
% variableRange = 5.0;
% numberOfGenerations = 100;
% fitness = zeros(populationSize,1);

% R
% ///////////////////////
% Average Best Fitness: 0.16151
% STD Best Fitness: 0.14388
% Max Best Fitness: 0.33333
% Best x found: 0.00015259    -0.99994
% ///////////////////////
% populationSize = 30;
% numberOfGenes = 30;
% crossOverProbability = 0.8;
% mutationProbability = 0.025;
% tournamentSelectionParameter = 0.75;
% tournamentSize = 5;
% nbrOfCopies = 1;
% variableRange = 5.0;
% numberOfGenerations = 100;
% fitness = zeros(populationSize,1);


% R
% ///////////////////////
% Average Best Fitness: 0.13058
% STD Best Fitness: 0.14395
% Max Best Fitness: 0.33333
% Best x found: 0.00015259    -0.99994
% ///////////////////////
% populationSize = 30;
% numberOfGenes = 30;
% crossOverProbability = 0.8;
% mutationProbability = 0.025;
% tournamentSelectionParameter = 0.6;
% tournamentSize = 2;
% nbrOfCopies = 1;
% variableRange = 5.0;
% numberOfGenerations = 100;
% fitness = zeros(populationSize,1);

% R
% ///////////////////////
% Average Best Fitness: 0.22117
% STD Best Fitness: 0.1339
% Max Best Fitness: 0.33333
% Best x found: 0.00015259    -0.99994
% ///////////////////////
% populationSize = 30;
% numberOfGenes = 30;
% crossOverProbability = 0.8;
% mutationProbability = 0.05;
% tournamentSelectionParameter = 0.6;
% tournamentSize = 2;
% nbrOfCopies = 1;
% variableRange = 5.0;
% numberOfGenerations = 100;
% fitness = zeros(populationSize,1);

% R
% ///////////////////////
% Average Best Fitness: 0.20869
% STD Best Fitness: 0.13754
% Max Best Fitness: 0.33333
% Best x found: 0.00015259    -0.99994
% ///////////////////////
% populationSize = 30;
% numberOfGenes = 30;
% crossOverProbability = 0.8;
% mutationProbability = 0.05;
% tournamentSelectionParameter = 0.6;
% tournamentSize = 4;
% nbrOfCopies = 1;
% variableRange = 5.0;
% numberOfGenerations = 100;
% fitness = zeros(populationSize,1);



% R
% ///////////////////////
% Average Best Fitness: 0.24522
% STD Best Fitness: 0.1366
% Max Best Fitness: 0.33333
% Best x found: 0.00015259    -0.99994
% ///////////////////////
% populationSize = 30;
% numberOfGenes = 30;
% crossOverProbability = 0.75;
% mutationProbability = 0.1;
% tournamentSelectionParameter = 0.6;
% tournamentSize = 4;
% nbrOfCopies = 1;
% variableRange = 5.0;
% numberOfGenerations = 100;
% fitness = zeros(populationSize,1);