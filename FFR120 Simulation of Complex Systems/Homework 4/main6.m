clear all
clc



%% %%%%%%% Network 1 %%%%%%%%
s1 = LoadNetwork1;
G1 = graph;
for i=1:length(s1)
    try
        G1 = addedge(G1,s1(i,1),s1(i,2));
    catch        
    end
end

%%
A1 = adjacency(G1);
L = CalulcateLengths(A1);
clustering1 = ClusteringCoefficient(A1)
average1 = sum(sum(L))/sum(sum(L>0))
diameter1 = max(max(L))
%%
subplot(1,2,1)
plot(G1,'Layout','circle')
title('Network 1')
subplot(1,2,2)
spy(A1)
title(['clustering: ' num2str(clustering1) ', average path length: ' num2str(average1) ', diameter: ' num2str(diameter1)])


%% %%%%%%% Network 2 %%%%%%%%
s2 = LoadNetwork2;
G2 = graph
for i=1:length(s2)
    try
        G2 = addedge(G2,s2(i,1),s2(i,2));
    catch        
    end
end
%%
A2 = adjacency(G2);
L = CalulcateLengths(A2);
clustering2 = ClusteringCoefficient(A2)
average2 = sum(sum(L))/sum(sum(L>0))
diameter2 = max(max(L))
%%
subplot(1,2,1)
plot(G2,'Layout','circle')
title('Network 2')
subplot(1,2,2)
spy(A2)
title(['clustering: ' num2str(clustering2) ', average path length: ' num2str(average2) ', diameter: ' num2str(diameter2)])

%% Network 3
s3 = LoadNetwork3;
G3 = graph;
for i=1:length(s3)
    try
        G3 = addedge(G3,s3(i,1),s3(i,2));
    catch        
    end
end

%%
A3 = adjacency(G3);
L = CalulcateLengths(A3);
clustering3 = ClusteringCoefficient(A3)
average3 = sum(sum(L))/sum(sum(L>0))
diameter3 = max(max(L))
%%
subplot(1,2,1)
plot(G3,'Layout','circle')
title('Network 3')
subplot(1,2,2)
spy(A3)
title(['clustering: ' num2str(clustering3) ', average path length: ' num2str(average3) ', diameter: ' num2str(diameter3)])



%%
subplot(2,3,1)
plot(G1,'Layout','force')
title('Network 1')
subplot(2,3,4)
spy(A1)
title(['clustering: ' num2str(clustering1) ', ave. path length: ' num2str(average1) ', diameter: ' num2str(diameter1)], 'FontSize', 7)
subplot(2,3,2)
plot(G2,'Layout','force')
title('Network 2')
subplot(2,3,5)
spy(A2)
title(['clustering: ' num2str(clustering2) ', ave. path length: ' num2str(average2) ', diameter: ' num2str(diameter2)], 'FontSize', 7)
subplot(2,3,3)
plot(G3,'Layout','force')
title('Network 3')
subplot(2,3,6)
spy(A3)
title(['clustering: ' num2str(clustering3) ', average path length: ' num2str(average3) ', diameter: ' num2str(diameter3)], 'FontSize', 7)

%%

subplot(1,3,1)
D1 = degree(G1);
meanDegree1 = mean(D1)
[k,freq] = EmpiricalCDF(D1);
loglog(k, freq)
xlabel('Degree')
ylabel('CCDF')
title('Network 1')
subplot(1,3,2)
D2 = degree(G2);
meanDegree2 = mean(D2)
[k,freq] = EmpiricalCDF(D2);
loglog(k, freq)
xlabel('Degree')
ylabel('CCDF')
title('Network 2')
subplot(1,3,3)
D3 = degree(G3);
meanDegree3 = mean(D3)
[k,freq] = EmpiricalCDF(D3);
loglog(k, freq)
xlabel('Degree')
ylabel('CCDF')
title('Network 3')
