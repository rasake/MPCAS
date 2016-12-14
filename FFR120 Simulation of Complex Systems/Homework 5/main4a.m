%% %%%%%%%% More vaccination %%%%%%%%%%%%
clear all
clc


%% %%%%%%%%%%%%%%% Random Graph %%%%%%%%%%%%%%
subplot(1,2,1)
p = 0.015;
nbrNodes = 300;
nbrDataPoints = 50;
nbrRealisations = 50;

%% Random Vaccination
f = linspace(0,1,nbrDataPoints);
A0 = ERadjecencyMatrix( p,nbrNodes );
clstrSizesR = zeros(nbrDataPoints,1);
for i=1:nbrDataPoints
    nbrNodesToDel = floor(f(i)*nbrNodes);
    relClst = zeros(nbrRealisations,1);
    for j=1:nbrRealisations
        A = A0;
        jumbledNodes = randperm(nbrNodes);
        nodesToDelete = jumbledNodes(1:nbrNodesToDel);
        A(nodesToDelete,:) = [];
        A(:,nodesToDelete) = [];
        G = graph(A);
        c = conncomp(G);
        relClst(j) = sum(c==1)/nbrNodes;
    end
    clstrSizesR(i) = mean(relClst);
end
plot(f,clstrSizesR)
hold on
%% Smart Vaccination 1
f = linspace(0,1,nbrDataPoints);
A0 = ERadjecencyMatrix( p,nbrNodes );
clstrSizesS = zeros(nbrDataPoints,1);
for i=1:nbrDataPoints
    nbrNodesToDel = floor(f(i)*nbrNodes);
    relClst = zeros(nbrRealisations,1);
    for j=1:nbrRealisations
        A = A0;
        D = sum(A);
        [sortedValues,sortIndex] = sort(D,'descend');
        nodesToDelete = sortIndex(1:nbrNodesToDel);
        A(nodesToDelete,:) = [];
        A(:,nodesToDelete) = [];
        G = graph(A);
        c = conncomp(G);
        relClst(j) = sum(c==1)/nbrNodes;
    end
    clstrSizesS(i) = mean(relClst);
end
plot(f,clstrSizesS)
%% Smart Vaccination 2
f = linspace(0,1,nbrDataPoints);
A0 = ERadjecencyMatrix( p,nbrNodes );
clstrSizesS2= zeros(nbrDataPoints,1);
for i=1:nbrDataPoints
    nbrNodesToDel = floor(f(i)*nbrNodes);
    relClst = zeros(nbrRealisations,1);
    for j=1:nbrRealisations
        A = A0;
        A = vaccinateNeighbours( A, nbrNodesToDel);
        G = graph(A);
        c = conncomp(G);
        relClst(j) = sum(c==1)/nbrNodes;
    end
    clstrSizesS2(i) = mean(relClst);
end
plot(f,clstrSizesS2)
hold off
xlabel('Fraction of nodes remove')
ylabel('Size of largest cluster')
legend(['Random Vaccination', 'Vaccinating Nodes with High Degree'])
title('Effect of vaccination on Random Graph')
legend('Random Vaccination', 'Vaccinating Nodes with High Degree', 'Vaccinating Neighbours')
xlabel('Fraction of nodes removed')





%%  %%%%%%%%%%% Pref. Growth Network %%%%%%%%%%%%%%%%%
subplot(1,2,2)
n0 = 5;
m = 3;
nbrNewNodes = 300;
nbrNodes = n0+nbrNewNodes;
nbrDataPoints = 50;
nbrRealisations = 50;

%% Random Vaccination
f = linspace(0,1,nbrDataPoints);
clstrSizesR = zeros(nbrDataPoints,1);
G0 = MakePrefNetwork(n0,m,nbrNewNodes);
for i=1:nbrDataPoints
    nbrNodesToDel = floor(f(i)*nbrNodes);
    relClst = zeros(nbrRealisations,1);
    for j=1:nbrRealisations
        A = adjacency(G0);
        jumbledNodes = randperm(nbrNodes);
        nodesToDelete = jumbledNodes(1:nbrNodesToDel);
        A(nodesToDelete,:) = [];
        A(:,nodesToDelete) = [];
        G = graph(A);
        c = conncomp(G);
        relClst(j) = sum(c==1)/nbrNodes;
    end
    clstrSizesR(i) = mean(relClst);
end
plot(f,clstrSizesR)
hold on


%% Smart Vaccination 1
f = linspace(0,1,nbrDataPoints);

clstrSizesS= zeros(nbrDataPoints,1);
G0 = MakePrefNetwork(n0,m,nbrNewNodes);
for i=1:nbrDataPoints
    nbrNodesToDel = floor(f(i)*nbrNodes);
    relClst = zeros(nbrRealisations,1);
    for j=1:nbrRealisations
        A = adjacency(G0);
        D = sum(A);
        [sortedValues,sortIndex] = sort(D,'descend');
        nodesToDelete = sortIndex(1:nbrNodesToDel);
        A(nodesToDelete,:) = [];
        A(:,nodesToDelete) = [];
        G = graph(A);
        c = conncomp(G);
        relClst(j) = sum(c==1)/nbrNodes;
    end
    clstrSizesS(i) = mean(relClst);
end
plot(f,clstrSizesS)


%% Smart Vaccination 2
f = linspace(0,1,nbrDataPoints);
clstrSizesS2= zeros(nbrDataPoints,1);
G0 = MakePrefNetwork(n0,m,nbrNewNodes);
for i=1:nbrDataPoints
    nbrNodesToDel = floor(f(i)*nbrNodes);
    relClst = zeros(nbrRealisations,1);
    for j=1:nbrRealisations
        A = adjacency(G0);
        A = vaccinateNeighbours( A, nbrNodesToDel);
        G = graph(A);
        c = conncomp(G);
        relClst(j) = sum(c==1)/nbrNodes;
    end
    clstrSizesS2(i) = mean(relClst);
end
%%
plot(f,clstrSizesS2)
hold off
xlabel('Fraction of nodes remove')
ylabel('Size of largest cluster')
legend(['Random Vaccination', 'Vaccinating Nodes with High Degree'])
title('Effect of vaccination on Random Graph')
legend('Random Vaccination', 'Vaccinating Nodes with High Degree', 'Vaccinating Neighbours')
xlabel('Fraction of nodes removed')



