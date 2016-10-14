function [ mutatedChromosome ] = Mutate( chromosome, mutationProbability )
%MUTATE Perform swap mutatation with given mutation probability
%for each gene

nGenes = size(chromosome,2);
mutatedChromosome = chromosome;
for i = 1:nGenes
    r=rand;
    if (r < mutationProbability)
        iAllele = mutatedChromosome(i);
        j = randi(nGenes);
        jAllele = mutatedChromosome(j);
        mutatedChromosome(i) = jAllele;
        mutatedChromosome(j) = iAllele;
    end
end

end