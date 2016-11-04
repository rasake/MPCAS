function [ trainData, valData ] = LoadData
data = dlmread('task3_data.txt');
nbrDataPoints = length(data);
[trainData, idx] = datasample(data,fix(nbrDataPoints*0.7), 'Replace', false);
valData = data;
valData(idx,:) = [];
end

