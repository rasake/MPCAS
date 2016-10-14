function [ modifiedChromosome ] = LimitLength(chromosome, maxChromosomeLength)

if length(chromosome) > maxChromosomeLength
    modifiedChromosome = chromosome(1:maxChromosomeLength);
else
    modifiedChromosome = chromosome;
end

end

