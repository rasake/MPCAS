function [ f ] = EvaluateIndividual( x )

f = (exp(-x(1)^2 - x(2)^2) + sqrt(5)*sin(x(2)*x(1)*x(1))^2 + ...
    2*cos( 2*x(1) + 3*x(2))^2 ) / (1+x(1)^2+x(2)^2);

end

