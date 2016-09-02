% test PolynomialDifferentiation

%% Test 1: first order derivative
poly = [1 2 1];
expectedDerivative = [2 2];
computedDerivative = PolynomialDifferentiation( poly, 1);
assert( isequal(expectedDerivative, computedDerivative) )

%% Test 2: Passing constant zero ploynomial
poly = [];
expectedDerivative = [];
computedDerivative = PolynomialDifferentiation( poly, 1);
assert( isequal(expectedDerivative, computedDerivative) )

%% Test 3: Returning constant zero ploynomial
poly = [1];
expectedDerivative = [];
computedDerivative = PolynomialDifferentiation( poly, 1);
assert( isequal(expectedDerivative, computedDerivative) )

%% Test 2: Passing polynomial containing zero
poly = [1 0 0 1]; % [a0 a1 a2 a3]
expectedDerivative = [0 0 3];
computedDerivative = PolynomialDifferentiation( poly, 1);
assert( isequal(expectedDerivative, computedDerivative) )


%% Test 4: Secoond order derivative
poly = [1 2 1];
expectedDerivative = [2];
computedDerivative = PolynomialDifferentiation( poly, 2);
assert( isequal(expectedDerivative, computedDerivative) )

%% Test 5: Third order derivative

poly = [0 0 0 2];
expectedDerivative = [12];
computedDerivative = PolynomialDifferentiation( poly, 3);
assert( isequal(expectedDerivative, computedDerivative) )

%% Test 6: Zero order derivative

poly = [0 0 0 2];
expectedDerivative = [0 0 0 2];
computedDerivative = PolynomialDifferentiation( poly, 0);
assert( isequal(expectedDerivative, computedDerivative) )