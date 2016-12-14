function [ B ] = ModularityMatrix( adjacencyMatrix, m )
deg = sum(adjacencyMatrix)';
B =adjacencyMatrix - deg*deg'/(2*m);
end

