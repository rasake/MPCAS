clear all
clc
close all

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
plotting = false;


[positionMatrix, velocityMatrix] = InitializeParticles(nbrOfParticles,...
    searchSpaceDim, positionMin, positionMax, deltaT);
bestPositionsMatrix = positionMatrix;
bestPositionEver = positionMatrix(1,:);


inertiaWeight = startingInertiaWeight;
for k = 1:nbrOfGenerations
    inertiaWeight = max(inertiaWeight*beta, lowerBoundInertiaWeight);
    
    functionValues = evaluateSwarmA(positionMatrix);
    functionValuesBestPos = evaluateSwarmA(bestPositionsMatrix);
    minimum = evaluateSwarmA(bestPositionEver);
    
    % Update best positions
    for i=1:nbrOfParticles
        if functionValues(i) < functionValuesBestPos(i)
            bestPositionsMatrix(i,:) = positionMatrix(i,:);
        end
        if functionValues(i) < minimum
            bestPositionEver = positionMatrix(i,:);
        end
    end
    velocityMatrix = UpdateVelocity(positionMatrix, velocityMatrix, ...
        bestPositionsMatrix, bestPositionEver, c1, c2, deltaT, inertiaWeight, vMax);
    positionMatrix = positionMatrix + velocityMatrix * deltaT;
    if plotting
        pause(0.05)
        plot(positionMatrix(:,1), positionMatrix(:,2), 'r*')
        %TODO remove hardcoding
        axis([-40,40,-40,40])
    end
end

disp('Best position found')
disp(bestPositionEver)
disp('with function value ')
disp(minimum)
