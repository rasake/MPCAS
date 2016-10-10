function [ newChromosome1, newChromosome2 ] = Cross( chromosome1, chromosome2, genesPerInstruction )
%CROSS Adapted to linear genetic programming

nGenes1 = size(chromosome1,2);
nGenes2 = size(chromosome2,2);
nGenesMin = min(nGenes1,nGenes2);
tmpA = fix(randi(nGenesMin)/genesPerInstruction);
tmpB = fix(randi(nGenesMin)/genesPerInstruction);
% tmpA = genesPerInstruction*randi(nGenesMin/genesPerInstruction) % Bug: cannot become 1
% tmpB = genesPerInstruction*randi(nGenesMin/genesPerInstruction)
crossoverPointA = min(tmpA, tmpB);
crossoverPointB = max(tmpA, tmpB);

newChromosome1 = [chromosome1(1:crossoverPointA) chromosome2(crossoverPointA+1:crossoverPointB) chromosome1(crossoverPointB+1:end)];
newChromosome2 = [chromosome2(1:crossoverPointA) chromosome1(crossoverPointA+1:crossoverPointB) chromosome2(crossoverPointB+1:end)];

end