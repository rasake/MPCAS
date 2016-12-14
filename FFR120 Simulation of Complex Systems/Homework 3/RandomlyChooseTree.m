function [ i,j ] = RandomlyChooseTree( forrestMatrix )
%RANDOMLYCHOOSETREE Summary of this function goes here
%   Detailed explanation goes here

[X,Y] = find(forrestMatrix==1);
k = randi(length(X));

i = X(k);
j = Y(k);
if forrestMatrix(i,j) == 0
    disp('oh, shit')
end