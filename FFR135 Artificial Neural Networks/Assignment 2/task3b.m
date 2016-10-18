clear all
close all
clc

maxNbrRadFunctions = 20;
nbrInputNodes = 2;
etaUnsup= 0.02;
etaSup = 0.1;
tMaxUnsup = 1e5;
tMaxSup = 3e3;
beta = 0.5;
nbrTrials = 20;

classErrorAverages = zeros(1,maxNbrRadFunctions);
parfor k = 1:maxNbrRadFunctions
    nbrRadialFunctions = k;
    classErrorList = ones(1,nbrTrials);
    networksStruct = struct;
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
    classErrorAverages(k) = mean(classErrorList);
end

%% Plot results

plot(classErrorAverages)
xlabel('Number of raidial functions')
ylabel('Average classification error')

title('Classification error of hybrid nework')
