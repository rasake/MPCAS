clear all
clc
n0 = 5;
m = 2;
nbrNewNodes = 500;

adjacencyMatrix = zeros(n0,n0);
adjacencyMatrix(1,2:end) = ones(1,n0-1);
adjacencyMatrix(2:end,1) = ones(n0-1,1);
G = graph(adjacencyMatrix);

%% Add edges
for i = 1:nbrNewNodes
    G = AddPrefNode(G,m);
end
%%
subplot(1,2,1)
%%
plot(G, 'Layout','force')
title('Preferential Growth Network')

%% Power law
subplot(1,2,2)
D = degree(G);
[k,freq] = EmpiricalCDF(D);
loglog(k, freq)
hold on
gamma = 3;
theo = m^2*k.^(-gamma+1);
loglog(k,theo,'r')
title('Degree Distribution')
xlabel('Degree')
ylabel('CCDF')
legend('Empirical Distribution', 'Theorethical DIstribution')
hold off