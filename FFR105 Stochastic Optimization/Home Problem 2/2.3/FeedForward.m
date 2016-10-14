function [ output ] = FeedForward( input, weights, thresholds, beta )
%FEEDFORWARD weights should be a cell storing the weight matrices, input
%should be a column vector, thresholds should be a cell storing the treshold
%vectors

nbrLayers = length(weights) + 1;
nodes = cell(1,nbrLayers);
nodes{1} = input;
for i = 1:nbrLayers-1
    iInput = nodes{i};
    iWeightMatrix = weights{i};
    iThresholds = thresholds{i};
    iLocalField = iWeightMatrix*iInput-iThresholds;
    iOutput = tanh(beta*iLocalField);
    nodes{i+1} = iOutput;
end

output = nodes{end};

end
