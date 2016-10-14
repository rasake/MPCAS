function [ mutatedChromosome ] = CreepMutate( chromosome, mutationProbability, creepRate )

nGenes = size(chromosome,2);
mutatedChromosome = chromosome;
for j = 1:nGenes
    r=rand;
    if (r < mutationProbability)       
        mutatedChromosome(j) = chromosome(j)+randn*creepRate;
    end
end

end