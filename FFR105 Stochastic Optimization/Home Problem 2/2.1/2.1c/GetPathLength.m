function [ totDistance ] = GetPathLength(path,cityLocations)

route = [path path(1)];

totDistance = 0;

for i=1:length(route)-1
    positionCityA = cityLocations(route(i),:);
    positionCityB = cityLocations(route(i+1),:);
    
    iDistance= norm(positionCityB - positionCityA);
    totDistance = totDistance + iDistance;
end

