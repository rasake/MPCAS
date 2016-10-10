function population = InitializePopulation(populationSize,minChromosomeLength, maxChromosomeLength, nbrOperators, nbrVarRegisters, nbrConstRegisters);
population = [];
for i = 1:populationSize
 chromosomeLength = minChromosomeLength + fix(rand*(maxChromosomeLength-minChromosomeLength+1));
 nbrInstructions = ceil(chromosomeLength/4);
 tmpChromosome = [];
 for i=1:nbrInstructions
    gene1 = randi(nbrOperators);
    gene2 = randi(nbrVarRegisters);
    gene3 = randi(nbrVarRegisters+nbrConstRegisters);
    gene4 = randi(nbrVarRegisters+nbrConstRegisters);
    tmpInstruction = [gene1 gene2 gene3 gene4];
 tmpChromosome = [tmpChromosome tmpInstruction];
 end
 tmpIndividual = struct('Chromosome',tmpChromosome);
 population = [population tmpIndividual];
end

