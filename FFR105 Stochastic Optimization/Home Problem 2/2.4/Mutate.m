function [ newChromosome ] = Mutate(chromosome, mutationProbability, nbrVariableRegisters, nbrConstantRegisters)
%MUTATE Assumes ther are only four operators

nbrGenes = length(chromosome);
nbrOperands = nbrVariableRegisters + nbrConstantRegisters;
newChromosome = chromosome;
for i = 1:nbrGenes
   if rand < mutationProbability
       switch mod(i,4)
           case 1
               newChromosome(i) = randi(4);
           case 2
               newChromosome(i) = randi(nbrVariableRegisters);
           case {3,4}
               newChromosome(i) = randi(nbrOperands);          
       end
   end
end

end

