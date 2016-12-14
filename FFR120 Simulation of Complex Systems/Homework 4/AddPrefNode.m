function [ G ] = AddPrefNode(G,m)
D = degree(G);
startNode = length(D)+1;
cumFit = cumulativeFitnesses(D);
indeces = 1:length(D);
for i = 1:m
    tmp = RWS(cumFit);
    cumFit = [cumFit(1:tmp-1) cumFit(tmp+1:end)];
    targetNode = indeces(tmp);
    indeces = [indeces(1:tmp-1) indeces(tmp+1:end)];
    G = addedge(G,startNode,targetNode,1);
end
end

