function [ iSelected ] = RWS(cumulativeFitnesses)
r = rand;
A = r > cumulativeFitnesses;
iSelected = find(A==0, 1, 'first');
end

