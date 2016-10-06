function [positionMatrix, velocityMatrix] = InitializeParticles(nbrOfParticles, ...
    searchSpaceDim, positionMin, positionMax, deltaT)

positionMatrix = zeros(nbrOfParticles, searchSpaceDim);
velocityMatrix = zeros(nbrOfParticles, searchSpaceDim);
for i = 1:nbrOfParticles
   for j = 1:searchSpaceDim
       positionMatrix(i,j) = positionMin + rand*(positionMax-positionMin);
       velocityMatrix(i,j) = (positionMax-positionMin)/deltaT * (-1/2+rand);
   end
end

end

