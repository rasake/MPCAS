function [ fitness ] = EvaluateIndividual( chromosome, cityLocations )
%EVALUATEINDIVIDUAL Calculates the fitness defined as the inverse of the
%total length of the path

route = [chromosome chromosome(1)];

totDistance = 0;

for i=1:length(route)-1
    positionCityA = cityLocations(route(i));
    positionCityB = cityLocations(route(i+1));
    
    iDistance= norm(positionCityB - positionCityA);
    totDistance = totDistance + iDistance;

fitness = 1 / totDistance;
end

