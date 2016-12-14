clear all
clc

A = LoadCommEx;
m = sum(sum(A))/2;
G = graph(A)



%%
[Q,communities] = DivideGraph(A);
%%
h = plot(G);
highlight(h,communities{1},'NodeColor','g')
highlight(h,communities{2},'NodeColor','r')
highlight(h,communities{3},'NodeColor','b')
title(['Community Example Network, modularity: ' num2str(Q)])

%% 
h = plot(G,'NodeLabel',{},'Layout','force');
myColorMap = parula(256);
for i=1:length(communities)
  theIntensity = floor(i/length(communities)*256); 
  theLineColor = myColorMap(theIntensity, :);
  highlight(h,communities{i},'NodeColor',theLineColor)
end
