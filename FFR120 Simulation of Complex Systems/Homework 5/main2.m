%% %%%%%% S-R Plot %%%%%%%%%%%%%

clear all
clc

nbrNodes = 300;
p = 0.1;
c = 6;

nbrDatatPoints = 10;
R = linspace(1e-4,1,nbrDatatPoints);
clstrSizes = zeros(nbrDatatPoints,1);
for i =1:nbrDatatPoints
    iR = R(i);
    phi = 1/(1+1/iR);
    A = adjSmallWorld(nbrNodes, p, c);
    A = Perculate( A, 1-phi);
    C = ClusterMatrix(A);
    maxClstr = max(sum(C));
    clstrSizes(i) = maxClstr/length(A);
end

plot(R,clstrSizes)
xlabel('R')
ylabel('Rel. Maximum Cluster Size')
title('Cluster Size for Percolated Small World Network')
% 
% A = Perculate( A, 1-phi);
% subplot(1,2,2)
% G = graph(A);
% plot(G,'Layout','force','NodeLabel',{})

%
% %%
% [Q,communities] = DivideGraph(A);
%
% h = plot(G,'NodeLabel',{},'Layout','force');
% myColorMap = parula(256);
% for i=1:length(communities)
%   theIntensity = floor(i/length(communities)*256);
%   theLineColor = myColorMap(theIntensity, :);
%   highlight(h,communities{i},'NodeColor',theLineColor)
% end
%

% %%
% C = ClusterMatrix(A);
% maxClusterSize = max(sum(C))