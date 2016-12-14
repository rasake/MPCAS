%% Erdos-Renyi %%
clear all
clc
nbrNodes = 500;
p = 0.2;
maxK = nbrNodes-1;
adjacencyMatrix = ERadjecencyMatrix(p,nbrNodes);
degreeDist = DegreDistribution(adjacencyMatrix);
G=graph(adjacencyMatrix);

subplot(1,2,1)
plot(G)
title('Erdos-Renyi Network')
subplot(1,2,2)
histogram(degreeDist,'Normalization','pdf')
hold on


maxDegree = max(degreeDist);
k=0:1:maxDegree;
theoProb = zeros(maxDegree+1,1);
for i=1:maxDegree+1
    theoProb(i) = theroritcalDegreeDistER(p,nbrNodes,k(i));
end
plot(k,theoProb)
title('Degree Distribution')
xlabel('Degree')
xlabel('Frequency')


