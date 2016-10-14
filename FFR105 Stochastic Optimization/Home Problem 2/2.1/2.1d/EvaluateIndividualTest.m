% test EvaluateIndividual

%% Test sum of mutated chromosome

% Load City Locations
cityLocations = LoadCityLocations();
numberOfGenes = length(cityLocations);


chromosome = linspace(1,50,50);
disp(EvaluateIndividual(chromosome, cityLocations));
