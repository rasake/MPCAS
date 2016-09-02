% test NewtonRaphson

%% Test 1: A polynom with known min
poly = [10 -2 -1 1 1];
start_guess = 1.5;
expected_min = 0.763284;
tolerance = 0.0001;
iterationValues = NewtonRaphson(poly, start_guess, tolerance);
assert( abs(iterationValues(end)== expected_min) < tolerance)

%% Test 2: Another polynom with known min
poly = [10 -2 1 1 0 2];
start_guess = 1.5;
expected_min = 0.459706;
tolerance = 0.0001;
iterationValues = NewtonRaphson(poly, start_guess, tolerance);
assert( abs(iterationValues(end)== expected_min) < tolerance)




%% Test 1: Polynom where fBis is zero so the step goes to inf


%% Test 1: Non converging polynom?
