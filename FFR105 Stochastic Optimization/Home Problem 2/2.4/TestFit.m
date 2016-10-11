
bestChromosomeEver = [1  4  2  6  1  1  2  6  1  3  6  6  1  3  6  2  3  2  2  6  2  1  5  5  1  3  2  3  1  2  6  4  3  2  3  2];
nbrVarRegisters = 4;
constants = [1 -1];

functionData = LoadFunctionData;
nbrDataPoints = size(functionData,1);

resultingFunction = InstructionsToString(bestChromosomeEver, nbrVarRegisters, constants);
disp('Best function found')
disp(['y = ' resultingFunction])
y_hat = zeros(1,nbrDataPoints);
for i = 1:nbrDataPoints
    y_hat(i) = RunInstructions(functionData(i,1), bestChromosomeEver, nbrVarRegisters, constants);    
end

hold on
plot(functionData(:,1), functionData(:,2))
plot(functionData(:,1), y_hat, 'r*')

