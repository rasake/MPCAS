% test DecodeChromosome

%% Test 1: g(2,1) = 2275
x = [2,1];
gExpected = 2275;
fExpected = 1/gExpected;
fCalculated = EvaluateIndividual(x);
assert(fExpected == fCalculated)
