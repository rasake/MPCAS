function [ visibility ] = GetVisibility( cityLocations )
%GETVISIBILITY Returns matrix with visibility of each edgde defined as the
%inverse of the Euclidian distance between corresponding nodes
nbrOfCities = length(cityLocations);

visibility = zeros(nbrOfCities, nbrOfCities);

for j=1:nbrOfCities
    jLoc = cityLocations(j);
    for i=1:nbrOfCities
        iLoc = cityLocations(i);
        ijDistance = norm(iLoc-jLoc);
        visibility(i,j) = 1/ijDistance;
    end
end
end

