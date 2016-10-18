clear all
close all
clc

nbrInputNodes = 2;
nbrRadialFunctions = 5;
etaUnsup= 0.02;
etaSup = 0.1;
tMaxUnsup = 1e5;
tMaxSup = 3e3;
beta = 0.5;
nbrTrials = 20;

classErrorList = ones(nbrTrials);
for i = 1:nbrTrials
[radWeights, perWeights, perThreshold, classError, trData,valData] = TrainHybridNetwork(nbrInputNodes, ...
    nbrRadialFunctions, etaUnsup, etaSup, tMaxUnsup, tMaxSup, beta);
networksStruct(i).radialWeights = radWeights;
networksStruct(i).perceptronWeights = perWeights;
networksStruct(i).perceptronThreshold = perThreshold;
networksStruct(i).trainData = trData;
networksStruct(i).valData = valData;

classErrorList(i) = classError;
end

%% Extract best network
[minError, index] = min(classError);
disp(['Minimal classification error achieved: ' num2str(minError)])
disp(['Average classification error achieved: ' num2str(mean(classErrorList))]);
radWeigths = networksStruct(index).radialWeights;
perWeights = networksStruct(index).perceptronWeights;
perThreshold = networksStruct(index).perceptronThreshold;
valData = networksStruct.valData;


%% Plot decision boundary
xMin = -20;
xMax = 30;
yMin = -10;
yMax = 15;
resolution = 100;
[XA,YA,XB,YB] = FindDecisionBoundary( radWeigths, perWeights, ...
    perThreshold,beta, xMin,xMax,yMin,yMax, resolution );
plot(XA,YA, 'r.', 'MarkerSize', 9)
hold on
plot(XB,YB, 'b.','MarkerSize', 9)


%% Plot input data
allData = dlmread('task3_data.txt');
nbrDataPoints = length(allData);
plot(allData(1:1000,2), allData(1:1000,3), 'r*')
hold on
plot(allData(1001:2000,2), allData(1001:2000,3), 'b*')

%% Plot radial weights
plot(radWeigths(:,1),radWeigths(:,2), 'kd', 'MarkerFaceColor', 'k')

%% Set up labels etc
xlabel('$\xi_1$', 'Interpreter', 'LaTex')
ylabel('$\xi_2$', 'Interpreter', 'LaTex')

legend1 = '$\vec{\xi} : \mathcal{O} \geq 0$';
legend2 = '$\vec{\xi} : \mathcal{O} < 0$';
legend3 = 'Sampled data for which $\zeta \geq 0$';
legend4 = 'Sampled data for which $\zeta < 0$';
legend5 = 'Radial weight vectors';
allLegends = {legend1,legend2,legend3,legend4,legend5};
legend(allLegends, 'Interpreter', 'LaTex', 'FontSize', 8)

titleStr = ['Best clustering achieved with ' num2str(nbrRadialFunctions) ' radial basis functions'];
title(titleStr, 'FontSize', 13)

