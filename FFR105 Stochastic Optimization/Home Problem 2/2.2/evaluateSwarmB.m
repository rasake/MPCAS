function [functionValues] = evaluateSwarmB(positionMatrix)
positionMatrix = round(positionMatrix);

nbrOfParticles = size(positionMatrix,1);
functionValues = zeros(nbrOfParticles,1);
Q = [35 -20 -10 32 -10
    -20 40 -6 -31 32
    -10 -6 11 -6 -10
    32 -31 -6 38 -20
    -10 32 -10 -20 31];
c = -[15; 27; 36; 18; 12];

%functionValues = c'*positionMatrix' + positionMatrix * Q * positionMatrix';
for i=1:nbrOfParticles
    iX = positionMatrix(i,:)';
    functionValues(i) = c'*iX + iX'*Q*iX;
end

end

