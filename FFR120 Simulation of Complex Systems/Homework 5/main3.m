%% %%%%%%%% Vaccination %%%%%%%%%%%%
clear all
clc


%% Random Graph
p = 0.01;
nbrNodes = 300;
nbrDataPoints = 10;
nbrRealisations = 15;

%% Random Vaccination
f = linspace(0,1,nbrDataPoints);

clstrSizesR = zeros(nbrDataPoints,1);
for i=1:nbrDataPoints
    nbrNodesToDel = floor(f(i)*nbrNodes);
    relClst = zeros(nbrRealisations,1);
    for j=1:nbrRealisations
        A = ERadjecencyMatrix( p,nbrNodes );
        jumbledNodes = randperm(nbrNodes);
        nodesToDelete = jumbledNodes(1:nbrNodesToDel);
        A(nodesToDelete,:) = [];
        A(:,nodesToDelete) = [];
        C = ClusterMatrix(A);
        relClst(j) = max(sum(C))/length(A);
    end
    clstrSizesR(i) = mean(relClst);
end
plot(f,clstrSizesR)
hold on
%% Smart Vaccination
f = linspace(0,1,nbrDataPoints);

clstrSizesS= zeros(nbrDataPoints,1);
for i=1:nbrDataPoints
    nbrNodesToDel = floor(f(i)*nbrNodes);
    relClst = zeros(nbrRealisations,1);
    for j=1:nbrRealisations
        A = ERadjecencyMatrix( p,nbrNodes );
        D = sum(A);
        [sortedValues,sortIndex] = sort(D,'descend');
        nodesToDelete = sortIndex(1:nbrNodesToDel);
        A(nodesToDelete,:) = [];
        A(:,nodesToDelete) = [];
        C = ClusterMatrix(A);
        relClst(j) = max(sum(C))/length(A);
    end
    clstrSizesS(i) = mean(relClst);
end
plot(f,clstrSizesS)
hold off



%% Pref. Growth Network
n0 = 5;
m = 3;
nbrNewNodes = 200;
nbrNodes = n0+nbrNewNodes;
nbrDataPoints = 20;
nbrRealisations = 5;

%% Random Vaccination
f = linspace(0,1,nbrDataPoints);
clstrSizesR = zeros(nbrDataPoints,1);
for i=1:nbrDataPoints
    nbrNodesToDel = floor(f(i)*nbrNodes);
    relClst = zeros(nbrRealisations,1);
    for j=1:nbrRealisations
        G = MakePrefNetwork(n0,m,nbrNewNodes);
        A = adjacency(G);
        jumbledNodes = randperm(nbrNodes);
        nodesToDelete = jumbledNodes(1:nbrNodesToDel);
        A(nodesToDelete,:) = [];
        A(:,nodesToDelete) = [];
        C = ClusterMatrix(A);
        relClst(j) = max(sum(C))/length(A);
    end
    clstrSizesR(i) = mean(relClst);
end
plot(f,clstrSizesR)
hold on


%% Smart Vaccination
f = linspace(0,1,nbrDataPoints);

clstrSizesS= zeros(nbrDataPoints,1);
for i=1:nbrDataPoints
    nbrNodesToDel = floor(f(i)*nbrNodes);
    relClst = zeros(nbrRealisations,1);
    for j=1:nbrRealisations
        G = MakePrefNetwork(n0,m,nbrNewNodes);
        A = adjacency(G);
        [sortedValues,sortIndex] = sort(D,'descend');
        nodesToDelete = sortIndex(1:nbrNodesToDel);
        A(nodesToDelete,:) = [];
        A(:,nodesToDelete) = [];
        C = ClusterMatrix(A);
        relClst(j) = max(sum(C))/length(A);
    end
    clstrSizesS(i) = mean(relClst);
end
plot(f,clstrSizesS)
hold off





