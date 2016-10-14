% test EvaluateIndividual


%% Test simple path

% Load City Locations
cityLocations = [0,0;2,0;2,2;0,2];
path = [1,2,3,4];
expectedPathLength = 8;
expectedFitness = 1/expectedPathLength;
calculatedFitness = EvaluateIndividual(path, cityLocations);
assert(expectedFitness == calculatedFitness);

%% Test symmetric path

% Load City Locations
cityLocations = [0,0;2,0;2,2;0,2];
path = [1,3,2,4];
expectedPathLength = 4*(1+sqrt(2));
expectedFitness = 1/expectedPathLength;
calculatedFitness = EvaluateIndividual(path, cityLocations);
assert(expectedFitness == calculatedFitness);


%% Test advanced path

% Load City Locations
cityLocations = [0,0;2,0;3,2;0,2];
path = [1,3,2,4];
expectedPathLength = sqrt(13) + sqrt(5) + 2*sqrt(2) + 2;
expectedFitness = 1/expectedPathLength;
calculatedFitness = EvaluateIndividual(path, cityLocations);
assert(expectedFitness == calculatedFitness);


%% Test path from example cities

% Load City Locations
cityLocations = LoadCityLocations();
cityLocations = cityLocations(1:4,:);
path = [4,1,3,2];
expectedFitness = 0.0494;
calculatedFitness = EvaluateIndividual(path, cityLocations);
assert(expectedFitness - calculatedFitness < 0.0001);




%% Compare 5-city route

% Load City Locations
nbrCitiesInRoute = 4;
cityLocations = LoadCityLocations();
cityLocations = cityLocations(1:nbrCitiesInRoute,:);
path = randperm(nbrCitiesInRoute);
fitnessHampus = EvaluateIndividual(path, cityLocations);
fitnessRasmus = EvaluateIndividualR(path, cityLocations);
assert(fitnessHampus == fitnessRasmus);


%% Compare 6-city route

% Load City Locations
nbrCitiesInRoute = 6;
cityLocations = LoadCityLocations();
cityLocations = cityLocations(1:nbrCitiesInRoute,:);
path = randperm(nbrCitiesInRoute);
fitnessHampus = EvaluateIndividual(path, cityLocations);
fitnessRasmus = EvaluateIndividualR(path, cityLocations);
assert(fitnessHampus == fitnessRasmus);



%% Compare 50-city route

% Load City Locations
cityLocations = LoadCityLocations();
numberOfGenes = length(cityLocations);
path = randperm(numberOfGenes);
fitnessHampus = EvaluateIndividual(path, cityLocations);
fitnessRasmus = EvaluateIndividualR(path, cityLocations);
assert(fitnessHampus == fitnessRasmus);
