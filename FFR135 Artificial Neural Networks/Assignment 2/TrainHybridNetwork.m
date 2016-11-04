function [ radialWeigths, perceptronWeights, peceptronThreshold, classificationError, trainData, valData] = TrainHybridNetwork( nbrInputNodes, nbrRadialFunctions,...
    etaUnsup, etaSup, tMaxUnsup, tMaxSup, beta)


%% Load data
[trainData, valData] = LoadData;
nbrDataPointsTrain = length(trainData);
nbrDataPointsVal = length(valData);



%% Initialize weights and threshold
radialWeigths = 2*rand(nbrRadialFunctions, nbrInputNodes)-1;
perceptronWeights = 2*rand(nbrRadialFunctions,1)-1;
peceptronThreshold = 2*rand-1;

%% Unsupervised learning
% TODO randomly select pattern

for t = 1:tMaxUnsup
    r = randi(nbrDataPointsTrain);
    pattern = trainData(r,2:end)';
    radialNeuronValues = zeros(nbrRadialFunctions,1);
    for i = 1:nbrRadialFunctions
        radius = norm(pattern-radialWeigths(i,:)');
        radialNeuronValues(i,1) = exp(-radius^2/2);
    end
    radialNeuronValues = radialNeuronValues/sum(radialNeuronValues);
    [val, winning_index] = max(radialNeuronValues);
    delta_win = etaUnsup*(pattern'-radialWeigths(winning_index,:));
    radialWeigths(winning_index,:) = radialWeigths(winning_index,:) + delta_win;
end


%% Supervised learning
for t = 1:tMaxSup
    %randomly select pattern
    r = randi(nbrDataPointsTrain);
    pattern = trainData(r,2:end)';
    expectedOutput = trainData(r,1);
    %Feed forward
    radialNeuronValues = zeros(nbrRadialFunctions,1);
    for i = 1:nbrRadialFunctions
        radius = norm(pattern-radialWeigths(i,:)');
        radialNeuronValues(i,1) = exp(-radius^2/2);
    end
    radialNeuronValues = radialNeuronValues/sum(radialNeuronValues);
    localField = perceptronWeights' * radialNeuronValues  - peceptronThreshold;
    networkOutput = tanh(beta*localField);
    %Propogate back, percepton layer only!
    outputError = gPrime(localField,beta)*(expectedOutput-networkOutput);
    deltaPerceptronWeights = etaSup*outputError*radialNeuronValues;
    deltaPerceptronThreshold = etaSup*(-outputError);
    perceptronWeights = perceptronWeights + deltaPerceptronWeights;
    peceptronThreshold = peceptronThreshold + deltaPerceptronThreshold;
end

%% Classification error for validation set
errorSum = 0;
for k = 1:nbrDataPointsVal
    pattern = valData(k,2:end)';
    expectedOutput = valData(k,1);
    %Feed forward
    radialNeuronValues = zeros(nbrRadialFunctions,1);
    for i = 1:nbrRadialFunctions
        radius = norm(pattern-radialWeigths(i,:)');
        radialNeuronValues(i,1) = exp(-radius^2/2);
    end
    radialNeuronValues = radialNeuronValues/sum(radialNeuronValues);
    localField = perceptronWeights' * radialNeuronValues - peceptronThreshold;
    networkOutput = tanh(beta*localField);
    iError = abs(expectedOutput-sign(networkOutput));
    errorSum = errorSum + iError;
end
classificationError = 0.5 * errorSum/nbrDataPointsVal;
    
end

