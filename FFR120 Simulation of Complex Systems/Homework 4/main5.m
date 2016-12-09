clear all
clc

A = LoadSmallworld; % loads small-world network in variable A
G = graph(A);
L = CalulcateLengths(A);
average = sum(sum(L))/sum(sum(L>0))
diameter = max(max(L))
plot(G)
title(['Small World Example Network, average path length: ' num2str(average) ', diameter: ' num2str(diameter)])

