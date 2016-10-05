function [ iSelected ] = TournamentSelect( fitness, tournamentSelectionParameter, tournamentSize )

populationSize = size(fitness,1);
indicesContestants = zeros(1,tournamentSize);
fitnessContestants = zeros(1,tournamentSize);
% Randomly Select individuals to enter the tournament
for k = 1:tournamentSize
    kIndex = 1 + fix(rand*populationSize);
    kFitness = fitness(kIndex);
    indicesContestants(k) = kIndex;
    fitnessContestants(k) = kFitness;
end

iSelected = tournamentHeat(fitnessContestants, indicesContestants, tournamentSelectionParameter);

end


function iSelected = tournamentHeat(fitnessContestants, indicesContestants, tournamentSelectionParameter)
r = rand;
if r < tournamentSelectionParameter % return best individual
    [fitnessBest, localIndicesBestIndivuals] = max(fitnessContestants); % Note that there may be more than one best indivudal
    iBestIndividual = indicesContestants(localIndicesBestIndivuals(1)); % In the case of multiple best individuals we choose the first one
    iSelected = iBestIndividual;
elseif length(fitnessContestants) == 1 % return worst individual
    iSelected = indicesContestants;
else % Remove best individual from tournament and have anoher heat
    [fitnessBest, indexTmp] = max(fitnessContestants); % Note that there may be more than one best indivudal
    localIndexBestIndivual = indexTmp(1);  % In the case of multiple best individuals we choose the first one
    fitnessContestants = [fitnessContestants(1:localIndexBestIndivual-1) fitnessContestants(localIndexBestIndivual+1:end)];
    indicesContestants = [indicesContestants(1:localIndexBestIndivual-1) indicesContestants(localIndexBestIndivual+1:end)];
    iSelected = tournamentHeat(fitnessContestants, indicesContestants, tournamentSelectionParameter);
end


end