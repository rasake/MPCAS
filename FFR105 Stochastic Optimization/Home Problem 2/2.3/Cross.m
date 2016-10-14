function [ newChromosome1, newChromosome2 ] = Cross( chromosome1, chromosome2)
%CROSS Chromosomes ar assumed to have same length

nGenes = size(chromosome1,2);
crossoverPoint = randi(nGenes);

newChromosome1 = [chromosome1(1:crossoverPoint) chromosome2(crossoverPoint+1:end)];
newChromosome2 = [chromosome2(1:crossoverPoint) chromosome1(crossoverPoint+1:end)];
end