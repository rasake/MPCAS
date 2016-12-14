function [ Q,s ] = modularity(B,m)
[V,D] = eig(B);
s=sign(V(:,end));
Q = 1/(4*m)*s'*B*s;
end

