function [ cumFit ] = cumulativeFitnesses( fitnesses )
nbrEntries = length(fitnesses);
tot = sum(fitnesses);
cumFit = zeros(1,nbrEntries);
for i = 1:nbrEntries
cumFit(i) = sum(fitnesses(1:i))/tot;
end

