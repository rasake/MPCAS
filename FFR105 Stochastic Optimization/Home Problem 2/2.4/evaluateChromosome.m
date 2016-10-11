function [ fitness ] = evaluateChromosome( chromosome, functionData, nbrVariableRegisters, constants)

nbrDataPoints = size(functionData,1);
rmsSum = 0;
for i = 1:nbrDataPoints
    x = functionData(i,1);
    y = functionData(i,2);
    y_hat = RunInstructions(x,chromosome,nbrVariableRegisters,constants);
    rmsSum = rmsSum + (y_hat-y)^2;
end
rms = sqrt(rmsSum/nbrDataPoints);
fitness = 1/rms;
end