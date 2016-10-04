% test GerNearestNeighbourPath

%% Test sum of mutated chromosome

nbrOfGenes = 50;
populationSize = 500;

population = InitializePopulation(populationSize,nbrOfGenes);
expectedSum = nbrOfGenes*(nbrOfGenes+1)/2;
for k=1:populationSize
   chromosome = population(k,:);
   mutatedChromosome = Mutate(chromosome, 0.5);
   mutatedSum = sum(mutatedChromosome);
   assert(mutatedSum == expectedSum);
end


%% Test product of mutated chromosome

nbrOfGenes = 20; %factorial only exact up to N=21
populationSize = 500;

population = InitializePopulation(populationSize,nbrOfGenes);
expectedProduct = factorial(nbrOfGenes);
for k=1:populationSize
   chromosome = population(k,:);
   mutatedChromosome = Mutate(chromosome, 0.5);
   mutatedProduct = prod(mutatedChromosome);
   assert(mutatedProduct == expectedProduct);
end
