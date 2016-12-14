function [ forrestMatrixOut] = BurnRec( forrestMatrix, i, j)
%BURN Summary of this function goes here
%   Detailed explanation goes here
[maxIndexI, maxIndexJ] = size(forrestMatrix);

i = mod(i, maxIndexI);
if i == 0
    i = maxIndexI;
end
j = mod(j, maxIndexJ);
if j == 0
    j = maxIndexJ;
end

if forrestMatrix(i,j) == 1 % there's a tree to burn
    % burn tree i,j
    forrestMatrix(i,j) = 0;
    % recursively ignite neighbors
    forrestMatrix = BurnRec(forrestMatrix, i+1,j);
    forrestMatrix = BurnRec(forrestMatrix, i-1,j);
    forrestMatrix = BurnRec(forrestMatrix, i,j+1);
    forrestMatrix = BurnRec(forrestMatrix, i,j-1);
end
forrestMatrixOut = forrestMatrix;
imagesc(forrestMatrix)
drawnow
end

