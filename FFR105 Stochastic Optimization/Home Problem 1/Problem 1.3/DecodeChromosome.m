function [ x ] = DecodeChromosome( chromosome, nbrOfVariables,variableRange )

nGenes = size(chromosome,2);
genesPerVariable = nGenes/nbrOfVariables;

x = zeros(1, nbrOfVariables);
for j = 1:nbrOfVariables;
    startIndex = (j-1)*genesPerVariable + 1;
    stopIndex = j*genesPerVariable;
    jTemp = 0;
    iPower = 1;
    for iPosition = startIndex:stopIndex
        jTemp = jTemp + chromosome(iPosition)*2^(-iPower); % jTemp in range [-0.5,0.5]
        iPower = iPower + 1;
    end
    x(j) = -variableRange + 2*variableRange/(1-2^(-genesPerVariable)) * jTemp; % Rescaling to requested range
end

