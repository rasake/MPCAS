function [ minimum ] = GradientDescent( x0, mu, eta, T )

jX = x0;
jGrad = Gradient(x0(1),x0(2),mu);
while norm(jGrad) >= T
    jGrad = Gradient(jX(1),jX(2),mu);
    jX = jX - eta*jGrad;
end

minimum = jX;

end
