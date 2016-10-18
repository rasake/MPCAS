function [XA,YA,XB,YB] = FindDecisionBoundary( radWeights, perWeights, ...
    perThreshold,beta, xMin,xMax,yMin,yMax, resolution )
xgv = linspace(xMin,xMax,resolution);
ygv = linspace(yMin,yMax,resolution);
[X,Y] = meshgrid(xgv,ygv);
X = reshape(X, 1, resolution^2);
Y = reshape(Y, 1, resolution^2);
nbrRadialFunctions = size(radWeights,1);

XA = []; YA = [];
XB = []; YB = [];
for k = 1:resolution^2
    pattern = [X(k);Y(k)];
    %Feed forward
    radialNeuronValues = zeros(nbrRadialFunctions,1);
    for i = 1:nbrRadialFunctions
        radius = norm(pattern-radWeights(i,:)');
        radialNeuronValues(i,1) = exp(-radius^2/2);
    end
    radialNeuronValues = radialNeuronValues/sum(radialNeuronValues);
    localField = perWeights' * radialNeuronValues - perThreshold;
    networkOutput = tanh(beta*localField);
    if networkOutput >= 0
        XA = [XA X(k)];
        YA = [YA Y(k)];
    else
        XB = [XB X(k)];
        YB = [YB Y(k)];
    end
end

end

