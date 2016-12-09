function [ prob ] = theroritcalDegreeDistER(p,n,k)
prob = nchoosek(n-1,k)*p.^k*(1-p).^(n-1-k);
end

