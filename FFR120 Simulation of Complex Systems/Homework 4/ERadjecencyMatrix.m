function [ adjacencyMatrix ] = ERadjecencyMatrix( p,n )
adjacencyMatrix = rand(n,n)<p;
adjacencyMatrix = adjacencyMatrix.*triu(ones(n),1);
adjacencyMatrix = adjacencyMatrix + adjacencyMatrix';
end

