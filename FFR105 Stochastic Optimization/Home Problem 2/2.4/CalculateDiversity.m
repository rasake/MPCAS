function [ diversity ] = CalculateDiversity( population, populationSize )
D = 0;
for i = 1:populationSize-1
    iChromosome = population(i).Chromosome;
    for j = i+1:populationSize
        jChromosome = population(j).Chromosome;
        nGenesI = size(iChromosome,2);
        nGenesJ = size(jChromosome,2);
        nGenesMin = min(nGenesI,nGenesJ);
        d = 0;
        for k = 1:nGenesMin
            if iChromosome(k) ~= jChromosome(k)
                d = d+1;
            end
        d = d/nGenesMin;
        end
        D = D+d;   
    end
end
D = 2*D/populationSize/(populationSize-1);
diversity = D;
end

