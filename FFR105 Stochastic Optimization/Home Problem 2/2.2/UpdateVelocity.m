function  [newVelocityMatrix] = UpdateVelocity(positionMatrix, velocityMatrix, ...
    bestPositionsMatrix, bestPositionEver, c1, c2, deltaT, inertiaWeight, vMax)
%UPDATEVELOCITY Summary of this function goes here
%   Detailed explanation goes here

nbrOfParticles = size(positionMatrix,1);
newVelocityMatrix = velocityMatrix;
for i = 1:nbrOfParticles
   iPos = positionMatrix(i,:);
   iVel = velocityMatrix(i,:);
   iBestPos = bestPositionsMatrix(i,:);
   iNewVel = inertiaWeight*iVel + c1*rand*(iBestPos-iPos)/deltaT + ...
       c2*rand*(bestPositionEver-iPos)/deltaT;
   
   % restrict velocity
   iNewVel = max(iNewVel, -vMax);
   iNewVel = min(iNewVel, vMax);   
   newVelocityMatrix(i,:) = iNewVel; 
end
end

