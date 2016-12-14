function [ neighboursI, neighboursJ ] = GetNeumannNeighbours( forrestMatrix, i, j )

neighboursI = [];
neighboursJ = [];
[tmpI, tmpJ] = WrapIndex(forrestMatrix, i+1, j); % West
neighboursI = [neighboursI, tmpI];
neighboursJ = [neighboursJ, tmpJ];
[tmpI, tmpJ] = WrapIndex(forrestMatrix, i-1, j); %East
neighboursI = [neighboursI, tmpI];
neighboursJ = [neighboursJ, tmpJ];
[tmpI, tmpJ] = WrapIndex(forrestMatrix, i, j+1); % North
neighboursI = [neighboursI, tmpI];
neighboursJ = [neighboursJ, tmpJ];
[tmpI, tmpJ] = WrapIndex(forrestMatrix, i, j-1); % South
neighboursI = [neighboursI, tmpI];
neighboursJ = [neighboursJ, tmpJ];

end

