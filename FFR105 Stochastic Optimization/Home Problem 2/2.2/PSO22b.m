clear all
clc
close all

nbrOfParticles = 30;
nbrOfGenerations = 1000;
searchSpaceDim = 5;
positionMin = -30;
positionMax = 30;
crazinessProbability = 1/nbrOfParticles;
deltaT = 1;
vMax = (positionMax-positionMin) / deltaT;
c1=1;
c2=1;
startingInertiaWeight = 1.4;
lowerBoundInertiaWeight = 0.35;
beta = 0.996;


[positionMatrix, velocityMatrix] = InitializeParticles(nbrOfParticles,...
    searchSpaceDim, positionMin, positionMax, deltaT);
bestPositionsMatrix = positionMatrix;
bestPositionEver = positionMatrix(1,:);


inertiaWeight = startingInertiaWeight;
for k = 1:nbrOfGenerations
inertiaWeight = max(inertiaWeight*beta, lowerBoundInertiaWeight);
    
functionValues = evaluateSwarmB(positionMatrix);
functionValuesBestPositions = evaluateSwarmB(bestPositionsMatrix);
minimum = evaluateSwarmB(bestPositionEver);

% Update best positions
for i=1:nbrOfParticles
    if functionValues(i) < functionValuesBestPositions(i)
        bestPositionsMatrix(i,:) = positionMatrix(i,:);
    end
    if functionValues(i) < minimum
        bestPositionEver = positionMatrix(i,:);
    end
end


velocityMatrix = UpdateVelocity(positionMatrix, velocityMatrix, ...
    bestPositionsMatrix, bestPositionEver, c1, c2, deltaT, inertiaWeight, vMax);
positionMatrix = positionMatrix + velocityMatrix * deltaT;

positionMatrix = Craziness(positionMatrix, crazinessProbability, positionMin, positionMax);

end

disp('Best position found')
disp(round(bestPositionEver))
disp('with function value')
disp(minimum)
