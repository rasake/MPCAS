function [ forrestMatrix ] = Burn( forrestMatrix, i, j )
%BURN2 Summary of this function goes here
%   Detailed explanation goes here

ignitedTreesI = i;
ignitedTreesJ = j;

while ~isempty(ignitedTreesI)
    tmpI = [];
    tmpJ = [];
    for k=1:length(ignitedTreesI)
        if forrestMatrix(ignitedTreesI(k),ignitedTreesJ(k)) == 1 % there's a tree to ignite    
            % burn down ignited tree
            forrestMatrix(ignitedTreesI(k),ignitedTreesJ(k)) = 0;
            % Add comsutible neighbours to tmp variables
            [neighboursI,neighboursJ] = ...
                GetNeumannNeighbours(forrestMatrix, ignitedTreesI(k),ignitedTreesJ(k));        
            tmpI = [tmpI, neighboursI]; % Cannot pre-allocate since we do not now how many neighbours will be ignited in advance
            tmpJ = [tmpJ, neighboursJ];
        end
    end
    ignitedTreesI = tmpI; % Update ignited trees for next iteration
    ignitedTreesJ = tmpJ;
%     imagesc(forrestMatrix)
%     drawnow
end
end

