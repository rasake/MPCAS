function [functionValues] = evaluateSwarmA(positionMatrix)
nbrOfParticles = size(positionMatrix,1);
functionValues = zeros(nbrOfParticles,1);
for i=1:nbrOfParticles
    iX = positionMatrix(i,1);
    iY = positionMatrix(i,2);
    functionValues(i) = 1 + (-13+iX-iY^3+5*iY^2-2*iY)^2 + (-29+iX+iY^3+iY^2-14*iY)^2;
end
end

