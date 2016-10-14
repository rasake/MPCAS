function [ newPositionMatrix] = Craziness(positionMatrix, crazinessProbability, positionMin, positionMax)

nbrOfParticles = size(positionMatrix,1);
searchSpaceDim = size(positionMatrix,2);
newPositionMatrix = positionMatrix;
for i=1:nbrOfParticles
   for j = 1:searchSpaceDim
       if  rand < crazinessProbability
           newPositionMatrix(i,j) = positionMin + rand*(positionMax-positionMin);
       end
   end
end

end

