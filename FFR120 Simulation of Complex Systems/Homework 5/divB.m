function [ Bneg, Bpos ] = divB( B,s )
u = s>0;
Bpos = B(u,u);
Bpos = Bpos - diag(sum(Bpos));
v = s<0;
Bneg = B(v,v);
Bneg = Bneg - diag(sum(Bneg));
end

