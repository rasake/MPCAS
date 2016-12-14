%% Test algorithm

clear all
clc
nbrNodes = 200;
c=22;
adjacancyMatrix = zeros(nbrNodes,nbrNodes);
for i=1:c/2
    tmp = ones(nbrNodes-i,1);
    adjacancyMatrix = adjacancyMatrix + diag(tmp,i);
    tmp = ones(i,1);
    adjacancyMatrix = adjacancyMatrix + diag(tmp,nbrNodes-i);
end
adjacancyMatrix = adjacancyMatrix + adjacancyMatrix';
clusteringC = ClusteringCoefficient(adjacancyMatrix)
theoC = 0.75*(c-2)/(c-1)

%% Actual 
clear all
A = LoadSmallworld; % loads small-world network in variable A
G = graph(A);
clusteringC = ClusteringCoefficient(A)
plot(G)
title(['Small World Example Network, Clust.coeff.: ' num2str(clusteringC)])

