function [ data ] = ExcessDegreeDistr( A, nbrSamples )
%EXCESSDEGREEDISTR Summary of this function goes here
%   Detailed explanation goes here

data = [];
while length(data)<nbrSamples
    rnode = randi(length(A));
    neighbours = find(logical(A(rnode,:)));
    if ~isempty(neighbours)
        nodeToSample = neighbours(randi(length(neighbours)));
        iDegree = sum(A(nodeToSample,:))-1;
        data = [data iDegree];
    end
end

