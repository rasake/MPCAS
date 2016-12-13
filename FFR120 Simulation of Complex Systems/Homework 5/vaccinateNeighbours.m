function [ A ] = vaccinateNeighbours( A, nbrVaccinations )

for i=1:nbrVaccinations
    rnode = randi(length(A));
    neighbours = find(logical(A(rnode,:)));
    if ~isempty(neighbours)
        nodeToVaccinate = neighbours(randi(length(neighbours)));
        A(nodeToVaccinate,:) = [];
        A(:,nodeToVaccinate) = [];
    end
end
end

