%% %%%%%%%% Vaccination %%%%%%%%%%%%
clear all
clc


%% Random Graph
p = 0.015;
nbrNodes = 300;
nbrDataPoints = 60;
nbrRealisations = 70;

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
%% Smart Vaccination
f = linspace(0,1,nbrDataPoints);
A0 = ERadjecencyMatrix( p,nbrNodes );
clstrSizesS= zeros(nbrDataPoints,1);
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
hold off
xlabel('Fraction of nodes remove')
ylabel('Size of largest cluster')
legend(['Random Vaccination', 'Vaccinating Nodes with High Degree'])
title('Effect of vaccination on Random Graph')
legend('Random Vaccination', 'Vaccinating Nodes with High Degree')
xlabel('Fraction of nodes removed')
%
%
% %% Pref. Growth Network
% n0 = 5;
% m = 3;
% nbrNewNodes = 300;
% nbrNodes = n0+nbrNewNodes;
% nbrDataPoints = 100;
% nbrRealisations = 100;
%
% %% Random Vaccination
% f = linspace(0,1,nbrDataPoints);
% clstrSizesR = zeros(nbrDataPoints,1);
% G0 = MakePrefNetwork(n0,m,nbrNewNodes);
% for i=1:nbrDataPoints
%     nbrNodesToDel = floor(f(i)*nbrNodes);
%     relClst = zeros(nbrRealisations,1);
%     for j=1:nbrRealisations
%         A = adjacency(G0);
%         jumbledNodes = randperm(nbrNodes);
%         nodesToDelete = jumbledNodes(1:nbrNodesToDel);
%         A(nodesToDelete,:) = [];
%         A(:,nodesToDelete) = [];
%         G = graph(A);
%         c = conncomp(G);
%         relClst(j) = sum(c==1)/nbrNodes;
%     end
%     clstrSizesR(i) = mean(relClst);
% end
% plot(f,clstrSizesR)
% hold on
%
%
% %% Smart Vaccination
% f = linspace(0,1,nbrDataPoints);
%
% clstrSizesS= zeros(nbrDataPoints,1);
% G0 = MakePrefNetwork(n0,m,nbrNewNodes);
% for i=1:nbrDataPoints
%     nbrNodesToDel = floor(f(i)*nbrNodes);
%     relClst = zeros(nbrRealisations,1);
%     for j=1:nbrRealisations
%         A = adjacency(G0);
%         D = sum(A);
%         [sortedValues,sortIndex] = sort(D,'descend');
%         nodesToDelete = sortIndex(1:nbrNodesToDel);
%         A(nodesToDelete,:) = [];
%         A(:,nodesToDelete) = [];
%         G = graph(A);
%         c = conncomp(G);
%         relClst(j) = sum(c==1)/nbrNodes;
%     end
%     clstrSizesS(i) = mean(relClst);
% end
% plot(f,clstrSizesS)
% hold off

