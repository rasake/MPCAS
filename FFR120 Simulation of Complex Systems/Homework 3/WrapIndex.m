function [ wrappedI, wrappedJ ] = WrapIndex( forrestMatrix, i, j )
%WRAPINDEX Summary of this function goes here
%   Detailed explanation goes here
%Periodic boundary
[maxIndexI, maxIndexJ] = size(forrestMatrix);
wrappedI = mod(i, maxIndexI);
if wrappedI == 0
    wrappedI = maxIndexI;
end
wrappedJ = mod(j, maxIndexJ);
if wrappedJ == 0
    wrappedJ = maxIndexJ;
end

end

