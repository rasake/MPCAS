% test PolynomialDifferentiation


%% Test 1: first order derivative
poly = [1 2 1];
expected_derivative = [2 1];
assert(PolynomialDifferentiation( poly, 1) == expected_derivative)

 
%% Test 2: Passing constant zero ploynomial
poly = [1 0 0 1];
expected_derivative = [3 0 0];
assert(PolynomialDifferentiation( poly, 1) == expected_derivative)

%% Test 3: Returning constant zero ploynomial
poly = [1];
expected_derivative = [];
assert(PolynomialDifferentiation( poly, 1) == expected_derivative)


%% Test 4: Secoond order derivative
poly = [1 2 1];
expected_derivative = [2];
assert(PolynomialDifferentiation( poly, 2) == expected_derivative)

%% Test 4: Third order derivative

poly = [2 0 0 0];
expected_derivative = [12];
assert(PolynomialDifferentiation( poly, 3) == expected_derivative)
