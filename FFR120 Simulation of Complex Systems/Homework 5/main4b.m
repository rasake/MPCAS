%% %%%%%%% Degree and Excess Degree %%%%%%%%%%

%% Random Graph
subplot(1,2,1)
p = 0.015;
nbrNodes = 300;

A = ERadjecencyMatrix( p,nbrNodes );
B = ERadjecencyMatrix( p,nbrNodes );
dataA = ExcessDegreeDistr(A, nbrSamples);
dataB = ExcessDegreeDistr(B, nbrSamples);

%%
histogram([sum(A) sum(B)],'Normalization','pdf')
hold on
histogram([dataA dataB],'Normalization','pdf')
legend('Degree', 'Excess Degree')
title('Random Graph')
ylabel('Relative frequency')


%% Pref. Growth Network
subplot(1,2,2)

n0 = 5;
m = 3;
nbrNewNodes = 600;
nbrSamples = 600;

GA = MakePrefNetwork(n0,m,nbrNewNodes);
A = adjacency(GA);
GB = MakePrefNetwork(n0,m,nbrNewNodes);
B = adjacency(GB);
dataA = ExcessDegreeDistr(A, nbrSamples);
dataB = ExcessDegreeDistr(B, nbrSamples);

%%
histogram([sum(A) sum(B)],50,'Normalization','pdf')
hold on
histogram([dataA dataB],50,'Normalization','pdf')
legend('Degree', 'Excess Degree')
title('Preferential Growth Network')
ylabel('Relative frequency')

