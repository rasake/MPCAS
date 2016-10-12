close all
%bestChromosomeEver = [1  4  4  4  1  1  1  2  2  2  2  2  1  4  2  1  1  2  6  6  3  2  1  4  3  3  2  2  2  3  2  6  4  1  1  3  1  3  1  6];
% ganska nära
%bestChromosomeEver = [2  3  1  7  2  5  2  5  3  1  3  6  3  4  3  5  1  5  2  1  4  5  1  6  4  3  7  3  4  1  4  6  1  1  3  6  3  2  6  5  2  2  5  1  4  1  6  2  2  5  6  4  2  4  3  7];
bestChromosomeEver = [1  3  1  3  2  2  3  7  2  4  4  5  1  5  2  2  1  5  4  7  4  3  7  4  3  3  2  7  3  4  2  7  3  2  3  6  3  3  2  3  2  1  7  3  1  4  5  7  4  1  2  1  3  2  2  7];


nbrVarRegisters = 5;
constants = [1 -1];

functionData = LoadFunctionData;
nbrDataPoints = size(functionData,1);
x = functionData(:,1);
resultingFunction = InstructionsToString(bestChromosomeEver, nbrVarRegisters, constants);
disp('Best function can be simplified to')
disp(['y = ' resultingFunction])
y_hat = zeros(1,nbrDataPoints);
for i = 1:nbrDataPoints
    y_hat(i) = RunInstructions(x(i), bestChromosomeEver, nbrVarRegisters, constants);    
end

y_hat2 = zeros(1,nbrDataPoints);
for i = 1:nbrDataPoints
    y_hat2(i) =  (-(x(i)--1))/(-1-(-(x(i)--1))^2);
end



hold on
plot(functionData(:,1), functionData(:,2))
plot(functionData(:,1), y_hat, 'r')
plot(functionData(:,1), y_hat2, 'g*')

