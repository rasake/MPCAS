function [ G ]  = MakePrefNetwork(n0,m,nbrNewNodes )
adjacencyMatrix = zeros(n0,n0);
adjacencyMatrix(1,2:end) = ones(1,n0-1);
adjacencyMatrix(2:end,1) = ones(n0-1,1);
G = graph(adjacencyMatrix);

%% Add edges
for i = 1:nbrNewNodes
    G = AddPrefNode(G,m);
end
end