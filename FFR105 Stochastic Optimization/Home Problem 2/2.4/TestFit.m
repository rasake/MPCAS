close all

% Encoding: 4 var.registers, constants = [1 -1]
bestChromosomeEver = [1 3 5 1 1 4 3 1 1 3 4 5 1 2 3 4 4 4 2 1 1 3 4 6 2 2 2 5 1 2 3 2 4 3 1 2 4 1 4 2];

nbrVarRegisters = 4;
constants = [1 -1];

functionData = LoadFunctionData;
nbrDataPoints = size(functionData,1);
x = functionData(:,1);

% Auxiliary code for simplification of results
% resultingFunction = InstructionsToString(bestChromosomeEver, nbrVarRegisters, constants);
% disp('Best function can be simplified to')
% disp(['y = ' resultingFunction])
% y_hat2 = zeros(1,nbrDataPoints);
% for i = 1:nbrDataPoints
%     y_hat2(i) = RunInstructions(x(i), bestChromosomeEver, nbrVarRegisters, constants);    
% end

y_hat= zeros(1,nbrDataPoints);
for i = 1:nbrDataPoints
    y_hat(i) = (4*x(i)+3) / (4*x(i)^2+5*x(i)+3);
end

disp('Best fit found: y = (4x+3)/(4x^2+5x+3)')
disp(['Error: ' num2str(1/evaluateChromosome(bestChromosomeEver,functionData,nbrVarRegisters,constants))])

hold on
plot(functionData(:,1), functionData(:,2))
plot(functionData(:,1), y_hat, 'r')
xlabel('x')
ylabel('y')
legend('Original data', 'Best Fit')

%plot(functionData(:,1), y_hat2, '*')
