% This is just a wrapper file that makes several atttempts at using the LGP
% function to find a fit
clear all
clc

nbrTrials = 4;
chromosomes = cell(1, nbrTrials);
fitness = zeros(1, nbrTrials);
parfor i = 1:nbrTrials
    [iBestChromosome, iBestFitness] = LGP;    
    chromosomes{i} = iBestChromosome;
    fitness(i) = iBestFitness;
    fid = fopen(['results_' num2str(i) '.txt'],'wt');
    fprintf(fid, num2str(iBestChromosome));
    fclose(fid);
end
[value,index] = max(fitness);
bestEver = chromosomes{index};
disp('Best chromosome found')
disp(bestEver)
clear all
