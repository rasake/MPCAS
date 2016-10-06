clear all
clc
close all
% TODO Choose suitable parameters
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
fitnessHistory = [];
for k = 1:nbrOfGenerations
inertiaWeight = max(inertiaWeight*beta, lowerBoundInertiaWeight);
    
fitness = evaluateSwarmB(positionMatrix);
bestFitnesses = evaluateSwarmB(bestPositionsMatrix);
bestFitnessEver = evaluateSwarmB(bestPositionEver);

% Update best positions
for i=1:nbrOfParticles
    if fitness(i) < bestFitnesses(i)
        bestPositionsMatrix(i,:) = positionMatrix(i,:);
    end
    if fitness(i) < bestFitnessEver
        bestPositionEver = positionMatrix(i,:);
        fitnessHistory = [fitnessHistory; bestFitnessEver k];
%         disp('New bestPositionEver')
%         disp(bestPositionEver)
%         disp('with fitness ')
%         disp(bestFitnessEver)
    end
end


velocityMatrix = UpdateVelocity(positionMatrix, velocityMatrix, ...
    bestPositionsMatrix, bestPositionEver, c1, c2, deltaT, inertiaWeight, vMax);
positionMatrix = positionMatrix + velocityMatrix * deltaT;

positionMatrix = Craziness(positionMatrix, crazinessProbability, positionMin, positionMax);

end
round(bestPositionEver)
