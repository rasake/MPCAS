function [ C ] = ClusterMatrix( A )
nbrNodes = length(A);
C = false(nbrNodes,nbrNodes);
u = ones(nbrNodes);
diagHelper = diag(u)==1;
for k=1:nbrNodes
    C = C + (A^k)~=0;
    C = logical(C.*diagHelper);
end
end

