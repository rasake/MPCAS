clear all
clc
close all

% TODO Choose suitable parameters
nbrOfParticles = 30;
nbrOfGenerations = 250;
searchSpaceDim = 2;
positionMin = -10;
positionMax = 10;
deltaT = 1;
vMax = (positionMax-positionMin) / deltaT;
c1=2;
c2=2;
startingInertiaWeight = 1.4;
lowerBoundInertiaWeight = 0.3;
beta = 0.95;



[positionMatrix, velocityMatrix] = InitializeParticles(nbrOfParticles,...
    searchSpaceDim, positionMin, positionMax, deltaT);
bestPositionsMatrix = positionMatrix;
bestPositionEver = positionMatrix(1,:);
plot(positionMatrix(:,1), positionMatrix(:,2), 'r*')
%TODO remove hardcoding
axis([-40,40,-40,40])

inertiaWeight = startingInertiaWeight;
fitnessHistory = [];
for k = 1:nbrOfGenerations
inertiaWeight = max(inertiaWeight*beta, lowerBoundInertiaWeight);
    
fitness = evaluateSwarmA(positionMatrix);
bestFitnesses = evaluateSwarmA(bestPositionsMatrix);
bestFitnessEver = evaluateSwarmA(bestPositionEver);

% Update best positions
for i=1:nbrOfParticles
    if fitness(i) < bestFitnesses(i)
        bestPositionsMatrix(i,:) = positionMatrix(i,:);
    end
    if fitness(i) < bestFitnessEver
        bestPositionEver = positionMatrix(i,:);
        fitnessHistory = [fitnessHistory bestFitnessEver];
%         disp('New bestPositionEver')
%         disp(bestPositionEver)
%         disp('with fitness ')
%         disp(bestFitnessEver)
    end
end


velocityMatrix = UpdateVelocity(positionMatrix, velocityMatrix, ...
    bestPositionsMatrix, bestPositionEver, c1, c2, deltaT, inertiaWeight, vMax);
positionMatrix = positionMatrix + velocityMatrix * deltaT;
pause(0.05)
plot(positionMatrix(:,1), positionMatrix(:,2), 'r*')
%TODO remove hardcoding
axis([-40,40,-40,40])

end

