function [ tour, totalTourLength ] = GetNearestNeighbourPath(cityLocations)
totalTourLength = 0;

nbrOfCities = length(cityLocations);

tour = zeros(1,nbrOfCities);
jLoc = randi(nbrOfCities);
tour(1) = jLoc;

for j = 1:nbrOfCities-1
    jLoc = cityLocations(tour(j),:);
    jShortestDistance = Inf;

    for i = 1:nbrOfCities
        iLoc = cityLocations(i,:);
        ijDistance = norm(jLoc - iLoc);
        if ~any(tour==i) && ijDistance < jShortestDistance
            jBestIndex = i;
            jShortestDistance = ijDistance;
        end
    end
    tour(j+1) = jBestIndex;
    totalTourLength = totalTourLength + jShortestDistance;
end

% go back to original city
lastLoc =  cityLocations(tour(end),:);
firstLoc = cityLocations(tour(1),:);
totalTourLength = totalTourLength + norm(lastLoc-firstLoc);


end

